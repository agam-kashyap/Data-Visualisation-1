import matplotlib.pyplot as plt
from tqdm import tqdm

file = open("./ExtractedCompleteData/multifield.0030.txt","r")
density = []
for lines in tqdm(range(0, 600*248*248)):
	d = file.readline()
	props = d.split(" ")
	density.append(float(props[1]))
print(len(density))

slice = [20, 30, 50, 100, 124, 150, 200, 230]
for slicenum in slice:
	planeslice = []
	for i in tqdm(range(0, 600*248*248)):
		if(i == slicenum): planeslice.append(density[i])
		else:
			if((i-slicenum)%600 == 0):
				planeslice.append(density[i])

	print(len(planeslice))

	Y = []
	Z = []
	for i in range(0,248):
		for j in range(0,248):
			Y.append(j)
			Z.append(i)
	plt.figure("0030 YZ "+str(slicenum) +" temp")
	plt.scatter(Y,Z, c=planeslice, cmap='hot')
	plt.title("0030 YZ "+str(slicenum) +" temp")
	plt.savefig("0030 YZ "+str(slicenum) +" temp.png")
	# plt.show()