"""Analysis module."""
from operator import itemgetter

import matplotlib.pyplot as plt

from raytracer._utils.decorators import SaveOutput

from raytracer.elements import SphericalRefraction

from raytracer.rays import Ray

from raytracer.elements import OutputPlane

from raytracer.rays import RayBundle

from raytracer.lenses import *

import numpy as np

def task8():
    """
    Task 8.

    In this function you should check your propagate_ray function properly
    finds the correct intercept and correctly refracts a ray. Don't forget
    to check that the correct values are appended to your Ray object.
    """

    ray = Ray(np.array([0, 0, 0]), np.array([0, 0, 1]))

    aperature = SphericalRefraction(20, 5, 10, 1, 1.5) 

    new_ray = aperature.propagate_ray(ray)
    print("final pos:", ray.pos())
    print("final direc:", ray.direc())
    print("vertices:", ray.vertices())
    print("propagated ray:", repr(new_ray))
    print(new_ray)

@SaveOutput("task10")
def task10():
    """
    Task 10.

    In this function you should create Ray objects with the given initial positions.
    These rays should be propagated through the surface, up to the output plane.
    You should then plot the tracks of these rays.
    This function should return the matplotlib figure of the ray paths.

    Returns:
        Figure: the ray path plot.
    """
    ray = Ray(np.array([0, 0, 0]), np.array([0, 0, 1]))

    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5) #given values in the task

    screen = OutputPlane(250)

    surface.propagate_ray(ray)
    screen.propagate_ray(ray)

    vertices = ray.vertices() #tracing the travel of the ray

    z = [point[2] for point in vertices] #plot z-direction the direction of ray travel on x-axis in the plot
    y = [point[1] for point in vertices]

    plt.plot(z, y)
    plt.xlabel("Ray travelling in z-direction")
    plt.ylabel("y-direction")


@SaveOutput("task11", plot_output_indices=itemgetter(0))
def task11():
    """
    Task 11.

    In this function you should propagate the three given paraxial rays through the system
    to the output plane and the tracks of these rays should then be plotted.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for ray paths
    2. the calculated focal point.

    Returns:
        tuple[Figure, float]: the ray path plot and the focal point
    """
    ray_1 = Ray(np.array([0.1, 0.1, 0]), np.array([0, 0, 1]))

    ray_2 = Ray(np.array([0, 0, 0]), np.array([0, 0, 1]))

    ray_3 = Ray(np.array([-0.1, -0.1, 0]), np.array([0, 0, 1]))

    rays = [ray_1, ray_2, ray_3]

    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5) #given values in the task

    screen = OutputPlane(250)

    for i in rays:
        surface.propagate_ray(i)
        screen.propagate_ray(i)
        vertices = i.vertices()
        z = [point[2] for point in vertices] #plot z-direction the direction of ray travel on x-axis in the plot
        y = [point[1] for point in vertices]
        plt.plot(z, y)
        print(surface.focal_point())
        #NEEDS TO RETURN TUPLE!!

    return


@SaveOutput("task12")
def task12():
    """
    Task 12.

    In this function you should create a RayBunble and propagate it to the output plane
    before plotting the tracks of the rays.
    This function should return the matplotlib figure of the track plot.

    Returns:
        Figure: the track plot.
    """

    rb = RayBundle()
    rb = RayBundle(rmax=5., nrings=5., multi=6)

    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5)
    screen = OutputPlane(250)

    rb.propagate_bundle([surface, screen]) #the refracting elements are surface and the screen

    return rb.track_plot()



@SaveOutput("task13", plot_output_indices=itemgetter(0))
def task13():
    """
    Task 13.

    In this function you should again create and propagate a RayBundle to the output plane
    before plotting the spot plot.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the spot plot
    2. the simulation RMS

    Returns:
        tuple[Figure, float]: the spot plot and rms
    """

    rb = RayBundle()
    rb = RayBundle(rmax=5., nrings=5., multi=6)

    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5)

    focal_point = surface.focal_point()

    screen = OutputPlane(focal_point) #screen placed at the focal point

    rb.propagate_bundle([surface, screen])

    rms_point = rb.rms()
    
    return rb.spot_plot(), rms_point


@SaveOutput("task14", plot_output_indices=itemgetter(0))
def task14():
    """
    Task 14.

    In this function you will trace a number of RayBundles through the optical system and
    plot the RMS and diffraction scale dependence on input beam radii.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the diffraction scale plot
    2. the simulation RMS for input beam radius 2.5
    3. the diffraction scale for input beam radius 2.5

    Returns:
        tuple[Figure, float, float]: the plot, the simulation RMS value, the diffraction scale.
    """
    radii = []
    rms_values = []
    diff_values = []
    rms_2_5 = 0
    diff_2_5 = 0
    for i in np.linspace(0.1, 10., 240): #240 chosen so we get a value in one of the steps close to 2.5 mm
        rb = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        surface = SphericalRefraction(100, 34, 0.03, 1, 1.5)
        focal_point = surface.focal_point()
        screen = OutputPlane(focal_point) #screen placed at the focal point
        rb.propagate_bundle([surface, screen])
        rms_point = rb.rms()
        radii.append(i)
        rms_values.append(rms_point)
        
        wavelength = 588e-6 #in milimeters
        aperature = 2 * i #diameter of the refracting surface
        del_x = wavelength * focal_point / aperature
        diff_values.append(del_x)

        if np.isclose(i, 2.5):
            rms_2_5 = rb.rms()
            diff_2_5 = del_x
    
    plt.plot(radii, rms_values, label ="RMS value")
    plt.plot(radii, diff_values, label = "Diffraction scale")
    plt.xlabel("Input beam radius (mm)")
    plt.ylabel("Spot size (mm)")
    
    plt.legend()

    return plt.gcf(), rms_2_5, diff_2_5



@SaveOutput(["task15a", "task15b"], plot_output_indices=itemgetter(0, 2))
def task15():
    """
    Task 15.

    In this function you will create plano-convex lenses in each orientation and propagate a RayBundle
    through each to their respective focal point. You should then plot the spot plot for each orientation.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the spot plot for the plano-convex system
    2. the focal point for the plano-convex lens
    3. the matplotlib figure object for the spot plot for the convex-plano system
    4  the focal point for the convex-plano lens


    Returns:
        tuple[Figure, float, Figure, float]: the spot plots and rms for plano-convex and convex-plano.
    """

    pc = PlanoConvex(z_0=100, curvature1=0., curvature2=-0.02, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    focal_point_pc = pc.focal_point_lens()
    screen_pc = OutputPlane(focal_point_pc)

    cp = PlanoConvex(z_0=100, curvature1=0.02, curvature2=0., n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    focal_point_cp = cp.focal_point_lens()
    screen_cp = OutputPlane(focal_point_cp)

    rb_1 = RayBundle(rmax=5., nrings=5., multi=6) #light beam with a radius of 5 mm
    rb_1.propagate_bundle([pc, screen_pc])

    rb_2 = RayBundle(rmax=5., nrings=5., multi=6)
    rb_2.propagate_bundle([cp, screen_cp])

    print("PC focal:", focal_point_pc)
    print("CP focal:", focal_point_cp)

    print(rb_1.rays()[0].vertices())
    print(rb_2.rays()[0].vertices())    

    return rb_1.spot_plot(), focal_point_pc, rb_2.spot_plot(), focal_point_cp


@SaveOutput("task16", plot_output_indices=itemgetter(0))
def task16():
    """
    Task 16.

    In this function you will be again plotting the radial dependence of the RMS and diffraction values
    for each orientation of your lens.
    This function should return the following items as a tuple in the following order:
    1. the matplotlib figure object for the diffraction scale plot
    2. the RMS for input beam radius 3.5 for the plano-convex system
    3. the RMS for input beam radius 3.5 for the convex-plano system
    4  the diffraction scale for input beam radius 3.5

    Returns:
        tuple[Figure, float, float, float]: the plot, RMS for plano-convex, RMS for convex-plano, diffraction scale.
    """
    radii = []
    rms_pc = []
    rms_cp = []
    diff_val_pc = []
    diff_val_cp = []
    rms_3_5_pc = 0
    rms_3_5_cp = 0
    diff_3_5 = 0
    pc = PlanoConvex(z_0=100, curvature1=0., curvature2=-0.02, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    focal_point_pc = pc.focal_point_lens()
    screen_pc = OutputPlane(focal_point_pc) 
    cp = PlanoConvex(z_0=100, curvature1=0.02, curvature2=0., n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    focal_point_cp = cp.focal_point_lens()
    screen_cp = OutputPlane(focal_point_cp)
    for i in np.linspace(0.1, 10., 240): 
        rb_pc = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        rb_cp = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        rb_pc.propagate_bundle([pc, screen_pc])
        rb_cp.propagate_bundle([cp, screen_cp])
        rms_pc.append(rb_pc.rms())
        rms_cp.append(rb_cp.rms())
        radii.append(i)
        
        
        wavelength = 588e-6 #in milimeters
        aperature = 2 * i #diameter of the refracting surface
        del_x_pc = wavelength * focal_point_pc / aperature
        del_x_cp = wavelength * focal_point_cp / aperature
        diff_val_pc.append(del_x_pc)
        diff_val_cp.append(del_x_cp)

        if np.isclose(i, 3.5):
            rms_3_5_pc = rb_pc.rms()
            rms_3_5_cp = rb_cp.rms()
            diff_3_5 = del_x_pc
    
    plt.plot(radii, rms_pc, label ="RMS value plano convex")
    #plt.plot(radii, diff_val_pc, label = "Diffraction scale plano convex")
    plt.plot(radii, rms_cp, label ="RMS value convex plano")
    plt.plot(radii, diff_val_cp, label = "Diffraction scale for pc & cp")
    plt.xlabel("Input beam radius (mm)")
    plt.ylabel("Spot size (mm)")
    
    plt.legend()

    print(rms_3_5_pc)
    print(rms_3_5_cp)

    return plt.gcf(), rms_3_5_pc, rms_3_5_cp, diff_3_5


@SaveOutput("task17", plot_output_indices=itemgetter(0))
def task17():
    from scipy.optimize import minimize
    """
    Task 17.

    In this function you will be first plotting the spot plot for your PlanoConvex lens with the curved
    side first (at the focal point). You will then be optimising the curvatures of a BiConvex lens
    in order to minimise the RMS spot size at the same focal point. This function should return
    the following items as a tuple in the following order:
    1. The comparison spot plot for both PlanoConvex (curved side first) and BiConvex lenses at PlanoConvex focal point.
    2. The RMS spot size for the PlanoConvex lens at focal point
    3. the RMS spot size for the BiConvex lens at PlanoConvex focal point

    Returns:
        tuple[Figure, float, float]: The combined spot plot, RMS for the PC lens, RMS for the BiConvex lens
    """

    cpl = PlanoConvex(z_0=100, curvature1=0.02, curvature2=0., n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    rb_cpl = RayBundle(rmax=5., nrings=5., multi=6)
    rb_bil = RayBundle(rmax=5., nrings=5., multi=6)
    focal_point_cpl = cpl.focal_point_lens()
    screen_cpl = OutputPlane(focal_point_cpl) 

    def rms_minimize(curvatures):
        c1, c2 = curvatures
        biconvex_lens = BiConvex(z_0=100, curvature1=c1, curvature2=c2, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
        rb_bil.propagate_bundle([biconvex_lens, screen_cpl])
        return rb_bil.rms()

    rb_cpl.propagate_bundle([cpl, screen_cpl])
    rms_cpl = rb_cpl.rms()
    
    result = minimize(rms_minimize, x0 = [0.02, -0.02]) 
    c1_opt, c2_opt = result.x #returns the optimal parameter (curvature) values that minimizes the RMS
    rms_min = result.fun

    biconvex_opt = BiConvex(z_0=100, curvature1=c1_opt, curvature2=c2_opt, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.) #creating a new biconvex lens that minimizes the RMS
    rb_bil.propagate_bundle([biconvex_opt, screen_cpl])

    for ray in rb_cpl.rays():
        final_pos = ray.vertices()[-1]
        plt.scatter(final_pos[0], final_pos[1], label="PlanoConvex", color = "blue")
    for ray in rb_bil.rays():
        final_pos = ray.vertices()[-1]
        plt.scatter(final_pos[0], final_pos[1], label="BiConvex", color = "red")
    plt.xlabel("x position (mm)")
    plt.ylabel("y position (mm)")

    return plt.gcf(), rms_cpl, rms_min


@SaveOutput("task18", plot_output_indices=itemgetter(0))
def task18():
    """
    Task 18.

    In this function you will be testing your reflection modelling. Create a new SphericalReflecting surface
    and trace a RayBundle through it to the OutputPlane.This function should return
    the following items as a tuple in the following order:
    1. The track plot showing reflecting ray bundle off SphericalReflection surface.
    2. The focal point of the SphericalReflection surface.

    Returns:
        tuple[Figure, float]: The track plot, the focal point
    """
    return


@SaveOutput(["task19a", "task19b"])
def task19():
    """
    Task 19.

    In this function you will be quantifing the amount of spherical aberration.
    Create a new ConvexPlano lens and trace a RayBundle through it to the OutputPlane
    located at the focal point.
    This function should return two matplotlib figures as a tuple in the following order:
    1. The plot showing the transverse spherical aberration i.e. rms as a function of beam radius at focal point.
    2. The plot showing the longitudinal spherical aberration i.e. z intercept of a ray as a function
       of transverse distance from optical axis.

    Returns:
        tuple[Figure, Figure]: Transverse spherical aberration plot, longitudinal spherical aberration plot
    """
    return


@SaveOutput("task20")
def task20():
    """
    Task 20.

    In this function you will investigate dispersion. Create several Rays with different wavelengths.
    Plot the paths of these rays through a BiConvex lens made of BK7 glass to an OutputPlane at z=200.
    This function should return the track plot of the path of your Rays through the glass lens.

    Returns:
        Figure: The ray track plot.
    """
    return


if __name__ == "__main__":

    # Run task 8 function
    #task8()

    # Run task 10 function
    #FIG10 = task10()

    # Run task 11 function
    #task11()
    #FIG11, FOCAL_POINT = task11()

    # Run task 12 function
    #FIG12 = task12()

    # Run task 13 function
    #FIG13, TASK13_RMS = task13()

    # Run task 14 function
    #FIG14, TASK14_RMS, TASK14_DIFF_SCALE = task14()

    # Run task 15 function
    #FIG15_PC, FOCAL_POINT_PC, FIG15_CP, FOCAL_POINT_CP = task15()

    # Run task 16 function
    #FIG16, PC_RMS, CP_RMS, TASK16_DIFF_SCALE = task16()

    # Run task 17 function
    FIG17, CP_RMS, BICONVEX_RMS = task17()

    # Run task 18 function
    # FIG18, FOCAL_POINT = task18()

    # Run task 19 function
    # FIG19_TVSA, FIG19_LGSA = task19()

    # Run task 20 function
    # FIG20 = task20()

    plt.show()
