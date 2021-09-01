import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.animation
import os
import multiprocessing as mp
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

properties = {
        "density" : {"cmap": 'Blues_r', "pos": 0, "vmin": 20, "vmax": 18020},
        "temp" : {"cmap": 'hot', "pos": 1, "vmin": 72.16, "vmax": 30350},
        "ab_H2" : {"cmap": 'cividis', "pos": 8, "vmin": 1.76e-14, "vmax": 6.911e-05}
    }

X = []
Z = []
for i in tqdm(range(0,248)):
    for j in range(0,600):
        X.append(j)
        Z.append(i)

def graph_creator(args):
    file = args[0]
    slicenum = args[1]
    prop_name = args[2]
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

    fig, (ax, cax) = plt.subplots(nrows=2, figsize=(10,8), gridspec_kw={"height_ratios":[1, 0.05]})
    f=ax.scatter(X,Z, c=planeslice, cmap=properties[prop_name]["cmap"], vmin=properties[prop_name]["vmin"], vmax=properties[prop_name]["vmax"])
    cb = fig.colorbar(f, cax=cax, orientation="horizontal")
    ax.set_title(timestep + " XZ " + str(slicenum) +" "+prop_name, fontsize=15)
    ax.set_xlabel('X position($10^{-3}$ parsecs)', fontsize=10)
    ax.set_ylabel('Z position($10^{-3}$ parsecs)', fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    fig.canvas.draw()  
    fig.savefig("./Images/Final/"+ prop_name + "/XZ.slice"+str(slicenum)+"."+prop_name+"." + timestep+ ".png", dpi=300)
    
    print(timestep + " complete!")

    
def YsliceExtractor(prop_name, slicenum):   
    arguments = []
    for file in sorted(os.listdir("./ExtractedCompleteData")):
        temp_list = []
        temp_list.append(file)
        temp_list.append(slicenum)
        temp_list.append(prop_name)
        arguments.append(temp_list)

    for args in arguments:
        graph_creator(args)
    print(prop_name+ " completed!!!!!!!!!")

YsliceExtractor("ab_H2", 125)