"""
Sección de operaciones aritméticas.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QMessageBox
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_PRIMARIO, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER
from src.funciones.funciones_procesamiento import operacion_escalar


class SeccionAritmetica(SeccionBase):
    """Sección para operaciones aritméticas con escalares."""
    
    def __init__(self, ventana_principal):
        super().__init__("ARITMÉTICA", COLOR_PRIMARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de operaciones aritméticas."""
        self.crear_boton("Suma", COLOR_PRIMARIO, 
                        lambda: self.mostrar_dialogo_aritmetica('suma'))
        
        self.crear_boton("Resta", COLOR_PRIMARIO, 
                        lambda: self.mostrar_dialogo_aritmetica('resta'))
        
        self.crear_boton("Multiplicar", COLOR_PRIMARIO, 
                        lambda: self.mostrar_dialogo_aritmetica('multiplicacion'))
        
        self.crear_boton("Dividir", COLOR_PRIMARIO, 
                        lambda: self.mostrar_dialogo_aritmetica('division'))
    
    def mostrar_dialogo_aritmetica(self, operacion):
        """Muestra diálogo para operaciones aritméticas con escalar"""
        dialogo = DialogoBase(self.ventana_principal, f"Operación Aritmética: {operacion.upper()}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Input de valor escalar
        valor_layout = QHBoxLayout()
        valor_label = QLabel("Valor escalar:")
        valor_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        valor_spin = QSpinBox()
        valor_spin.setRange(-255, 255)
        valor_spin.setValue(50)
        valor_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
            }}
        """)
        
        valor_layout.addWidget(valor_label)
        valor_layout.addWidget(valor_spin, 1)
        dialogo.layout_principal.addLayout(valor_layout)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                valor = valor_spin.value()
                resultado = operacion_escalar(imagen, valor, operacion)
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(f"{operacion.upper()} aplicada con valor {valor}")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al aplicar operación:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

