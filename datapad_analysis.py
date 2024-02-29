import pandas as pd
import xlrd
import sys

# Check for required arguments:
#   - The datapad spreadsheet
#   - The name of the outcome variable
if (len(sys.argv) < 3):
    sys.exit("Error: Syntax: python datapad_analysis.py path/to/spreadsheet.xlsx \"Outcome Variable Name\"")

df = pd.read_excel(sys.argv[1])
df.drop([0, 1], inplace=True)           # Remove units and titles
df.reset_index(drop=True, inplace=True) # Reset indexing back to 0
ov = sys.argv[2]                        # The outcome variable, "MAP" or "MDP"

if ov != "MDP" and ov != "MAP":
    sys.exit("Syntax Error: Must choose between MAP (Mean Arterial Pressure) and MDP (Mean Diastolic Pressure) for outcome variable.\n\n\
Example:\n\t$ python datapad_analysis.py path/to/spreadsheet.xlsx \"MDP\"")

######################################
#   Constants and global variables   #
######################################
comnums = df.iloc[:, 4] # The burst comment numbers
outcome = df.iloc[:, 5] if ov == "MDP" else df.iloc[:, 6] # MDP or MAP depending

#TODO: Change this value to 7 once MAP is added into data pad
burst_sizes = df.iloc[:, 6] # The burst size or "Integrated MSNA max-min"
data_len = len(comnums) # The default length of data

#######################
#   Actual analysis   #
#######################

# Determining bursts from burst comment numbers
is_burst = []
burst_cnt = 0
for i in range(data_len):
    if i == 0:
        if (comnums[i] != comnums[i+1]): burst_cnt += 1
        is_burst.append(comnums[i] != comnums[i+1])
    else:
        if (comnums[i] != comnums[i-1]): burst_cnt +=1
        is_burst.append(comnums[i] != comnums[i-1])


# Normalizing burst sizes
largest_burst = burst_sizes.max() # Grabbing the largest burst
normalized_percent_burst_sizes = [] # Normalize burst sizes
for i in range(data_len):
    if is_burst[i]:
        normalized_percent_burst_sizes.append(burst_sizes[i] / largest_burst * 100)
    else:
        normalized_percent_burst_sizes.append(None)

# Calculating absolute values in sets of 12 post-burst cardiac cycles
abs_vals = []
for i in range(data_len):
    cc = []
    if is_burst[i]:
        # If it cannot be tracked for 12 cardiac cycles, exit
        if (i + 13 >= data_len):
            break
        
        for j in range(i, i+13):
            cc.append(outcome[j])

        abs_vals.append(cc)

full_12cc_burst_cnt = len(abs_vals) # The number of bursts with 12 post-burst cc data available

# Calculate absolute change in sets of 12 post-burst cardiac cycles
abs_change_vals = []
for i in range(full_12cc_burst_cnt):
    cc = []
    for j in range(1, 13):
        cc.append(abs_vals[i][j] - abs_vals[i][0])

    abs_change_vals.append(cc)

# Calculate percent change
percent_change_vals = []
for i in range(full_12cc_burst_cnt):
    cc = []
    for j in range(0, 12):
        cc.append(abs_change_vals[i][j] / abs_vals[i][0] * 100)

    percent_change_vals.append(cc)

# Averaging a set of 12 cardiac cycles
avg_abs_change = [0]*12
for i in range(full_12cc_burst_cnt):
    for j in range(12):
        avg_abs_change[j] += abs_change_vals[i][j]

avg_abs_change = [x / full_12cc_burst_cnt for x in avg_abs_change]

# Averaging the percentages for a set of 12 cardiac cycles
abs_percent_change = [0] * 12
for i in range(len(percent_change_vals)):
    for j in range(12):
        abs_percent_change[j] += percent_change_vals[i][j]
abs_percent_change = [x / len(percent_change_vals) for x in abs_percent_change]

print("Max average absolute change:", max(avg_abs_change))
print("Max absolute percent change:", max(abs_percent_change))