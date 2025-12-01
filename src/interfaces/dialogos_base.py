"""
Utilidades y diálogos base para la interfaz.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QGroupBox, QRadioButton, QMessageBox
)
from PySide6.QtCore import Qt
from src.config import (
    COLOR_FONDO, COLOR_OSCURO, COLOR_PRIMARIO, COLOR_TEXT_PRIMARY,
    COLOR_BORDER, COLOR_CARD, COLOR_EXITO, COLOR_ERROR
)


class DialogoBase(QDialog):
    """Clase base para crear diálogos con estilo consistente."""
    
    def __init__(self, parent, titulo, ancho=450):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumWidth(ancho)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_OSCURO}, stop:1 {COLOR_FONDO});
                border: 3px solid {COLOR_PRIMARIO};
                border-radius: 15px;
            }}
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton {{
                padding: 12px 24px;
                font-size: 13px;
                font-weight: 700;
                border-radius: 10px;
                border: 2px solid {COLOR_BORDER};
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                border: 2px solid {COLOR_PRIMARIO};
            }}
        """)
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setSpacing(15)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
    
    def agregar_selector_imagen(self, ventana_principal):
        """Agrega selector de imagen al diálogo."""
        grupo_box = QGroupBox("Seleccionar imagen objetivo:")
        grupo_box.setStyleSheet(f"""
            QGroupBox {{
                color: {COLOR_TEXT_PRIMARY};
                font-weight: bold;
                font-size: 14px;
                border: 3px solid {COLOR_PRIMARIO};
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 18px;
                background: {COLOR_CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px;
                background: {COLOR_PRIMARIO};
                border-radius: 6px;
            }}
        """)
        
        grupo_layout = QVBoxLayout(grupo_box)
        
        self.radio_img1 = QRadioButton("Imagen 1 (Principal)")
        self.radio_img1.setChecked(True)
        self.radio_img1.setStyleSheet(f"""
            QRadioButton {{
                color: {COLOR_TEXT_PRIMARY}; 
                font-size: 13px;
                font-weight: 600;
                padding: 6px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
            }}
        """)
        
        self.radio_img2 = QRadioButton("Imagen 2 (Segunda)")
        self.radio_img2.setStyleSheet(f"""
            QRadioButton {{
                color: {COLOR_TEXT_PRIMARY}; 
                font-size: 13px;
                font-weight: 600;
                padding: 6px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
            }}
        """)
        
        self.radio_resultado = QRadioButton("Resultado (Operación Lógica)")
        self.radio_resultado.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 12px;")
        
        grupo_layout.addWidget(self.radio_img1)
        grupo_layout.addWidget(self.radio_img2)
        grupo_layout.addWidget(self.radio_resultado)
        
        self.layout_principal.addWidget(grupo_box)
        self.ventana_principal = ventana_principal
    
    def obtener_imagen_seleccionada(self):
        """Retorna la imagen seleccionada y su label."""
        if self.radio_img1.isChecked():
            if self.ventana_principal.imagen_actual is None:
                QMessageBox.warning(self, "Advertencia", "Imagen 1 no está cargada")
                return None, None
            return self.ventana_principal.imagen_actual, self.ventana_principal.label_imagen_principal
        elif self.radio_img2.isChecked():
            if self.ventana_principal.imagen_segunda is None:
                QMessageBox.warning(self, "Advertencia", "Imagen 2 no está cargada")
                return None, None
            return self.ventana_principal.imagen_segunda, self.ventana_principal.label_segunda
        else:
            if self.ventana_principal.imagen_resultado_logico is None:
                QMessageBox.warning(self, "Advertencia", "No hay resultado de operación lógica")
                return None, None
            return self.ventana_principal.imagen_resultado_logico, self.ventana_principal.label_resultado_logico
    
    def actualizar_imagen_seleccionada(self, resultado):
        """Actualiza la imagen seleccionada con el resultado."""
        if self.radio_img1.isChecked():
            self.ventana_principal.imagen_actual = resultado.copy()
            self.ventana_principal._mostrar_imagen(self.ventana_principal.label_imagen_principal, 
                                                   self.ventana_principal.imagen_actual)
        elif self.radio_img2.isChecked():
            self.ventana_principal.imagen_segunda = resultado.copy()
            self.ventana_principal._mostrar_imagen(self.ventana_principal.label_segunda, 
                                                   self.ventana_principal.imagen_segunda)
        else:
            self.ventana_principal.imagen_resultado_logico = resultado.copy()
            self.ventana_principal.label_resultado_logico.setVisible(True)
            self.ventana_principal._mostrar_imagen(self.ventana_principal.label_resultado_logico, 
                                                   self.ventana_principal.imagen_resultado_logico)
    
    def agregar_botones(self, callback_aplicar):
        """Agrega botones estándar Aplicar/Cancelar."""
        btn_layout = QHBoxLayout()
        
        btn_aplicar = QPushButton("Aplicar")
        btn_aplicar.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_EXITO};
                color: white;
            }}
            QPushButton:hover {{
                background: {COLOR_PRIMARIO};
            }}
        """)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_ERROR};
                color: white;
            }}
        """)
        
        btn_aplicar.clicked.connect(callback_aplicar)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_aplicar)
        btn_layout.addWidget(btn_cancelar)
        self.layout_principal.addLayout(btn_layout)
