import numpy as np
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
        
