import sys
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def fstr(f):
    return str(round(f, 2))

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
    return str


x = {
        'a': 1, 
        'b': 2.2567, 
        'c': {
                'd': 4.3234,
                'e': 2.236,
                'f': [1, 2, 3, 123.4827],
                'g': {
                        'h': 4.2345,
                        'i': [4,2,5,8,231.323]
                     }
             },
        'j': [1, 2, 3, 4, 5.281239]
     }
print(output_str(x))
