"""
Funciones de Morfologia Matematica
Implementa las operaciones morfologicas basicas para procesamiento de imagenes binarias.

Operaciones disponibles:
- Erosion: Reduce el tamano de objetos blancos, elimina ruido pequeno
- Dilatacion: Expande objetos blancos, rellena huecos pequenos
- Apertura: Erosion seguida de dilatacion, elimina ruido externo
- Cierre: Dilatacion seguida de erosion, rellena huecos internos
- Gradiente morfologico: Diferencia entre dilatacion y erosion, detecta bordes
- Top Hat: Diferencia entre imagen original y apertura, realza detalles claros
- Black Hat: Diferencia entre cierre e imagen original, realza detalles oscuros
"""

import cv2
import numpy as np


def erosion(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica la operacion de erosion a una imagen.
    
    La erosion reduce el tamano de los objetos blancos eliminando pixeles en los bordes.
    Es util para:
    - Eliminar ruido pequeno (puntos blancos)
    - Separar objetos que estan ligeramente conectados
    - Reducir el tamano de estructuras
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 5
        iteraciones: Numero de veces que se aplica la operacion, por defecto 1
        
    Returns:
        Imagen erosionada
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar erosion
    imagen_erosionada = cv2.erode(imagen, kernel, iterations=iteraciones)
    
    return imagen_erosionada


def dilatacion(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica la operacion de dilatacion a una imagen.
    
    La dilatacion expande el tamano de los objetos blancos agregando pixeles en los bordes.
    Es util para:
    - Rellenar pequenos huecos dentro de objetos
    - Conectar componentes cercanos
    - Aumentar el tamano de estructuras
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 5
        iteraciones: Numero de veces que se aplica la operacion, por defecto 1
        
    Returns:
        Imagen dilatada
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar dilatacion
    imagen_dilatada = cv2.dilate(imagen, kernel, iterations=iteraciones)
    
    return imagen_dilatada


def apertura(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica la operacion de apertura (erosion seguida de dilatacion).
    
    La apertura es util para:
    - Eliminar ruido externo (puntos blancos pequenos fuera de objetos)
    - Suavizar contornos externos
    - Separar objetos que estan unidos por conexiones delgadas
    - Mantener el tamano aproximado de los objetos principales
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 5
        iteraciones: Numero de veces que se aplica la operacion, por defecto 1
        
    Returns:
        Imagen con apertura aplicada
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar apertura usando la funcion optimizada de OpenCV
    imagen_apertura = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel, iterations=iteraciones)
    
    return imagen_apertura


def cierre(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica la operacion de cierre (dilatacion seguida de erosion).
    
    El cierre es util para:
    - Rellenar huecos internos (agujeros pequenos dentro de objetos)
    - Cerrar brechas en contornos
    - Conectar componentes que estan muy cerca
    - Suavizar contornos internos manteniendo el tamano aproximado
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 5
        iteraciones: Numero de veces que se aplica la operacion, por defecto 1
        
    Returns:
        Imagen con cierre aplicado
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar cierre usando la funcion optimizada de OpenCV
    imagen_cierre = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel, iterations=iteraciones)
    
    return imagen_cierre


def gradiente_morfologico(imagen, tamano_kernel=5):
    """
    Calcula el gradiente morfologico (diferencia entre dilatacion y erosion).
    
    El gradiente morfologico es util para:
    - Detectar bordes de objetos
    - Resaltar contornos
    - Encontrar limites entre regiones
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 5
        
    Returns:
        Imagen con gradiente morfologico
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar gradiente morfologico
    gradiente = cv2.morphologyEx(imagen, cv2.MORPH_GRADIENT, kernel)
    
    return gradiente


def top_hat(imagen, tamano_kernel=9):
    """
    Aplica la operacion Top Hat (diferencia entre imagen original y apertura).
    
    Top Hat es util para:
    - Realzar detalles claros pequenos
    - Extraer elementos mas brillantes que el fondo
    - Corregir iluminacion no uniforme
    - Detectar objetos pequenos brillantes
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 9
        
    Returns:
        Imagen con Top Hat aplicado
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar Top Hat
    tophat = cv2.morphologyEx(imagen, cv2.MORPH_TOPHAT, kernel)
    
    return tophat


def black_hat(imagen, tamano_kernel=9):
    """
    Aplica la operacion Black Hat (diferencia entre cierre e imagen original).
    
    Black Hat es util para:
    - Realzar detalles oscuros pequenos
    - Extraer elementos mas oscuros que el fondo
    - Detectar valles y depresiones
    - Detectar objetos pequenos oscuros
    
    Args:
        imagen: Imagen de entrada (puede ser color o escala de grises)
        tamano_kernel: Tamano del kernel (debe ser impar), por defecto 9
        
    Returns:
        Imagen con Black Hat aplicado
    """
    # Asegurar que el tamano del kernel sea impar
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1
    
    # Crear el kernel estructurante
    kernel = np.ones((tamano_kernel, tamano_kernel), np.uint8)
    
    # Aplicar Black Hat
    blackhat = cv2.morphologyEx(imagen, cv2.MORPH_BLACKHAT, kernel)
    
    return blackhat


def apertura_tradicional(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica apertura de forma tradicional (erosion manual seguida de dilatacion).
    
    Esta implementacion aplica manualmente erosion y luego dilatacion,
    equivalente a la apertura pero mostrando los pasos intermedios.
    
    Args:
        imagen: Imagen de entrada
        tamano_kernel: Tamano del kernel, por defecto 5
        iteraciones: Numero de iteraciones, por defecto 1
        
    Returns:
        Imagen con apertura tradicional
    """
    # Primero erosion
    img_erosionada = erosion(imagen, tamano_kernel, iteraciones)
    # Luego dilatacion
    img_apertura = dilatacion(img_erosionada, tamano_kernel, iteraciones)
    
    return img_apertura


def cierre_tradicional(imagen, tamano_kernel=5, iteraciones=1):
    """
    Aplica cierre de forma tradicional (dilatacion manual seguida de erosion).
    
    Esta implementacion aplica manualmente dilatacion y luego erosion,
    equivalente al cierre pero mostrando los pasos intermedios.
    
    Args:
        imagen: Imagen de entrada
        tamano_kernel: Tamano del kernel, por defecto 5
        iteraciones: Numero de iteraciones, por defecto 1
        
    Returns:
        Imagen con cierre tradicional
    """
    # Primero dilatacion
    img_dilatada = dilatacion(imagen, tamano_kernel, iteraciones)
    # Luego erosion
    img_cierre = erosion(img_dilatada, tamano_kernel, iteraciones)
    
    return img_cierre
