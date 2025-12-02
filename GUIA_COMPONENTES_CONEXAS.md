#  Guía Completa: Análisis de Componentes Conexas

##  ¿Qué son las Componentes Conexas?

Las componentes conexas son **regiones de píxeles conectados** en una imagen binaria. Se utiliza para:
- Contar objetos en una imagen
- Detectar y separar formas
- Analizar estructuras en imágenes médicas, industriales, etc.
- Eliminar ruido pequeño
- Extraer el objeto más grande

---

##  Proceso Completo Paso a Paso

### **PASO 1: Cargar la Imagen**
1. Haz clic en el botón **"Cargar Imagen"** (sección ARCHIVO)
2. Selecciona una imagen desde tu computadora
3. La imagen aparecerá en el panel "IMAGEN 1"

---

### **PASO 2: Convertir a Modo Binario (OBLIGATORIO)**

Las componentes conexas **solo funcionan en imágenes binarias** (blanco y negro, sin grises).

#### Opción A: Usar Segmentación Automática
En la sección **SEGMENTACIÓN**, prueba alguno de estos métodos:
- **"Otsu"** - El más recomendado, calcula automáticamente el mejor umbral
- **"Kapur"** - Basado en entropía, bueno para imágenes complejas
- **"Mín. Histograma"** - Encuentra el valle entre dos picos del histograma
- **"Por Media"** - Simple, usa el promedio de intensidades

**Recomendación:** Comienza con **Otsu**, es el más confiable.

#### Opción B: Cambiar Modo de Visualización
1. En la sección **MODOS**, haz clic en **"Modo Binaria"**
2. Esto convierte automáticamente la imagen a blanco y negro

---

### **PASO 3: Etiquetar Componentes Conexas**

Una vez que tienes la imagen binaria:

1. Ve a la sección **COMPONENTES CONEXAS**
2. Haz clic en **"Etiquetar"**
3. Aparecerá un diálogo con opciones:

   **Conectividad:**
   - **4 (vecinos laterales)**: Solo considera píxeles arriba, abajo, izquierda, derecha
   - **8 (incluye diagonales)**: Considera también los 4 vecinos diagonales
   
    **Recomendación:** Usa **8** para detectar más componentes conectadas

4. Haz clic en **"Aplicar"**

**Resultado:**
- La imagen se colorea automáticamente con colores aleatorios
- Cada color representa una componente conexa diferente
- En la barra inferior verás: "✓ Etiquetado completo: X componente(s)"
- En la consola se imprime información detallada

---

### **PASO 4: Explorar las Componentes (Opciones Disponibles)**

Después de etiquetar, puedes usar estas funciones:

####  **"Colorear Etiquetas"**
- Vuelve a colorear las componentes con una nueva paleta aleatoria
- Útil si los colores se confunden

####  **"Componente Mayor"**
- Extrae solo la componente conexa más grande
- Muestra su área en píxeles
- Útil para eliminar ruido pequeño

####  **"Regiones Numeradas"**
- Dibuja cada región con:
  - Color único
  - Contorno negro grueso
  - Número identificador en el centro
- Perfecto para reportes y análisis visual

####  **"Comparar Segm."**
- Compara la imagen original con las componentes detectadas
- Dibuja fronteras verdes alrededor de cada componente
- Muestra cantidad de componentes en original vs etiquetado

---

##  Ejemplo de Flujo Completo

```
1. Cargar Imagen
   
2. Aplicar Segmentación (Botón "Otsu")
   
3. Etiquetar Componentes (Conectividad 8)
   
4. Ver Regiones Numeradas
  
5. (Opcional) Extraer Componente Mayor
  
6. (Opcional) Comparar Segmentación
  
7. Guardar Resultado
```

