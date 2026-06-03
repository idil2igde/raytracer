from raytracer.elements import *
from raytracer.rays import *
#importing all from elements.py and rays.py

class PlanoConvex:
    def __init__(self, z_0 = 100, curvature1 = 0., curvature2 = 0., n_inside = 1.5168, n_outside = 1., thickness = 5., aperature = 50.):
        self.__z_0 = z_0
        self.__curvature1 = curvature1
        self.__curvature2 = curvature2
        self.__n_inside = n_inside
        self.__n_outside = n_outside
        self.__thickness = thickness
        self.__aperature = aperature
        #creating the two curvatures seperately
        self.__plane_surface = SphericalRefraction(z_0, aperature, curvature1, n_outside, n_inside) 
        self.__concave_lens = SphericalRefraction(z_0 + thickness, aperature, curvature2, n_inside, n_outside)
        #creating the ray bundle
    def create_ray(self):
        rays = RayBundle() #automatically creates object with the given values
        return rays
    def propagate_bundle_lens(self, ray): #propagating the rays in the bundle  
        self.__plane_surface.propagate_ray(ray)
        self.__concave_lens.propagate_ray(ray)
    #focal point calculator using the Lens Makers' Formula
    def focal_point_lens(self):
        f_inverse = (self.__n_inside - 1) * (-1 / self.__curvature2)
        focal_point_lens = (1 / f_inverse) + self.__z_0 + self.__thickness
        return focal_point_lens 
    #creating the output plane at the focal point
    def OutputPlane_lens(self):
        screen_lens = OutputPlane(self.focal_point_lens())
        return screen_lens
    #creating a spot plot at the output plane
    def spot_plot_lens(self):
        rays = self.create_ray()
        return rays.spot_plot()
        
    