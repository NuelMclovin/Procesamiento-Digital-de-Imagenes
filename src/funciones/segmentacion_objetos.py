"""Funciones de segmentación de objetos específicos.

Incluye un pipeline para extraer una botella usando dos máscaras (mask_A y mask_B)
que luego se combinan con una operación lógica AND.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np

from .funciones_brillo import correccion_gamma
from .funciones_segmentacion import segmentacion_otsu
from .funciones_umbralizacion import umbral_fijo
from .funciones_morfologia import (
    top_hat,
    gradiente_morfologico,
    cierre,
    apertura,
    dilatacion,
)
from .componentes_conexas import etiquetar_componentes
from .operaciones_logicas import operacion_logica


@dataclass(frozen=True)
class ResultadoSegmentacionBotella:
    mask_a: np.ndarray
    mask_b: np.ndarray
    mask_final: np.ndarray
    recorte_bgr: np.ndarray
    debug: dict[str, Any]


def _asegurar_uint8_binaria(mask: np.ndarray) -> np.ndarray:
    if mask is None:
        raise ValueError("La máscara es None")
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    if mask.ndim == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # Normalizar a 0/255
    mask = (mask > 0).astype(np.uint8) * 255
    return mask


def _seleccionar_mejor_componente(
    binaria: np.ndarray,
    *,
    area_min: int,
    min_aspect: float,
    max_area_ratio: float,
) -> np.ndarray:
    """Selecciona la componente que mejor parece una botella (grande y alargada)."""
    binaria = _asegurar_uint8_binaria(binaria)
    h, w = binaria.shape[:2]
    area_total = float(h * w)
    max_area = int(area_total * max_area_ratio)

    num_labels, labels, stats, _ = etiquetar_componentes(binaria, connectivity=8)
    if num_labels <= 1:
        return binaria

    mejor_idx = None
    mejor_score = -1.0

    for lab in range(1, num_labels):
        x, y, bw, bh, area = stats[lab]
        if area < area_min:
            continue
        if area > max_area:
            continue

        denom = float(min(bw, bh)) if min(bw, bh) > 0 else 1.0
        aspect = float(max(bw, bh)) / denom
        if aspect < min_aspect:
            continue

        # Score: prioriza área y alargamiento.
        area_norm = float(area) / area_total
        aspect_norm = min(aspect / 10.0, 1.0)
        score = 0.75 * area_norm + 0.25 * aspect_norm

        if score > mejor_score:
            mejor_score = score
            mejor_idx = lab

    if mejor_idx is None:
        return binaria

    return (labels == mejor_idx).astype(np.uint8) * 255


def segmentar_botella_doble_mascara(
    imagen: np.ndarray,
    *,
    gamma_a: float = 0.7,
    kernel_tophat: int = 13,
    kernel_morf_a: int = 7,
    area_min_a: int = 1500,
    min_aspect_a: float = 2.0,
    kernel_grad: int = 7,
    thr_grad: int = 35,
    kernel_dilate_b: int = 5,
    iter_dilate_b: int = 2,
    kernel_close_b: int = 9,
    area_min_b: int = 1200,
    min_aspect_b: float = 2.0,
    max_area_ratio: float = 0.45,
) -> ResultadoSegmentacionBotella:
    """Extrae una botella usando dos máscaras y una operación lógica AND.

    Genera:
    - mask_A: basada en brillo (TopHat + Otsu + morfología + componentes)
    - mask_B: basada en contornos (gradiente morfológico + umbral fijo + morfología + componentes)
    - mask_final = mask_A AND mask_B
    - recorte_bgr = imagen original en BGR enmascarada por mask_final
    """
    if imagen is None:
        raise ValueError("La imagen de entrada es None")

    if imagen.ndim == 2:
        imagen_bgr = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)
        gray = imagen
    else:
        imagen_bgr = imagen
        gray = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

    # -------------------------
    # MÁSCARA A (brillo / objeto claro)
    # -------------------------
    gray_gamma = correccion_gamma(gray, gamma_a)
    th = top_hat(gray_gamma, kernel_tophat)
    th = cv2.normalize(th, None, 0, 255, cv2.NORM_MINMAX)
    th = th.astype(np.uint8)
    th_blur = cv2.GaussianBlur(th, (5, 5), 0)
    mask_a_raw, _ = segmentacion_otsu(th_blur)
    mask_a_raw = _asegurar_uint8_binaria(mask_a_raw)
    mask_a_m = cierre(mask_a_raw, kernel_morf_a, 1)
    mask_a_m = apertura(mask_a_m, max(3, kernel_morf_a - 2), 1)
    mask_a = _seleccionar_mejor_componente(
        mask_a_m,
        area_min=area_min_a,
        min_aspect=min_aspect_a,
        max_area_ratio=max_area_ratio,
    )

    # -------------------------
    # MÁSCARA B (contorno / forma)
    # -------------------------
    grad = gradiente_morfologico(gray, kernel_grad)
    grad = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    mask_b_raw = umbral_fijo(grad, thr_grad)
    mask_b_raw = _asegurar_uint8_binaria(mask_b_raw)
    mask_b_m = dilatacion(mask_b_raw, kernel_dilate_b, iter_dilate_b)
    mask_b_m = cierre(mask_b_m, kernel_close_b, 1)
    mask_b_m = apertura(mask_b_m, max(3, kernel_dilate_b), 1)
    mask_b = _seleccionar_mejor_componente(
        mask_b_m,
        area_min=area_min_b,
        min_aspect=min_aspect_b,
        max_area_ratio=max_area_ratio,
    )

    # -------------------------
    # AND final + recorte
    # -------------------------
    mask_final = operacion_logica(mask_a, mask_b, "AND")
    mask_final = _asegurar_uint8_binaria(mask_final)

    recorte = cv2.bitwise_and(imagen_bgr, imagen_bgr, mask=mask_final)

    debug: dict[str, Any] = {
        "gray": gray,
        "gray_gamma": gray_gamma,
        "tophat": th,
        "tophat_blur": th_blur,
        "mask_a_raw": mask_a_raw,
        "mask_a_morf": mask_a_m,
        "gradiente": grad,
        "mask_b_raw": mask_b_raw,
        "mask_b_morf": mask_b_m,
    }

    return ResultadoSegmentacionBotella(
        mask_a=mask_a,
        mask_b=mask_b,
        mask_final=mask_final,
        recorte_bgr=recorte,
        debug=debug,
    )
