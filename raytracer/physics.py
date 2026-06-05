"""
Module defining the physics of light reflection or refracting from materials. Includes DispersiveMaterials class using Sellmeier
coefficients to calculate the refractive indices of light at given wavelengths
"""
import numpy as np

def refract(direc, normal, n_1, n_2): 
    """
    Using Snell's Law, given the direction of the light ray, the normal of the optical element
    ligth interacts with and the refractive indices of the optical medium and where light intiially
    travels calculates and returns the direction of refracted ray as a numpy array, vector.
    
    Returns None if total internal refrlection occurs.
    """
    direc = np.array(direc, dtype = float)
    normal = np.array(normal, dtype = float)
    direc = direc / np.linalg.norm(direc) #normalizing to get unit vectors for both direction and normal to the surface
    normal = normal / np.linalg.norm(normal)
    sin_1 = np.linalg.norm(np.cross(direc, normal)) #incident angle from normal and direction of incident ray
    cos_1 = -np.dot(direc, normal)
    eta = n_1 / n_2
    if eta > 1 and sin_1 > 1/eta:
        return None #total internal reflection
    direc_refract = eta * direc + (eta * cos_1 - np.sqrt(1 - eta * eta * sin_1 * sin_1)) * normal
    norm_direc_r = direc_refract / np.linalg.norm(direc_refract)
    return norm_direc_r

def reflect(direc, normal): 
    """
    Calculates the direction fo teh relected ray from the optical element at the surface.
    """ 
    direc_reflect = direc - 2 * np.dot(direc, normal) * normal #the incident and reflected angles are equal
    norm_direc_ref = direc_reflect / np.linalg.norm(direc_reflect)
    return norm_direc_ref

class DispersiveMaterial:
    """
    Represents a dispersive optical element using the Sellmeier coeffieicents.
    """
    def __init__(self, b_coeffs = (1. , 2., 3.), c_coeffs=(4., 5., 6)):
        self.__b_coeffs = b_coeffs #Sellmeier coefficients
        self.__c_coeffs = c_coeffs
    def ref_index(self, wavelength): 
        """
        Calculates the refractive index of light given the wavelength using the Sellmeier equation.
        """
        term = 0
        for i in range(3):
            numerator = self.__b_coeffs[i] * wavelength * wavelength
            denominator = wavelength * wavelength - self.__c_coeffs[i]
            term += numerator / denominator
        refractive_index = np.sqrt(1 + term)
        return refractive_index

