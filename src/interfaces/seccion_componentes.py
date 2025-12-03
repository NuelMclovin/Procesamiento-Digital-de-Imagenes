"""
Sección de análisis de componentes conexas.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QMessageBox, QComboBox, QCheckBox
import cv2
import numpy as np
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_ADVERTENCIA, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER
from src.funciones.funciones_procesamiento import (
    etiquetar_componentes,
    colorear_etiquetas,
    dibujar_regiones_numeradas,
    preprocesar_imagen,
    filtrar_componentes_pequenas,
    obtener_estadisticas_componentes
)


class SeccionComponentes(SeccionBase):
    """Sección para análisis de componentes conexas."""
    
    def __init__(self, ventana_principal):
        super().__init__("COMPONENTES CONEXAS", COLOR_ADVERTENCIA, ventana_principal)
        # Variables para almacenar las etiquetas y la imagen binaria
        self.etiquetas_actuales = None
        self.imagen_binaria_original = None
    
    def crear_botones(self):
        """Crea los botones de componentes conexas."""
        self.crear_boton("Etiquetar", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_etiquetar())
        
        self.crear_boton("Colorear Etiquetas", COLOR_ADVERTENCIA, 
                        lambda: self.colorear_componentes())
    
    def mostrar_dialogo_etiquetar(self):
        """Muestra diálogo para etiquetar componentes conexas"""
        if self.ventana_principal.imagen_actual is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", "Primero carga una imagen.")
            return
        
        dialogo = DialogoBase(self.ventana_principal, "Etiquetar Componentes Conexas", 450)
        
        # Selector de conectividad
        conectividad_layout = QHBoxLayout()
        conectividad_label = QLabel("Conectividad:")
        conectividad_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        conectividad_combo = QComboBox()
        conectividad_combo.addItems(["4 (vecinos laterales)", "8 (incluye diagonales)"])
        conectividad_combo.setCurrentIndex(1)  # Por defecto 8
        conectividad_combo.setStyleSheet(f"""
            QComboBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                selection-background-color: {COLOR_ADVERTENCIA};
            }}
        """)
        
        conectividad_layout.addWidget(conectividad_label)
        conectividad_layout.addWidget(conectividad_combo, 1)
        dialogo.layout_principal.addLayout(conectividad_layout)
        
        # Checkbox para preprocesamiento morfológico
        morfo_checkbox = QCheckBox("Aplicar preprocesamiento morfológico (eliminar ruido)")
        morfo_checkbox.setChecked(True)
        morfo_checkbox.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        dialogo.layout_principal.addWidget(morfo_checkbox)
        
        # Filtrado por área mínima
        area_layout = QHBoxLayout()
        area_label = QLabel("Área mínima (píxeles):")
        area_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        area_spinbox = QSpinBox()
        area_spinbox.setRange(0, 10000)
        area_spinbox.setValue(50)
        area_spinbox.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        area_layout.addWidget(area_label)
        area_layout.addWidget(area_spinbox, 1)
        dialogo.layout_principal.addLayout(area_layout)
        
        # Información mejorada
        info_label = QLabel(
            " IMPORTANTE:\n"
            "• La imagen se invertirá para detectar objetos oscuros\n"
            "• El preprocesamiento morfológico elimina ruido pequeño\n"
            "• El filtro de área elimina componentes muy pequeñas\n"
            "• Conectividad 4: solo vecinos laterales\n"
            "• Conectividad 8: incluye diagonales (recomendado)"
        )
        info_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY}; 
                font-size: 11px; 
                padding: 12px;
                background: {COLOR_CARD};
                border: 1px solid {COLOR_ADVERTENCIA};
                border-radius: 6px;
            }}
        """)
        info_label.setWordWrap(True)
        dialogo.layout_principal.addWidget(info_label)
        
        def aplicar():
            try:
                # Extraer valor de conectividad del texto
                texto_conectividad = conectividad_combo.currentText()
                conectividad = 4 if texto_conectividad.startswith("4") else 8
                
                # Convertir a binaria si no lo está
                img = self.ventana_principal.imagen_actual.copy()
                
                # Si es color, convertir a grises
                if len(img.shape) == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Asegurar que sea binaria (0 o 255)
                if img.max() > 1 or img.dtype != np.uint8:
                    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
                else:
                    # Si ya es binaria pero con valores 0-1, escalar a 0-255
                    if img.max() == 1:
                        img = img * 255
                
                # INVERTIR la imagen para que objetos oscuros sean detectados como componentes
                img = cv2.bitwise_not(img)
                
                # Aplicar preprocesamiento si está activado
                if morfo_checkbox.isChecked():
                    img = preprocesar_imagen(img, usar_morfo=True, kernel_size=3)
                
                # Etiquetar componentes con estadísticas
                num_labels, labels, stats, centroids = etiquetar_componentes(img, conectividad)
                
                # Filtrar componentes pequeñas
                area_minima = area_spinbox.value()
                if area_minima > 0:
                    labels, eliminadas = filtrar_componentes_pequenas(labels, area_minima)
                    num_labels = labels.max() + 1
                else:
                    eliminadas = 0
                
                # Guardar etiquetas y la imagen binaria original
                self.etiquetas_actuales = labels
                self.imagen_binaria_original = img
                
                # Obtener estadísticas detalladas
                estadisticas = obtener_estadisticas_componentes(labels)
                
                # Mostrar resultado coloreado automáticamente
                resultado = colorear_etiquetas(labels)
                
                self.ventana_principal.imagen_actual = resultado
                self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                       self.ventana_principal.imagen_actual)
                
                # Mensaje informativo detallado
                num_componentes = num_labels - 1  # Restamos el fondo
                self.ventana_principal.info_label.setText(
                    f" Etiquetado: {num_componentes} componente(s) | "
                    f"Conectividad: {conectividad} | Filtradas: {eliminadas} | Coloreado automático"
                )
                
                # Mostrar información adicional en consola
                print(f"\n{'='*70}")
                print(f"ANÁLISIS DE COMPONENTES CONEXAS")
                print(f"{'='*70}")
                print(f"Conectividad: {conectividad}")
                print(f"Preprocesamiento morfológico: {'Sí' if morfo_checkbox.isChecked() else 'No'}")
                print(f"Área mínima: {area_minima} px")
                print(f"Componentes detectadas: {num_componentes}")
                print(f"Componentes filtradas: {eliminadas}")
                print(f"Dimensiones: {img.shape}")
                print(f"\n{'='*70}")
                print(f"ESTADÍSTICAS POR COMPONENTE:")
                print(f"{'='*70}")
                for stat in estadisticas:
                    print(f"Componente {stat['etiqueta']}:")
                    print(f"  Área: {stat['area']} px")
                    print(f"  Perímetro: {stat['perimetro']:.2f} px")
                    print(f"  Centroide: {stat['centroide']}")
                    print(f"  Aspect Ratio: {stat['aspect_ratio']:.2f}")
                    print(f"  Circularidad: {stat['circularidad']:.2f}")
                    print(f"  BBox: {stat['bbox']}")
                print(f"{'='*70}\n")
                
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al etiquetar:\n{str(e)}\n\nAsegúrate de que la imagen esté en formato correcto.")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def colorear_componentes(self):
        """Colorea las componentes etiquetadas"""
        if self.etiquetas_actuales is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", 
                               "Primero etiqueta las componentes usando el botón 'Etiquetar'.")
            return
        
        try:
            resultado = colorear_etiquetas(self.etiquetas_actuales)
            
            self.ventana_principal.imagen_actual = resultado
            self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                   self.ventana_principal.imagen_actual)
            
            num_componentes = int(self.etiquetas_actuales.max())
            self.ventana_principal.info_label.setText(
                f" Componentes coloreadas con paleta aleatoria | Total: {num_componentes} componente(s)")
        except Exception as e:
            QMessageBox.critical(self.ventana_principal, "Error", f"Error al colorear:\n{str(e)}")
