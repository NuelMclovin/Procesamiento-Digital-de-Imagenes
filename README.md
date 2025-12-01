# Procesamiento Digital de Imágenes

Aplicación de escritorio para procesamiento de imágenes desarrollada con **Python**, **PySide6** y **OpenCV**.

## 🎯 Características

- **Interfaz gráfica modular** con secciones desplegables
- **Gestión de imágenes**: Cargar, guardar y visualizar hasta 2 imágenes simultáneamente
- **Generación de ruido**: Sal y pimienta, Gaussiano
- **Filtros de reducción de ruido**: Promediador, Mediana, Gaussiano, Bilateral, Mínimo, Máximo, Moda
- **Operaciones aritméticas**: Suma, resta, multiplicación, división (con escalares e imágenes)
- **Operaciones lógicas**: AND, OR, XOR, NOT
- **Umbralización**: Fija y adaptativa
- **Ajuste de brillo**: Múltiples técnicas de ecualización y corrección gamma
- **Segmentación**: Otsu, Kapur, mínimo del histograma, múltiples umbrales
- **Análisis de componentes conexas**
- **Visualización de histogramas** en tiempo real

## 🛠️ Tecnologías

- **Python 3.11+**
- **PySide6** - Interfaz gráfica
- **OpenCV (cv2)** - Procesamiento de imágenes
- **NumPy** - Operaciones numéricas
- **Matplotlib** - Generación de histogramas
- **SciPy** - Análisis de señales

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/NuelMclovin/Procesamiento-Digital-de-Imagenes.git
cd Procesamiento-Digital-de-Imagenes
```

2. Instala las dependencias:
```bash
pip install -r requerimeintos.txt
```

## 🚀 Uso

Ejecuta la aplicación:
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
Ruido Final/
├── main.py                          # Punto de entrada de la aplicación
├── requerimeintos.txt               # Dependencias del proyecto
├── src/
│   ├── config.py                    # Configuración global (colores, tamaños)
│   ├── funciones/                   # Módulos de procesamiento
│   │   ├── operaciones_aritmeticas.py
│   │   ├── operaciones_logicas.py
│   │   ├── componentes_conexas.py
│   │   ├── funciones_ruido.py
│   │   ├── funciones_filtrado.py
│   │   ├── funciones_umbralizacion.py
│   │   ├── funciones_brillo.py
│   │   ├── funciones_segmentacion.py
│   │   ├── imagen_multiversion.py
│   │   └── funciones_procesamiento.py  # Hub de importación
│   └── interfaces/                  # Módulos de interfaz gráfica
│       ├── interfaz_principal.py    # Ventana principal
│       ├── dialogos_base.py         # Clase base para diálogos
│       ├── seccion_base.py          # Clase base para secciones
│       ├── seccion_archivo.py       # Carga/guardado de imágenes
│       ├── seccion_ruido.py
│       ├── seccion_filtros.py
│       ├── seccion_modos.py
│       ├── seccion_aritmetica.py
│       ├── seccion_logicas.py
│       ├── seccion_umbral.py
│       ├── seccion_brillo.py
│       └── seccion_segmentacion.py
```

## 🎨 Arquitectura Modular

El proyecto utiliza una arquitectura modular con:
- **Separación de responsabilidades**: Procesamiento e interfaz en módulos independientes
- **Clases base reutilizables**: `SeccionBase` y `DialogoBase` para consistencia
- **Hub de importación**: `funciones_procesamiento.py` re-exporta todas las funciones
- **35 funciones** de procesamiento organizadas por categoría

## 📸 Funcionalidades Principales

### Generación de Ruido
- Ruido Sal y Pimienta (configurable)
- Ruido Gaussiano (media y sigma ajustables)

### Filtros
- Promediador simple y pesado
- Mediana
- Gaussiano
- Bilateral
- Mínimo / Máximo
- Moda

### Operaciones
- Aritméticas: con escalares e imágenes
- Lógicas: AND, OR, XOR, NOT

### Segmentación
- Método de Otsu
- Entropía de Kapur
- Mínimo del histograma
- Umbral por media
- Múltiples umbrales
- Umbral por banda

## 👨‍💻 Autor

**Emanuel Mejía Pérez**  
ESCOM - IPN  
Procesamiento Digital de Imágenes - 4BM2

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos.

---

⭐ Si te fue útil, considera darle una estrella al repositorio
