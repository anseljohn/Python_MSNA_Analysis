import subprocess
import sys

#https://stackoverflow.com/questions/12332975/installing-python-module-within-code
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
	
install("cffi")

import os
#This would need to be changed based on where you keep the code
os.chdir('C:/Users/Miguel Anselmo/Dev/adinstruments_sdk_python/adi')

# For 64 bit windows
exec(open("cffi_build.py").read())