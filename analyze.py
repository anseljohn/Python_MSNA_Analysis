import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

bc_no = 0               # Index for burst comment number array
burst_size = 1          # Index for burst sizes array

mat = scipy.io.loadmat(input("Enter matlab file path: "))         # Load in the matlab file through user inputed file path
titles = mat["titles"]                                          # The array of channel titles
# bc_no_arr = mat["data"][bc_no]                                  # The array for burst comment numbers
# bs_arr = mat["data"][burst_size]                                # The array for burst sizes
# data_len = len(bc_no_arr)                                       # Easy access for array length

def is_title(title):
    for curr_title in titles:
        print(curr_title)
        if title == curr_title:
            return True
    return False

# Titles need formatting, there can be trailing whitespace when exporting to .mat
for i in range(len(titles)):
    titles[i] = titles[i].strip()

# Checking for required channels in case invalid data is entered
if not is_title("ECG"): 
    sys.exit("No ECG data found.")
if not is_title("Integrated MSNA"):
    sys.exit("No integrated MSNA data found.")

print(len(mat["data"][0]))
print(mat)

#plt.plot(np.asarray(mat["data"][0]))
#plt.plot(mat["data"][0])
#plt.show()

# # Determining bursts based on burst comment numbers
# bursts = []
# for i in range(len(bc_no_arr)):
#     burst = False
#     if i == 0:
#         burst = bc_no_arr[i] != bc_no_arr[i+1]
#     else:
#         burst = bc_no_arr[i] != bc_no_arr[i-1]
#     bursts.append(burst)

# # Get the largest burst
# max_burst = float('-inf')
# for i in range(data_len):
#     curr_burst = bs_arr[i]
#     max_burst = curr_burst if bursts[i] and bs_arr[i] > max_burst else max_burst

# # Normalize burst sizes and turn into percentages
# for i in range(data_len):
#     bs_arr[i] = bs_arr[i] / max_burst * 100 if bursts[i] else float('-inf')