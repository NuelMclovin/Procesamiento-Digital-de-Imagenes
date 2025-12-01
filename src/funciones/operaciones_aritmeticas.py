"""
Funciones de operaciones aritméticas entre imágenes y escalares.
"""

import cv2
import numpy as np


def operacion_escalar(imagen, escalar, operacion):
    """
    Aplica una operación aritmética entre una imagen y un escalar.
    
    Args:
        imagen: numpy array (puede ser color, grises o binaria)
        escalar: valor numérico (int o float)
        operacion: 'suma', 'resta', 'multiplicacion', 'division'
    
    Returns:
        imagen resultante (con valores normalizados a 0-255)
    """
    img = imagen.astype(np.float32)
    
    if operacion == 'suma':
        resultado = img + escalar
    elif operacion == 'resta':
        resultado = img - escalar
    elif operacion == 'multiplicacion':
        resultado = img * escalar
    elif operacion == 'division':
        if escalar != 0:
            resultado = img / escalar
        else:
            resultado = img
    else:
        resultado = img
    
    # Normalizar a rango 0-255
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)


def operacion_entre_imagenes(img1, img2, operacion):
    """
    Aplica una operación aritmética entre dos imágenes.
    
    Args:
        img1: numpy array (imagen 1)
        img2: numpy array (imagen 2)
        operacion: 'suma', 'resta', 'multiplicacion', 'division'
    
    Returns:
        imagen resultante
    """
    # Hacer copias para evitar modificar las originales
    img1 = img1.copy()
    img2 = img2.copy()
    
    # Asegurar que ambas tengan el mismo tamaño
    if img1.shape != img2.shape:
        # Redimensionar img2 al tamaño de img1
        if len(img1.shape) == 3:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        else:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    i1 = img1.astype(np.float32)
    i2 = img2.astype(np.float32)
    
    if operacion == 'suma':
        resultado = i1 + i2
    elif operacion == 'resta':
        resultado = i1 - i2
    elif operacion == 'multiplicacion':
        # Normalizar multiplicación: dividir entre 255 para mantener rango
        resultado = (i1 * i2) / 255.0
    elif operacion == 'division':
        # Evitar división por cero y normalizar resultado
        resultado = np.divide(i1, i2 + 1e-10, out=np.zeros_like(i1), where=i2!=0)
        # Normalizar el resultado al rango 0-255
        if resultado.max() > 0:
            resultado = (resultado / resultado.max()) * 255.0
    else:
        resultado = i1
    
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)
