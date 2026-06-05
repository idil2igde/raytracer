from raytracer.elements import *
from raytracer.rays import *
#importing all from elements.py and rays.py

class PlanoConvex:
    def __init__(self, z_0 = 100, curvature1 = 0., curvature2 = -0.02, n_inside = 1.5168, n_outside = 1., thickness = 5., aperture = 50.):
        self.__z_0 = z_0
        self.__curvature1 = curvature1
        self.__curvature2 = curvature2
        self.__n_inside = n_inside
        self.__n_outside = n_outside
        self.__thickness = thickness
        self.__aperature = aperture
        #creating the two curvatures seperately
        self.__plane_surface = SphericalRefraction(z_0, aperture, curvature1, n_outside, n_inside) 
        self.__concave_lens = SphericalRefraction(z_0 + thickness, aperture, curvature2, n_inside, n_outside)
    def propagate_ray(self, ray): #propagating the rays in the bundle  
        self.__plane_surface.propagate_ray(ray)
        self.__concave_lens.propagate_ray(ray)
    #focal point calculator usign paraxial approximation, just propagating the ray through the refracting surface to see where it ends up
    def focal_point_lens(self):
        ray = Ray(np.array([1e-7, 0, 0]), np.array([0, 0, 1])) #a suffeciently small height was chosen for paraxial approximation to work in position[0]
        self.propagate_ray(ray)
        pos = ray.pos()
        direc = ray.direc()
        l = -pos[0] / direc[0]
        z_focus = pos[2] + l * direc[2] #returns the z poisiton of the focal length

        return z_focus
    
class ConvexPlano(OpticalElement):
     pass

class BiConvex:
    def __init__(self, z_0 = 100, curvature1 = 0.02, curvature2 = -0.02, n_inside = 1.5168, n_outside = 1., thickness = 5., aperture = 50.):
            self.__z_0 = z_0
            self.__curvature1 = curvature1
            self.__curvature2 = curvature2
            self.__n_inside = n_inside
            self.__n_outside = n_outside
            self.__thickness = thickness
            self.__aperature = aperture
            #creating the two curvatures seperately
            self.__surface1 = SphericalRefraction(z_0, aperture, curvature1, n_outside, n_inside) 
            self.__surface2 = SphericalRefraction(z_0 + thickness, aperture, curvature2, n_inside, n_outside)
    def propagate_ray(self, ray): #propagating the rays in the bundle  
        self.__surface1.propagate_ray(ray)
        self.__surface2.propagate_ray(ray) 
    def focal_point_bilens(self):
        ray = Ray(np.array([0.1, 0, 0]), np.array([0, 0, 1]))
        self.propagate_ray(ray)
        pos = ray.pos()
        direc = ray.direc()
        l = -pos[0] / direc[0]
        z_focus = pos[2] + l * direc[2] #returns the z poisiton of the focal length
        return z_focus
    def c1(self):
         return self.__curvature1
    def c2(self):
         return self.__curvature2