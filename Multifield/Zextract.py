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
    for i in range(0,248*600):
        indices.append(600*248*slicenum +i)
    
    planeslice = []
    for i in tqdm(indices):
	    planeslice.append(selected_property[i])

    print(len(planeslice))

    X = []
    Z = []
    for i in tqdm(range(0,248)):
	    for j in range(0,600):
		    X.append(j)
		    Z.append(i)
    plt.figure("0030 XY "+str(slicenum) +" "+ prop_name)
    plt.scatter(X,Z, c=planeslice, cmap='hot')
    plt.title("0030 XY "+str(slicenum) +" "+prop_name)
    plt.savefig("0030 XY "+str(slicenum) +" "+prop_name+".png")
    print("Slice "+str(slicenum)+" Complete!")