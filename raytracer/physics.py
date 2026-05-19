import numpy as np

def refract(direc, normal, n_1, n_2):
    sin_1 = np.cross(direc, normal) #incident angle from normal and direction of incident ray
    frac = n_1 / n_2
    if sin_1 > 1/frac:
        return None #total internal reflection
    direc_refract = np.arcsin(frac * sin_1) #from Snell's Law
    return direc_refract