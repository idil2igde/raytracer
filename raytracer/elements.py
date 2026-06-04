from raytracer.rays import Ray
#importing Ray class from raytracer folder and rays file
import numpy as np
from raytracer.physics import *


class OpticalElement:
        def intercept(self, ray):
                #tests whether the ray will intercept with the optical object
                raise NotImplementedError('intercept() needs to be implemented in derived classes')
        def propagate_ray(self, ray):
                #tests hwo the ray propogates in the optical object and update the ray's internal characteristics such as poisiton and direction
                raise NotImplementedError('propagate_ray() needs to be implemented in derived classes')
        

class SphericalRefraction(OpticalElement):
        def __init__(self, z_0 = 0., aperture = 0., curvature = 0., n_1 = 0., n_2 = 0.):
                self.__z0 = z_0
                #where surface intercepts optical axis (z-axis)
                self.__aperture = aperture
                #extend of surface from optical axis 
                self.__curvature = curvature
                #curvature of the surface (radius of spherical surface)
                self.__n1 = n_1
                self.__n2 = n_2
        #the accessor methods for each parameter of SphericalRefraction initialization method
        def z_0(self):
                return self.__z0
        def aperture(self):
                return self.__aperture
        def curvature(self):
                return self.__curvature
        def n_1(self, wavelength = None):
                if isinstance(self.__n1, (float, int)):
                        return self.__n1
                return self.__n1.ref_index(wavelength)
        def n_2(self, wavelength = None):
                if isinstance(self.__n2, (float, int)):
                        return self.__n2
                return self.__n2.ref_index(wavelength)
        
        def intercept(self, ray): #where the ray intercepts the spherical surface
                direc = ray.direc()
                pos = ray.pos()
                curv = self.curvature()
                if curv == 0:
                        z_init = ray.pos()[2]
                        z_direc = ray.direc()[2]
                        if z_direc == 0: #if the ray is moving parallel to the plane
                                return None
                        l = (self.__z0 - z_init) / z_direc #distance travelled in ray direction before ray hits the plane
                        if l < 0: # if the surface is behind the ray
                                return None
                        return pos + l * direc #position where the ray hits the plane
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
                valid = [] 
                for l in [l1, l2]:
                        if l > 0: #ray travelling forward
                                point = pos + l * direc #where the ray strikes the physical surface
                                radial_distance = np.sqrt(point[0]**2 + point[1]**2) #Pythagoras' theorem
                                if radial_distance <= self.__aperture: #if the ray hits the spherical point beyond the space aperture is filling
                                        valid.append(point)
                if len(valid) == 0:
                        return None #if there are no valid points for both roots
                intercept_pos = min(valid, key = lambda point: np.dot(point - pos, direc)) #if both roots are valid, detecting the ray that hits the surface first

                return intercept_pos
        
        def propagate_ray(self, ray): #trace the ray until intercept
                direc = ray.direc()
                n_1 = self.n_1(ray.wavelength())
                n_2 = self.n_2(ray.wavelength())
                curv = self.curvature()
                
                new_pos = self.intercept(ray)
                if new_pos is None:
                        return None

                if curv == 0:
                        normal = np.array([0, 0, -1])
                else:
                        rad = 1 / curv 
                        z0 = self.z_0()
                        centre = np.array([0, 0, z0 + rad])
                        normal = new_pos - centre #normal to a spherical surface
                        normal = normal / np.linalg.norm(normal) #finding direction
                        if np.dot(normal, direc) > 0:
                                normal = -normal #from Snell's Law
                
                new_direc = refract(direc, normal, n_1, n_2)
                
                if new_direc is None:
                        return None
                ray.append(new_pos, new_direc)
                return ray
                
        def focal_point(self, wavelength): #calculating the focal point of a refracting spherical surface
                n1 = self.n_1(wavelength)
                n2 = self.n_2(wavelength)
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

class SphericalReflection(SphericalRefraction): #since reflection class has exactly the same methods and variables contained in refract class we can just inherit it
        def __init__(self, z_0 = 0., aperture = 0., curvature = 0.):
                super().__init__(z_0 = z_0, aperture = aperture, curvature = curvature, n_1 = 1, n_2 = 2)
        def propagate_ray(self, ray):
                direc = ray.direc()
                curv = self.curvature()
                
                new_pos = self.intercept(ray)
                if new_pos is None:
                        return None

                if curv == 0:
                        normal = np.array([0, 0, -1])
                else:
                        rad = 1 / curv 
                        z0 = self.z_0()
                        centre = np.array([0, 0, z0 + rad])
                        normal = new_pos - centre #normal to a spherical surface
                        normal = normal / np.linalg.norm(normal) #finding direction
                        if np.dot(normal, direc) > 0:
                                normal = -normal #from Snell's Law
                new_direc = reflect(direc, normal)
                if new_direc is None:
                        return None
                ray.append(new_pos, new_direc)
                return ray
        def focal_point(self):
                curv = self.curvature()
                rad = 1 / curv
                focal_point = rad / 2 #focal point equation for spherical mirrors
                #z0 = self.z_0()
                return focal_point



