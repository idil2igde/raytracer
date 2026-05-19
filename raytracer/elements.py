from raytracer.rays import Ray
#importing Ray class from raytracer folder and rays file

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
                self.__aperature = aperature
                self.__curvature = curvature
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
                