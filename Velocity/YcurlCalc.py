import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import os
from tqdm import tqdm

FFMpegWriter = matplotlib.animation.writers['ffmpeg']
metadata = dict(title='Velocity Change', artist='Agam',
                comment='This is NSFW')
writer = FFMpegWriter(fps=2, metadata=metadata)

slicenum = 125

# fig = plt.figure("Velocity XZ "+str(slicenum), figsize=(30,30))
fig, ax = plt.subplots()
with writer.saving(fig, "Velocity.XZ.slice"+str(slicenum)+".mp4", dpi=100):
    for file in sorted(os.listdir("./ExtractedCompleteData")):
        f = open("./ExtractedCompleteData/"+file)
        timestep = file.split(".")[1]

        colorfile = open("../Multifield/ExtractedCompleteData/multifield."+file.split(".")[1]+".txt")

        indices = []
        for i in range(0,248):
            for j in range(0,600):
                indices.append(600*248*i + 600*slicenum + j)
                indices.append(600*248*i + 600*(slicenum+1) + j)

        datapoint = []
        datatemp = []
        for i in tqdm(range(0, 600*248*248)):
            dp = f.readline()
            datapoint.append(dp)

            cf = colorfile.readline()
            temperature = cf.split(" ")
            datatemp.append(float(temperature[1]))

        print(file + " Read Complete!")

        req_data = {}
        for i in tqdm(indices):
            dp = datapoint[i].split(" ")
            vec3 = {
                "X": float(dp[0]),
                "Y": float(dp[1]),
                "Z": float(dp[2]),
            }
            req_data[i] = vec3
        print("Point Extraction Complete!")

        # curl(x,y) 
        # curl(y,z)
        # index iteration will be from [0, 599) for X, [0, 248) for Z, since the i+1, k+1 indices are required for calculation
        # So, we should have data of 599*248

        # For a given (i,j,k) it's linear index can be given as: 
        # X*Y*k + X*j + i

        curl_xy = []
        curl_yz = []
        X_pos = []
        Z_pos = []
        X = 600
        Y = 248

        colorval = []

        max_c_xy = -1
        min_c_xy = 10e9
        max_c_yz = -1
        min_c_yz = 10e9

        for i in tqdm(range(599)):
            for j in range(247):
                vy_i1jk = req_data[X*Y*j + X*(slicenum+1) + i]["Y"]
                vy_ijk  = req_data[X*Y*j + X*slicenum + i]["Y"]
                vx_ij1k = req_data[X*Y*(j+1) + X*slicenum + i]["X"]
                vx_ijk  = req_data[X*Y*j + X*slicenum + i]["X"]

                vz_ij1k = req_data[X*Y*j + X*(slicenum+1) + i]["Z"]
                vz_ijk  = req_data[X*Y*j + X*slicenum + i]["Z"]
                vy_ijk1 = req_data[X*Y*(j+1) + X*slicenum + i]["Y"]

                X_pos.append(i)
                Z_pos.append(j)
                
                calc_curl_xy = (vy_i1jk - vy_ijk - vx_ij1k + vx_ijk)/0.001
                calc_curl_yz = (vz_ij1k - vz_ijk - vy_ijk1 + vy_ijk)/0.001
                curl_xy.append(calc_curl_xy)
                curl_yz.append(calc_curl_yz)

                if(calc_curl_xy < min_c_xy): min_c_xy = calc_curl_xy
                if(calc_curl_xy > max_c_xy): max_c_xy = calc_curl_xy
                if(calc_curl_yz < min_c_yz): min_c_yz = calc_curl_yz
                if(calc_curl_yz > max_c_yz): max_c_yz = calc_curl_yz

                colorval.append(datatemp[X*Y*j + X*slicenum + i])

        for i in range(599*247):
            curl_xy[i] = math.tanh(curl_xy[i])
            curl_yz[i] = math.tanh(curl_yz[i])

        ax.set_title("Velocity XZ "+timestep+ " slice125", fontsize=30)
        ax.quiver(X_pos, Z_pos, curl_yz, curl_xy, colorval, cmap='hot')
        writer.grab_frame()
        print(timestep + " complete!")