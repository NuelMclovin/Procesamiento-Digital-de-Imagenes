"""
Interfaz principal del sistema de procesamiento de imágenes.
Versión modular con secciones separadas en archivos independientes.
Cada operación tiene su propio botón con diálogo para seleccionar imagen objetivo y parámetros.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QScrollArea,
    QSlider, QSpinBox, QComboBox, QGroupBox, QDialog, QSizePolicy,
    QRadioButton, QButtonGroup, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from src.config import *
from src.funciones.funciones_procesamiento import (
    ImagenMultiVersion, operacion_escalar, operacion_logica,
    agregar_ruido_sal_pimienta, agregar_ruido_gaussiano,
    filtro_promediador, filtro_promediador_pesado,
    filtro_mediana, filtro_gaussiano, filtro_bilateral,
    filtro_moda, filtro_minimo, filtro_maximo,
    umbral_fijo, umbral_adaptativo,
    ecualizacion_uniforme, ecualizacion_exponencial, ecualizacion_rayleigh,
    ecualizacion_hipercubica, ecualizacion_logaritmica_hiperbolica,
    funcion_potencia, correccion_gamma,
    segmentacion_otsu, segmentacion_kapur, segmentacion_minimo_histograma,
    segmentacion_media, segmentacion_multiples_umbrales, segmentacion_umbral_banda,
    etiquetar_componentes, extraer_componente_mas_grande, colorear_etiquetas,
    comparar_segmentaciones, dibujar_regiones_numeradas
)

# Importar secciones modulares
from src.interfaces.seccion_archivo import SeccionArchivo
from src.interfaces.seccion_aritmetica import SeccionAritmetica
from src.interfaces.seccion_logicas import SeccionLogicas
from src.interfaces.seccion_ruido import SeccionRuido
from src.interfaces.seccion_filtros import SeccionFiltros
from src.interfaces.seccion_umbral import SeccionUmbral
from src.interfaces.seccion_brillo import SeccionBrillo
from src.interfaces.seccion_segmentacion import SeccionSegmentacion
from src.interfaces.seccion_componentes import SeccionComponentes
from src.interfaces.seccion_modos import SeccionModos


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación con toolbar horizontal completa."""
    
    def __init__(self):
        super().__init__()
        # Variables de estado
        self.imagen_cargada = None  # ImagenMultiVersion original (Imagen 1)
        self.imagen_actual = None  # Imagen numpy actual trabajando sobre Imagen 1
        self.imagen_original_backup = None  # Backup de la imagen original
        self.imagen_segunda = None  # Segunda imagen para operaciones
        self.imagen_segunda_cargada = None  # ImagenMultiVersion segunda
        self.imagen_segunda_backup = None  # Backup de segunda imagen
        self.imagen_resultado_logico = None  # Resultado de operaciones lógicas
        self.modo_actual = 'color'  # 'color', 'grises', 'binaria'
        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz gráfica con menú lateral izquierdo"""
        self.setWindowTitle("Procesamiento de Imágenes - PDI")
        self.setGeometry(50, 50, 1600, 900)
        
        # Widget central y layout principal (HORIZONTAL)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        #PANEL LATERAL IZQUIERDO (HERRAMIENTAS) 
        panel_lateral = QWidget()
        panel_lateral.setFixedWidth(230)
        panel_lateral.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_CARD}, stop:0.5 {COLOR_OSCURO}, stop:1 {COLOR_CARD});
                border-right: 4px solid;
                border-image: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:0.5 {COLOR_ACENTO}, stop:1 {COLOR_SECUNDARIO}) 1;
            }}
        """)
        
        # Scroll vertical para el panel lateral
        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        panel_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        panel_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: {COLOR_OSCURO};
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 6px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_ACENTO}, stop:1 {COLOR_SECUNDARIO});
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        panel_widget = QWidget()
        panel_layout = QVBoxLayout(panel_widget)
        panel_layout.setSpacing(8)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        
        # Crear secciones modulares
        panel_layout.addWidget(SeccionArchivo(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionAritmetica(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionLogicas(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionRuido(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionFiltros(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionUmbral(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionBrillo(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionSegmentacion(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionComponentes(self))
        
        panel_layout.addWidget(self._crear_separador_horizontal())
        panel_layout.addWidget(SeccionModos(self))
        
        panel_layout.addStretch()
        
        # Indicador de modo actual en el panel
        self.label_modo = QLabel(f"Modo:\n{self.modo_actual.upper()}")
        self.label_modo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_modo.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
                padding: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 12px;
                border: 2px solid {COLOR_TEXT_PRIMARY};
                margin-top: 10px;
            }}
        """)
        panel_layout.addWidget(self.label_modo)
        
        panel_scroll.setWidget(panel_widget)
        
        panel_lateral_layout = QVBoxLayout(panel_lateral)
        panel_lateral_layout.setContentsMargins(0, 0, 0, 0)
        panel_lateral_layout.addWidget(panel_scroll)
        
        main_layout.addWidget(panel_lateral)
        
        #  ÁREA PRINCIPAL (DERECHA) 
        area_principal = QWidget()
        area_layout = QVBoxLayout(area_principal)
        area_layout.setSpacing(0)
        area_layout.setContentsMargins(0, 0, 0, 0)
        
        #  ÁREA DE IMÁGENES (3 PANELES HORIZONTALES) 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: {COLOR_FONDO};
                border: none;
            }}
            QScrollBar:vertical, QScrollBar:horizontal {{
                background: {COLOR_OSCURO};
                width: 14px;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 7px;
                min-height: 30px;
                min-width: 30px;
            }}
            QScrollBar::handle:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_ACENTO}, stop:1 {COLOR_EXITO});
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
        """)
        
        area_imagenes = QWidget()
        imagenes_layout = QHBoxLayout(area_imagenes)
        imagenes_layout.setSpacing(10)
        imagenes_layout.setContentsMargins(10, 10, 10, 10)
        
        # Panel 1: Imagen Principal (Imagen 1)
        self.label_imagen_principal = self._crear_panel_imagen("IMAGEN 1", COLOR_PRIMARIO)
        imagenes_layout.addWidget(self.label_imagen_principal, 1)
        
        # Panel 2: Segunda Imagen (Imagen 2)
        self.label_segunda = self._crear_panel_imagen("IMAGEN 2", COLOR_SECUNDARIO)
        imagenes_layout.addWidget(self.label_segunda, 1)
        
        # Panel 3: Resultado Lógico (oculto por defecto)
        self.label_resultado_logico = self._crear_panel_imagen("RESULTADO", COLOR_EXITO)
        self.label_resultado_logico.setVisible(False)
        imagenes_layout.addWidget(self.label_resultado_logico, 1)
        
        scroll_area.setWidget(area_imagenes)
        area_layout.addWidget(scroll_area, 1)
        
        #  BARRA DE INFORMACIÓN INFERIOR 
        self.info_label = QLabel("Carga una imagen para comenzar")
        self.info_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_PRIMARIO}, stop:0.3 {COLOR_ACENTO}, 
                    stop:0.7 {COLOR_SECUNDARIO}, stop:1 {COLOR_PRIMARIO});
                padding: 14px 24px;
                border-top: 3px solid {COLOR_TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
        """)
        area_layout.addWidget(self.info_label)
        
        main_layout.addWidget(area_principal, 1)
        
        # Estilo general de la ventana
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {COLOR_FONDO};
            }}
        """)
    
    # ========================================================================
    # MÉTODOS DE INTERFAZ - CREACIÓN DE WIDGETS
    # ========================================================================
    
    def _crear_separador_horizontal(self):
        """Crea un separador horizontal para el panel lateral"""
        sep = QWidget()
        sep.setFixedHeight(3)
        sep.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_OSCURO}, stop:0.5 {COLOR_PRIMARIO}, stop:1 {COLOR_OSCURO});
                margin: 8px 0px;
                border-radius: 2px;
            }}
        """)
        return sep
    
    def _crear_panel_imagen(self, titulo, color_borde):
        """Crea un panel contenedor para mostrar imágenes"""
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        panel.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_CARD}, stop:1 {COLOR_OSCURO});
                border: 3px solid {color_borde};
                border-radius: 15px;
                padding: 8px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título del panel con fondo degradado
        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color_borde}, stop:1 {COLOR_SECUNDARIO});
                border: none;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        layout.addWidget(titulo_label)
        
        # Label para la imagen con borde mejorado
        imagen_label = QLabel("Sin imagen")
        imagen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen_label.setScaledContents(False)
        imagen_label.setMaximumHeight(340)
        imagen_label.setStyleSheet(f"""
            QLabel {{
                background: {COLOR_FONDO};
                border: 3px dashed {color_borde};
                border-radius: 12px;
                color: {COLOR_TEXT_SECONDARY};
                font-size: 12px;
                font-weight: 600;
                min-height: 240px;
                max-height: 340px;
                padding: 10px;
            }}
        """)
        imagen_label.setObjectName("imagen_contenedor")
        layout.addWidget(imagen_label, 1)
        
        # Label para el histograma con borde iluminado
        histograma_label = QLabel("Histograma")
        histograma_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        histograma_label.setMaximumHeight(140)
        histograma_label.setMinimumHeight(140)
        histograma_label.setStyleSheet(f"""
            QLabel {{
                background: {COLOR_FONDO};
                border: 2px solid {color_borde};
                border-radius: 10px;
                color: {COLOR_TEXT_SECONDARY};
                font-size: 11px;
                padding: 4px;
            }}
        """)
        histograma_label.setObjectName("histograma_contenedor")
        layout.addWidget(histograma_label)
        
        return panel
    
    # MÉTODOS DE CARGA Y VISUALIZACIÓN
    
    def cargar_imagen(self):
        """Cargar imagen principal (Imagen 1)"""
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Imagen Principal", "",
            ";;".join(FORMATOS_IMAGEN)
        )
        
        if archivo:
            try:
                # Cargar con OpenCV
                img = cv2.imread(archivo)
                if img is None:
                    raise ValueError("No se pudo cargar la imagen")
                
                # Crear ImagenMultiVersion
                self.imagen_cargada = ImagenMultiVersion(img)
                self.imagen_actual = self.imagen_cargada.get_version(self.modo_actual).copy()
                self.imagen_original_backup = self.imagen_actual.copy()
                
                # Ocultar panel de resultado lógico
                self.label_resultado_logico.setVisible(False)
                self.imagen_resultado_logico = None
                
                # Mostrar en panel principal
                self._mostrar_imagen(self.label_imagen_principal, self.imagen_actual)
                
                self.info_label.setText(f"Imagen 1 cargada: {archivo.split('/')[-1]}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar imagen:\n{str(e)}")
    
    def cargar_segunda_imagen(self):
        """Cargar segunda imagen (Imagen 2)"""
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Segunda Imagen", "",
            ";;".join(FORMATOS_IMAGEN)
        )
        
        if archivo:
            try:
                img = cv2.imread(archivo)
                if img is None:
                    raise ValueError("No se pudo cargar la imagen")
                
                self.imagen_segunda_cargada = ImagenMultiVersion(img)
                self.imagen_segunda = self.imagen_segunda_cargada.get_version(self.modo_actual).copy()
                self.imagen_segunda_backup = self.imagen_segunda.copy()
                
                # Ocultar panel de resultado lógico
                self.label_resultado_logico.setVisible(False)
                self.imagen_resultado_logico = None
                
                self._mostrar_imagen(self.label_segunda, self.imagen_segunda)
                
                self.info_label.setText(f"Imagen 2 cargada: {archivo.split('/')[-1]}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar segunda imagen:\n{str(e)}")
    
    def _mostrar_imagen(self, label_parent, imagen):
        """Mostrar imagen numpy en un label dentro de un panel"""
        if imagen is None:
            return
        
        # Buscar el label contenedor de imagen dentro del panel
        imagen_label = label_parent.findChild(QLabel, "imagen_contenedor")
        if imagen_label is None:
            return
        
        # Convertir a formato Qt para mostrar en el label porque la libreria no acepta numpy directamente 
        if len(imagen.shape) == 2:  # Escala de grises
            h, w = imagen.shape
            bytes_per_line = w
            # Asegurar que los datos sean contiguos en memoria
            img_contiguous = np.ascontiguousarray(imagen)
            q_img = QImage(img_contiguous.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:  # Color
            h, w, ch = imagen.shape
            bytes_per_line = ch * w
            # Convertir BGR a RGB y asegurar que sea contiguo
            rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            rgb_contiguous = np.ascontiguousarray(rgb)
            q_img = QImage(rgb_contiguous.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        
        # Escalar manteniendo aspecto
        scaled_pixmap = pixmap.scaled(
            imagen_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        imagen_label.setPixmap(scaled_pixmap)
        
        # Actualizar histograma
        self._actualizar_histograma(label_parent, imagen)
    
    def _actualizar_histograma(self, label_parent, imagen):
        """Genera y muestra el histograma de una imagen"""
        if imagen is None:
            return
        
        # Buscar el label de histograma
        histograma_label = label_parent.findChild(QLabel, "histograma_contenedor")
        if histograma_label is None:
            return
        
        try:
            # Crear figura de matplotlib
            fig, ax = plt.subplots(figsize=(4, 1.5), dpi=100)
            fig.patch.set_facecolor(COLOR_FONDO)
            ax.set_facecolor(COLOR_FONDO)
            
            # Calcular histograma según tipo de imagen
            if len(imagen.shape) == 2:  # Escala de grises
                hist = cv2.calcHist([imagen], [0], None, [256], [0, 256])
                ax.plot(hist, color='white', linewidth=1.5)
                ax.fill_between(range(256), hist.flatten(), alpha=0.3, color='white')
            else:  # Color (BGR)
                colores = [('blue', 'b'), ('green', 'g'), ('red', 'r')]
                for i, (nombre, color) in enumerate(colores):
                    hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
                    ax.plot(hist, color=color, linewidth=1, alpha=0.7, label=nombre[0].upper())
                ax.legend(loc='upper right', fontsize=6, framealpha=0.3)
            
            # Estilo del gráfico
            ax.set_xlim([0, 256])
            ax.set_ylim([0, None])
            ax.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=7)
            ax.spines['bottom'].set_color(COLOR_BORDER)
            ax.spines['top'].set_color(COLOR_BORDER)
            ax.spines['left'].set_color(COLOR_BORDER)
            ax.spines['right'].set_color(COLOR_BORDER)
            ax.grid(True, alpha=0.2, color=COLOR_BORDER)
            
            # Convertir figura a QPixmap para mostrar en QLabel
            canvas = FigureCanvasAgg(fig)
            canvas.draw()
            buf = canvas.buffer_rgba()
            w, h = canvas.get_width_height()
            qimg = QImage(buf, w, h, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Escalar y mostrar 
            scaled_pixmap = pixmap.scaled(
                histograma_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            histograma_label.setPixmap(scaled_pixmap)
            
            plt.close(fig)
            
        except Exception as e:
            histograma_label.setText(f"Error: {str(e)[:20]}")
    
    def guardar_resultado(self):
        """Guardar imagen seleccionada por el usuario"""
        # Crear diálogo de selección
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Guardar Imagen")
        dialogo.setMinimumWidth(400)
        dialogo.setStyleSheet(f"""
            QDialog {{
                background: {COLOR_FONDO};
            }}
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 13px;
            }}
            QPushButton {{
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                border-radius: 8px;
                border: 2px solid {COLOR_BORDER};
            }}
        """)
        
        layout = QVBoxLayout(dialogo)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        titulo = QLabel("Selecciona qué imagen guardar:")
        titulo.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px; font-weight: bold;")
        layout.addWidget(titulo)
        
        # Grupo de radio buttons
        grupo_box = QGroupBox("Imagen a guardar:")
        grupo_box.setStyleSheet(f"""
            QGroupBox {{
                color: {COLOR_TEXT_PRIMARY};
                font-weight: bold;
                border: 2px solid {COLOR_PRIMARIO};
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        grupo_layout = QVBoxLayout(grupo_box)
        
        radio_img1 = QRadioButton("Imagen 1 (Principal)")
        radio_img1.setChecked(True)
        radio_img1.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 12px;")
        radio_img1.setEnabled(self.imagen_actual is not None)
        
        radio_img2 = QRadioButton("Imagen 2 (Segunda)")
        radio_img2.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 12px;")
        radio_img2.setEnabled(self.imagen_segunda is not None)
        
        radio_resultado = QRadioButton("Resultado (Operación Lógica)")
        radio_resultado.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 12px;")
        radio_resultado.setEnabled(self.imagen_resultado_logico is not None)
        
        grupo_layout.addWidget(radio_img1)
        grupo_layout.addWidget(radio_img2)
        grupo_layout.addWidget(radio_resultado)
        
        layout.addWidget(grupo_box)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setStyleSheet(f"""
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
        
        def realizar_guardado():
            # Determinar qué imagen guardar
            if radio_img1.isChecked():
                imagen_guardar = self.imagen_actual
                nombre_img = "Imagen 1"
            elif radio_img2.isChecked():
                imagen_guardar = self.imagen_segunda
                nombre_img = "Imagen 2"
            else:
                imagen_guardar = self.imagen_resultado_logico
                nombre_img = "Resultado"
            
            if imagen_guardar is None:
                QMessageBox.warning(self, "Advertencia", "La imagen seleccionada no está disponible")
                return
            
            dialogo.accept()
            
            # Abrir diálogo de guardado
            archivo, _ = QFileDialog.getSaveFileName(
                self, f"Guardar {nombre_img}", "",
                "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp);;TIFF (*.tiff)"
            )
            
            if archivo:
                try:
                    cv2.imwrite(archivo, imagen_guardar)
                    QMessageBox.information(self, "Éxito", "Imagen guardada correctamente")
                    self.info_label.setText(f"Imagen guardada: {archivo.split('/')[-1]}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al guardar:\n{str(e)}")
        
        btn_guardar.clicked.connect(realizar_guardado)
        btn_cancelar.clicked.connect(dialogo.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialogo.exec()
    
    def resetear_imagen(self):
        """Resetear imagen actual a la original"""
        if self.imagen_original_backup is not None:
            self.imagen_actual = self.imagen_original_backup.copy()
            self._mostrar_imagen(self.label_imagen_principal, self.imagen_actual)
            self.info_label.setText("Imagen reseteada a original")
        
        if self.imagen_segunda_backup is not None:
            self.imagen_segunda = self.imagen_segunda_backup.copy()
            self._mostrar_imagen(self.label_segunda, self.imagen_segunda)
        
        # Ocultar panel de resultado lógico
        self.label_resultado_logico.setVisible(False)
        self.imagen_resultado_logico = None
    
    def mostrar_comparacion(self):
        """Mostrar ventana de comparación antes/después"""
        if self.imagen_original_backup is None or self.imagen_actual is None:
            QMessageBox.warning(self, "Advertencia", "Necesitas cargar una imagen primero")
            return
        
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Comparación: Original vs Actual")
        dialogo.resize(1000, 500)
        dialogo.setStyleSheet(f"""
            QDialog {{
                background: {COLOR_FONDO};
            }}
        """)
        
        layout = QHBoxLayout(dialogo)
        layout.setSpacing(20)
        
        # Panel original
        panel_orig = self._crear_panel_comparacion("ORIGINAL", self.imagen_original_backup)
        layout.addWidget(panel_orig, 1)
        
        # Panel actual
        panel_actual = self._crear_panel_comparacion("ACTUAL", self.imagen_actual)
        layout.addWidget(panel_actual, 1)
        
        dialogo.exec()
    
    def _crear_panel_comparacion(self, titulo, imagen):
        """Crea panel para ventana de comparación"""
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        
        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }}
        """)
        panel_layout.addWidget(titulo_label)
        
        imagen_label = QLabel()
        imagen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Convertir imagen
        if len(imagen.shape) == 2:
            h, w = imagen.shape
            q_img = QImage(imagen.data, w, h, w, QImage.Format.Format_Grayscale8)
        else:
            h, w, ch = imagen.shape
            rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            q_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_img)
        scaled = pixmap.scaled(450, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        imagen_label.setPixmap(scaled)
        
        panel_layout.addWidget(imagen_label, 1)
        
        return panel
    
    def cambiar_modo(self, nuevo_modo):
        """Cambiar modo de visualización (color, grises, binaria)"""
        self.modo_actual = nuevo_modo
        self.label_modo.setText(f"Modo:\n{self.modo_actual.upper()}")
        
        # Actualizar imagen principal
        if self.imagen_cargada is not None:
            self.imagen_actual = self.imagen_cargada.get_version(nuevo_modo).copy()
            self.imagen_original_backup = self.imagen_actual.copy()
            self._mostrar_imagen(self.label_imagen_principal, self.imagen_actual)
        
        # Actualizar segunda imagen
        if self.imagen_segunda_cargada is not None:
            self.imagen_segunda = self.imagen_segunda_cargada.get_version(nuevo_modo).copy()
            self.imagen_segunda_backup = self.imagen_segunda.copy()
            self._mostrar_imagen(self.label_segunda, self.imagen_segunda)
        
        self.info_label.setText(f"Modo cambiado a: {nuevo_modo.upper()}")



def main():
    """Funcion principal para ejecutar la aplicacion"""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
