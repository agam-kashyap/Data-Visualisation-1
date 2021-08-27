import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import math, os

'''
0 0
1 0
2 0
3 0
4 0
5 0
. .
. .
. .
.
.
.
.
0 1
1 1
2 1
3 1
. .
. .
.
.
0 n
. .
. .
.
.
m n 
'''
path = "./PropertyData"
filename = "multifield.0030.XY.slice124.temp.txt"
X = []
Y = []
data = []
max = 0.0
min = 1.0E9
# filename = "multifield.0030.XY.slice124.density".split(".")
filename = filename.split(".")
datafile = open("./PropertyData/"+filename[0]+"."+filename[1]+"."+filename[2]+"."+filename[3]+"."+filename[4]+".txt", "r")
for i in range(0,248):
    for j in range(0,600):
        X.append(j)
        Y.append(i)
        value_string = datafile.readline()
        if(value_string == ""):
            data.append(0)
        else:
            data.append(float(value_string))
        if(data[-1] > max):
            max = data[-1]
        if(data[-1] < min):
            min = data[-1]

print(min, max)
plt.figure(filename[1]+ " " + filename[2] + " " + filename[3] + " " + filename[4])
plt.scatter(X,Y,c=data, cmap='Blues_r')
plt.title(filename[1]+ " " + filename[2] + " " + filename[3] + " " + filename[4])
# plt.savefig(filename[1]+ " " + filename[2] + " " + filename[3] + " " + filename[4]+".png")
plt.show()