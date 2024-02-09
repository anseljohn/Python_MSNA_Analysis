import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

mat = scipy.io.loadmat(input("Enter matlab file path: "))       # Load in the matlab file through user inputed file path
data = mat["data"]
titles = mat["titles"]                                          # The array of channel titles

# Get the index of the array holding "title"'s data e.g. "ECG" data
# Exits with failure if the data cannot be found
def get_title_ind(title):
    for i in range(len(titles)):
        if titles[i].strip() == title: # Titles may end up with trailing whitespace which must be stripped
            return i
    sys.exit("No " + title + " data found.")

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

AAC = []

APC = []

print("Max average absolute change: %d", max(AAC))
print("Max absolute percent change: %d", max(APC))