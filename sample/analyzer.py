import statistics as stats
import numpy as np

class Analyzer:
    # Absolute change values in sets of 12 cardiac cycles
    abs_change_vals = []

    # Number of bursts with 12 post-burst cardiac cycle data
    full_12cc_burst_cnt = 0

    def __init__(self, data_len, burst_checks, outcome):
        self.data_len = data_len
        self.burst_checks = burst_checks
        self.outcome = outcome

    def burst_check(self, i, for_bursts):
        return (for_bursts and self.burst_checks[i]) or (not for_bursts and not self.burst_checks[i])

    # Gets absolute values, absolute change values, and percent change values for bursts or non-bursts
    # Returns a dictionary containing labelled data (for the purpose of writing to file)
    # Parameters:
    #   for_bursts (bool) : whether to calculate these values for bursts or non_bursts
    def overall_calculations(self, for_bursts):
        # Calculating absolute values in sets of 12 post-burst cardiac cycles
        abs_vals = []
        for i in range(self.data_len):
            cc = []
            if self.burst_check(i, for_bursts):
                # If it cannot be tracked for 12 cardiac cycles, exit
                if (i + 13 >= self.data_len):
                    break
                
                for j in range(i, i+13):
                    cc.append(self.outcome[j])

                abs_vals.append(cc)

        self.full_12cc_burst_cnt = len(abs_vals) # The number of bursts with 12 post-burst cc data available

        # Calculate absolute change in sets of 12 post-burst cardiac cycles
        for i in range(self.full_12cc_burst_cnt):
            cc = []
            for j in range(1, 13):
                cc.append(abs_vals[i][j] - abs_vals[i][0])

            self.abs_change_vals.append(cc)

        # Calculate percent change
        percent_change_vals = []
        for i in range(self.full_12cc_burst_cnt):
            cc = []
            for j in range(0, 12):
                cc.append(self.abs_change_vals[i][j] / abs_vals[i][0] * 100)

            percent_change_vals.append(cc)

        # Averaging a set of 12 cardiac cycles
        avg_abs_change = [0]*12
        for i in range(self.full_12cc_burst_cnt):
            for j in range(12):
                avg_abs_change[j] += self.abs_change_vals[i][j]

        avg_abs_change = [x / self.full_12cc_burst_cnt for x in avg_abs_change]

        # Averaging the percentages for a set of 12 cardiac cycles
        avg_percent_change = [0] * 12
        for i in range(len(percent_change_vals)):
            for j in range(12):
                avg_percent_change[j] += percent_change_vals[i][j]
        avg_percent_change = [x / len(percent_change_vals) for x in avg_percent_change]

        return {
            "Overall Neurovascular Transduction" :
                {
                    "Absolute Change" : 
                        {
                            "Average (12 cc)" : avg_abs_change,
                            "Standard Deviation (12 cc)" : [stats.stdev(np.array(self.abs_change_vals)[:, i]) for i in range(12)], 
                            "Max AAC" : max(avg_abs_change)
                        },

                    "Percent Change" :
                        {
                            "Average (12 cc)" : avg_percent_change,
                            "Standard Deviation (12 cc)" : [stats.stdev(np.array(percent_change_vals)[:, i]) for i in range(12)],
                            "Max APC" : max(avg_percent_change)
                        }
                }
        }

    # Returns a dictionary to access singlet, doublet, triplet, and overall data
    # Each of the burst patterns' data contain the number of occurrences, 
    # overall NVTD values, and its average normalizde burst amplitude
    #   i.e. 
    #       pattern()['Singlets']['Count'] is the number of triplet bursts
    #       pattern()['Doublets']['Overall NVTD (12cc)] is the average 12cc nvtd values for doublets
    #       pattern()['Overall']['Average Normalized Burst Amplitude'] is the overall average normalized burst amplitude
    #           ** NOTE ** Average normalized burst amplitude is only calculated for bursts
    #           So pattern(data, False)['Singlets']['Average Normalized Burst Amplitude'] is invalid.
    def patterns(self, normalized_burst_amplitude_percent, for_bursts):
        #TODO: change the structure of this depending on its usage
        # A dictionary of 
        seq_lens = {}
        i = 0
        while i < self.data_len:
            j = i
            if self.burst_check(i, for_bursts):
                seq_lens[i] = 0

                seq_len = 0
                while j < self.data_len and self.burst_check(j, for_bursts):
                    seq_len += 1
                    j += 1

                # Quadruplets+ aren't counted
                if seq_len <= 3:
                    seq_lens[i] = seq_len

            i = j+1
        
        seqs = ['Singlets', 'Doublets', 'Triplets', 'Overall']
        seq_data_titles = ['Count', 'Overall NVTD (12 cc)', 'Average Normalized Burst Amplitude']
        seq_data = {
                        seq_data_titles[0] : 0,
                        seq_data_titles[1] : [0]*12,
                        seq_data_titles[2] : 0
                   }
        if for_bursts:
            seq_data[seq_data_titles[2]] = 0

            for key in seq_lens.keys():
                seq_len = seq_lens[key]
                for i in range(key, key + seq_len):
                    curr_amplitude = normalized_burst_amplitude_percent[i]
                    data_by_seq[seqs[seq_len-1]][seq_data_titles[2]] += curr_amplitude
                    data_by_seq[seqs[3]][seq_data_titles[2]] += curr_amplitude

        data_by_seq = {}
        for i in range(4):
            data_by_seq[seqs[i]] = seq_data.copy()
        
        for i in range(self.full_12cc_burst_cnt):
            if i in seq_lens:
                seq = seqs[seq_lens[i] - 1]
                seq_overall_NVTD = data_by_seq[seq][seq_data_titles[1]]
                data_by_seq[seq][seq_data_titles[1]] = [x + y for x, y in zip(seq_overall_NVTD, self.abs_change_vals[i])]
                data_by_seq[seq][seq_data_titles[0]] += 1
                data_by_seq[seqs[3]][seq_data_titles[1]] = [x + y for x, y in zip(data_by_seq['Overall'][seq_data_titles[1]], self.abs_change_vals[i])]
                data_by_seq[seqs[3]][seq_data_titles[0]] += 1

        for seq in seqs:
            data_by_seq[seq][seq_data_titles[2]] /= data_by_seq[seq][seq_data_titles[0]]
            data_by_seq[seq][seq_data_titles[1]] = [x / data_by_seq[seq][seq_data_titles[0]] for x in data_by_seq[seq][seq_data_titles[1]]]

        return {"Neurovascular Transduction by Burst Pattern" : data_by_seq}