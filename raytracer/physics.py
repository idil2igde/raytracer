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
def reflect(direc, normal): #calculating the 
    direc_reflect = direc - 2 * np.dot(direc, normal) * normal
    norm_direc_ref = direc_reflect / np.linalg.norm(direc_reflect)
    return norm_direc_ref

class DispersiveMaterial:
    def __init__(self, b_coeffs = (1. , 2., 3.), c_coeffs=(4., 5., 6)):
        self.__b_coeffs = b_coeffs #Sellmeier coefficients
        self.__c_coeffs = c_coeffs
    def ref_index(self, wavelength): #Sellmeier equation to calculate the refractive index for a specific wavelength using the coefficients
        term = 0
        for i in range(3):
            numerator = self.__b_coeffs[i] * wavelength * wavelength
            denominator = wavelength * wavelength - self.__c_coeffs[i]
            term += numerator / denominator
        refractive_index = np.sqrt(1 + term)
        return refractive_index

