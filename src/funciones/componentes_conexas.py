"""
Funciones de análisis de componentes conexas.
"""

import cv2
import numpy as np


def preprocesar_imagen(img, usar_morfo=True, kernel_size=3):
    """
    Preprocesa la imagen binaria para mejorar la detección de componentes.
    
    Args:
        img: Imagen binaria
        usar_morfo: Si aplicar operaciones morfológicas
        kernel_size: Tamaño del kernel morfológico
    
    Returns:
        Imagen preprocesada
    """
    img_proc = img.copy()
    
    if usar_morfo:
        # Crear kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        # Closing: cerrar pequeños agujeros
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_CLOSE, kernel)
        
        # Opening: eliminar ruido pequeño
        img_proc = cv2.morphologyEx(img_proc, cv2.MORPH_OPEN, kernel)
    
    return img_proc


def filtrar_componentes_pequenas(labels, area_minima):
    """
    Filtra componentes con área menor al umbral.
    
    Args:
        labels: Matriz de etiquetas
        area_minima: Área mínima en píxeles
    
    Returns:
        labels_filtradas: Matriz de etiquetas filtrada
        componentes_eliminadas: Número de componentes eliminadas
    """
    labels_filtradas = labels.copy()
    componentes_eliminadas = 0
    
    # Obtener área de cada componente
    for lab in range(1, labels.max() + 1):
        area = np.sum(labels == lab)
        if area < area_minima:
            labels_filtradas[labels == lab] = 0
            componentes_eliminadas += 1
    
    # Reetiquetar componentes restantes
    labels_unicas = np.unique(labels_filtradas)
    labels_nuevas = np.zeros_like(labels_filtradas)
    
    for idx, lab in enumerate(labels_unicas):
        if lab != 0:
            labels_nuevas[labels_filtradas == lab] = idx
    
    return labels_nuevas, componentes_eliminadas


def obtener_estadisticas_componentes(labels):
    """
    Calcula estadísticas de las componentes conexas.
    
    Args:
        labels: Matriz de etiquetas
    
    Returns:
        dict con estadísticas de cada componente
    """
    estadisticas = []
    
    for lab in range(1, labels.max() + 1):
        mask = (labels == lab).astype(np.uint8)
        
        # Área
        area = np.sum(mask)
        
        # Perímetro
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        perimetro = cv2.arcLength(contours[0], True) if contours else 0
        
        # Centroide
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        
        # Bounding box
        if contours:
            x, y, w, h = cv2.boundingRect(contours[0])
            aspect_ratio = float(w) / h if h > 0 else 0
        else:
            x, y, w, h = 0, 0, 0, 0
            aspect_ratio = 0
        
        # Circularidad (4π * área / perímetro²)
        circularidad = (4 * np.pi * area) / (perimetro ** 2) if perimetro > 0 else 0
        
        estadisticas.append({
            'etiqueta': lab,
            'area': area,
            'perimetro': perimetro,
            'centroide': (cx, cy),
            'bbox': (x, y, w, h),
            'aspect_ratio': aspect_ratio,
            'circularidad': circularidad
        })
    
    return estadisticas


def etiquetar_componentes(bin_img, connectivity=8):
    """
    Etiqueta componentes conexas usando OpenCV con estadísticas.
    
    Args:
        bin_img: Imagen binaria
        connectivity: 4 u 8
    
    Returns:
        num_labels: número de componentes
        labels: matriz de etiquetas
        stats: estadísticas de cada componente (área, bbox, etc.)
        centroids: centroides de cada componente
    """
    if bin_img.dtype != np.uint8:
        bin_img = bin_img.astype(np.uint8)
    
    # Usar connectedComponentsWithStats para obtener más información
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img, connectivity=connectivity)
    
    return num_labels, labels, stats, centroids


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


def dibujar_regiones_numeradas(labels, original_bin=None, mostrar_info=True):
    """
    Dibuja cada región etiquetada con contorno, número y opcionalmente información adicional.
    
    Args:
        labels: Matriz de etiquetas
        original_bin: Imagen binaria original (opcional)
        mostrar_info: Si mostrar información adicional (área)
    
    Returns:
        Imagen con regiones numeradas
    """
    h, w = labels.shape

    # Crear fondo negro
    bg = np.zeros((h, w, 3), dtype=np.uint8)

    n = int(labels.max())
    # Fondo negro, componentes blancas
    palette = [(0, 0, 0)] + [(255, 255, 255) for _ in range(n)]

    out = bg.copy()

    for lab in range(1, n+1):
        mask = (labels == lab).astype(np.uint8)
        
        # Colorear región
        out[mask > 0] = palette[lab]
        
        # Dibujar contorno blanco más grueso
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue
            
        cv2.drawContours(out, contours, -1, (200, 200, 200), 2)
        
        # Calcular centroide y área
        M = cv2.moments(mask)
        area = np.sum(mask)
        
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Dibujar número grande y visible
            font_scale = 0.8
            thickness = 2
            
            # Texto con fondo para mejor visibilidad
            text = str(lab)
            (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_BOLD, font_scale, thickness)
            
            # Dibujar rectángulo de fondo
            cv2.rectangle(out, (cx - text_w//2 - 5, cy - text_h//2 - 5), 
                         (cx + text_w//2 + 5, cy + text_h//2 + 5), (0, 0, 0), -1)
            
            # Dibujar número en negro con borde blanco
            cv2.putText(out, text, (cx - text_w//2, cy + text_h//2), 
                       cv2.FONT_HERSHEY_BOLD, font_scale, (0, 0, 0), thickness + 2)
            cv2.putText(out, text, (cx - text_w//2, cy + text_h//2), 
                       cv2.FONT_HERSHEY_BOLD, font_scale, (255, 255, 255), thickness)
            
            # Mostrar área si está activado
            if mostrar_info and area > 100:
                info_text = f"A:{area}px"
                cv2.putText(out, info_text, (cx - 30, cy + 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 0), 1)

    return out
