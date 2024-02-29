class Transduction_Analysis:
    # Absolute change values in sets of 12 cardiac cycles
    abs_change_vals = []

    # Number of bursts with 12 post-burst cardiac cycle data
    full_12cc_burst_cnt = 0

    def __init__(self, data_len, outcome, burst_checks, normalized_burst_amplitude_percent):
        self.data_len = data_len
        self.outcome = outcome
        self.burst_checks = burst_checks
        self.normalized_burst_amplitude_percent = normalized_burst_amplitude_percent

    # Calculates max overall transduction values
    # Returns:
    #   [max average absolute change, max average percent change]
    def overall_NVTD(self):
        # Calculating absolute values in sets of 12 post-burst cardiac cycles
        abs_vals = []
        for i in range(self.data_len):
            cc = []
            if self.burst_checks[i]:
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
        avg_abs_percent_change = [0] * 12
        for i in range(len(percent_change_vals)):
            for j in range(12):
                avg_abs_percent_change[j] += percent_change_vals[i][j]
        avg_abs_percent_change = [x / len(percent_change_vals) for x in avg_abs_percent_change]

        return [max(avg_abs_change), max(avg_abs_percent_change)]


    # Returns a matrix corresponding to [burst_frequency][value]
    #   [0][] = singlets
    #   [1][] = doublets
    #   [2][] = triplets
    #   [3][] = overall
    #
    #   [][0] = total number of bursts per burst frequency
    #   [][1] = 12 cc overall NVTD per burst frequency
    #   [][2] = average normalized burst amplitude per burst frequency
    #
    #   i.e. 
    #       burst_pattern()[2][0] is the number of triplet bursts
    #       burst_pattern()[1][1] is the average 12cc nvtd values for doublets
    #       burst_pattern()[3][2] is the overall average normalized burst amplitude
    def burst_pattern(self):
        #TODO: change the structure of this depending on its usage
        # A dictionary of 
        seq_lens = {}
        i = 0
        while i < self.data_len:
            j = i
            if (self.burst_checks[i]):
                seq_lens[i] = 0

                seq_len = 0
                while j < self.data_len and self.burst_checks[j]:
                    seq_len += 1
                    j += 1

                # Quadruplets+ aren't considered
                if seq_len <= 3:
                    seq_lens[i] = seq_len

            i = j+1
        data_by_seq = [     #      Count          Overall NVTD,       Avg Normalized Burst Amplitude
                                    [0,              [0]*12,                     0],                                # Singlets
                                    [0,              [0]*12,                     0],                                # Doublets
                                    [0,              [0]*12,                     0],                                # Triplets
                                    [0,              [0]*12,                     0],                                # Overall
                                ]
        seq_cnt_ind = 0
        seq_ONVTD_ind = 1
        seq_amp_ind = 2

        for i in range(self.full_12cc_burst_cnt):
            if i in seq_lens:
                seq_ind = seq_lens[i] - 1
                seq_overall_NVTD = data_by_seq[seq_ind][1]
                data_by_seq[seq_ind][seq_ONVTD_ind] = [x + y for x, y in zip(seq_overall_NVTD, self.abs_change_vals[i])]
                data_by_seq[seq_ind][seq_cnt_ind] += 1
                data_by_seq[3][seq_ONVTD_ind] = [x + y for x, y in zip(data_by_seq[3][seq_ONVTD_ind], self.abs_change_vals[i])]
                data_by_seq[3][seq_cnt_ind] += 1

        for key in seq_lens.keys():
            seq_len = seq_lens[key]
            for i in range(key, key + seq_len):
                curr_amplitude = self.normalized_burst_amplitude_percent[i]
                data_by_seq[seq_len-1][seq_amp_ind] += curr_amplitude
                data_by_seq[3][seq_amp_ind] += (curr_amplitude)

        for i in range(4):
            data_by_seq[i][seq_amp_ind] /= data_by_seq[i][seq_cnt_ind]
            data_by_seq[i][seq_ONVTD_ind] = [x / data_by_seq[i][seq_cnt_ind] for x in data_by_seq[i][seq_ONVTD_ind]]

        return data_by_seq