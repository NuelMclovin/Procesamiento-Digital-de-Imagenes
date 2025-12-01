"""
Funciones de segmentacion de imagenes por diferentes tecnicas.
"""

import cv2
import numpy as np


def segmentacion_otsu(imagen):
    """
    Aplica segmentacion por metodo de Otsu.
    
    Args:
        imagen: Imagen de entrada
        
    Returns:
        Tupla (imagen_segmentada, umbral_utilizado)
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    umbral, imagen_segmentada = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagen_segmentada, umbral


def entropia_kapur(histograma, total_pixceles):
    """
    Calcula el umbral óptimo usando entropía de Kapur.
    
    Args:
        histograma: Histograma de la imagen
        total_pixceles: Total de píxeles en la imagen
        
    Returns:
        Umbral óptimo
    """
    max_entropia = -1
    umbral_optimo = 0
    
    for t in range(255):
        clase1 = histograma[:t]
        clase2 = histograma[t:]
        
        p1 = np.sum(clase1) / total_pixceles
        p2 = np.sum(clase2) / total_pixceles
        
        if p1 == 0 or p2 == 0:
            continue
        
        h1 = -np.sum((clase1 / np.sum(clase1)) * np.log(clase1 / np.sum(clase1) + 1e-10))
        h2 = -np.sum((clase2 / np.sum(clase2)) * np.log(clase2 / np.sum(clase2) + 1e-10))
        
        entropia_total = p1 * h1 + p2 * h2
        
        if entropia_total > max_entropia:
            max_entropia = entropia_total
            umbral_optimo = t
    
    return umbral_optimo


def segmentacion_kapur(imagen):
    """
    Aplica segmentación por técnica de entropía de Kapur.
    
    Args:
        imagen: Imagen de entrada
        
    Returns:
        Tupla (imagen_segmentada, umbral_utilizado)
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    histograma, _ = np.histogram(imagen, bins=256, range=(0, 256))
    total_pixceles = imagen.size
    
    umbral = entropia_kapur(histograma, total_pixceles)
    imagen_segmentada = (imagen > umbral).astype(np.uint8) * 255
    
    return imagen_segmentada, umbral


def segmentacion_minimo_histograma(imagen):
    """
    Aplica segmentación por método del mínimo del histograma.
    
    Args:
        imagen: Imagen de entrada
        
    Returns:
        Tupla (imagen_segmentada, umbral_utilizado)
    """
    from scipy.signal import find_peaks as fp
    
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    histograma, _ = np.histogram(imagen, bins=256, range=(0, 256))
    
    picos, _ = fp(histograma, distance=20)
    if len(picos) >= 2:
        minimo = np.argmin(histograma[picos[0]:picos[1]]) + picos[0]
    else:
        minimo = 127  # Valor por defecto
    
    imagen_segmentada = (imagen > minimo).astype(np.uint8) * 255
    
    return imagen_segmentada, minimo


def segmentacion_media(imagen):
    """
    Aplica segmentación por umbral de media.
    
    Args:
        imagen: Imagen de entrada
        
    Returns:
        Tupla (imagen_segmentada, umbral_utilizado)
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    umbral = np.mean(imagen)
    imagen_segmentada = (imagen >= umbral).astype(np.uint8) * 255
    
    return imagen_segmentada, umbral


def segmentacion_multiples_umbrales(imagen, T1, T2):
    """
    Aplica segmentación por múltiples umbrales.
    
    Args:
        imagen: Imagen de entrada
        T1: Primer umbral
        T2: Segundo umbral
        
    Returns:
        Imagen segmentada con tres niveles (0, 127, 255)
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    imagen_segmentada = np.zeros_like(imagen)
    imagen_segmentada[imagen < T1] = 0
    imagen_segmentada[(imagen >= T1) & (imagen < T2)] = 127
    imagen_segmentada[imagen >= T2] = 255
    
    return imagen_segmentada


def segmentacion_umbral_banda(imagen, T1, T2):
    """
    Aplica segmentación por umbral banda.
    
    Args:
        imagen: Imagen de entrada
        T1: Umbral inferior
        T2: Umbral superior
        
    Returns:
        Imagen segmentada (binaria)
    """
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    imagen_segmentada = np.zeros_like(imagen)
    imagen_segmentada[(imagen >= T1) & (imagen <= T2)] = 255
    
    return imagen_segmentada
