import sys
import pandas as pd
import transduction_analysis as ta

# Check validity of call
if (len(sys.argv) < 3):
    sys.exit("Syntax Error:\n\t$ python analyze.py [path/to/spreadsheet.py] [outcome variable: MDP or MAP]")

#######################
#   Data formatting   #
#######################
df = pd.read_excel(sys.argv[1])
df.drop([0, 1], inplace=True)           # Remove units and titles
df.reset_index(drop=True, inplace=True) # Reset indexing back to 0
ov = sys.argv[2]                        # The outcome variable, "MAP" or "MDP"

# Check that outcome variable is valid
if ov != "MDP" and ov != "MAP":
    sys.exit("Syntax Error: Must choose between MAP (Mean Arterial Pressure) and MDP (Mean Diastolic Pressure) for outcome variable.\n\n\
Example:\n\t$ python datapad_analysis.py path/to/spreadsheet.xlsx \"MDP\"")

############################################################
#   Getting required arguments for analyses calculations   #
############################################################
comnums = df.iloc[:, 4] # The burst comment numbers
outcome = df.iloc[:, 5] if ov == "MDP" else df.iloc[:, 6] # MDP or MAP depending

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
analyzer = ta.Transduction_Analysis(data_len, outcome, burst_checks, normalized_burst_amplitude_percent)

# Calculating and printing overall NVTD values
overall_NVTD_values = analyzer.overall_NVTD()
print("Max Overall Transduction Values:")
print("\tAverage Absolute Change: " + str(overall_NVTD_values[0]))
print("\tAverage Percent Change:  " + str(overall_NVTD_values[1]) + "\n")

# Calculating and printing overall NVTD values per burst frequency
burst_pattern_values = analyzer.burst_pattern()
print("Average Normalized Burst Sizes Per Sequence:")

for i in range(4):
    if i == 0:   print("\tSinglets:")
    elif i == 1: print("\tDoublets:")
    elif i == 2: print("\tTriplets:")
    elif i == 3: print("\tOverall")

    print("\t\tCount: " + str(burst_pattern_values[i][0]))
    print("\t\tOverall NVTD: ", end="")
    print(burst_pattern_values[i][1])
    print("\t\tAverage Normalized Burst Amplitude: " + str(burst_pattern_values[i][2]))
    print()g

