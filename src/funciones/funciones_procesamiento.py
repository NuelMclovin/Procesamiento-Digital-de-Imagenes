"""
Funciones de procesamiento de imágenes.
Archivo de re-exportación que importa todas las funciones desde los módulos especializados.

Este archivo mantiene la compatibilidad con código existente mientras organiza
las funciones en módulos separados por categoría.
"""

# Importar clase ImagenMultiVersion
from .imagen_multiversion import ImagenMultiVersion

# Importar operaciones aritméticas
from .operaciones_aritmeticas import (
    operacion_escalar,
    operacion_entre_imagenes
)

# Importar operaciones lógicas
from .operaciones_logicas import operacion_logica

# Importar análisis de componentes conexas
from .componentes_conexas import (
    etiquetar_componentes,
    extraer_componente_mas_grande,
    colorear_etiquetas,
    comparar_segmentaciones,
    dibujar_regiones_numeradas
)

# Importar funciones de ruido
from .funciones_ruido import (
    agregar_ruido_sal_pimienta,
    agregar_ruido_gaussiano
)

# Importar funciones de filtrado
from .funciones_filtrado import (
    filtro_promediador,
    filtro_promediador_pesado,
    filtro_mediana,
    filtro_gaussiano,
    filtro_moda,
    filtro_minimo,
    filtro_maximo,
    filtro_bilateral
)

# Importar funciones de umbralización
from .funciones_umbralizacion import (
    umbral_fijo,
    umbral_adaptativo
)

# Importar funciones de ajuste de brillo
from .funciones_brillo import (
    ecualizacion_uniforme,
    ecualizacion_exponencial,
    ecualizacion_rayleigh,
    ecualizacion_hipercubica,
    ecualizacion_logaritmica_hiperbolica,
    funcion_potencia,
    correccion_gamma
)

# Importar funciones de segmentación
from .funciones_segmentacion import (
    segmentacion_otsu,
    entropia_kapur,
    segmentacion_kapur,
    segmentacion_minimo_histograma,
    segmentacion_media,
    segmentacion_multiples_umbrales,
    segmentacion_umbral_banda
)


# Exportar todo para mantener compatibilidad
__all__ = [
    # Clase ImagenMultiVersion
    "ImagenMultiVersion",
    
    # Operaciones aritméticas
    "operacion_escalar",
    "operacion_entre_imagenes",
    
    # Operaciones lógicas
    "operacion_logica",
    
    # Componentes conexas
    "etiquetar_componentes",
    "extraer_componente_mas_grande",
    "colorear_etiquetas",
    "comparar_segmentaciones",
    "dibujar_regiones_numeradas",
    
    # Ruido
    "agregar_ruido_sal_pimienta",
    "agregar_ruido_gaussiano",
    
    # Filtrado
    "filtro_promediador",
    "filtro_promediador_pesado",
    "filtro_mediana",
    "filtro_gaussiano",
    "filtro_moda",
    "filtro_minimo",
    "filtro_maximo",
    "filtro_bilateral",
    
    # Umbralización
    "umbral_fijo",
    "umbral_adaptativo",
    
    # Brillo
    "ecualizacion_uniforme",
    "ecualizacion_exponencial",
    "ecualizacion_rayleigh",
    "ecualizacion_hipercubica",
    "ecualizacion_logaritmica_hiperbolica",
    "funcion_potencia",
    "correccion_gamma",
    
    # Segmentación
    "segmentacion_otsu",
    "entropia_kapur",
    "segmentacion_kapur",
    "segmentacion_minimo_histograma",
    "segmentacion_media",
    "segmentacion_multiples_umbrales",
    "segmentacion_umbral_banda"
]


# ============================================================================
# NOTA: Este archivo ahora actúa como un hub de importación.
# Las implementaciones reales están en los módulos especializados:
#
# - imagen_multiversion.py: Clase ImagenMultiVersion
# - operaciones_aritmeticas.py: Operaciones aritméticas con escalares e imágenes
# - operaciones_logicas.py: Operaciones lógicas (AND, OR, XOR, NOT)
# - componentes_conexas.py: Análisis de componentes conexas
# - funciones_ruido.py: Generación de ruido (sal y pimienta, gaussiano)
# - funciones_filtrado.py: Filtros de reducción de ruido y suavizado
# - funciones_umbralizacion.py: Técnicas de binarización
# - funciones_brillo.py: Ecualización de histogramas y corrección gamma
# - funciones_segmentacion.py: Técnicas de segmentación (Otsu, Kapur, etc.)
#
# Este diseño modular facilita el mantenimiento y la extensión del código.
# ============================================================================
