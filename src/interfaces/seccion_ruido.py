"""
Sección de generación de ruido.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QDoubleSpinBox, QSpinBox, QMessageBox
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import (
    COLOR_ADVERTENCIA, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER,
    RUIDO_SAL_PIMIENTA_DEFAULT, RUIDO_GAUSSIANO_MEDIA_DEFAULT, RUIDO_GAUSSIANO_SIGMA_DEFAULT
)
from src.funciones.funciones_procesamiento import agregar_ruido_sal_pimienta, agregar_ruido_gaussiano


class SeccionRuido(SeccionBase):
    """Sección para agregar ruido a las imágenes."""
    
    def __init__(self, ventana_principal):
        super().__init__("RUIDO", COLOR_ADVERTENCIA, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de generación de ruido."""
        self.crear_boton("Sal/Pimienta", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_ruido('sal_pimienta'))
        
        self.crear_boton("Gaussiano", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_ruido('gaussiano'))
    
    def mostrar_dialogo_ruido(self, tipo):
        """Muestra diálogo para agregar ruido"""
        titulo = "Sal y Pimienta" if tipo == 'sal_pimienta' else "Gaussiano"
        dialogo = DialogoBase(self.ventana_principal, f"Agregar Ruido: {titulo}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Parámetros según tipo de ruido
        if tipo == 'sal_pimienta':
            param_layout = QHBoxLayout()
            param_label = QLabel("Cantidad (0.0 - 1.0):")
            param_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            
            param_spin = QDoubleSpinBox()
            param_spin.setRange(0.0, 1.0)
            param_spin.setSingleStep(0.01)
            param_spin.setValue(RUIDO_SAL_PIMIENTA_DEFAULT)
            param_spin.setDecimals(3)
            param_spin.setStyleSheet(f"""
                QDoubleSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            
            param_layout.addWidget(param_label)
            param_layout.addWidget(param_spin, 1)
            dialogo.layout_principal.addLayout(param_layout)
            
            params = {'cantidad': param_spin}
            
        else:  # gaussiano
            media_layout = QHBoxLayout()
            media_label = QLabel("Media:")
            media_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            media_spin = QSpinBox()
            media_spin.setRange(-100, 100)
            media_spin.setValue(RUIDO_GAUSSIANO_MEDIA_DEFAULT)
            media_spin.setStyleSheet(f"""
                QSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            media_layout.addWidget(media_label)
            media_layout.addWidget(media_spin, 1)
            dialogo.layout_principal.addLayout(media_layout)
            
            sigma_layout = QHBoxLayout()
            sigma_label = QLabel("Sigma (Desv. Est.):")
            sigma_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            sigma_spin = QSpinBox()
            sigma_spin.setRange(1, 100)
            sigma_spin.setValue(RUIDO_GAUSSIANO_SIGMA_DEFAULT)
            sigma_spin.setStyleSheet(f"""
                QSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            sigma_layout.addWidget(sigma_label)
            sigma_layout.addWidget(sigma_spin, 1)
            dialogo.layout_principal.addLayout(sigma_layout)
            
            params = {'media': media_spin, 'sigma': sigma_spin}
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                if tipo == 'sal_pimienta':
                    cantidad = params['cantidad'].value()
                    resultado = agregar_ruido_sal_pimienta(imagen, cantidad)
                    self.ventana_principal.info_label.setText(f"Ruido sal/pimienta agregado (cantidad: {cantidad})")
                else:
                    media = params['media'].value()
                    sigma = params['sigma'].value()
                    resultado = agregar_ruido_gaussiano(imagen, media, sigma)
                    self.ventana_principal.info_label.setText(f"Ruido gaussiano agregado (μ={media}, σ={sigma})")
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

