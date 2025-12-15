"""
Clase base para las secciones de la interfaz.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from src.config import COLOR_TEXT_PRIMARY, COLOR_BORDER, COLOR_SECUNDARIO, COLOR_HOVER


class SeccionBase(QWidget):
    """Clase base para crear secciones colapsables en el panel lateral."""
    
    def __init__(self, titulo, color_titulo, ventana_principal):
        super().__init__()
        self.titulo = titulo
        self.color_titulo = color_titulo
        self.ventana_principal = ventana_principal
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de la sección."""
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Botón de título (expandir/contraer)
        self.btn_titulo = QPushButton(f"▼ {self.titulo}")
        self.btn_titulo.setMinimumHeight(35)
        self.btn_titulo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_titulo.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                padding: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color_titulo}, stop:1 {COLOR_SECUNDARIO});
                border-radius: 8px;
                margin-top: 6px;
                border: 2px solid {COLOR_BORDER};
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_HOVER}, stop:1 {self.color_titulo});
                border: 2px solid {self.color_titulo};
            }}
        """)
        
        # Contenedor de botones (colapsable)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(4)
        self.contenedor_layout.setContentsMargins(4, 4, 4, 4)
        self.contenedor.setVisible(True)
        
        # Conectar toggle
        self.btn_titulo.clicked.connect(self.toggle_seccion)
        
        layout.addWidget(self.btn_titulo)
        layout.addWidget(self.contenedor)
        
        # Crear botones de la sección
        self.crear_botones()
    
    def toggle_seccion(self):
        """Expandir/contraer la sección."""
        visible = self.contenedor.isVisible()
        self.contenedor.setVisible(not visible)
        self.btn_titulo.setText(f"{'▼' if not visible else '▶'} {self.titulo}")
    
    def crear_botones(self):
        """Método a sobrescribir por las clases hijas para crear sus botones."""
        pass
    
    def crear_boton(self, texto, color, callback):
        """Crea un botón para la sección."""
        btn = QPushButton(texto)
        btn.setMinimumHeight(38)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1f2e, stop:1 #0f1419);
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {color};
                border-radius: 10px;
                font-size: 9px;
                font-weight: 600;
                padding: 8px 10px;
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {COLOR_SECUNDARIO});
                border: 2px solid {COLOR_TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background: #0f1419;
                border: 2px solid {color};
                padding-top: 10px;
                padding-bottom: 6px;
            }}
        """)
        btn.clicked.connect(callback)
        self.contenedor_layout.addWidget(btn)
        return btn
    
    def aplicar_a_imagenes(self, dialogo, funcion_procesamiento):
        """
        Aplica una función de procesamiento a la(s) imagen(es) seleccionada(s).
        
        Args:
            dialogo: El diálogo que contiene el selector de imagen
            funcion_procesamiento: Función que recibe una imagen y retorna el resultado procesado
        
        Returns:
            resultado procesado (imagen única o lista de imágenes)
        """
        imagen, label = dialogo.obtener_imagen_seleccionada()
        
        if imagen is None:
            return None
        
        # Si se seleccionó "Ambas"
        if imagen == 'ambas':
            resultados = []
            for img, lbl in label:
                resultado = funcion_procesamiento(img)
                resultados.append(resultado)
            return resultados
        else:
            # Una sola imagen
            return funcion_procesamiento(imagen)
