import sys
import os
import pandas as pd
import sample.analyzer as anlz 

# Check validity of call
if (len(sys.argv) < 2):
    sys.exit("Syntax Error:\n\t$ python analyze.py [path/to/spreadsheet.py]")

########################
#   Helper functions   #
########################
# Convert to string and round to two decimal points
def fstr(f):
    return str(round(f, 2))

# Analysis output formatting
# transduction_analysis.overall_NVTD() returns a dictionary of data based on
# average absolute change and average absolute percent change. This function
# formats the data to be pretty for output
def output_str(out, depth=0):
    str = ""
    for title in out.keys():
        curr = out[title]
        for i in range(depth):
            str += "\t"

        if isinstance(curr, dict):
            str += title + ":\n" + output_str(curr, depth+1)
        else:
            str += title + ": "
            
            if isinstance(curr, list):
                str += "["
                for i in range(len(curr) - 1):
                    str += fstr(curr[i]) + ", "
                str += fstr(curr[i+1]) + "]\n"
            else:
                str += fstr(curr) + "\n"

    str += "\n"

    return str

#######################
#   Data formatting   #
#######################
# Create output directory
if not os.path.exists("./analysis_output"):
    os.mkdir("./analysis_output")

df = pd.read_excel(sys.argv[1])          # Reading in the file
df.drop([0, 1], inplace=True)            # Remove units and titles
df.reset_index(drop=True, inplace=True)  # Reset indexing back to 0

xl = pd.ExcelFile(sys.argv[1])
outcome_variables = {"MDP": 5, "MAP": 6} # Outcome variables and their respective indices

#TODO: Handle outputting for multiple participants, add rest of code into FOR
for participant in xl.sheet_names:
    df = xl.parse(participant)
    df.drop([0, 1], inplace=True)
    df.reset_index(drop=True, inplace=True)

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

# Analyzing for MDP and MAP
for outcome_var in outcome_variables.keys():
    # Getting the outcome variable data
    outcome = df.iloc[:, outcome_variables[outcome_var]] if outcome_var == "MDP" else df.iloc[:, 5] #TODO: remove IF once MAP is added
    analyzer = anlz.Analyzer(data_len, burst_checks) # Instanciating the analyzer

    overall_NVTD_values = analyzer.overall_NVTD(outcome) # Calculating overall NVTD values
    burst_pattern_values = analyzer.burst_pattern(normalized_burst_amplitude_percent) # Calculating overall NVTD values per burst frequency

    # Writing everything to file
    with open(outcome_var + '_transduction_analysis.txt', 'w') as f:
        f.write("Transduction Analysis Using " + outcome_var + " as the Outcome Variable\n\n")

        f.write(output_str(overall_NVTD_values))
        f.write(output_str(burst_pattern_values))