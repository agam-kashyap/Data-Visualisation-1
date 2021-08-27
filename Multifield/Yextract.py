import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.animation import FuncAnimation
import matplotlib.animation
import numpy as np
import os

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

X = []
Z = []
for i in tqdm(range(0,248)):
    for j in range(0,600):
        X.append(j)
        Z.append(i)

slicenum = 125
prop_name = "temp"
min = 10e9
max = -1

def update(file):
    openfile = open("./ExtractedCompleteData/" + file,"r")
    timestep = file.split(".")[1]
    selected_property = []
    for lines in tqdm(range(0, 600*248*248)):
        d = openfile.readline()
        props = d.split(" ")
        selected_property.append(float(props[properties[prop_name]["pos"]]))

    indices = []
    for i in range(0,248):
        for j in range(0,600):
            indices.append(600*248*i + 600*slicenum + j)
    
    planeslice = []
    for i in tqdm(indices):
        planeslice.append(selected_property[i])
        if(selected_property[i] > max): 
            max=selected_property[i]
        if(selected_property[i] < min):
            min = selected_property[i]

    plt.scatter(X,Z, c=planeslice, cmap=properties[prop_name]["cmap"])
    plt.title(timestep + " XZ " + str(slicenum) +" "+prop_name)

fig = plt.figure("XZ "+str(slicenum) + " "+ prop_name, figsize=(30,30))
with writer.saving(fig, "XZ.slice"+str(slicenum)+"."+prop_name+".mp4", dpi=100):
    for file in sorted(os.listdir("./ExtractedCompleteData")):
        # update(file)
        print("Reading "+ file)
        openfile = open("./ExtractedCompleteData/" + file,"r")
        timestep = file.split(".")[1]
        selected_property = []
        for lines in tqdm(range(0, 600*248*248)):
            d = openfile.readline()
            props = d.split(" ")
            selected_property.append(float(props[properties[prop_name]["pos"]]))

        indices = []
        for i in range(0,248):
            for j in range(0,600):
                indices.append(600*248*i + 600*slicenum + j)
        
        planeslice = []
        for i in tqdm(indices):
            planeslice.append(selected_property[i])
            if(selected_property[i] > max): 
                max=selected_property[i]
            if(selected_property[i] < min):
                min = selected_property[i]

        plt.scatter(X,Z, c=planeslice, cmap=properties[prop_name]["cmap"])
        plt.title(timestep + " XZ " + str(slicenum) +" "+prop_name, fontsize=30)
        writer.grab_frame()
        print(timestep + " complete!")

print(min, max)