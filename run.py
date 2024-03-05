import sys
import pandas as pd
import transduction_analysis as ta

# Check validity of call
if (len(sys.argv) < 2):
    sys.exit("Syntax Error:\n\t$ python analyze.py [path/to/spreadsheet.py]")

########################
#   Helper functions   #
########################
def fstr(f):
    return str(round(f, 2))

#######################
#   Data formatting   #
#######################
df = pd.read_excel(sys.argv[1])
df.drop([0, 1], inplace=True)            # Remove units and titles
df.reset_index(drop=True, inplace=True)  # Reset indexing back to 0
outcome_variables = {"MDP": 5, "MAP": 6} # Outcome variables and their respective indices

############################################################
#   Getting required arguments for analyses calculations   #
############################################################
comnums = df.iloc[:, 4] # The burst comment numbers

#TODO: Change this value to 7 once MAP is added into data pad
burst_sizes = df.iloc[:, 6] # The burst size or "Integrated MSNA max-min"
data_len = len(comnums) # The default length of data
burst_checks = []
normalized_burst_amplitude_percent = [] # Normalize burst sizes

# Determining bursts from burst comment numbers
burst_cnt = 0
for i in range(data_len):
    if i == 0:
        if (comnums[i] != comnums[i+1]): burst_cnt += 1
        burst_checks.append(comnums[i] != comnums[i+1])
    else:
        if (comnums[i] != comnums[i-1]): burst_cnt +=1
        burst_checks.append(comnums[i] != comnums[i-1])

# Normalizing burst sizes
largest_burst = burst_sizes.max() # Grabbing the largest burst
for i in range(data_len):
    if burst_checks[i]:
        normalized_burst_amplitude_percent.append(burst_sizes[i] / largest_burst * 100)
    else:
        normalized_burst_amplitude_percent.append(None)

# Creating the analyzer
for outcome_var in outcome_variables.keys():
    outcome = df.iloc[:, outcome_variables[outcome_var]] if outcome_var == "MDP" else df.iloc[:, 5] #TODO: remove IF once MAP is added
    analyzer = ta.Transduction_Analysis(data_len, outcome, burst_checks, normalized_burst_amplitude_percent)

    overall_NVTD_values = analyzer.overall_NVTD()   # Calculating overall NVTD values
    burst_pattern_values = analyzer.burst_pattern() # Calculating overall NVTD values per burst frequency

    # Writing everything to file
    with open(outcome_var + '_transduction_analysis.txt', 'w') as f:
        f.write("Transduction Analysis Using " + outcome_var + " as the Outcome Variable\n\n")
        f.write("Max Overall Transduction Values:\n")
        f.write("\tAverage Absolute Change: " + fstr(overall_NVTD_values[0]) + "\n")
        f.write("\tAverage Percent Change: " + fstr(overall_NVTD_values[1]) + "\n\n")

        f.write("Average Normalized Burst Sizes Per Sequence:\n")

        for i in range(4):
            if i == 0:   f.write("\tSinglets:\n")
            elif i == 1: f.write("\tDoublets:\n")
            elif i == 2: f.write("\tTriplets:\n")
            elif i == 3: f.write("\tOverall:\n")

            f.write("\t\tCount: " + fstr(burst_pattern_values[i][0]) + "\n")
            f.write("\t\tOverall NVTD (12 cc): [")
            bpv_NVTD = burst_pattern_values[i][1]
            bpv_NVTD_len = len(bpv_NVTD)
            for j in range(bpv_NVTD_len - 1):
                f.write(fstr(bpv_NVTD[j]) + ", ")
            f.write(fstr(bpv_NVTD[bpv_NVTD_len - 1]) + "]\n")
            f.write("\t\tAverage Normalized Burst Amplitude: " + fstr(burst_pattern_values[i][2]) + "\n\n")

