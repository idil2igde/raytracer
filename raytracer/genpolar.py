import numpy as np

def rtrings(rmax=5., nrings=5, multi=6):
    yield 0., 0.

    for iring in range(1, int(nrings)+1): #0th ring doesn't make sense so range starts from 1
            radius = iring * rmax / nrings
            npoints = iring * multi
            for ipoint in range(npoints):
                theta = np.pi * 2 * ipoint / npoints
                yield radius, theta
        

"""
for iring in range(1, int(nrings)+1): #0th ring doesn't make sense so range starts from 1
            radius = iring * rmax / nrings
            npoints = iring * multi
            for ipoint in range(npoints):
                theta = np.pi * 2 * ipoint / npoints
                x =  np.cos(theta) * radius
                y = np.sin(theta) * radius
                ray = Ray(np.array([x , y , 0]), np.array([0, 0, 1])) #direction is along optical axis and z start position is 0
                self.__rays.append(ray) #create a ray list of spherical coordinates
        
"""