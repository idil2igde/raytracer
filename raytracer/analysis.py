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

    rays = [Ray(np.array([0, 0, 0]), np.array([0, 0, 1])), Ray(np.array([0, 1, 0]), np.array([0, 0, 1])), Ray(np.array([0, -1, 0]), np.array([0, 0, 1]))]

    surface = SphericalRefraction(20, 5, 10, 1, 1.5) 

    for ray in rays:
        surface.propagate_ray(ray)
      
    return rays[1]

@SaveOutput("task10")
def task10():
    plt.figure()
    """
    Task 10.

    In this function you should create Ray objects with the given initial positions.
    These rays should be propagated through the surface, up to the output plane.
    You should then plot the tracks of these rays.
    This function should return the matplotlib figure of the ray paths.

    Returns:
        Figure: the ray path plot.
    """
    positions = ([0, 4, 0], [0, 1, 0], [0, 0.2, 0], [0, 0, 0], [0, -0.2, 0], [0, -1, 0], [0, -4, 0])
    #positions given in the task

    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5) #given values in the task

    screen = OutputPlane(250)

    for pos in positions:
        ray = Ray(np.array(pos), np.array([0, 0, 1]))
        surface.propagate_ray(ray)
        screen.propagate_ray(ray)

        vertices = ray.vertices() #tracing the travel of the ray

        z = [point[2] for point in vertices] #plot z-direction the direction of ray travel on x-axis in the plot
        y = [point[1] for point in vertices]

        plt.plot(z, y)

    plt.title("Track Plot of Rays Through a Refracting Surface")
    plt.xlabel("Ray travelling in z-direction")
    plt.ylabel("y-direction")
    return plt.gcf()


@SaveOutput("task11", plot_output_indices=itemgetter(0))
def task11():
    plt.figure()
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

    screen = OutputPlane(surface.focal_point())

    for i in rays:
        surface.propagate_ray(i)
        screen.propagate_ray(i)
        vertices = i.vertices()
        z = [point[2] for point in vertices] #plot z-direction the direction of ray travel on x-axis in the plot
        y = [point[1] for point in vertices]
    
        plt.plot(z, y)
    
    plt.title("Paraxial Ray Plot for Focal Point Determination")
    plt.xlabel("z position (mm)")
    plt.ylabel("y position (mm)")

    return plt.gcf(), surface.focal_point()


@SaveOutput("task12")
def task12():
    plt.figure()
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
    
    plt.title("Ray Bundle Track Plot")
    plt.xlabel("z position (mm)")
    plt.ylabel("y position (mm)")
    return rb.track_plot()



@SaveOutput("task13", plot_output_indices=itemgetter(0))
def task13():
    plt.figure()
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
    
    fig1 = rb.spot_plot()
    plt.title("Spot Plot at the Focal Point Screen")

    return fig1, rms_point


@SaveOutput("task14", plot_output_indices=itemgetter(0))
def task14():
    plt.figure()
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
    surface = SphericalRefraction(100, 34, 0.03, 1, 1.5)
    focal_point = surface.focal_point()
    screen = OutputPlane(focal_point) #screen placed at the focal point
    
    for i in np.linspace(0.1, 10., 240): #240 chosen so we get a value in one of the steps close to 2.5 mm
        rb = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        rb.propagate_bundle([surface, screen])
        rms_point = rb.rms()
        radii.append(i)
        rms_values.append(rms_point)
        
        wavelength = 588e-6 #in milimeters
        aperature = 2 * 2 * i #diameter of the refracting surface
        del_x = wavelength * focal_point / aperature
        diff_values.append(del_x)
    
    rb = RayBundle(rmax = 2.5, nrings = 5, multi = 6)
    rb.propagate_bundle([surface, screen])
    rms_2_5 = rb.rms()
    aperture_2_5 = 2 * 2 * 2.5
    diff_2_5 = wavelength * focal_point / aperture_2_5
    
    plt.title("RMS Spot Size and Diffraction Scale vs. Input Beam Radius")
    plt.plot(radii, rms_values, label ="RMS value")
    plt.plot(radii, diff_values, label = "Diffraction scale")
    plt.xlabel("Input beam radius (mm)")
    plt.ylabel("Spot size (mm)")
    
    plt.legend()

    return plt.gcf(), rms_2_5, diff_2_5



@SaveOutput(["task15a", "task15b"], plot_output_indices=itemgetter(0, 2))
def task15():
    plt.figure()
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

    fig1 =  rb_1.spot_plot()
    plt.title("Spot Diagram for Plano-Convex Lens")

    fig2 = rb_2.spot_plot()
    plt.title("Spot Diagram for Convex-Plano Lens")

    return fig1, focal_point_pc, fig2, focal_point_cp


@SaveOutput("task16", plot_output_indices=itemgetter(0))
def task16():
    plt.figure()
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
    wavelength = 588e-6 #in milimeters
    for i in np.linspace(0.1, 10., 240): 
        rb_pc = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        rb_cp = RayBundle(rmax=i, nrings=5., multi=6) #max radius 10 and min 0.1 milimeters
        rb_pc.propagate_bundle([pc, screen_pc])
        rb_cp.propagate_bundle([cp, screen_cp])
        rms_pc.append(rb_pc.rms())
        rms_cp.append(rb_cp.rms())
        radii.append(i)
        
        
        aperature = 2 * 2 * i #diameter of the refracting surface
        del_x_pc = wavelength * focal_point_pc / aperature
        del_x_cp = wavelength * focal_point_cp / aperature
        diff_val_pc.append(del_x_pc)
        diff_val_cp.append(del_x_cp)

    rb_pc = RayBundle(rmax=3.5, nrings=5., multi=6)
    rb_cp = RayBundle(rmax=3.5, nrings=5., multi=6)

    rb_pc.propagate_bundle([pc, screen_pc])
    rb_cp.propagate_bundle([cp, screen_cp])

    rms_3_5_pc = rb_pc.rms()
    rms_3_5_cp = rb_cp.rms()

    aperture = 2 * 3.5
    diff_3_5 = wavelength * (focal_point_pc - 105.) / aperture #the effective focal length is measured from the rear end of the lens therefore 5 mm thickness and z_0 at 100 results in 105. mm
    
    plt.title("RMS Spot Size and Diffraction Scale for PlanoConvex and ConvexPlano Lenses")
    plt.plot(radii, rms_pc, label ="RMS value plano convex")
    #plt.plot(radii, diff_val_pc, label = "Diffraction scale plano convex")
    plt.plot(radii, rms_cp, label ="RMS value convex plano")
    plt.plot(radii, diff_val_cp, label = "Diffraction scale for pc & cp")
    plt.xlabel("Input beam radius (mm)")
    plt.ylabel("Spot size (mm)")
    
    plt.legend()

    print(focal_point_pc)
    print(focal_point_cp)

    return plt.gcf(), rms_3_5_pc, rms_3_5_cp, diff_3_5


@SaveOutput("task17", plot_output_indices=itemgetter(0))
def task17():
    from scipy.optimize import minimize
    plt.figure()
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
    rb_bil = RayBundle(rmax=5., nrings=5., multi=6)
    rb_cpl = RayBundle(rmax=5., nrings=5., multi=6)
    focal_point_cpl = cpl.focal_point_lens()
    screen_cpl = OutputPlane(focal_point_cpl) 

    def rms_minimize(curvatures): #using the curvatures as parameters of hte biconvex lens to find the minimized rms
        c1, c2 = curvatures
        biconvex_lens = BiConvex(z_0=100, curvature1=c1, curvature2=c2, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
        rb = RayBundle(rmax=5., nrings=5., multi=6)
        rb.propagate_bundle([biconvex_lens, screen_cpl])
        return rb.rms()

    rb_cpl.propagate_bundle([cpl, screen_cpl])
    rms_cpl = rb_cpl.rms()
    
    result = minimize(rms_minimize, x0 = [0.02, -0.02]) 
    c1_opt, c2_opt = result.x #returns the optimal parameter (curvature) values that minimizes the RMS
    rms_min = result.fun #returns the minimized rms value

    biconvex_opt = BiConvex(z_0=100, curvature1=c1_opt, curvature2=c2_opt, n_inside=1.5168, n_outside=1., thickness=5., aperture=50.) #creating a new biconvex lens that minimizes the RMS
    rb_bil.propagate_bundle([biconvex_opt, screen_cpl])

    #to plot both spot plots on the same graphs instead of using spot_plot() functions I do the scatter plots individually
    for ray in rb_cpl.rays(): 
        final_pos = ray.vertices()[-1]
        plt.scatter(final_pos[0], final_pos[1], label="PlanoConvex", color = "blue")
    for ray in rb_bil.rays():
        final_pos = ray.vertices()[-1]
        plt.scatter(final_pos[0], final_pos[1], label="BiConvex", color = "red")
    plt.title("Comparison of Plano-Convex and Bi-Convex Spot Plots")
    plt.xlabel("x position (mm)")
    plt.ylabel("y position (mm)")

    return plt.gcf(), rms_cpl, rms_min


@SaveOutput("task18", plot_output_indices=itemgetter(0))
def task18():
    plt.figure()
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
    sph_refl = SphericalReflection(z_0=100., aperture=6., curvature=-0.02)
    rb = RayBundle(rmax=5., nrings=5., multi=6)
    screen = OutputPlane(50)
    rb.propagate_bundle([sph_refl, screen])
    focal_point = sph_refl.focal_point()

    fig = rb.spot_plot()
    plt.title("Spot Plot for Spherical Reflection")
    return fig, focal_point


@SaveOutput(["task19a", "task19b"])
def task19():
    plt.figure()
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
    radii = []
    rms_pc = []
    z_intercept = []
    r = []
    pc = PlanoConvex(z_0=100, curvature1=0.02, curvature2=0., n_inside=1.5168, n_outside=1., thickness=5., aperture=50.)
    focal_point_pc = pc.focal_point_lens()
    screen_pc = OutputPlane(focal_point_pc) 
    for i in np.linspace(0.1, 20., 480): #for each ray bundle ring calculating rms
        rb_pc = RayBundle(rmax=i, nrings=5., multi=6) 
        rb_pc.propagate_bundle([pc, screen_pc])
        rms_pc.append(rb_pc.rms())
        radii.append(i)

        for ray in rb_pc.rays(): #for each ray in the bundle calculating the transverse distance from the optical axis and the z intercept
            z_intercept.append(ray.z_int()())
            start_pos = ray.vertices()[0]
            r_add = np.sqrt(start_pos[0] * start_pos[0] + start_pos[1] * start_pos[1])
            r.append(r_add)
    
    fig1 = plt.figure()
    plt.title("Transverse Spherical Aberration")
    plt.plot(radii, rms_pc)
    plt.xlabel("Input beam radius (mm)")
    plt.ylabel("RMS spot size (mm)")
    
    fig2 = plt.figure()
    plt.title("Longitudinal Spherical Aberration")
    plt.scatter(r, z_intercept)
    plt.axhline(focal_point_pc)
    plt.xlabel("Transverse distance from optical axis (mm)")
    plt.ylabel("z intercept (mm)")

    return fig1, fig2


@SaveOutput("task20")
def task20():
    plt.figure()
    """
    Task 20.

    In this function you will investigate dispersion. Create several Rays with different wavelengths.
    Plot the paths of these rays through a BiConvex lens made of BK7 glass to an OutputPlane at z=200.
    This function should return the track plot of the path of your Rays through the glass lens.

    Returns:
        Figure: The ray track plot.
    """
    BK7 = DispersiveMaterial(b_coeffs = (1.03961212, 0.231792344, 1.01046945), c_coeffs = (0.00600069867, 0.0200179144, 103.560653))
    wavelengths = [400e-6, 450e-6, 500e-6, 550e-6, 600e-6, 650e-6, 700e-6]
    biconvex_lens = BiConvex(z_0=100, curvature1=0.02, curvature2=-0.02, n_inside = BK7, n_outside=1., thickness=5., aperture=50.)
    screen = OutputPlane(200.) #randomly positioned screem
    for wl in wavelengths:
        ray = Ray(pos=np.array([1., 0., 0.]), direc=np.array([0., 0., 1.]), wavelength=wl)
        biconvex_lens.propagate_ray(ray)
        screen.propagate_ray(ray)
        vertices = ray.vertices()
        z = [v[2] for v in vertices]
        x = [v[0] for v in vertices]

        plt.plot(z, x)

        plt.title("Dispersion of Light Through BK7 Bi-Convex Lens")
        plt.xlabel("z (mm)")
        plt.ylabel("x (mm)")
        

    return plt.gcf()


if __name__ == "__main__":

    # Run task 8 function
    task8()

    # Run task 10 function
    FIG10 = task10()

    # Run task 11 function
    FIG11, FOCAL_POINT = task11()

    # Run task 12 function
    FIG12 = task12()

    # Run task 13 function
    FIG13, TASK13_RMS = task13()

    # Run task 14 function
    FIG14, TASK14_RMS, TASK14_DIFF_SCALE = task14()

    # Run task 15 function
    FIG15_PC, FOCAL_POINT_PC, FIG15_CP, FOCAL_POINT_CP = task15()

    # Run task 16 function
    #task16()
    FIG16, PC_RMS, CP_RMS, TASK16_DIFF_SCALE = task16()

    # Run task 17 function
    FIG17, CP_RMS, BICONVEX_RMS = task17()

    # Run task 18 function
    FIG18, FOCAL_POINT = task18()

    # Run task 19 function
    FIG19_TVSA, FIG19_LGSA = task19()

    # Run task 20 function
    FIG20 = task20()

    plt.show()
