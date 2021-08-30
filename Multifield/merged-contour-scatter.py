from matplotlib import cm
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.animation
import os
import multiprocessing as mp

def YsliceExtractor(slicenum):
    FFMpegWriter = matplotlib.animation.writers['ffmpeg']
    metadata = dict(title='trial_pleasework', artist='Agam',
                    comment='FuckYouPython')
    writer = FFMpegWriter(fps=2, metadata=metadata)

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

    min = 10e9
    max = -1

    fileno = [30, 40, 50, 60, 70, 80, 85, 90]
    fig, ax = plt.subplots(figsize=(30,30))
    global cf
    cf = ax.contour([i for i in range(2)], [i for i in range(2)], [[i for i in range(2)] for j in range(2)])
    with writer.saving(fig, "XZ.slice"+str(slicenum)+"TempContourDensityColormap.mp4", dpi=100):
        for number in fileno:
            # update(file)
            print("Reading "+ str(number)) 
            openfile = open("./ExtractedCompleteData/multifield.00" + str(number) + ".txt","r")
            prop_name_1 = "temp"
            prop_name_2 = "density"

            selected_property_1 = []
            selected_property_2 = []
            for lines in tqdm(range(0, 600*248*248)):
                d = openfile.readline()
                props = d.split(" ")
                selected_property_1.append(float(props[properties[prop_name_1]["pos"]]))
                selected_property_2.append(float(props[properties[prop_name_2]["pos"]]))

            slicenum = 125
            indices = []
            for i in range(0,248):
                for j in range(0,600):
                    indices.append(600*248*i + 600*slicenum + j)

            planeslice_1 = []
            planeslice_2 = []
            for i in tqdm(indices):
                planeslice_1.append(selected_property_1[i])
                planeslice_2.append(selected_property_2[i])

            X_pos = []
            Z_pos = []
            data_1 = [[0 for i in range(0, 248)] for j in range(0,600)]
            # data_2 = [[0 for i in range(0, 248)] for j in range(0,600)]
            X = [i for i in range(0,600)]
            Z = [i for i in range(0,248)]
            for i in tqdm(range(0,248)):
                for j in range(0,600):
                    X_pos.append(j)
                    Z_pos.append(i)
                    data_1[j][i] = planeslice_1[600*i + j]
                    # data_2[j][i] = planeslice_2[599*i + j]
            for coll in cf.collections:
                coll.remove()
            cm = ax.scatter(Z_pos,X_pos, c=planeslice_2, cmap='Blues_r')
            cf = ax.contour(Z, X, data_1, levels=[500, 2000, 4000, 20000, 30000] , cmap='hot')
            ax.set_title(str(number) + " XZ " + str(slicenum) +" Temp Contour + Density Colormap", fontsize=20)
            writer.grab_frame()
            print(str(number) + " complete!")

    print(min, max)

YsliceExtractor(125)