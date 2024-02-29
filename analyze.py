import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

#################
#   Constants   #
#################
COM_TYPE = 4
COM_POS = 2

#################################################################################
#   Getting base required data (data, titles, comments) and checking validity   #
#################################################################################

# Exit if the there aren't enough arguments
if (len(sys.argv) < 3):
    sys.exit("Error: Syntax: python analyze.py path/to/matlab_data.mat \"Outcome Variable Name\"")

mat = scipy.io.loadmat(sys.argv[1]) # Loading the matlab file in by command line arg
titles = mat["titles"] # The array of channel titles
coms = mat["com"] # The array of comments and their info
com_names = mat["comtext"] # The array of comment names

# Data is structured as such:
# [channel 1 start, ..., channel 1 end, channel 2 start, ..., channel 2 end , ...]
data = mat["data"]

# Checking if BURST exists
has_burst = False
for com in mat["comtext"]:
    if com.strip() == "BURST":
        has_burst = True
        break

if not has_burst:
    sys.exit("No burst comments found. Please make sure to label MSNA bursts as \"BURST\"")

########################
#   Helper functions   #
########################

# Get the index "title"'s data e.g. "ECG" data
# Exits with failure if the data cannot be found
def ind(title):
    for i in range(len(titles)):
        if titles[i].strip() == title: # Titles may end up with trailing whitespace which must be stripped
            return i
    sys.exit("No " + title + " data found.")

# Get the entire array of data corresponding to a channel
# i.e. get_data('ECG') will return data[start of ecg data, ..., end of ecg data]
def get_data(title):
    title_ind = ind(title)
    start = int(mat['datastart'].item(title_ind)) # Get the starting index from datastart
    end = int(mat['dataend'].item(title_ind)) # Get the end index from dataend
    return data[start:end]

# Get the index of "com"'s data e.g. "BURST"
# Exits with failure if the comment does not exist
def com_ind(com):
    for i in range(len(com_names)):
        if com_names[i].strip() == com:
            return i
    sys.exit("Comment \"" + com + "\" not found.")

burst_ind = -1
for i in range(len(com_names)):
    if com_names[i].strip() == "BURST":
        burst_ind = i

if burst_ind == -1:
    sys.exit("\"BURST\" comments not found. Please label MSNA bursts as \"BURST\".")

# Determines if the comment you're looking at is labelled des
# i.e. is_com(3, "BURST") returns whether comment #4 is labelled "BURST"
def is_com(com_ind, des):
    return coms[com_ind][4] == com_ind(des)
def is_com(com_ind):
    return coms[com_ind][4] == com_ind("BURST")

#####################################
#   Getting required channel data   #
#####################################

outcome = get_data(sys.argv[2])
ecg = get_data("ECG")
msna = get_data("Integrated MSNA")
#bc_no = get_data("Burst Comment Number")
#bs = get_data("Burst Size")
data_len = len(ecg)

is_burst = {}
for i in range(len(coms)):
    if is_com(i):
        is_burst[coms[i][COM_POS]] = True

#######################
#   Actual analysis   #
#######################

# Determining bursts based on burst comment numbers
is_burst = []
for i in range(len(bc_no)):
    burst = False
    if i == 0:
        burst = bc_no[i] != bc_no[i+1]
    else:
        burst = bc_no[i] != bc_no[i-1]
    is_burst.append(burst)

# Get the largest burst
max_burst = float('-inf')
for i in range(data_len):
    curr_burst = bs[i]
    if is_burst[i] and curr_burst > max_burst:
        max_burst = curr_burst

# Normalize burst sizes and turn into percentages
for i in range(data_len):
    bs[i] = bs[i] / max_burst * 100 if is_burst[i] else float('-inf')

# Calculating absolute values in sets of 12 cardiac cycles
abs_vals = []
for i in range(data_len):
    cc = []
    incr = 1
    if is_burst[i]:
        for j in range(incr, 13 + incr):
            cc.append(outcome[i])

    incr += 1
    abs_vals.append(cc)

# Calculating absolute value change in sets of 12 cardiac cycles
abs_change_vals = []
for i in range(len(abs_vals)):
    cc = []
    for j in range(1, 13):
        cc.append(abs_vals[i][j] - abs_vals[i][0])

# Calculating the percent change
percent_change_vals = []
for i in range(len(abs_change_vals)):
    cc = []
    for j in range(1, 13):
        cc.append(abs_change_vals[i][j] / abs_change_vals[i][0] * 100)

# Averaging a set of 12 cardiac cycles
avg_abs_change = []
for i in range(len(abs_change_vals)):
    for j in range(13):
        avg_abs_change[j] += abs_vals[i][j]
avg_abs_change = [x / len(abs_vals) for x in avg_abs_change]

# Averaging the percentages for a set of 12 cardiac cycles
abs_percent_change = []
for i in range(len(percent_change_vals)):
    for j in range(12):
        abs_percent_change[j] += percent_change_vals[i][j]
abs_percent_change = [x / len(percent_change_vals) for x in abs_percent_change]

print("Max average absolute change: %d", max(avg_abs_change))
print("Max absolute percent change: %d", max(abs_percent_change))

