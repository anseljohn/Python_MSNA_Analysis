import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def ind(title):
    for i in range(len(titles)):
        if titles[i].strip() == title: # Titles may end up with trailing whitespace which must be stripped
            return i
    sys.exit("No " + title + " data found.")

def get_data(title):
    start = int(mat['datastart'][0][ind(title)])
    end = int(mat['dataend'][0][ind(title)])
    return data[start:end]


# Exit if there aren't enough arguments
if (len(sys.argv) < 3):
    sys.exit("Error: Syntax: python analyze.py path/to/matlab_data.mat \"Outcome Variable Name\"")

# Loading the matlab file in by command line arg
mat = scipy.io.loadmat(sys.argv[1]) 

data = mat['data'][0]
titles = mat['titles']
ecg = get_data("ECG")
print(ecg)
print(mat)
print(mat["com"])