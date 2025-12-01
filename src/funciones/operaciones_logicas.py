"""
Funciones de operaciones logicas entre imagenes.
"""

import cv2
import numpy as np


def operacion_logica(img1, img2, operacion):
    """ Aplica una operación lógica entre dos imagenes. """
    # Hacer copias para evitar modificar las originales
    img1 = img1.copy()
    
    # Para operación NOT, no se necesita img2
    if operacion == 'NOT':
        return cv2.bitwise_not(img1)
    
    img2 = img2.copy()
    
    # Asegurar que ambas tengan el mismo tamaño
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Asegurar que ambas tengan el mismo formato de canales
    if len(img1.shape) != len(img2.shape):
        if len(img1.shape) == 2 and len(img2.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        elif len(img1.shape) == 3 and len(img2.shape) == 2:
            img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    
    if operacion == 'AND':
        return cv2.bitwise_and(img1, img2)
    elif operacion == 'OR':
        return cv2.bitwise_or(img1, img2)
    elif operacion == 'XOR':
        return cv2.bitwise_xor(img1, img2)
    else:
        return img1
