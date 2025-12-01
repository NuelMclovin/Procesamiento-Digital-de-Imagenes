"""
Funciones de umbralización para binarización de imágenes.
"""

import cv2
import numpy as np


def umbral_fijo(imagen, umbral=127):
    """
    Aplica umbralización con valor fijo.
    
    Args:
        imagen: Imagen de entrada (se convierte a grises si es color)
        umbral: Valor de umbral (0-255)
    
    Returns:
        Imagen binarizada
    """
    # Convertir a grises si es necesario
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    
    _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
    return resultado


def umbral_adaptativo(imagen, block_size=11, C=2):
    """
    Aplica umbralización adaptativa.
    
    Args:
        imagen: Imagen de entrada (se convierte a grises si es color)
        block_size: Tamaño del bloque (debe ser impar)
        C: Constante a restar de la media
    
    Returns:
        Imagen binarizada
    """
    # Convertir a grises si es necesario
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    
    resultado = cv2.adaptiveThreshold(
        imagen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, C
    )
    return resultado
