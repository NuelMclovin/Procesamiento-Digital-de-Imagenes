"""
Funciones de ajuste de brillo y ecualización de histogramas.
"""

import cv2
import numpy as np


def ecualizacion_uniforme(imagen):
    """
    Aplica ecualización uniforme del histograma.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        
    Returns:
        Imagen ecualizada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(imagen)


def ecualizacion_exponencial(imagen):
    """
    Aplica ecualización exponencial.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        
    Returns:
        Imagen con ecualización exponencial aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return np.uint8(255 * (1 - np.exp(-imagen / 255)))


def ecualizacion_rayleigh(imagen):
    """
    Aplica ecualización Rayleigh.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        
    Returns:
        Imagen con ecualización Rayleigh aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return np.uint8(255 * np.sqrt(imagen / 255))


def ecualizacion_hipercubica(imagen):
    """
    Aplica ecualización hipercúbica.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        
    Returns:
        Imagen con ecualización hipercúbica aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return np.uint8(255 * (imagen / 255) ** 4)


def ecualizacion_logaritmica_hiperbolica(imagen):
    """
    Aplica ecualización logarítmica hiperbólica.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        
    Returns:
        Imagen con ecualización logarítmica hiperbólica aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return np.uint8(255 * np.log1p(imagen) / np.log1p(255))


def funcion_potencia(imagen, potencia=2):
    """
    Aplica función potencia.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        potencia: Exponente de la función potencia
        
    Returns:
        Imagen con función potencia aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    return np.uint8(255 * (imagen / 255) ** potencia)


def correccion_gamma(imagen, gamma):
    """
    Aplica corrección gamma.
    
    Args:
        imagen: Imagen de entrada en escala de grises
        gamma: Valor de gamma para la corrección
        
    Returns:
        Imagen con corrección gamma aplicada
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen_gamma = np.power(imagen / 255.0, gamma) * 255
    return np.uint8(imagen_gamma)
