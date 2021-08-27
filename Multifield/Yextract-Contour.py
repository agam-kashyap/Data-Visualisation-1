import matplotlib.pyplot as plt
from tqdm import tqdm

properties = {
    "density" : {"cmap": 'Blues_r', "pos": 0},
    "temp" : {"cmap": 'hot', "pos": 1} 
}

file = open("./ExtractedCompleteData/multifield.0030.txt","r")
prop_name = "temp"

selected_property = []
for lines in tqdm(range(0, 600*248*248)):
	d = file.readline()
	props = d.split(" ")
	selected_property.append(float(props[properties[prop_name]["pos"]]))
print(len(selected_property))

slice = [20, 30, 50, 100, 124, 150, 200, 230]
for slicenum in slice:
    indices = []
    for i in range(0,248):
        for j in range(0,600):
            indices.append(600*248*i + 600*slicenum + j)
    
    planeslice = []
    min = 10e9
    max = -1
    for i in tqdm(indices):
        planeslice.append(selected_property[i])
        if(selected_property[i] > max): 
            max=selected_property[i]
        if(selected_property[i] < min):
            min = selected_property[i]
    
    print(min)
    print(max)
    print(len(planeslice))

    data = [[0 for i in range(0, 248)] for j in range(0,600)]
    X = [i for i in range(0,600)]
    Z = [i for i in range(0,248)]
    for i in tqdm(range(0,248)):
        for j in range(0,600):
            # X.append(j)
            # Z.append(i)
            data[j][i] = planeslice[599*i + j]

    plt.figure("0030 XZ "+str(slicenum) +" "+ prop_name)
    # plt.scatter(X,Z, c=planeslice, cmap='hot')
    plt.contourf(Z,X, data, cmap='hot')
    plt.title("0030 XZ "+str(slicenum) +" "+prop_name)
    plt.show()
    # plt.savefig("0030 XZ "+str(slicenum) +" "+prop_name+".png")
    print("Slice "+str(slicenum)+" Complete!")