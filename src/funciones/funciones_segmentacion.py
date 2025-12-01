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
    
    # Probabilidades normalizadas
    prob = histograma / total_pixceles
    
    for t in range(1, 255):  # Empezar en 1 para evitar clases vacías
        # Probabilidades acumuladas
        w0 = np.sum(prob[:t])
        w1 = np.sum(prob[t:])
        
        if w0 == 0 or w1 == 0:
            continue
        
        # Entropía de la clase 0 (fondo)
        h0 = 0
        for i in range(t):
            if prob[i] > 0:
                p_i_w0 = prob[i] / w0
                h0 -= p_i_w0 * np.log(p_i_w0)
        
        # Entropía de la clase 1 (objeto)
        h1 = 0
        for i in range(t, 256):
            if prob[i] > 0:
                p_i_w1 = prob[i] / w1
                h1 -= p_i_w1 * np.log(p_i_w1)
        
        # Entropía total (SIN multiplicar por w0 y w1)
        entropia_total = h0 + h1
        
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
