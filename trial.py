import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random

def main():
    numframes = 10
    numpoints = 10
    color_data = np.random.random((numframes, numpoints))
    x, y, c = np.random.random((3, numpoints))

    fig = plt.figure()
    scat = plt.scatter(x, y, c=c, cmap='Blues')

    ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes),
                                  fargs=(color_data, scat))
    plt.show()

def update_plot(i, data, scat):
    scat.set_array(np.array([random.random() for x in range(10)]))
    return scat,

main()