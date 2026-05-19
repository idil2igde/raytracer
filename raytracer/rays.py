import numpy as np
class Ray:
    def __init__(self, pos = np.array([0, 0, 0]), direc = np.array([0, 0, 1])):
        self.__pos = pos
        self.__direc = direc
    #access methods
    def pos(self):
        return self.__pos
    def direc(self):
        return self.__direc
    def append(self, pos, direc):
        #adding new points in the z direction
        self.pos()[2] += 1
    def vertices(self):
        #returning all the points along the ray as a list
        return self.__pos[2]
        
