import matplotlib.pyplot as plt
from tqdm import tqdm

properties = {
    "density" : {"cmap": 'Blues_r', "pos": 0},
    "temp" : {"cmap": 'hot', "pos": 1} 
}

file = open("./ExtractedCompleteData/multifield.0030.txt","r")
prop_name_1 = "temp"
prop_name_2 = "density"

selected_property_1 = []
selected_property_2 = []
for lines in tqdm(range(0, 600*248*248)):
	d = file.readline()
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

plt.figure("0030 XZ "+str(slicenum) +" "+ prop_name_1 + " " + prop_name_2)
plt.scatter(Z_pos,X_pos, c=planeslice_2, cmap='Blues_r')
plt.contour(Z,X, data_1, levels=[500, 2000, 4000, 20000, 30000] , cmap='hot')
plt.show()
    # plt.savefig("0030 XZ "+str(slicenum) +" "+prop_name+".png")