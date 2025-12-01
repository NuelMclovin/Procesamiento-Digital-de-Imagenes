"""
Sección de modos de visualización.
"""

from PySide6.QtWidgets import QLabel, QMessageBox
import cv2
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_EXITO, COLOR_INFO, COLOR_OSCURO, COLOR_ACENTO


class SeccionModos(SeccionBase):
    """Sección para cambiar entre modos de visualización."""
    
    def __init__(self, ventana_principal):
        super().__init__("MODOS", COLOR_EXITO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de modos."""
        self.crear_boton("Color", COLOR_EXITO, 
                        lambda: self.mostrar_dialogo_modo('color'))
        
        self.crear_boton("Grises", COLOR_INFO, 
                        lambda: self.mostrar_dialogo_modo('grises'))
        
        self.crear_boton("Binaria", COLOR_OSCURO, 
                        lambda: self.mostrar_dialogo_modo('binaria'))
    
    def mostrar_dialogo_modo(self, modo):
        """Muestra diálogo para cambiar modo de color con selector de imagen"""
        nombres = {'color': 'Color', 'grises': 'Escala de Grises', 'binaria': 'Binaria'}
        
        dialogo = DialogoBase(self.ventana_principal, f"Cambiar a: {nombres[modo]}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Información
        info = QLabel(f"Se convertirá la imagen seleccionada a modo {nombres[modo]}")
        info.setStyleSheet(f"color: {COLOR_ACENTO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                # Convertir imagen según el modo
                if modo == 'grises':
                    if len(imagen.shape) == 3:
                        resultado = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
                    else:
                        resultado = imagen.copy()
                elif modo == 'binaria':
                    if len(imagen.shape) == 3:
                        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
                    else:
                        gris = imagen.copy()
                    _, resultado = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
                else:  # color
                    if len(imagen.shape) == 2:
                        resultado = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)
                    else:
                        resultado = imagen.copy()
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                
                QMessageBox.information(dialogo, "Éxito", f"Modo cambiado a {nombres[modo]}")
                dialogo.accept()
                
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al cambiar modo: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

