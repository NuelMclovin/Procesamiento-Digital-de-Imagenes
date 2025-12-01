"""
Funciones de filtrado para reducción de ruido y suavizado de imágenes.
"""

import cv2
import numpy as np


def filtro_promediador(imagen, kernel_size=5):
    """
    Aplica un filtro promediador (blur).
    Calcula el promedio aritmético de todos los píxeles vecinos en una ventana.
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel (debe ser impar)
    
    Returns:
        Imagen filtrada
    """
    return cv2.blur(imagen, (kernel_size, kernel_size))


def filtro_promediador_pesado(imagen, n=5):
    """
    Aplica un filtro promediador con pesos personalizados.
    Usa un kernel 3x3 con todos los valores en 1, normalizado por n.
    
    Args:
        imagen: Imagen de entrada
        n: Factor de normalización
    
    Returns:
        Imagen filtrada
    """
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32)
    return cv2.filter2D(imagen, -1, kernel / n)


def filtro_mediana(imagen, kernel_size=5):
    """
    Aplica filtro de mediana para reducir ruido.
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel (debe ser impar)
    
    Returns:
        Imagen filtrada
    """
    return cv2.medianBlur(imagen, kernel_size)


def filtro_gaussiano(imagen, kernel_size=5, sigma=1.0):
    """
    Aplica filtro gaussiano para suavizar la imagen.
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel (debe ser impar)
        sigma: Desviación estándar del kernel gaussiano
    
    Returns:
        Imagen suavizada
    """
    return cv2.GaussianBlur(imagen, (kernel_size, kernel_size), sigma)


def filtro_moda(imagen, kernel_size=5):
    """
    Aplica un filtro de moda.
    Reemplaza cada píxel por el valor más frecuente en su vecindad.
    Usa mediana como aproximación rápida.
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel (debe ser impar)
    
    Returns:
        Imagen filtrada
    """
    return cv2.medianBlur(imagen, kernel_size)


def filtro_minimo(imagen, kernel_size=5):
    """
    Aplica un filtro de mínimo (erosión).
    Reemplaza cada píxel por el valor mínimo en su vecindad.
    Útil para eliminar ruido de sal (píxeles blancos).
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel
    
    Returns:
        Imagen filtrada
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(imagen, kernel)


def filtro_maximo(imagen, kernel_size=5):
    """
    Aplica un filtro de máximo (dilatación).
    Reemplaza cada píxel por el valor máximo en su vecindad.
    Útil para eliminar ruido de pimienta (píxeles negros).
    
    Args:
        imagen: Imagen de entrada
        kernel_size: Tamaño del kernel
    
    Returns:
        Imagen filtrada
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(imagen, kernel)


def filtro_bilateral(imagen, d=9, sigma_color=75, sigma_space=75):
    """
    Aplica filtro bilateral para suavizar preservando bordes.
    
    Args:
        imagen: Imagen de entrada
        d: Diámetro del píxel neighborhood
        sigma_color: Filtro sigma en el espacio de color
        sigma_space: Filtro sigma en el espacio de coordenadas
    
    Returns:
        Imagen filtrada
    """
    return cv2.bilateralFilter(imagen, d, sigma_color, sigma_space)
