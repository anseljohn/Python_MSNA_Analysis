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

def list_stringify(lst, depth=0):
    str = ""

    if depth != 0:
        str += "\n"
    for i in range(depth):
        str += "\t"

    str += "["

    for i in range(len(lst)):
        curr = lst[i]

        if isinstance(curr, list):
            str += list_stringify(curr, depth+1)
        else:
            str += fstr(curr) + (", " if i != len(lst) - 1 else "")
    str += "]"

    return str


# Analysis output formatting
# transduction_analysis.overall_NVTD() returns a dictionary of data based on
# average absolute change and average absolute percent change. This function
# formats the data to be pretty for output
def output_str(out, depth=0):
    #if type(out) == tuple:
        #out = list(out)

    str = ""
    for title in out.keys():
        curr = out[title]
        for i in range(depth):
            str += "\t"

        if isinstance(curr, dict):
            str += title + ":\n" + output_str(curr, depth+1)
        else:
            if isinstance(curr, tuple):
                curr = list(curr)
            str += title + ": "
            
            if isinstance(curr, list):
                str += list_stringify(curr)
            else:
                str += fstr(curr) + "\n"
        str += "\n"

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
participant_data = {}
for participant in xl.sheet_names:
    participant_data[participant] = {}

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
        participant_data[participant][outcome_var] = []
        # Getting the outcome variable data
        outcome = df.iloc[:, outcome_variables[outcome_var]] if outcome_var == "MDP" else df.iloc[:, 5] #TODO: remove IF once MAP is added
        analyzer = anlz.Analyzer(data_len, burst_checks) # Instanciating the analyzer

        for bool in [True, False]:
            participant_data[participant][outcome_var].append(analyzer.overall_calculations(outcome, bool)) # Overall NVTD values, burst and non-bursts
            participant_data[participant][outcome_var].append(analyzer.patterns(normalized_burst_amplitude_percent, bool)) # per burst/non-burst frequency
        
        participant_data[participant][outcome_var].append(analyzer.tertiles(outcome))

for participant in participant_data.keys():
    data = participant_data[participant]
    for outcome_var in data.keys():
        # Writing everything to file
        with open('./analysis_output/' + participant + '_' + outcome_var + '_transduction_analysis.txt', 'w') as f:
            f.write("Transduction Analysis Using " + outcome_var + " as the Outcome Variable\n\n")

            for d in data[outcome_var]:
                f.write(output_str(d))