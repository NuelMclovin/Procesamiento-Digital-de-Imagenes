"""
Sección de umbralización.
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QComboBox, QMessageBox
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import (
    COLOR_TERCIARIO, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER,
    UMBRAL_DEFAULT
)
from src.funciones.funciones_procesamiento import umbral_fijo, umbral_adaptativo


class SeccionUmbral(SeccionBase):
    """Sección para técnicas de umbralización."""
    
    def __init__(self, ventana_principal):
        super().__init__("UMBRAL", COLOR_TERCIARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de umbralización."""
        self.crear_boton("Fijo", COLOR_TERCIARIO, 
                        lambda: self.mostrar_dialogo_umbral('fijo'))
        
        self.crear_boton("Adaptativo", COLOR_TERCIARIO, 
                        lambda: self.mostrar_dialogo_umbral('adaptativo'))
    
    def mostrar_dialogo_umbral(self, tipo):
        """Muestra diálogo para umbralización"""
        titulo = "Umbral Fijo" if tipo == 'fijo' else "Umbral Adaptativo"
        dialogo = DialogoBase(self.ventana_principal, titulo)
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Parámetros
        if tipo == 'fijo':
            umbral_layout = QHBoxLayout()
            umbral_label = QLabel("Valor umbral (0-255):")
            umbral_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            
            umbral_spin = QSpinBox()
            umbral_spin.setRange(0, 255)
            umbral_spin.setValue(UMBRAL_DEFAULT)
            umbral_spin.setStyleSheet(f"""
                QSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            
            umbral_layout.addWidget(umbral_label)
            umbral_layout.addWidget(umbral_spin, 1)
            dialogo.layout_principal.addLayout(umbral_layout)
            
            params = {'umbral': umbral_spin}
            
        else:  # adaptativo
            block_layout = QHBoxLayout()
            block_label = QLabel("Tamaño bloque (impar):")
            block_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            
            block_combo = QComboBox()
            block_combo.addItems(['3', '5', '7', '9', '11', '13', '15', '17', '19', '21'])
            block_combo.setCurrentText('11')
            block_combo.setStyleSheet(f"""
                QComboBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            
            block_layout.addWidget(block_label)
            block_layout.addWidget(block_combo, 1)
            dialogo.layout_principal.addLayout(block_layout)
            
            c_layout = QHBoxLayout()
            c_label = QLabel("Constante C:")
            c_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            
            c_spin = QSpinBox()
            c_spin.setRange(-50, 50)
            c_spin.setValue(2)
            c_spin.setStyleSheet(f"""
                QSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            
            c_layout.addWidget(c_label)
            c_layout.addWidget(c_spin, 1)
            dialogo.layout_principal.addLayout(c_layout)
            
            params = {'block_size': block_combo, 'C': c_spin}
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                if tipo == 'fijo':
                    umbral_val = params['umbral'].value()
                    resultado = umbral_fijo(imagen, umbral_val)
                    self.ventana_principal.info_label.setText(f"Umbral fijo aplicado (valor: {umbral_val})")
                else:
                    block_size = int(params['block_size'].currentText())
                    C = params['C'].value()
                    resultado = umbral_adaptativo(imagen, block_size, C)
                    self.ventana_principal.info_label.setText(f"Umbral adaptativo aplicado (block: {block_size}, C: {C})")
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

