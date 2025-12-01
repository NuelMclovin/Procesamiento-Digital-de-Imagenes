"""
Funciones de análisis de componentes conexas.
"""

import cv2
import numpy as np


def etiquetar_componentes(bin_img, connectivity=8):
    """
    Etiqueta componentes conexas usando OpenCV.
    
    Args:
        bin_img: Imagen binaria
        connectivity: 4 u 8
    
    Returns:
        num_labels: número de componentes
        labels: matriz de etiquetas
    """
    if bin_img.dtype != np.uint8:
        bin_img = bin_img.astype(np.uint8)
    return cv2.connectedComponents(bin_img, connectivity=connectivity)


def extraer_componente_mas_grande(labels):
    """
    Retorna la etiqueta de la componente más grande (excluyendo fondo).
    
    Args:
        labels: Matriz de etiquetas
    
    Returns:
        Etiqueta de la componente más grande
    """
    labs, counts = np.unique(labels, return_counts=True)
    lab_counts = {int(l): int(c) for l, c in zip(labs, counts) if int(l) != 0}
    return max(lab_counts.items(), key=lambda x: x[1])[0] if lab_counts else None


def colorear_etiquetas(labels):
    """
    Convierte matriz de etiquetas en imagen RGB coloreada.
    
    Args:
        labels: Matriz de etiquetas
    
    Returns:
        Imagen RGB coloreada
    """
    h, w = labels.shape
    out = np.zeros((h, w, 3), dtype=np.uint8)
    n = labels.max()
    
    rng = np.random.default_rng(12345)
    palette = [(0, 0, 0)] + [tuple(rng.integers(50, 230, size=3).tolist()) for _ in range(n)]
    
    for lab in range(0, n+1):
        out[labels == lab] = palette[lab]
    return out


def comparar_segmentaciones(original_bin, labels):
    """
    Compara segmentación original con etiquetada y dibuja fronteras.
    
    Args:
        original_bin: Imagen binaria original
        labels: Matriz de etiquetas
    
    Returns:
        Imagen con fronteras dibujadas
    """
    num_orig, _ = cv2.connectedComponents(original_bin)
    num_new = int(labels.max())
    
    print(f"Componentes (original): {num_orig - 1}")
    print(f"Componentes (etiquetado): {num_new}")
    
    overlay = cv2.cvtColor((original_bin > 0).astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)
    
    for lab in range(1, num_new+1):
        mask = (labels == lab).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)
    
    return overlay


def dibujar_regiones_numeradas(labels, original_bin=None):
    """
    Dibuja cada región etiquetada con un color, contorno y su número centrado.
    
    Args:
        labels: Matriz de etiquetas
        original_bin: Imagen binaria original (opcional)
    
    Returns:
        Imagen con regiones numeradas
    """
    h, w = labels.shape

    if original_bin is not None:
        bg = cv2.cvtColor((original_bin > 0).astype(np.uint8) * 255, cv2.COLOR_GRAY2BGR)
    else:
        bg = np.zeros((h, w, 3), dtype=np.uint8)

    rng = np.random.default_rng(42)
    n = int(labels.max())
    palette = [(255, 255, 255)] + [tuple(rng.integers(80, 220, size=3).tolist()) for _ in range(n)]

    out = bg.copy()

    for lab in range(1, n+1):
        mask = (labels == lab).astype(np.uint8)
        coords = np.column_stack(np.where(mask > 0))
        
        if len(coords) == 0:
            continue
        
        # Colorear región
        out[mask > 0] = palette[lab]
        
        # Dibujar contorno
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, (0, 0, 0), 2)
        
        # Calcular centroide
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Dibujar número
            cv2.putText(out, str(lab), (cx-10, cy+10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    return out
