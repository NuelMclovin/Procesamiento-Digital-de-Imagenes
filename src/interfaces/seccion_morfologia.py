"""
Seccion de operaciones morfologicas.
"""

from PySide6.QtWidgets import (QLabel, QHBoxLayout, QSpinBox, QComboBox, 
                               QMessageBox)
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_ADVERTENCIA, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER
from src.funciones.funciones_morfologia import (
    erosion, dilatacion, apertura, cierre,
    gradiente_morfologico, top_hat, black_hat,
    apertura_tradicional, cierre_tradicional
)


class SeccionMorfologia(SeccionBase):
    """Seccion para operaciones de morfologia matematica."""
    
    def __init__(self, ventana_principal):
        super().__init__("MORFOLOGIA", COLOR_ADVERTENCIA, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de operaciones morfologicas."""
        self.crear_boton("Erosion", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('erosion'))
        
        self.crear_boton("Dilatacion", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('dilatacion'))
        
        self.crear_boton("Apertura", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('apertura'))
        
        self.crear_boton("Cierre", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('cierre'))
        
        self.crear_boton("Gradiente", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('gradiente'))
        
        self.crear_boton("Top Hat", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('tophat'))
        
        self.crear_boton("Black Hat", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('blackhat'))
        
        self.crear_boton("Apert. Trad.", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('apertura_trad'))
        
        self.crear_boton("Cierre Trad.", COLOR_ADVERTENCIA, 
                        lambda: self.mostrar_dialogo_morfologia('cierre_trad'))
    
    def mostrar_dialogo_morfologia(self, tipo):
        """Muestra dialogo para aplicar operaciones morfologicas"""
        titulos = {
            'erosion': 'Erosion',
            'dilatacion': 'Dilatacion',
            'apertura': 'Apertura',
            'cierre': 'Cierre',
            'gradiente': 'Gradiente Morfologico',
            'tophat': 'Top Hat',
            'blackhat': 'Black Hat',
            'apertura_trad': 'Apertura Tradicional',
            'cierre_trad': 'Cierre Tradicional'
        }
        
        descripciones = {
            'erosion': 'Reduce objetos blancos, elimina ruido pequeno',
            'dilatacion': 'Expande objetos blancos, rellena huecos',
            'apertura': 'Erosion + Dilatacion, elimina ruido externo',
            'cierre': 'Dilatacion + Erosion, rellena huecos internos',
            'gradiente': 'Detecta bordes y contornos',
            'tophat': 'Realza detalles claros pequenos',
            'blackhat': 'Realza detalles oscuros pequenos',
            'apertura_trad': 'Apertura aplicada manualmente',
            'cierre_trad': 'Cierre aplicado manualmente'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Morfologia: {titulos[tipo]}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Agregar descripcion de la operacion
        desc_label = QLabel(descripciones[tipo])
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_ADVERTENCIA};
                font-style: italic;
                padding: 8px;
                background: rgba(255, 193, 7, 0.1);
                border-radius: 6px;
                border: 1px solid {COLOR_ADVERTENCIA};
            }}
        """)
        dialogo.layout_principal.addWidget(desc_label)
        
        # Crear widgets de parametros
        params = self._crear_parametros_morfologia(dialogo, tipo)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                resultado, mensaje = self._aplicar_operacion_morfologica(imagen, tipo, params)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(mensaje)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def _crear_parametros_morfologia(self, dialogo, tipo):
        """Crea los widgets de parametros para operaciones morfologicas"""
        params = {}
        
        # Tamano de kernel
        kernel_layout = QHBoxLayout()
        kernel_label = QLabel("Tamano kernel (impar):")
        kernel_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        kernel_combo = QComboBox()
        kernel_combo.addItems(['3', '5', '7', '9', '11', '13', '15'])
        kernel_combo.setCurrentText('5')
        kernel_combo.setStyleSheet(f"""
            QComboBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
                min-width: 80px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {COLOR_TEXT_PRIMARY};
                margin-right: 8px;
            }}
        """)
        
        kernel_layout.addWidget(kernel_label)
        kernel_layout.addWidget(kernel_combo, 1)
        dialogo.layout_principal.addLayout(kernel_layout)
        params['kernel'] = kernel_combo
        
        # Iteraciones (solo para operaciones que lo soportan)
        if tipo in ['erosion', 'dilatacion', 'apertura', 'cierre', 'apertura_trad', 'cierre_trad']:
            iter_layout = QHBoxLayout()
            iter_label = QLabel("Iteraciones:")
            iter_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
            
            iter_spin = QSpinBox()
            iter_spin.setRange(1, 10)
            iter_spin.setValue(1)
            iter_spin.setStyleSheet(f"""
                QSpinBox {{
                    background: {COLOR_CARD};
                    color: {COLOR_TEXT_PRIMARY};
                    border: 2px solid {COLOR_BORDER};
                    border-radius: 6px;
                    padding: 6px;
                    min-width: 80px;
                }}
                QSpinBox::up-button, QSpinBox::down-button {{
                    background: {COLOR_ADVERTENCIA};
                    border-radius: 3px;
                    width: 20px;
                }}
            """)
            
            iter_layout.addWidget(iter_label)
            iter_layout.addWidget(iter_spin, 1)
            dialogo.layout_principal.addLayout(iter_layout)
            params['iteraciones'] = iter_spin
        
        return params
    
    def _aplicar_operacion_morfologica(self, imagen, tipo, params):
        """Aplica la operacion morfologica seleccionada"""
        kernel_size = int(params['kernel'].currentText())
        iteraciones = params.get('iteraciones')
        iter_value = iteraciones.value() if iteraciones else 1
        
        if tipo == 'erosion':
            resultado = erosion(imagen, kernel_size, iter_value)
            mensaje = f"Erosion aplicada (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
            
        elif tipo == 'dilatacion':
            resultado = dilatacion(imagen, kernel_size, iter_value)
            mensaje = f"Dilatacion aplicada (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
            
        elif tipo == 'apertura':
            resultado = apertura(imagen, kernel_size, iter_value)
            mensaje = f"Apertura aplicada (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
            
        elif tipo == 'cierre':
            resultado = cierre(imagen, kernel_size, iter_value)
            mensaje = f"Cierre aplicado (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
            
        elif tipo == 'gradiente':
            resultado = gradiente_morfologico(imagen, kernel_size)
            mensaje = f"Gradiente morfologico aplicado (kernel: {kernel_size}x{kernel_size})"
            
        elif tipo == 'tophat':
            resultado = top_hat(imagen, kernel_size)
            mensaje = f"Top Hat aplicado (kernel: {kernel_size}x{kernel_size})"
            
        elif tipo == 'blackhat':
            resultado = black_hat(imagen, kernel_size)
            mensaje = f"Black Hat aplicado (kernel: {kernel_size}x{kernel_size})"
            
        elif tipo == 'apertura_trad':
            resultado = apertura_tradicional(imagen, kernel_size, iter_value)
            mensaje = f"Apertura tradicional aplicada (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
            
        elif tipo == 'cierre_trad':
            resultado = cierre_tradicional(imagen, kernel_size, iter_value)
            mensaje = f"Cierre tradicional aplicado (kernel: {kernel_size}x{kernel_size}, iter: {iter_value})"
        
        return resultado, mensaje
