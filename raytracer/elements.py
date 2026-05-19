from raytracer.rays import Ray
#importing Ray class from raytracer folder and rays file
import numpy as np
from raytracer.physics import refract


class OpticalElement:
        def intercept(self, ray):
                #tests whether the ray will intercept with the optical object
                raise NotImplementedError('intercept() needs to be implemented in derived classes')
        def propagate_ray(self, ray):
                #tests hwo the ray propogates in the optical object and update the ray's internal characteristics such as poisiton and direction
                raise NotImplementedError('propagate_ray() needs to be implemented in derived classes')
        

class SphericalRefraction(OpticalElement):
        def __init__(self, z_0 = 0, aperature = 0, curvature = 0., n_1 = 0., n_2 = 0.):
                self.__z0 = z_0
                #where surface intercepts optical axis (z-axis)
                self.__aperature = aperature
                #extend of surface from optical axis 
                self.__curvature = curvature
                #curvature of the surface (radius of spherical surface)
                self.__n1 = n_1
                self.__n2 = n_2
        #the accessor methods for each parameter of SphericalRefraction initialization method
        def z_0(self):
                return self.__z0
        def aperature(self):
                return self.__aperature
        def curvature(self):
                return self.__curvature
        def n_1(self):
                return self.__n1
        def n_2(self):
                return self.__n2
        
        def intercept(self, ray):
                direc = ray.direc()
                pos = ray.pos()
                rad = self.curvature()
                dot_1 = np.dot(pos, direc)
                disc = dot_1 * dot_1 - (np.dot(pos, pos) - rad * rad)
                l1 = - dot_1 + np.sqrt(disc)
                l2 = - dot_1 - np.sqrt(disc)
                if disc < 0:
                        return None #no real solutions to quad formula exists for negative discriminant
                intercept_pos = pos + l1 * direc #ray only travels forward, adding intercept distance to initial ray position in ray direction
                return intercept_pos
        
        def propagate_ray(self, ray):
                direc = ray.direc()
                normal = np.array([0, 0, 1]) #normal to a spherical surface
                n_1 = self.n_1()
                n_2 = self.n_2()
                new_pos = self.intercept(ray)
                new_direc = refract(direc, normal, n_1, n_2)
                if new_direc is None:
                        return None
                if new_pos is None:
                        return None
                ray.append(new_pos, new_direc)

