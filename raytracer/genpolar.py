import numpy as np

def rtrings(rmax=5., nrings=5, multi=6):
    yield 0., 0.

    for iring in range(1, nrings + 1):
        radius = iring * rmax / nrings #max radius / number of rings gives the spacing between the riings
        npoints = iring * multi #number of points on each ring

        for ipoint in range(npoints):
            theta = 2 * np.pi * ipoint / npoints #location of ipoint in all points along the ring fraction times 2pi gives the angle
            yield radius, theta