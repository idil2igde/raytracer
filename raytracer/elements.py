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
        def __init__(self, z_0 = 0., aperature = 0., curvature = 0., n_1 = 0., n_2 = 0.):
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
        
        def intercept(self, ray): #where the ray intercepts the spherical surface
                direc = ray.direc()
                pos = ray.pos()
                curv = self.curvature()
                rad = 1 / curv #since the unit of curvature is mm-1, radius is inverse
                z0 = self.z_0()
                centre = np.array([0, 0, z0 + rad]) #centre of sphere is calculated by adding where surface crosses the z-axis and the radius of the sphere
                r = pos - centre #position of ray relative to the sphere centre
                dot_1 = np.dot(r, direc)
                disc = dot_1 * dot_1 - (np.dot(r, r) - rad * rad)
                if disc < 0:
                        return None #no real solutions to quad formula exists for negative discriminant
                l1 = - dot_1 + np.sqrt(disc)
                l2 = - dot_1 - np.sqrt(disc)
                valid = [l for l in [l1, l2] if l > 0] #choosing positive root 
                if len(valid) == 0:
                        return None #if both roots are not valid
                l = min(valid) #smallest possible positive root gives the first instance of intercept
                intercept_pos = pos + l * direc #ray only travels forward, adding intercept distance to initial ray position in ray direction

                return intercept_pos
        
        def propagate_ray(self, ray): #trace the ray until intercept
                direc = ray.direc()
                n_1 = self.n_1()
                n_2 = self.n_2()
                curv = self.curvature()
                rad = 1 / curv 
                z0 = self.z_0()
                centre = np.array([0, 0, z0 + rad])
                new_pos = self.intercept(ray)
                if new_pos is None:
                        return None
                normal = new_pos - centre #normal to a spherical surface
                normal = normal / np.linalg.norm(normal) #finding direction
                new_direc = refract(direc, normal, n_1, n_2)
                if new_direc is None:
                        return None
                ray.append(new_pos, new_direc)
                return ray
        
        def focal_point(self): #calculating the focal point of a refracting spherical surface
                n1 = self.n_1()
                n2 = self.n_2()
                rad = 1 / self.curvature()
                focal_point = n2 * rad / (n2 - n1) #paraxial focus of a single spherical refracting surface
                z0 = self.z_0()
                return focal_point + z0

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


