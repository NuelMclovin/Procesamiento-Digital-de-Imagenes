"""
Funciones para agregar diferentes tipos de ruido a imágenes.
"""

import numpy as np


def agregar_ruido_sal_pimienta(imagen, cantidad=0.02):
    """
    Agrega ruido sal y pimienta a una imagen.
    
    Args:
        imagen: Imagen de entrada
        cantidad: Proporción de píxeles a afectar (0.0 - 1.0)
    
    Returns:
        Imagen con ruido
    """
    resultado = imagen.copy()
    
    # Número de píxeles a afectar
    num_pixeles = int(cantidad * imagen.size)
    
    # Ruido sal (blanco)
    coords_sal = [np.random.randint(0, i, num_pixeles // 2) for i in imagen.shape[:2]]
    resultado[coords_sal[0], coords_sal[1]] = 255
    
    # Ruido pimienta (negro)
    coords_pimienta = [np.random.randint(0, i, num_pixeles // 2) for i in imagen.shape[:2]]
    resultado[coords_pimienta[0], coords_pimienta[1]] = 0
    
    return resultado


def agregar_ruido_gaussiano(imagen, media=0, sigma=20):
    """
    Agrega ruido gaussiano a una imagen.
    
    Args:
        imagen: Imagen de entrada
        media: Media de la distribución gaussiana
        sigma: Desviación estándar
    
    Returns:
        Imagen con ruido gaussiano
    """
    resultado = imagen.copy().astype(np.float32)
    
    # Generar ruido gaussiano
    ruido = np.random.normal(media, sigma, imagen.shape).astype(np.float32)
    
    # Agregar ruido
    resultado = resultado + ruido
    
    # Clip para mantener valores válidos
    resultado = np.clip(resultado, 0, 255)
    
    return resultado.astype(np.uint8)
