"""
Sección de ajuste de brillo.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QDoubleSpinBox, QPushButton, QMessageBox
import cv2
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_INFO, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER, COLOR_EXITO, COLOR_ERROR
from src.funciones.funciones_procesamiento import (
    ecualizacion_uniforme, ecualizacion_exponencial, ecualizacion_rayleigh,
    ecualizacion_hipercubica, ecualizacion_logaritmica_hiperbolica,
    funcion_potencia, correccion_gamma
)


class SeccionBrillo(SeccionBase):
    """Sección para técnicas de ajuste de brillo."""
    
    def __init__(self, ventana_principal):
        super().__init__("BRILLO", COLOR_INFO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de ajuste de brillo."""
        self.crear_boton("Ecualización Uniforme", COLOR_INFO, 
                        lambda: self.aplicar_ajuste_brillo('uniforme'))
        
        self.crear_boton("Exponencial", COLOR_INFO, 
                        lambda: self.aplicar_ajuste_brillo('exponencial'))
        
        self.crear_boton("Rayleigh", COLOR_INFO, 
                        lambda: self.aplicar_ajuste_brillo('rayleigh'))
        
        self.crear_boton("Hipercúbica", COLOR_INFO, 
                        lambda: self.aplicar_ajuste_brillo('hipercubica'))
        
        self.crear_boton("Log. Hiperbólica", COLOR_INFO, 
                        lambda: self.aplicar_ajuste_brillo('logaritmica'))
        
        self.crear_boton("Función Potencia", COLOR_INFO, 
                        lambda: self.mostrar_dialogo_potencia())
        
        self.crear_boton("Corrección Gamma", COLOR_INFO, 
                        lambda: self.mostrar_dialogo_gamma())
    
    def aplicar_ajuste_brillo(self, tipo):
        """Aplica técnicas de ajuste de brillo"""
        if self.ventana_principal.imagen_actual is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", "Primero carga una imagen.")
            return
        
        try:
            if tipo == 'uniforme':
                resultado = ecualizacion_uniforme(self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText("Ecualización uniforme aplicada")
            elif tipo == 'exponencial':
                resultado = ecualizacion_exponencial(self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText("Ecualización exponencial aplicada")
            elif tipo == 'rayleigh':
                resultado = ecualizacion_rayleigh(self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText("Ecualización Rayleigh aplicada")
            elif tipo == 'hipercubica':
                resultado = ecualizacion_hipercubica(self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText("Ecualización hipercúbica aplicada")
            elif tipo == 'logaritmica':
                resultado = ecualizacion_logaritmica_hiperbolica(self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText("Ecualización logarítmica hiperbólica aplicada")
            
            # Convertir a BGR si es necesario para visualización
            if len(resultado.shape) == 2:
                resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
            
            self.ventana_principal.imagen_actual = resultado
            self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                   self.ventana_principal.imagen_actual)
        except Exception as e:
            QMessageBox.critical(self.ventana_principal, "Error", f"Error al aplicar ajuste:\n{str(e)}")
    
    def mostrar_dialogo_potencia(self):
        """Muestra diálogo para función potencia"""
        dialogo = DialogoBase(self.ventana_principal, "Función Potencia", 400)
        
        # Parámetro potencia
        potencia_layout = QHBoxLayout()
        potencia_label = QLabel("Exponente (1-10):")
        potencia_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        potencia_spin = QDoubleSpinBox()
        potencia_spin.setRange(0.1, 10.0)
        potencia_spin.setValue(2.0)
        potencia_spin.setSingleStep(0.1)
        potencia_spin.setStyleSheet(f"""
            QDoubleSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        potencia_layout.addWidget(potencia_label)
        potencia_layout.addWidget(potencia_spin, 1)
        dialogo.layout_principal.addLayout(potencia_layout)
        
        def aplicar():
            if self.ventana_principal.imagen_actual is None:
                QMessageBox.warning(dialogo, "Advertencia", "Primero carga una imagen.")
                return
            
            try:
                potencia_val = potencia_spin.value()
                resultado = funcion_potencia(self.ventana_principal.imagen_actual, potencia_val)
                
                if len(resultado.shape) == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                
                self.ventana_principal.imagen_actual = resultado
                self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                       self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText(f"Función potencia aplicada (exp: {potencia_val:.2f})")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def mostrar_dialogo_gamma(self):
        """Muestra diálogo para corrección gamma"""
        dialogo = DialogoBase(self.ventana_principal, "Corrección Gamma", 400)
        
        # Parámetro gamma
        gamma_layout = QHBoxLayout()
        gamma_label = QLabel("Valor Gamma (0.1-5.0):")
        gamma_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        gamma_spin = QDoubleSpinBox()
        gamma_spin.setRange(0.1, 5.0)
        gamma_spin.setValue(1.5)
        gamma_spin.setSingleStep(0.1)
        gamma_spin.setStyleSheet(f"""
            QDoubleSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        gamma_layout.addWidget(gamma_label)
        gamma_layout.addWidget(gamma_spin, 1)
        dialogo.layout_principal.addLayout(gamma_layout)
        
        def aplicar():
            if self.ventana_principal.imagen_actual is None:
                QMessageBox.warning(dialogo, "Advertencia", "Primero carga una imagen.")
                return
            
            try:
                gamma_val = gamma_spin.value()
                resultado = correccion_gamma(self.ventana_principal.imagen_actual, gamma_val)
                
                if len(resultado.shape) == 2:
                    resultado = cv2.cvtColor(resultado, cv2.COLOR_GRAY2BGR)
                
                self.ventana_principal.imagen_actual = resultado
                self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                       self.ventana_principal.imagen_actual)
                self.ventana_principal.info_label.setText(f"Corrección gamma aplicada (γ={gamma_val:.2f})")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

