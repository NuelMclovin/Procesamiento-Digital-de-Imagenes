"""
Sistema Integrado de Procesamiento de Imágenes
Proyecto Final - PDI

Este es el archivo principal que ejecuta la aplicación.
Integra todas las funcionalidades de procesamiento de imágenes:
- Operaciones aritméticas con escalares
- Operaciones aritméticas entre imágenes
- Operaciones lógicas (AND, OR, XOR, NOT)
- Generación de ruido (Sal y Pimienta, Gaussiano)
- Aplicación de filtros de restauración
- Ajuste de brillo (7 técnicas de ecualización)
- Segmentación (6 técnicas de umbralización)
- Análisis de componentes conexas (etiquetado y coloreo)
"""

import sys
from PySide6.QtWidgets import QApplication
from src.interfaces.interfaz_principal import VentanaPrincipal


def main():
    """Función principal que inicia la aplicación."""
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Configurar estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()
    
    # Ejecutar el loop de eventos
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


