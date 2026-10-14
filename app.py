import streamlit as st
import re
import os
import pandas as pd
from ddgs import DDGS
import pdfplumber
from docx import Document

st.set_page_config(
    page_title="Detector de Plagio por Párrafos (Web)",
    page_icon="📑",
    layout="wide"
)

# Estilos visuales
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .plag-card {
        border-left: 5px solid #d32f2f;
        background-color: #fff5f5;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(file_bytes) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages_text)

def extract_text_from_docx(file_bytes):
    doc = Document(file_bytes)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def extract_coherent_paragraphs(text):
    """
    Reconstruye párrafos reales y coherentes (evitando títulos sueltos, 
    números de página, índices o líneas cortadas por el salto de página del PDF).
    """
    # 1. Unificar saltos de línea de renglón simples
    text_unwrapped = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    
    # 2. Dividir por oraciones respetando puntuación
    raw_sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])', text_unwrapped)
    
    paragraphs = []
    current_chunk = []
    current_word_count = 0
    
    for s in raw_sentences:
        s_clean = " ".join(s.split())
        words = s_clean.split()
        if not words:
            continue
            
        # Descartar líneas que sean índices con puntos suspensivos o números de página
        if s_clean.count('...') > 2 or s_clean.count('. . .') > 2:
            continue
            
        # Descartar encabezados cortos que no forman parte de un párrafo
        if len(words) < 5 and not s_clean.endswith('.'):
            continue
            
        current_chunk.append(s_clean)
        current_word_count += len(words)
        
        # Agrupar en párrafos coherentes de 35 a 80 palabras
        if current_word_count >= 35:
            full_para = " ".join(current_chunk)
            paragraphs.append(full_para)
            current_chunk = []
            current_word_count = 0
            
    if current_chunk and current_word_count >= 20:
        paragraphs.append(" ".join(current_chunk))
        
    return paragraphs

def create_search_query_from_paragraph(paragraph):
    """
    Extrae la frase más distintiva y conceptual del párrafo para la búsqueda web.
    """
    words = paragraph.split()
    # Si el párrafo tiene varias oraciones, toma la primera o segunda oración completa
    sentences = re.split(r'[.!?]+', paragraph)
    informative = [s.strip() for s in sentences if len(s.strip().split()) >= 8]
    
    if informative:
        target_words = informative[0].split()
        return " ".join(target_words[:14])
    else:
        return " ".join(words[:14])

def search_web_for_paragraph(paragraph):
    query = create_search_query_from_paragraph(paragraph)
    if not query or len(query.split()) < 5:
        return None
        
    try:
        results = list(DDGS().text(query, max_results=3))
        for r in results:
            url = r.get('href', '')
            title = r.get('title', '')
            snippet = r.get('body', '')
            if url and 'youtube' not in url.lower():
                # Comparar vocabulario del párrafo completo con el resultado web
                words_p = set(re.findall(r'\b\w{3,}\b', paragraph.lower()))
                words_w = set(re.findall(r'\b\w{3,}\b', (title + " " + snippet).lower()))
                
                if words_p:
                    overlap = len(words_p & words_w) / len(words_p)
                    # Umbral para párrafos: 30% o más de coincidencia léxica directa
                    if overlap >= 0.30:
                        return {
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'similarity': overlap,
                            'query_used': query
                        }
    except Exception:
        pass
    return None

st.title("🌐 Detector de Plagio Web por Párrafos Completos")
st.write("Analiza bloques de texto y párrafos completos de tu proyecto contra la web para identificar contenido copiado.")

tab1, tab2 = st.tabs(["📁 Subir Archivo (PDF, Word, TXT)", "✍️ Pegar Texto / Párrafo"])

input_text = ""

with tab1:
    uploaded_file = st.file_uploader("Sube tu archivo PDF, Word (.docx) o TXT", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        try:
            with st.spinner("Extrayendo texto del documento..."):
                if uploaded_file.name.endswith(".pdf"):
                    input_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".docx"):
                    input_text = extract_text_from_docx(uploaded_file)
                else:
                    input_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            st.success(f"✅ Documento cargado: **{len(input_text.split())} palabras totales**.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

with tab2:
    pasted_text = st.text_area(
        "O pega aquí directamente párrafos de internet o de tu documento:",
        height=180,
        placeholder="Pega uno o más párrafos completos aquí..."
    )
    if pasted_text:
        input_text = pasted_text

if input_text.strip():
    paragraphs = extract_coherent_paragraphs(input_text)
    total_paras = len(paragraphs)
    
    st.info(f"📄 Se detectaron **{total_paras} párrafos estructurados** en el documento.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio(
            "Alcance del análisis en la web:",
            [
                f"⚡ Muestra Rápida (15 párrafos)",
                f"🚀 Revisión Estándar (35 párrafos)",
                f"🔬 Revisión Profunda (70 párrafos)",
                f"🌐 TODO EL PROYECTO COMPLETO ({total_paras} párrafos)",
                f"⚙️ Personalizado (Elegir cantidad manual)"
            ],
            index=0
        )
    with col2:
        if "Personalizado" in mode:
            num_to_check = st.number_input("Número de párrafos a analizar:", min_value=1, max_value=max(1, total_paras), value=min(25, total_paras))
        elif "TODO EL PROYECTO" in mode:
            num_to_check = total_paras
        elif "Profunda" in mode:
            num_to_check = min(70, total_paras)
        elif "Estándar" in mode:
            num_to_check = min(35, total_paras)
        else:
            num_to_check = min(15, total_paras)

    if st.button("🚀 Iniciar Escaneo de Párrafos en la Web", type="primary"):
        if total_paras == 0:
            st.warning("No se encontraron párrafos con suficiente longitud (mínimo 25 palabras).")
        else:
            step = max(1, total_paras // num_to_check)
            selected = [paragraphs[i] for i in range(0, total_paras, step)][:num_to_check]
            
            st.write(f"### 🔍 Verificando {len(selected)} párrafos en internet...")
            
            progress_bar = st.progress(0)
            status_box = st.empty()
            
            matches = []
            
            for idx, para in enumerate(selected):
                percent = int(((idx + 1) / len(selected)) * 100)
                progress_bar.progress(percent)
                
                short_para = (para[:70] + "...") if len(para) > 70 else para
                status_box.info(f"⏳ **Párrafo {idx + 1} de {len(selected)} ({percent}%):** _{short_para}_")
                
                match = search_web_for_paragraph(para)
                if match:
                    matches.append({
                        'paragraph': para,
                        'title': match['title'],
                        'url': match['url'],
                        'snippet': match['snippet'],
                        'similarity': match['similarity']
                    })
            
            progress_bar.progress(100)
            status_box.empty()
            
            plag_rate = (len(matches) / len(selected)) * 100
            
            st.divider()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Párrafos Analizados", len(selected))
            m2.metric("Párrafos Coincidentes en la Web", len(matches))
            m3.metric("Nivel de Plagio Estimado", f"{plag_rate:.1f}%")
            
            if plag_rate >= 50:
                st.error(f"🚨 **ALTO NIVEL DE PLAGIO:** El {plag_rate:.1f}% de los párrafos analizados tienen coincidencias directas en la web.")
            elif plag_rate > 0:
                st.warning(f"⚠️ **SIMILITUD DETECTADA:** Se detectaron coincidencias web en el {plag_rate:.1f}% de los párrafos.")
            else:
                st.success("✅ **ORIGINAL:** No se detectó plagio en la web para los párrafos analizados.")
                
            if matches:
                st.subheader(f"📌 Detalle de Párrafos Coincidentes ({len(matches)} encontrados):")
                for i, m in enumerate(matches, 1):
                    with st.expander(f"🔴 Párrafo #{i} — {m['title']} ({m['similarity']*100:.0f}% de coincidencia)", expanded=True):
                        st.markdown("**📄 Párrafo en tu documento:**")
                        st.info(m['paragraph'])
                        st.markdown(f"**🌐 Fuente encontrada en la web:** [{m['title']}]({m['url']})")
                        st.markdown(f"**🔗 Enlace directo:** `{m['url']}`")
                        st.markdown("**🔍 Texto extraído del sitio web:**")
                        st.write(m['snippet'])
                        
                # Opción para descargar reporte
                report_df = pd.DataFrame(matches)[['title', 'url', 'similarity', 'paragraph', 'snippet']]
                csv = report_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar Reporte de Plagio (CSV)",
                    data=csv,
                    file_name="reporte_plagio_web.csv",
                    mime="text/csv"
                )
