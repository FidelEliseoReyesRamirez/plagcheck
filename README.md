# PlagCheck 🌐🔍
### Detector Inteligente de Plagio en la Web mediante Web Scraping en Tiempo Real

**PlagCheck** es una aplicación interactiva desarrollada en Python y Streamlit que analiza documentos académicos, tesis y textos contra internet en tiempo real para identificar posibles instancias de plagio, extrayendo las fuentes y los enlaces web exactos de donde proviene la información.

A diferencia de los detectores convencionales que fragmentan el texto en oraciones aisladas o títulos sueltos, **PlagCheck** reconstruye y analiza **párrafos conceptuales completos**, permitiendo evaluar desde muestras representativas hasta **el proyecto completo** de cientos de páginas.

---

## 🚀 Características Principales

* **Búsqueda Web en Tiempo Real (Web Scraping):** Utiliza el motor de indexación web `ddgs` (DuckDuckGo Search) para buscar coincidencias en internet sin necesidad de pagar por APIs privadas ni depender de servicios cerrados.
* **Análisis por Párrafos Coherentes:** Algoritmo que filtra índices, números de página y encabezados aislados para centrarse en párrafos sustanciales (35 a 80 palabras con sentido completo).
* **Compatibilidad Multiformato:**
  * Documentos PDF (`.pdf`) mediante extracción precisa de texto con `pdfplumber`.
  * Documentos de Microsoft Word (`.docx`) mediante `python-docx`.
  * Archivos de texto plano (`.txt`) o pegado directo de texto en la interfaz.
* **Escalabilidad y Alcance Flexible:**
  * ⚡ **Muestra Rápida:** 15 párrafos.
  * 🚀 **Revisión Estándar:** 35 párrafos.
  * 🔬 **Revisión Profunda:** 70 párrafos.
  * 🌐 **TODO EL PROYECTO COMPLETO:** Analiza todos los párrafos del documento de principio a fin.
  * ⚙️ **Modo Personalizado:** Selección manual de la cantidad deseada.
* **Visualización Dinámica:** Barra de progreso interactiva de 0% a 100%, mensajes de estado en vivo, tarjetas desplegables con las coincidencias, porcentaje de similitud y enlaces directos a las páginas web detectadas.
* **Exportación de Reportes:** Descarga de los resultados del análisis en formato CSV para su posterior revisión o archivo.

---

## 🛠️ Tecnologías y Librerías Utilizadas

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Frontend / UI** | [Streamlit](https://streamlit.io/) | Interfaz gráfica web interactiva, moderna y reactiva. |
| **Web Scraping** | [DDGS](https://github.com/deedy5/duckduckgo_search) | Consultas concurrentes en la web sin bloqueo de antibots. |
| **Extracción de PDF** | [pdfplumber](https://github.com/jsvine/pdfplumber) | Extracción fiel de texto en documentos y tesis complejas. |
| **Extracción de Word** | [python-docx](https://python-docx.readthedocs.io/) | Lectura de párrafos en archivos `.docx`. |
| **Manejo de Datos** | [pandas](https://pandas.pydata.org/) | Procesamiento tabular y exportación de reportes. |

---

## 📋 Requisitos Previos

* **Python 3.10** o superior instalado en el sistema.
* Conexión a internet activa (para el scraping en tiempo real).
* Gestor de paquetes `pip` y Git.

---

## 💻 Guía de Instalación y Ejecución

### 1. Clonar el repositorio
Abre tu terminal (PowerShell o CMD en Windows, o Terminal en Linux/macOS) y clona este repositorio:

```bash
git clone https://github.com/FidelEliseoReyesRamirez/plagcheck.git
cd plagcheck
```

### 2. (Opcional) Crear un entorno virtual
Recomendado para mantener las dependencias aisladas:

```bash
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# En Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
Instala los paquetes necesarios con un solo comando:

```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
Ejecuta la interfaz web con Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado en:
`http://localhost:8501`

---

## 📖 Modo de Uso

1. **Cargar el documento o texto:**
   * **Pestaña `📁 Subir Archivo`:** Arrastra tu documento `.pdf`, `.docx` o `.txt`. La aplicación detectará automáticamente el número de palabras y párrafos estructurados.
   * **Pestaña `✍️ Pegar Texto / Párrafo`:** Pega directamente fragmentos de texto copiados de internet para comprobarlos inmediatamente.
2. **Seleccionar el alcance:**
   * Elige entre una muestra rápida, profunda o la opción **"TODO EL PROYECTO COMPLETO"** para revisar todo el documento.
3. **Escanear en la Web:**
   * Haz clic en el botón **`🚀 Iniciar Escaneo de Párrafos en la Web`**.
   * Observa la barra de progreso en vivo mientras se consulta la web en tiempo real.
4. **Revisar los resultados:**
   * Consulta el porcentaje global de plagio estimado.
   * Revisa las tarjetas desplegables para contrastar el párrafo de tu documento frente al fragmento y la URL directa del sitio web.
   * Haz clic en **`📥 Descargar Reporte de Plagio (CSV)`** si deseas guardar los resultados.

---

## 👨‍💻 Créditos y Reconocimientos

* **Autor:** Fidel Eliseo Reyes Ramírez
* **Proyecto:** `plagcheck`
* **Inspiración y Reconocimiento Open Source:**
  * Comunidad de [Streamlit](https://github.com/streamlit/streamlit) por la plataforma de visualización.
  * Proyecto [duckduckgo_search (DDGS)](https://github.com/deedy5/duckduckgo_search) por la infraestructura de consulta web pública.
  * Comunidad de [pdfplumber](https://github.com/jsvine/pdfplumber) por el motor de extracción de documentos académicos.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).
