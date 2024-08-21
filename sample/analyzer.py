import statistics as stats
from enum import Enum

class Analyzer:
    class DivisionMethod(Enum):
        TERTILE = 3
        QUARTILE = 4

    # Absolute change values in sets of 12 cardiac cycles
    abs_change_vals = []

    # Number of bursts with 12 post-burst cardiac cycle data
    full_12cc_burst_cnt = 0

    def __init__(self, data_len, burst_checks):
        self.data_len = data_len
        self.burst_checks = burst_checks
    def burst_check(self, i, for_bursts):
        return (for_bursts and self.burst_checks[i]) or (not for_bursts and not self.burst_checks[i])
    
    # Gets absolute values, absolute change values for bursts or non-bursts
    # Returns a dictionary containing labelled data (for the purpose of writing to file)
    # Parameters:
    #   for_bursts (bool)       : whether to calculate these values for bursts or non_bursts
    #   xtiles (DivisionMethod) : whether to analyze using tertiles or quartiles
    def overall_calculations(self, outcome, for_bursts=True, xtiles=False):
        # Calculating absolute values in sets of 12 post-burst cardiac cycles
        abs_vals = []
        for i in range(self.data_len):
            cc = []
            if self.burst_check(i, for_bursts):
                # If it cannot be tracked for 12 cardiac cycles, exit
                if (i + 13 >= len(outcome)):
                    break
                
                for j in range(i, i+13):
                    cc.append(outcome[j])

                abs_vals.append(cc)

        if len(abs_vals) < 12: return ["NaN"]*13
        self.full_12cc_burst_cnt = len(abs_vals) # The number of bursts with 12 post-burst cc data available

        abs_change_vals = []
        # Calculate absolute change in sets of 12 post-burst cardiac cycles
        for i in range(self.full_12cc_burst_cnt):
            cc = []
            for j in range(1, 13):
                cc.append(abs_vals[i][j] - abs_vals[i][0])
            abs_change_vals.append(cc)
        
        if not xtiles:
            self.abs_change_vals = abs_change_vals

        # Averaging a set of 12 cardiac cycles
        avg_abs_change = [0]*12
        for i in range(self.full_12cc_burst_cnt):
            for j in range(12):
                avg_abs_change[j] += self.abs_change_vals[i][j]

        avg_abs_change = [x / self.full_12cc_burst_cnt for x in avg_abs_change]

        avg_abs_change.append(stats.fmean(avg_abs_change))
        return avg_abs_change
    
    def xtiles(self, outcome, partitioned_data, division_method: DivisionMethod):
        x = division_method.value
        minimum = min(partitioned_data)
        maximum = max(partitioned_data)
        delta = (maximum - minimum) / (float)(x)
        xtile_bounds = []
        for i in range(x):
            xtile_bounds.append(minimum + i*delta)

        xtiles = [[] for i in range(x)]

        for i in range(len(outcome)):
            partitioned_val = partitioned_data[i]
            outcome_val = outcome[i]
            for tile in xtile_bounds:
                if partitioned_val < tile:
                    xtiles[xtile_bounds.index(tile)].append(outcome_val)
                    break
        return [self.overall_calculations(xtile, xtiles=True) for xtile in xtiles]
    
    # def tertiles(self, outcome):
        # minimum = min(outcome)
        # maximum = max(outcome)
        # delta = (maximum - minimum) / 3.0
        # t1 = minimum + delta
        # t2 = minimum + 2*delta

        # tertile = [[], [], []]

        # for val in outcome:
        #     if val < t1:
        #         tertile[0].append(val)
        #     elif val < t2:
        #         tertile[1].append(val)
        #     else:
        #         tertile[2].append(val)

        # return [self.overall_calculations(tertile[0], xtiles=True),
        #         self.overall_calculations(tertile[1], xtiles=True),
        #         self.overall_calculations(tertile[2], xtiles=True)]
    
    # def quartiles(self, outcome, burst_sizes):
        # return self.xtiles(outcome, burst_sizes, self.DivisionMethod.QUARTILE)
