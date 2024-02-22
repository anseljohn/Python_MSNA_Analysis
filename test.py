import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

mat = scipy.io.loadmat(input("Enter matlab file path: "))       # Load in the matlab file through user inputed file path
data = mat['data'][0]
titles = mat['titles']

def starts(index):
    return int(mat['datastart'][0][index])

def ends(index):
    return int(mat['dataend'][0][index])

def ind(title):
    for i in range(len(titles)):
        if titles[i].strip() == title: # Titles may end up with trailing whitespace which must be stripped
            return i
    sys.exit("No " + title + " data found.")

def get_data(title):
    start = int(mat['datastart'][0][ind(title)])
    end = int(mat['dataend'][0][ind(title)])
    return data[start:end]

ecg = get_data("ECG")
print(ecg)