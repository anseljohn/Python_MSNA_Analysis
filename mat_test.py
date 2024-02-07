import scipy.io
mat = scipy.io.loadmat('CSP_001_HUT_VNSOFF.mat')
print(mat["data"][0])