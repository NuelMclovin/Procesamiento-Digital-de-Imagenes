"""
Clase para gestionar multiples versiones de una imagen (color, grises, binaria).
"""

import cv2
import numpy as np


class ImagenMultiVersion:
    """Almacena y gestiona las tres versiones de una imagen: color, grises y binaria."""
    
    def __init__(self, path_or_array, nombre="Imagen", thresh=127):
        """
        Inicializa la imagen en sus tres formatos.
        
        Args:
            path_or_array: Ruta de la imagen (str) o numpy array
            nombre: Nombre descriptivo
            thresh: Umbral para binarización
        """
        self.nombre = nombre
        self.thresh = thresh
        
        # Cargar imagen
        if isinstance(path_or_array, str):
            self.path = path_or_array
            # Cargar en color (BGR)
            img_bgr = cv2.imread(path_or_array)
            if img_bgr is None:
                raise FileNotFoundError(f"No se pudo cargar la imagen: {path_or_array}")
            # Mantener en BGR (formato de OpenCV)
            self.color = img_bgr.copy()
        else:
            # Ya es un numpy array
            self.path = None
            if len(path_or_array.shape) == 2:
                # Escala de grises, convertir a BGR
                self.color = cv2.cvtColor(path_or_array, cv2.COLOR_GRAY2BGR)
            elif path_or_array.shape[2] == 3:
                # Asumimos que viene en BGR desde cv2.imread
                self.color = path_or_array.copy()
            else:
                self.color = path_or_array.copy()
        
        # Convertir a escala de grises (desde BGR)
        self.grises = cv2.cvtColor(self.color, cv2.COLOR_BGR2GRAY)
        
        # Binarizar
        _, self.binaria = cv2.threshold(self.grises, thresh, 255, cv2.THRESH_BINARY)
        
        # Redimensionar todas a tamaño de referencia
        from src.config import TAMANO_REFERENCIA
        self.color = cv2.resize(self.color, TAMANO_REFERENCIA)
        self.grises = cv2.resize(self.grises, TAMANO_REFERENCIA)
        self.binaria = cv2.resize(self.binaria, TAMANO_REFERENCIA)
    
    def get_version(self, tipo):
        """Retorna la versión solicitada de la imagen."""
        if tipo == 'color':
            return self.color
        elif tipo == 'grises':
            return self.grises
        elif tipo == 'binaria':
            return self.binaria
        else:
            raise ValueError(f"Tipo de imagen no válido: {tipo}")
    
    def __str__(self):
        return f"ImagenMultiVersion({self.nombre}, thresh={self.thresh})"
