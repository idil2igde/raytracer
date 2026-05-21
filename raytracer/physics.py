import numpy as np

def refract(direc, normal, n_1, n_2): #assuming that incident and transmitted rays are normalized
    sin_1 = np.linalg.norm(np.cross(direc, normal)) #incident angle from normal and direction of incident ray
    cos_1 = -np.dot(direc, normal)
    eta = n_1 / n_2
    if sin_1 > 1/eta:
        return None #total internal reflection
    direc_refract = eta * direc + (eta * cos_1 - np.sqrt(1 - eta * eta * sin_1 * sin_1)) * normal
    norm_direc_r = direc_refract / np.linalg.norm(direc_refract)
    return norm_direc_r