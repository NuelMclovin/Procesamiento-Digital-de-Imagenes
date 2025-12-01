"""
Sección de filtros de restauración.
"""

from PySide6.QtWidgets import (QLabel, QHBoxLayout, QSpinBox, QComboBox, 
                               QDoubleSpinBox, QMessageBox)
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.config import (
    COLOR_ACENTO, COLOR_TEXT_PRIMARY, COLOR_CARD, COLOR_BORDER,
    KERNEL_SIZE_DEFAULT, FILTRO_GAUSSIANO_SIGMA,
    FILTRO_BILATERAL_D, FILTRO_BILATERAL_SIGMA_COLOR, FILTRO_BILATERAL_SIGMA_SPACE
)
from src.funciones.funciones_procesamiento import (
    filtro_promediador, filtro_promediador_pesado, filtro_mediana,
    filtro_moda, filtro_minimo, filtro_maximo, filtro_gaussiano, filtro_bilateral
)


class SeccionFiltros(SeccionBase):
    """Sección para aplicar filtros de restauración."""
    
    def __init__(self, ventana_principal):
        super().__init__("FILTROS", COLOR_ACENTO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de filtros."""
        self.crear_boton("Promediador", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('promediador'))
        
        self.crear_boton("Prom. Pesado", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('promediador_pesado'))
        
        self.crear_boton("Mediana", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('mediana'))
        
        self.crear_boton("Moda", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('moda'))
        
        self.crear_boton("Mínimo", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('minimo'))
        
        self.crear_boton("Máximo", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('maximo'))
        
        self.crear_boton("Gaussiano", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('gaussiano'))
        
        self.crear_boton("Bilateral", COLOR_ACENTO, 
                        lambda: self.mostrar_dialogo_filtro('bilateral'))
    
    def mostrar_dialogo_filtro(self, tipo):
        """Muestra diálogo para aplicar filtros"""
        titulos = {
            'promediador': 'Promediador',
            'promediador_pesado': 'Promediador Pesado',
            'mediana': 'Mediana',
            'moda': 'Moda',
            'minimo': 'Mínimo',
            'maximo': 'Máximo',
            'gaussiano': 'Gaussiano',
            'bilateral': 'Bilateral'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Filtro: {titulos[tipo]}")
        dialogo.agregar_selector_imagen(self.ventana_principal)
        
        # Crear widgets de parámetros según el tipo de filtro
        params = self._crear_parametros_filtro(dialogo, tipo)
        
        def aplicar():
            imagen, label = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                resultado, mensaje = self._aplicar_filtro(imagen, tipo, params)
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.info_label.setText(mensaje)
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error:\n{str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def _crear_parametros_filtro(self, dialogo, tipo):
        """Crea los widgets de parámetros según el tipo de filtro"""
        params = {}
        
        if tipo == 'promediador':
            params['kernel'] = self._crear_selector_kernel(dialogo)
            
        elif tipo == 'promediador_pesado':
            params['n'] = self._crear_spin_n(dialogo)
        
        elif tipo in ['mediana', 'moda', 'minimo', 'maximo']:
            params['kernel'] = self._crear_selector_kernel(dialogo)
            
        elif tipo == 'gaussiano':
            params['kernel'] = self._crear_selector_kernel(dialogo)
            params['sigma'] = self._crear_spin_sigma(dialogo)
            
        elif tipo == 'bilateral':
            params['d'] = self._crear_spin_d(dialogo)
            params['sigma_color'] = self._crear_spin_sigma_color(dialogo)
            params['sigma_space'] = self._crear_spin_sigma_space(dialogo)
        
        return params
    
    def _crear_selector_kernel(self, dialogo):
        """Crea un selector de tamaño de kernel"""
        kernel_layout = QHBoxLayout()
        kernel_label = QLabel("Tamaño kernel (impar):")
        kernel_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        kernel_combo = QComboBox()
        kernel_combo.addItems(['3', '5', '7', '9', '11', '13', '15'])
        kernel_combo.setCurrentText(str(KERNEL_SIZE_DEFAULT))
        kernel_combo.setStyleSheet(f"""
            QComboBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        kernel_layout.addWidget(kernel_label)
        kernel_layout.addWidget(kernel_combo, 1)
        dialogo.layout_principal.addLayout(kernel_layout)
        
        return kernel_combo
    
    def _crear_spin_n(self, dialogo):
        """Crea un spin box para el factor n"""
        n_layout = QHBoxLayout()
        n_label = QLabel("Factor n (normalización):")
        n_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        n_spin = QSpinBox()
        n_spin.setRange(1, 20)
        n_spin.setValue(5)
        n_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        n_layout.addWidget(n_label)
        n_layout.addWidget(n_spin, 1)
        dialogo.layout_principal.addLayout(n_layout)
        
        return n_spin
    
    def _crear_spin_sigma(self, dialogo):
        """Crea un spin box para sigma"""
        sigma_layout = QHBoxLayout()
        sigma_label = QLabel("Sigma:")
        sigma_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        sigma_spin = QDoubleSpinBox()
        sigma_spin.setRange(0.1, 10.0)
        sigma_spin.setSingleStep(0.1)
        sigma_spin.setValue(FILTRO_GAUSSIANO_SIGMA)
        sigma_spin.setDecimals(1)
        sigma_spin.setStyleSheet(f"""
            QDoubleSpinBox {{
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
        
        return sigma_spin
    
    def _crear_spin_d(self, dialogo):
        """Crea un spin box para diámetro del píxel"""
        d_layout = QHBoxLayout()
        d_label = QLabel("Diámetro pixel:")
        d_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        d_spin = QSpinBox()
        d_spin.setRange(1, 20)
        d_spin.setValue(FILTRO_BILATERAL_D)
        d_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        d_layout.addWidget(d_label)
        d_layout.addWidget(d_spin, 1)
        dialogo.layout_principal.addLayout(d_layout)
        
        return d_spin
    
    def _crear_spin_sigma_color(self, dialogo):
        """Crea un spin box para sigma color"""
        sc_layout = QHBoxLayout()
        sc_label = QLabel("Sigma Color:")
        sc_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        sc_spin = QSpinBox()
        sc_spin.setRange(1, 200)
        sc_spin.setValue(FILTRO_BILATERAL_SIGMA_COLOR)
        sc_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        sc_layout.addWidget(sc_label)
        sc_layout.addWidget(sc_spin, 1)
        dialogo.layout_principal.addLayout(sc_layout)
        
        return sc_spin
    
    def _crear_spin_sigma_space(self, dialogo):
        """Crea un spin box para sigma espacio"""
        ss_layout = QHBoxLayout()
        ss_label = QLabel("Sigma Espacio:")
        ss_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: bold;")
        
        ss_spin = QSpinBox()
        ss_spin.setRange(1, 200)
        ss_spin.setValue(FILTRO_BILATERAL_SIGMA_SPACE)
        ss_spin.setStyleSheet(f"""
            QSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        
        ss_layout.addWidget(ss_label)
        ss_layout.addWidget(ss_spin, 1)
        dialogo.layout_principal.addLayout(ss_layout)
        
        return ss_spin
    
    def _aplicar_filtro(self, imagen, tipo, params):
        """Aplica el filtro correspondiente y retorna el resultado y mensaje"""
        if tipo == 'promediador':
            kernel_size = int(params['kernel'].currentText())
            resultado = filtro_promediador(imagen, kernel_size)
            mensaje = f"Filtro promediador aplicado (kernel: {kernel_size})"
            
        elif tipo == 'promediador_pesado':
            n = params['n'].value()
            resultado = filtro_promediador_pesado(imagen, n)
            mensaje = f"Filtro promediador pesado aplicado (n: {n})"
            
        elif tipo == 'mediana':
            kernel_size = int(params['kernel'].currentText())
            resultado = filtro_mediana(imagen, kernel_size)
            mensaje = f"Filtro mediana aplicado (kernel: {kernel_size})"
            
        elif tipo == 'moda':
            kernel_size = int(params['kernel'].currentText())
            resultado = filtro_moda(imagen, kernel_size)
            mensaje = f"Filtro moda aplicado (kernel: {kernel_size})"
            
        elif tipo == 'minimo':
            kernel_size = int(params['kernel'].currentText())
            resultado = filtro_minimo(imagen, kernel_size)
            mensaje = f"Filtro mínimo aplicado (kernel: {kernel_size})"
            
        elif tipo == 'maximo':
            kernel_size = int(params['kernel'].currentText())
            resultado = filtro_maximo(imagen, kernel_size)
            mensaje = f"Filtro máximo aplicado (kernel: {kernel_size})"
            
        elif tipo == 'gaussiano':
            kernel_size = int(params['kernel'].currentText())
            sigma = params['sigma'].value()
            resultado = filtro_gaussiano(imagen, kernel_size, sigma)
            mensaje = f"Filtro gaussiano aplicado (kernel: {kernel_size}, σ: {sigma})"
            
        else:  # bilateral
            d = params['d'].value()
            sigma_color = params['sigma_color'].value()
            sigma_space = params['sigma_space'].value()
            resultado = filtro_bilateral(imagen, d, sigma_color, sigma_space)
            mensaje = f"Filtro bilateral aplicado (d:{d}, σC:{sigma_color}, σS:{sigma_space})"
        
        return resultado, mensaje
