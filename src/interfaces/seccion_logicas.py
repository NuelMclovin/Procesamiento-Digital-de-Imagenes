"""
Sección de operaciones lógicas.
"""

from PySide6.QtWidgets import QLabel, QMessageBox
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import COLOR_SECUNDARIO, COLOR_ACENTO
from src.funciones.funciones_procesamiento import operacion_logica


class SeccionLogicas(SeccionBase):
    """Sección para operaciones lógicas."""
    
    def __init__(self, ventana_principal):
        super().__init__("LÓGICAS", COLOR_SECUNDARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de operaciones lógicas."""
        self.crear_boton("AND", COLOR_SECUNDARIO, 
                        lambda: self.mostrar_dialogo_logica('AND'))
        
        self.crear_boton("OR", COLOR_SECUNDARIO, 
                        lambda: self.mostrar_dialogo_logica('OR'))
        
        self.crear_boton("XOR", COLOR_SECUNDARIO, 
                        lambda: self.mostrar_dialogo_logica('XOR'))
        
        self.crear_boton("NOT", COLOR_SECUNDARIO, 
                        lambda: self.mostrar_dialogo_logica('NOT'))
    
    def mostrar_dialogo_logica(self, operacion):
        """Muestra diálogo para operaciones lógicas"""
        dialogo = DialogoBase(self.ventana_principal, f"Operación Lógica: {operacion}")
        
        # Solo mostrar selector para NOT, para AND/OR/XOR no tiene sentido
        if operacion == 'NOT':
            dialogo.agregar_selector_imagen(self.ventana_principal)
            nota = QLabel("NOT se aplica solo a la imagen seleccionada")
            nota.setStyleSheet(f"color: {COLOR_ACENTO}; font-style: italic;")
            dialogo.layout_principal.addWidget(nota)
        else:
            # Para AND, OR, XOR mostrar información
            nota = QLabel(f"Se aplicará {operacion} entre Imagen 1 e Imagen 2\nEl resultado se mostrará en el panel RESULTADO")
            nota.setStyleSheet(f"color: {COLOR_ACENTO}; font-style: italic; font-size: 13px;")
            nota.setWordWrap(True)
            dialogo.layout_principal.addWidget(nota)
        
        def aplicar():
            if operacion == 'NOT':
                imagen, label = dialogo.obtener_imagen_seleccionada()
                if imagen is None:
                    return
            
            try:
                if operacion == 'NOT':
                    # NOT se aplica solo a la imagen seleccionada
                    resultado = operacion_logica(imagen, None, operacion)
                    dialogo.actualizar_imagen_seleccionada(resultado)
                    self.ventana_principal.info_label.setText(f"Operación {operacion} aplicada")
                else:
                    # Operaciones AND, OR, XOR requieren dos imágenes
                    if self.ventana_principal.imagen_actual is None:
                        QMessageBox.warning(self.ventana_principal, "Advertencia", "Necesitas cargar la Imagen 1")
                        return
                    
                    if self.ventana_principal.imagen_segunda is None:
                        QMessageBox.warning(self.ventana_principal, "Advertencia", "Necesitas cargar la Imagen 2 para operaciones lógicas")
                        return
                    
                    # Realizar operación entre imagen 1 e imagen 2
                    resultado = operacion_logica(self.ventana_principal.imagen_actual, 
                                                self.ventana_principal.imagen_segunda, operacion)
                    
                    # Mostrar resultado en panel RESULTADO
                    self.ventana_principal.imagen_resultado_logico = resultado
                    self.ventana_principal.label_resultado_logico.setVisible(True)
                    self.ventana_principal._mostrar_imagen(self.ventana_principal.label_resultado_logico, resultado)
                    self.ventana_principal.info_label.setText(f"Operación {operacion} entre Imagen 1 e Imagen 2")
                
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

