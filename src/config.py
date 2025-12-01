"""
Archivo de configuración y constantes del proyecto.
Contiene todas las constantes globales y configuraciones.
"""

# Tamaño de referencia para las imágenes
TAMANO_REFERENCIA = (400, 400)

# Ruta de imagen por defecto (puede ser modificada por el usuario)
IMAGEN_DEFAULT = r"C:\Users\cereb\Desktop\Escuela\Cuarto Semestre\PDI\Segundo Parcial\Minireto\IMG_BINARIAS\b2.png"

# Configuración de umbral para binarización
UMBRAL_DEFAULT = 127

# Configuración de ruido
RUIDO_SAL_PIMIENTA_DEFAULT = 0.02
RUIDO_GAUSSIANO_MEDIA_DEFAULT = 0
RUIDO_GAUSSIANO_SIGMA_DEFAULT = 20

# Configuración de filtros
KERNEL_SIZE_DEFAULT = 5
FILTRO_BILATERAL_D = 9
FILTRO_BILATERAL_SIGMA_COLOR = 75
FILTRO_BILATERAL_SIGMA_SPACE = 75
FILTRO_GAUSSIANO_SIGMA = 1.0

# Conectividad para componentes conexas
CONECTIVIDAD_DEFAULT = 8

# Colores de interfaz - Paleta Moderna Premium
COLOR_FONDO = "#0A0E27"  # Azul oscuro profundo
COLOR_PRIMARIO = "#667EEA"  # Índigo brillante
COLOR_SECUNDARIO = "#764BA2"  # Púrpura profundo
COLOR_TERCIARIO = "#F093FB"  # Rosa neón
COLOR_ACENTO = "#4FACFE"  # Azul cyan brillante
COLOR_EXITO = "#43E97B"  # Verde neón
COLOR_ERROR = "#FA709A"  # Rosa coral
COLOR_PELIGRO = "#FF6B6B"  # Rojo vibrante
COLOR_ADVERTENCIA = "#FFD93D"  # Amarillo dorado
COLOR_INFO = "#00F5FF"  # Cyan eléctrico
COLOR_OSCURO = "#1A1F3A"  # Azul oscuro profundo
COLOR_CLARO = "#F0F4F8"  # Gris claro
COLOR_CARD = "#1E2640"  # Azul grisáceo oscuro
COLOR_BORDER = "#2D3561"  # Azul gris medio
COLOR_TEXT_PRIMARY = "#FFFFFF"  # Blanco puro
COLOR_TEXT_SECONDARY = "#A8B2D1"  # Gris azulado claro
COLOR_HOVER = "#7C3AED"  # Púrpura hover
COLOR_SHADOW = "rgba(102, 126, 234, 0.4)"  # Sombra azul

# Formatos de imagen soportados
FORMATOS_IMAGEN = [
    "Imágenes (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)",
    "PNG (*.png)",
    "JPEG (*.jpg *.jpeg)",
    "BMP (*.bmp)",
    "TIFF (*.tiff *.tif)",
    "Todos los archivos (*.*)"
]
