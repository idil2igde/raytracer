import numpy as np
#from raytracer.elements import OpticalElement
import matplotlib.pyplot as plt
#from raytracer.elements import OutputPlane

class Ray:
    def __init__(self, pos = np.array([0, 0, 0]), direc = np.array([0, 0, 1])):
        self.__pos = pos #the current position of the ray / a point in space
        self.__direc = direc #the current direction of the ray
        self.__vertices = [self.__pos] #all the points (positions) the ray passes through
        #brackets to create a list out of array
    #access methods
    def pos(self):
        return self.__pos
    def direc(self):
        return self.__direc
    def append(self, pos, direc):
        #adding new points along the ray in 3D
        self.__pos = np.array(pos)
        self.__direc = np.array(direc)
        self.__vertices.append(self.__pos)
        return self
    def vertices(self):
        #returning all the points along the ray as a list
        return self.__vertices
    def __repr__(self):
        #to return ray object in string form to make it more comprehensible
        return f"Ray(pos={self.__pos}, direc={self.__direc})"


class RayBundle(Ray):
    def __init__(self, rmax = 5., nrings = 5., multi = 6): #ray bundle is a circular light beam
        self.__rmax = rmax
        self.__nrings = nrings
        self.__multi = multi
        self.__rays = []

        #we NEED to add the CENTRAL RING
        for iring in range(1, int(nrings)+1): #0th ring doesn't make sense so range starts from 1
            radius = iring * rmax / nrings
            npoints = iring * multi
            for ipoint in range(npoints):
                theta = np.pi * 2 * ipoint / npoints
                x =  np.cos(theta) * radius
                y = np.sin(theta) * radius
                ray = Ray(np.array([x , y , 0]), np.array([0, 0, 1])) #direction is along optical axis and z start position is 0
                self.__rays.append(ray) #create a ray list of spherical coordinates

    def rays(self):
        return self.__rays
    
    def propagate_bundle(self, elements): #elements is a list of OpticalElements objects
        rays = self.rays()
        for i in rays:
            for j in elements:
            #propagate each ray through each element so we need nested loops
                j.propagate_ray(i)
    
    def track_plot(self):
        rays = self.rays()
        for i in rays:
            vertices = i.vertices()
            z = [point[2] for point in vertices]
            y = [point[1] for point in vertices]
            plt.plot(z, y)
        return plt.gcf() #get current figure
    
    def rms(self):
        #how to get where ray intersects the screen?
        rays = self.rays()
        x0 = 0
        y0 = 0
        radius_sum = 0
        for i in rays: #calculating the centroid
            final_pos = i.vertices()[-1] #the last position in the vertices is where the ray intersects the screen
            x0 += final_pos[0] / len(rays)
            y0 += final_pos[1] / len(rays)
        #determining the distance of each ray from the centroid as a list
        R_i =[]
        for j in rays:
            final_pos = j.vertices()[-1]
            x = final_pos[0]
            y = final_pos[1]
            distance = np.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0))
            R_i.append(distance)
        #calculating the RMS radius
        for k in R_i:
            radius_sum += k * k
        rms = np.sqrt(radius_sum / len(rays))
        return rms
    
    def spot_plot(self): #plots the output x-y view of the screen
        plt.figure() #to prevent graphs from being plotted on top of each other

        rays = self.rays()
        for i in rays:
            final_pos = i.vertices()[-1] #position of rays when they intersect with the output plane
            x = final_pos[0]
            y = final_pos[1]
            plt.scatter(x,y) #creates a scatter plot with non-connected points
        
        return plt.gcf()

