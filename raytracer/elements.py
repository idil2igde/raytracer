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
                if disc < 0:
                        return None #no real solutions to quad formula exists for negative discriminant
                l1 = - dot_1 + np.sqrt(disc)
                l2 = - dot_1 - np.sqrt(disc)
                intercept_pos = pos + min(l1, l2) * direc #ray only travels forward, adding intercept distance to initial ray position in ray direction
                #we should check both roots and find out the smallest positive root
                return intercept_pos
        
        def propagate_ray(self, ray):
                direc = ray.direc()
                n_1 = self.n_1()
                n_2 = self.n_2()
                new_pos = self.intercept(ray)
                if new_pos is None:
                        return None
                normal = new_pos / np.linalg.norm(new_pos) #normal to a spherical surface
                new_direc = refract(direc, normal, n_1, n_2)
                if new_direc is None:
                        return None
                ray.append(new_pos, new_direc)
                return ray
        
class OutputPlane(OpticalElement):
        def __init__(self, z_0):
                self.__z0 = z_0
        
        def intercept(self, ray):
                z_0 = self.__z0 #where the plane is in z-direction
                z_init = ray.pos()[2]
                z_direc = ray.direc()[2]
                if z_direc == 0: #if the ray is moving parallel to the plane
                        return None
                l = (z_0 - z_init) / z_direc
                if l < 0: # if the surface is behind the ray
                        return None
                direc = ray.direc()
                pos = ray.pos()
                intercept_pos = pos + l * direc
                return intercept_pos
        
        def propagate_ray(self, ray):
                new_pos = self.intercept(ray)
                direc = ray.direc()
                if new_pos is None :
                        return None
                ray.append(new_pos, direc) #keeping the direction of the ray same
                return ray


