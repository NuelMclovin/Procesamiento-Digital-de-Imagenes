"""
Sección de técnicas de segmentación.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QMessageBox
import cv2
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_PELIGRO, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER
from src.funciones.funciones_procesamiento import (
    segmentacion_otsu, segmentacion_kapur, segmentacion_minimo_histograma,
    segmentacion_media, segmentacion_multiples_umbrales, segmentacion_umbral_banda
)


class SeccionSegmentacion(SeccionBase):
    """Sección para técnicas de segmentación."""
    
    def __init__(self, ventana_principal):
        super().__init__("SEGMENTACIÓN", COLOR_PELIGRO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de segmentación."""
        self.crear_boton("Otsu", COLOR_PELIGRO, 
                        lambda: self.aplicar_segmentacion('otsu'))
        
        self.crear_boton("Kapur", COLOR_PELIGRO, 
                        lambda: self.aplicar_segmentacion('kapur'))
        
        self.crear_boton("Mín. Histograma", COLOR_PELIGRO, 
                        lambda: self.aplicar_segmentacion('minimo'))
        
        self.crear_boton("Por Media", COLOR_PELIGRO, 
                        lambda: self.aplicar_segmentacion('media'))
        
        self.crear_boton("Múltiples Umbrales", COLOR_PELIGRO, 
                        lambda: self.mostrar_dialogo_segmentacion_multi())
        
        self.crear_boton("Umbral Banda", COLOR_PELIGRO, 
                        lambda: self.mostrar_dialogo_segmentacion_banda())
    
    def aplicar_segmentacion(self, tipo):
        """Aplica técnicas de segmentación"""
        dialogo = DialogoBase(self.ventana_principal, f"Segmentación: {tipo.capitalize()}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                if tipo == 'otsu':
                    resultado, _ = segmentacion_otsu(imagen)
                elif tipo == 'kapur':
                    resultado, _ = segmentacion_kapur(imagen)
                elif tipo == 'minimo':
                    resultado, _ = segmentacion_minimo_histograma(imagen)
                elif tipo == 'media':
                    resultado, _ = segmentacion_media(imagen)
                
                if len(resultado.shape) == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                
                mensajes = {
                    'otsu': "Segmentación Otsu aplicada",
                    'kapur': "Segmentación Kapur aplicada",
                    'minimo': "Segmentación mínimo histograma aplicada",
                    'media': "Segmentación por media aplicada"
                }
                
                mensaje = mensajes[tipo]
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(mensaje)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al aplicar segmentación:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def mostrar_dialogo_segmentacion_multi(self):
        """Muestra diálogo para segmentación por múltiples umbrales"""
        dialogo = DialogoBase(self.ventana_principal, "Segmentación Múltiples Umbrales", 400)
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Umbral 1
        t1_layout = QHBoxLayout()
        t1_label = QLabel("Umbral 1 (0-255):")
        t1_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        t1_spin = QSpinBox()
        t1_spin.setRange(0, 255)
        t1_spin.setValue(80)
        t1_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        t1_layout.addWidget(t1_label)
        t1_layout.addWidget(t1_spin, 1)
        dialogo.layout_principal.addLayout(t1_layout)
        
        # Umbral 2
        t2_layout = QHBoxLayout()
        t2_label = QLabel("Umbral 2 (0-255):")
        t2_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        t2_spin = QSpinBox()
        t2_spin.setRange(0, 255)
        t2_spin.setValue(150)
        t2_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        t2_layout.addWidget(t2_label)
        t2_layout.addWidget(t2_spin, 1)
        dialogo.layout_principal.addLayout(t2_layout)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                T1 = t1_spin.value()
                T2 = t2_spin.value()
                
                if T1 >= T2:
                    QMessageBox.warning(dialogo, "Advertencia", "T1 debe ser menor que T2")
                    return
                
                resultado = segmentacion_multiples_umbrales(imagen, T1, T2)
                if len(resultado.shape) == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                
                mensaje = f"Segmentación múltiples umbrales (T1: {T1}, T2: {T2})"
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(mensaje)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def mostrar_dialogo_segmentacion_banda(self):
        """Muestra diálogo para segmentación por umbral banda"""
        dialogo = DialogoBase(self.ventana_principal, "Segmentación Umbral Banda", 400)
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Umbral inferior
        t1_layout = QHBoxLayout()
        t1_label = QLabel("Umbral Inferior (0-255):")
        t1_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        t1_spin = QSpinBox()
        t1_spin.setRange(0, 255)
        t1_spin.setValue(80)
        t1_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        t1_layout.addWidget(t1_label)
        t1_layout.addWidget(t1_spin, 1)
        dialogo.layout_principal.addLayout(t1_layout)
        
        # Umbral superior
        t2_layout = QHBoxLayout()
        t2_label = QLabel("Umbral Superior (0-255):")
        t2_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        t2_spin = QSpinBox()
        t2_spin.setRange(0, 255)
        t2_spin.setValue(150)
        t2_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        t2_layout.addWidget(t2_label)
        t2_layout.addWidget(t2_spin, 1)
        dialogo.layout_principal.addLayout(t2_layout)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                T1 = t1_spin.value()
                T2 = t2_spin.value()
                
                if T1 >= T2:
                    QMessageBox.warning(dialogo, "Advertencia", "T1 debe ser menor que T2")
                    return
                
                resultado = segmentacion_umbral_banda(imagen, T1, T2)
                if len(resultado.shape) == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                
                mensaje = f"Segmentación umbral banda (T1: {T1}, T2: {T2})"
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(mensaje)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
