import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import numpy as np
import pickle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

SAVING = 0
DRAWING = 1
properties = {
        "density" : {"cmap": 'Blues_r', "pos": 0, "vmin": 20, "vmax": 18020},
        "temp" : {"cmap": 'hot', "pos": 1, "vmin": 72.16, "vmax": 30350},
        "ab_H2" : {"cmap": 'bone', "pos": 8, "vmin": 1.76e-14, "vmax": 6.911e-05},
        "ab_H-": {"cmap": 'pink', "pos": 7, "vmin": 1e-99, "vmax":1.629e-07},
        "ab_H2+": {"cmap": 'copper', "pos": 9, "vmin": 1e-99, "vmax": 1.691e-08}
    }

# Wanted to compare the abundance of the H- and H2+ with that of H2 but their abundance is so low that it is not possible to see visualisation for the same
# properties = {
#         "density" : {"cmap": 'Blues_r', "pos": 0, "vmin": 20, "vmax": 18020},
#         "temp" : {"cmap": 'hot', "pos": 1, "vmin": 72.16, "vmax": 30350},
#         "ab_H2" : {"cmap": 'bone', "pos": 8, "vmin": 1e-99, "vmax": 6.911e-05},
#         "ab_H-": {"cmap": 'bone', "pos": 7, "vmin": 1e-99, "vmax":6.911e-05},
#         "ab_H2+": {"cmap": 'bone', "pos": 9, "vmin": 1e-99, "vmax": 6.911e-05}
#     }

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
    timestep = file.split(".")[1]
    if(args[3] == SAVING):
        print("Reading "+ file)
        openfile = open("./ExtractedCompleteData/" + file,"r")    
        selected_property_1 = []
        selected_property_2 = []
        selected_property_3 = []
        for lines in tqdm(range(0, 600*248*248)):
            d = openfile.readline()
            props = d.split(" ")
            selected_property_1.append(float(props[properties[prop_name[0]]["pos"]]))
            selected_property_2.append(float(props[properties[prop_name[1]]["pos"]]))
            selected_property_3.append(float(props[properties[prop_name[2]]["pos"]]))

        indices = []
        for i in range(0,248):
            for j in range(0,600):
                indices.append(600*248*i + 600*slicenum + j)
        
        planeslice_1 = []
        planeslice_2 = []
        planeslice_3 = []

        min_prop_1 = 10e9 
        max_prop_1 = -1
        min_prop_2 = 10e9
        max_prop_2 = -1
        min_prop_3 = 10e9
        max_prop_3 = -1

        for i in tqdm(indices):
            planeslice_1.append(selected_property_1[i])
            planeslice_2.append(selected_property_2[i])
            planeslice_3.append(selected_property_3[i])

            if(selected_property_1[i] > max_prop_1): max_prop_1 = selected_property_1[i]
            if(selected_property_1[i] < min_prop_1): min_prop_1 = selected_property_1[i]
            if(selected_property_2[i] > max_prop_2): max_prop_2 = selected_property_2[i]
            if(selected_property_2[i] < min_prop_2): min_prop_2 = selected_property_2[i]
            if(selected_property_3[i] > max_prop_3): max_prop_3 = selected_property_3[i]
            if(selected_property_3[i] < min_prop_3): min_prop_3 = selected_property_3[i]
    
        filename_1 = timestep + "." + prop_name[0]+"."+ str(slicenum) + ".property.p"
        with open(filename_1, "wb") as filehandler:
            pickle.dump(np.asarray(planeslice_1), filehandler)
        filename_2 = timestep + "." + prop_name[1]+"."+ str(slicenum) + ".property.p"
        with open(filename_2, "wb") as filehandler:
            pickle.dump(np.asarray(planeslice_2), filehandler)
        filename_3 = timestep + "." + prop_name[2]+"."+ str(slicenum) + ".property.p"
        with open(filename_3, "wb") as filehandler:
            pickle.dump(np.asarray(planeslice_3), filehandler)
        return ((min_prop_1, min_prop_2, min_prop_3),(max_prop_1, max_prop_2, max_prop_3))

    elif(args[3] == DRAWING):
        print("Extracting Saved Data: " + file)
        filename_1 = timestep + "." + prop_name[0]+"."+ str(slicenum) + ".property.p"
        filename_2 = timestep + "." + prop_name[1]+"."+ str(slicenum) + ".property.p"
        filename_3 = timestep + "." + prop_name[2]+"."+ str(slicenum) + ".property.p"
        
        with open(filename_1, "rb") as filehandler:
            planeslice_1 = pickle.load(filehandler)
        
        with open(filename_2, "rb") as filehandler:
            planeslice_2 = pickle.load(filehandler)
        
        with open(filename_3, "rb") as filehandler:
            planeslice_3 = pickle.load(filehandler)
        
        fig1 = plt.figure(figsize=(10,10))
        # plt.title(timestep + " XZ " + str(slicenum) + " Comparision: H-, $H_2$, $H_{2+}$",fontsize=15)
        gs = fig1.add_gridspec(3, hspace = 0)
        axs = gs.subplots(sharex=True, sharey=True)
        f1 = axs[0].scatter(X,Z, c=planeslice_1, cmap=properties[prop_name[0]]["cmap"], vmin=properties[prop_name[0]]["vmin"], vmax=properties[prop_name[0]]["vmax"])
        f2 = axs[1].scatter(X,Z, c=planeslice_2, cmap=properties[prop_name[1]]["cmap"], vmin=properties[prop_name[1]]["vmin"], vmax=properties[prop_name[1]]["vmax"])
        f3 = axs[2].scatter(X,Z, c=planeslice_3, cmap=properties[prop_name[2]]["cmap"], vmin=properties[prop_name[2]]["vmin"], vmax=properties[prop_name[2]]["vmax"])
        c1 = fig1.colorbar(f1, ax=axs, orientation="vertical")
        c2 = fig1.colorbar(f2, ax=axs, orientation="vertical")
        c3 = fig1.colorbar(f3, ax=axs, orientation="vertical")

        fig1.text(0.04, 0.5, 'Z position($10^{-3}$ parsecs)', va='center', rotation='vertical')
        fig1.text(0.5, 0.04, 'X position($10^{-3}$ parsecs)', ha='center')
        for ax in range(len(axs)):
            axs[ax].set_ylabel(prop_name[ax])

        # for axi in axs.flat:
        #     axi.yaxis.set_major_locator(MultipleLocator(250))
        # plt.show()
        # ax.tick_params(axis='both', which='major', labelsize=10)
        # ax.tick_params(axis='both', which='minor', labelsize=10)
        # fig.canvas.draw()  
        fig1.savefig("./Images/Final/Comparision/XZ.slice"+str(slicenum)+"."+ timestep+ ".png", dpi=300)
        
        # print(timestep + " complete!")

    
def YsliceExtractor(prop_name, slicenum, action):   
    arguments = []
    minmax = []
    for file in sorted(os.listdir("./ExtractedCompleteData")):
        temp_list = []
        temp_list.append(file)
        temp_list.append(slicenum)
        temp_list.append(prop_name)
        temp_list.append(action)
        arguments.append(temp_list)

    for args in arguments:
        if(action == SAVING):
            minmax.append(graph_creator(args))
        else:
            graph_creator(args)

    if(action==SAVING):
        min_prop_1 = 10e9 
        max_prop_1 = -1
        min_prop_2 = 10e9
        max_prop_2 = -1
        min_prop_3 = 10e9
        max_prop_3 = -1
        print(minmax)
        for i in range(len(minmax)):
            # implies min prop set
            if(min_prop_1 > minmax[i][0][0]): min_prop_1 = minmax[i][0][0]
            if(min_prop_2 > minmax[i][0][1]): min_prop_2 = minmax[i][0][1]
            if(min_prop_3 > minmax[i][0][2]): min_prop_3 = minmax[i][0][2]
            if(max_prop_1 < minmax[i][1][0]): max_prop_1 = minmax[i][1][0]
            if(max_prop_2 < minmax[i][1][1]): max_prop_2 = minmax[i][1][1]
            if(max_prop_3 < minmax[i][1][2]): max_prop_3 = minmax[i][1][2]
        return (min_prop_1, max_prop_1, min_prop_2, max_prop_2, min_prop_3, max_prop_3)

# (min_prop_1, max_prop_1, min_prop_2, max_prop_2, min_prop_3, max_prop_3) = YsliceExtractor(["ab_H-","ab_H2","ab_H2+"], 125, SAVING)
# print("ab_H- " + str(min_prop_1) + " " + str(max_prop_1))
# print("ab_H2 " + str(min_prop_2) + " " + str(max_prop_2))
# print("ab_H2+ " + str(min_prop_3) + " " + str(max_prop_3))

YsliceExtractor(["ab_H-","ab_H2","ab_H2+"], 125, DRAWING)