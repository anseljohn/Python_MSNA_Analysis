import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

mat = scipy.io.loadmat(input("Enter matlab file path: "))       # Load in the matlab file through user inputed file path
outcome = input("Enter outcome variable: ")
data = mat["data"]                                              # The 2d array containing all data
titles = mat["titles"]                                          # The array of channel titles

# Get the index of the array holding "title"'s data e.g. "ECG" data
# Exits with failure if the data cannot be found
def get_title_ind(title):
    for i in range(len(titles)):
        if titles[i].strip() == title: # Titles may end up with trailing whitespace which must be stripped
            return i
    sys.exit("No " + title + " data found.")

outcome = data[get_title_ind(outcome)]
ecg = data[get_title_ind("ECG")]
msna = data[get_title_ind("Integrated MSNA")]
bc_no = data[get_title_ind("Burst Comment Number")]
bs = data[get_title_ind("Burst Size")]
data_len = len(ecg)

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