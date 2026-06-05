"""GenPolar module"""
import numpy as np

def rtrings(rmax=5., nrings=5, multi=6):
    """
    Generates polar coordinate concentring rings, centered at the origin 0 point.
    Calculates and yields the radius of the rings at a given point on the ring and the angle from the axis.
    """
    yield 0., 0.
    for iring in range(1, int(nrings)+1): #0th ring doesn't make sense so range starts from 1
            radius = iring * rmax / nrings
            npoints = iring * multi
            for ipoint in range(npoints):
                theta = np.pi * 2 * ipoint / npoints
                yield radius, theta
        
