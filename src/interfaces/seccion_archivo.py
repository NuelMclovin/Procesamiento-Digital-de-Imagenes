"""
Sección de operaciones de archivo (cargar, guardar, resetear, comparar).
"""

from src.interfaces.seccion_base import SeccionBase
from src.config import COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_EXITO, COLOR_ERROR, COLOR_ACENTO


class SeccionArchivo(SeccionBase):
    """Sección para operaciones de archivo."""
    
    def __init__(self, ventana_principal):
        super().__init__("ARCHIVO", COLOR_PRIMARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de la sección archivo."""
        self.crear_boton("Cargar Img 1", COLOR_PRIMARIO, 
                        self.ventana_principal.cargar_imagen)
        
        self.crear_boton("Cargar Img 2", COLOR_SECUNDARIO, 
                        self.ventana_principal.cargar_segunda_imagen)
        
        self.crear_boton("Guardar", COLOR_EXITO, 
                        self.ventana_principal.guardar_resultado)
        
        self.crear_boton("Resetear", COLOR_ERROR, 
                        self.ventana_principal.resetear_imagen)
        
        self.crear_boton("Comparar", COLOR_ACENTO, 
                        self.ventana_principal.mostrar_comparacion)
