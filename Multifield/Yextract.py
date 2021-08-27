import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.animation import FuncAnimation
import matplotlib.animation
import numpy as np

FFMpegWriter = matplotlib.animation.writers['ffmpeg']
metadata = dict(title='trial_pleasework', artist='Agam',
                comment='FuckYouPython')
writer = FFMpegWriter(fps=0.5, metadata=metadata)

properties = {
    "density" : {"cmap": 'Blues_r', "pos": 0},
    "temp" : {"cmap": 'hot', "pos": 1},
    "ab_H2" : {"cmap": 'cividis', "pos": 8}
}

#########################################################################
file = open("./ExtractedCompleteData/multifield.0030.txt","r")
prop_name = "density"

selected_property = []
for lines in tqdm(range(0, 600*248*248)):
    d = file.readline()
    props = d.split(" ")
    selected_property.append(float(props[properties[prop_name]["pos"]]))

X = []
Z = []
for i in tqdm(range(0,248)):
    for j in range(0,600):
        X.append(j)
        Z.append(i)

slices = [80, 100, 110, 115, 120, 124, 125, 130, 150]

def update(slicenum):
    indices = []
    for i in range(0,248):
        for j in range(0,600):
            indices.append(600*248*i + 600*slices[slicenum] + j)
    
    planeslice = []
    min = 10e9
    max = -1
    for i in tqdm(indices):
        planeslice.append(selected_property[i])
        if(selected_property[i] > max): 
            max=selected_property[i]
        if(selected_property[i] < min):
            min = selected_property[i]

    plt.scatter(X,Z, c=planeslice, cmap=properties[prop_name]["cmap"])
    plt.title("0030 XZ "+str(slices[slicenum]) +" "+prop_name)

fig = plt.figure("0030 XZ "+ prop_name)
with writer.saving(fig, "trial.mp4", dpi=100):
    for slicenum in range(len(slices)):
        update(slicenum)
        writer.grab_frame()
