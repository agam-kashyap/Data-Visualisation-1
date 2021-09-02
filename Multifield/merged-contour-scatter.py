from matplotlib import cm
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.animation
import os
import multiprocessing as mp

properties = {
        "density" : {"cmap": 'Blues_r', "pos": 0, "vmin": 20, "vmax": 18020},
        "temp" : {"cmap": 'hot', "pos": 1, "vmin": 72.16, "vmax": 30350},
        "ab_H2" : {"cmap": 'cividis', "pos": 8, "vmin": 1.76e-14, "vmax": 6.911e-05}
    }


X = [i for i in range(0,600)]
Z = [i for i in range(0,248)]

X_pos = []
Z_pos = []

for i in tqdm(range(0,248)):
    for j in range(0,600):
        X_pos.append(j)
        Z_pos.append(i)

def graph_creator(args):
    file = args[0]
    slicenum = args[1]
    prop_name_1 = args[2]
    prop_name_2 = args[3]
    openfile = open("./ExtractedCompleteData/" + file,"r")
    timestep = file.split(".")[1]

    print("Reading "+ str(timestep)) 

    selected_property_1 = []
    selected_property_2 = []
    for lines in tqdm(range(0, 600*248*248)):
        d = openfile.readline()
        props = d.split(" ")
        selected_property_1.append(float(props[properties[prop_name_1]["pos"]]))
        selected_property_2.append(float(props[properties[prop_name_2]["pos"]]))

    indices = []
    for i in range(0,248):
        for j in range(0,600):
            indices.append(600*248*i + 600*slicenum + j)

    planeslice_1 = []
    planeslice_2 = []
    for i in tqdm(indices):
        planeslice_1.append(selected_property_1[i])
        planeslice_2.append(selected_property_2[i])

    data_1 = [[0 for i in range(0, 248)] for j in range(0,600)]
    for i in tqdm(range(0,248)):
        for j in range(0,600):
            data_1[j][i] = planeslice_1[600*i + j]
    
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10,8), gridspec_kw={"height_ratios":[1, 0.05], "width_ratios":[1, 0.05]})
    fs = axs[0,0].scatter(Z_pos, X_pos, c=planeslice_2, cmap=properties[prop_name_2]["cmap"], vmin=properties[prop_name_2]["vmin"], vmax=properties[prop_name_2]["vmax"])
    fc = axs[0,0].contour(Z, X, data_1, levels=[0, 70, 500, 2000, 4000, 20000, 30000], cmap=properties[prop_name_1]["cmap"])
    axs[0,0].set_title(str(timestep) + " XZ " + str(slicenum) +" Temp Contour + Density Colormap", fontsize=15)
    axs[0,0].set_xlabel('Z position($10^{-3}$ parsecs)', fontsize=10)
    axs[0,0].set_ylabel('X position($10^{-3}$ parsecs)', fontsize=10)
    axs[0,0].tick_params(axis='both', which='major', labelsize=10)
    axs[0,0].tick_params(axis='both', which='minor', labelsize=10)

    fig.colorbar(fc, cax=axs[0,1], orientation="vertical")
    fig.colorbar(fs, cax=axs[1,0], orientation="horizontal")
    fig.savefig("./Images/Final/Combined/XZ.slice"+str(slicenum)+"."+ timestep+ ".png", dpi=300)
    print(fc.levels)
    print(str(timestep) + " complete!")

'''
prop_name_1 is the property name for which a contour plot will be generated
prop_name_2 is the property name for which the colormap will be generated
'''
def YsliceExtractor(prop_name_1, prop_name_2, slicenum):   
    arguments = []
    for file in sorted(os.listdir("./ExtractedCompleteData")):
        temp_list = []
        temp_list.append(file)
        temp_list.append(slicenum)
        temp_list.append(prop_name_1)
        temp_list.append(prop_name_2)
        arguments.append(temp_list)

    for args in arguments:
        graph_creator(args)
    print(prop_name_1+ " " + prop_name_2 +" completed!!!!!!!!!")

YsliceExtractor("temp", "density", 125)
