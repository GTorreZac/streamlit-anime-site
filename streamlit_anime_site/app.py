import streamlit as st
import pandas as pd
import json
import os
import base64
from pathlib import Path
from streamlit.components.v1 import html as st_html

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="MAL Anime Analytics",
    page_icon="🍙",
    layout="wide"
)

BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
FIG_PATH = BASE_PATH / "figures"
HTML_PATH = BASE_PATH / "html"
ASSETS_PATH = BASE_PATH / "assets"

# =========================
# ESTILOS CUSTOM (OTAKU)
# =========================
anime_css = """
<style>
/* Fondo general */
.stApp {
    background: radial-gradient(circle at top, #0f172a 0, #020617 45%, #020617 100%);
    color: #e5e7eb;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Barra lateral */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #111827 45%, #020617 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.35);
}

/* Títulos principales */
h1, h2, h3 {
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    letter-spacing: 0.03em;
}

/* Cards */
.anime-card {
    background: rgba(15,23,42,0.9);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow: 0 18px 45px rgba(15,23,42,0.85);
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.15rem 0.65rem;
    border-radius: 999px;
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    background: rgba(236,72,153,0.12);
    color: #f9a8d4;
}

/* Métricas */
.metric-kpi {
    font-size: 1.9rem;
    font-weight: 700;
    color: #e5e7eb;
}
.metric-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #9ca3af;
}

/* Separadores suaves */
hr {
    border: none;
    border-top: 1px solid rgba(148,163,184,0.35);
    margin: 1.4rem 0 0.8rem 0;
}

/* Links */
a {
    color: #22d3ee;
}
a:hover {
    color: #f97316;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #ec4899, #f97316);
    color: #0b1120;
    border-radius: 999px;
    border: none;
    padding: 0.45rem 1.1rem;
    font-weight: 600;
}
.stButton > button:hover {
    filter: brightness(1.1);
}

/* Header Hero con imagen de fondo */
.hero-header-container {
    position: relative;
    width: 100%;
    height: 400px;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-image-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
}

.hero-bg-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        to bottom,
        rgba(2, 6, 23, 0.75) 0%,
        rgba(2, 6, 23, 0.85) 50%,
        rgba(2, 6, 23, 0.9) 100%
    );
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 2rem;
    max-width: 900px;
}

.hero-content h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: #ffffff;
    text-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);
}

.hero-content p {
    font-size: 1.2rem;
    color: #e5e7eb;
    line-height: 1.6;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
}

.hero-badge-custom {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    background: rgba(236, 72, 153, 0.25);
    color: #fda4af;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
    border: 1px solid rgba(236, 72, 153, 0.3);
}

/* Scrollbar horizontal para anime cards */
.anime-scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 1.2rem;
    padding: 1.5rem 0.5rem;
    margin: 1.5rem 0;
    scroll-behavior: smooth;
}

.anime-scroll-container::-webkit-scrollbar {
    height: 10px;
}

.anime-scroll-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
}

.anime-scroll-container::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ec4899, #f97316);
    border-radius: 10px;
}

.anime-scroll-container::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #f97316, #ec4899);
}

.anime-card-scroll {
    min-width: 200px;
    max-width: 200px;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.35);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

.anime-card-scroll:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 28px rgba(236, 72, 153, 0.4);
    border-color: rgba(236, 72, 153, 0.6);
}

.anime-card-scroll img {
    width: 100%;
    height: 280px;
    object-fit: cover;
    display: block;
}

.anime-card-info {
    padding: 0.9rem;
}

.anime-card-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 0.4rem;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.6em;
}

.anime-card-score {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: #22d3ee;
    font-weight: 600;
}

.anime-card-rank {
    position: absolute;
    top: 0.6rem;
    left: 0.6rem;
    background: rgba(236, 72, 153, 0.95);
    color: #fff;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    z-index: 1;
}
</style>
"""
st.markdown(anime_css, unsafe_allow_html=True)

# =========================
# FUNCIONES AUXILIARES
# =========================
@st.cache_data
def load_dataset():
    df = pd.read_csv(DATA_PATH / "mal_anime.csv")
    return df

@st.cache_data
def load_summary():
    summary_file = DATA_PATH / "resumen_analisis.json"
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def show_figure(filename: str, title: str, description: str, explanation: str):
    st.subheader(title)
    st.image(str(FIG_PATH / filename), use_container_width=True)
    st.markdown(description)
    st.markdown("#### 📊 ¿Qué representa?")
    st.markdown(explanation)

def embed_html_chart(filename: str, height: int = 600):
    file_path = HTML_PATH / filename
    if not file_path.exists():
        st.warning(f"No se encontró el archivo `{filename}` en la carpeta `html/`.")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    st_html(content, height=height, scrolling=True)

def create_anime_scrollbar(dataframe, top_n=20):
    """Crea un scrollbar horizontal con las imágenes de los top animes usando st.components.html"""
    top_animes = dataframe.nlargest(top_n, 'Score')[['title', 'Score', 'image']].reset_index(drop=True)
    
    # Crear HTML completo
    scroll_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: "Inter", system-ui, -apple-system, sans-serif;
            }
            .scroll-container {
                overflow-x: auto;
                white-space: nowrap;
                padding: 20px 0;
                -webkit-overflow-scrolling: touch;
            }
            .scroll-container::-webkit-scrollbar {
                height: 10px;
            }
            .scroll-container::-webkit-scrollbar-track {
                background: rgba(15, 23, 42, 0.5);
                border-radius: 10px;
            }
            .scroll-container::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #ec4899, #f97316);
                border-radius: 10px;
            }
            .scroll-container::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #f97316, #ec4899);
            }
            .anime-card {
                display: inline-block;
                margin-right: 20px;
                width: 200px;
                vertical-align: top;
            }
            .card-inner {
                background: rgba(15, 23, 42, 0.9);
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid rgba(148, 163, 184, 0.35);
                position: relative;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .card-inner:hover {
                transform: translateY(-8px);
                box-shadow: 0 12px 28px rgba(236, 72, 153, 0.4);
                border-color: rgba(236, 72, 153, 0.6);
            }
            .rank-badge {
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(236, 72, 153, 0.95);
                color: #fff;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 700;
                z-index: 1;
            }
            .anime-img {
                width: 200px;
                height: 280px;
                object-fit: cover;
                display: block;
            }
            .card-info {
                padding: 12px;
            }
            .card-title {
                font-size: 14px;
                font-weight: 600;
                color: #e5e7eb;
                margin-bottom: 6px;
                line-height: 1.3;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                min-height: 36px;
                white-space: normal;
            }
            .card-score {
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 14px;
                color: #22d3ee;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="scroll-container">
    """
    
    for idx, row in top_animes.iterrows():
        rank = idx + 1
        title = row['title'].replace("'", "\\'").replace('"', '&quot;')
        score = row['Score']
        image_url = row['image'] if pd.notna(row['image']) else "https://via.placeholder.com/200x280?text=No+Image"
        
        scroll_html += f"""
            <div class="anime-card">
                <div class="card-inner">
                    <div class="rank-badge">#{rank}</div>
                    <img src="{image_url}" class="anime-img" 
                         onerror="this.src='https://via.placeholder.com/200x280?text=No+Image'">
                    <div class="card-info">
                        <div class="card-title">{title}</div>
                        <div class="card-score">⭐ {score:.2f}</div>
                    </div>
                </div>
            </div>
        """
    
    scroll_html += """
        </div>
    </body>
    </html>
    """
    
    st_html(scroll_html, height=400, scrolling=False)

# =========================
# DATOS
# =========================
df = load_dataset()
summary = load_summary()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.image(str(ASSETS_PATH / "anime_logo.png"), use_container_width=True)
    st.markdown("### MAL Anime Analytics")
    st.caption("Exploración completa del dataset de **MyAnimeList** con estilo otaku ✨")

    seccion = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "📊 Exploración general",
            "🎭 Géneros & Estudios",
            "📈 Correlaciones & Seaborn",
            "🧩 Dashboard Matplotlib",
            "🤖 Machine Learning",
            "🎮 Sistema de recomendación",
            "🎬 Animaciones"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("**Autor:** Gabriel Torres Zacarias  \n**Dataset:** 19,931 animes de MyAnimeList")

# =========================
# HEADER CON HERO
# =========================
hero_image_path = ASSETS_PATH / "hero_header.png"
if hero_image_path.exists():
    # Crear contenedor para el hero con imagen de alta calidad
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <div style="position: relative; border-radius: 16px; overflow: hidden;">
    """, unsafe_allow_html=True)
    
    # Imagen de fondo con st.image para mejor calidad
    st.image(str(hero_image_path), use_container_width=True)
    
    # Overlay y contenido sobre la imagen
    st.markdown("""
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                    background: linear-gradient(to bottom, rgba(2, 6, 23, 0.75) 0%, rgba(2, 6, 23, 0.85) 50%, rgba(2, 6, 23, 0.9) 100%);
                    display: flex; align-items: center; justify-content: center;
                    margin-top: -400px; height: 400px;">
            <div style="text-align: center; padding: 2rem; max-width: 900px; z-index: 2;">
                <div class="hero-badge-custom">Proyecto Final • Análisis de Datos</div>
                <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; color: #ffffff; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);">
                    🍙 Anime Data Hub
                </h1>
                <p style="font-size: 1.2rem; color: #e5e7eb; line-height: 1.6; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);">
                    Dashboard interactivo del universo de <strong>MyAnimeList</strong>: scores, géneros, estudios, 
                    tendencias históricas y un modelo de <em>machine learning</em> para entender qué hace grande a un anime.
                </p>
            </div>
        </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback al diseño anterior si no existe la imagen
    hero_cols = st.columns([2.8, 1.2])
    
    with hero_cols[0]:
        st.markdown('<div class="badge">Proyecto Final • Análisis de Datos</div>', unsafe_allow_html=True)
        st.markdown("# 🍙 Anime Data Hub")
        st.markdown(
            "Dashboard interactivo del universo de **MyAnimeList**: scores, géneros, estudios, "
            "tendencias históricas y un modelo de *machine learning* para entender qué hace grande a un anime."
        )
    with hero_cols[1]:
        if (ASSETS_PATH / "hero_city.jpg").exists():
            st.image(str(ASSETS_PATH / "hero_city.jpg"), use_container_width=True)

st.markdown("---")

# =========================
# SECCIONES
# =========================
if seccion == "🏠 Inicio":
    total_animes = summary.get("dataset", {}).get("total_animes", len(df))
    score_mean = summary.get("dataset", {}).get("score_mean", float(df["Score"].mean()))
    year_range = summary.get("dataset", {}).get("year_range", "")
    total_genres = summary.get("dataset", {}).get("total_genres", None)
    total_studios = summary.get("dataset", {}).get("total_studios", None)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-label">ANIMES REGISTRADOS</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-kpi">{total_animes:,.0f}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-label">SCORE PROMEDIO</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-kpi">{score_mean:.2f}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-label">RANGO DE AÑOS</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-kpi">{year_range}</div>', unsafe_allow_html=True)
    with c4:
        if total_genres and total_studios:
            st.markdown('<div class="metric-label">GÉNEROS / ESTUDIOS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-kpi">{total_genres} / {total_studios}</div>', unsafe_allow_html=True)

    st.markdown("### Vista rápida del DataFrame")
    st.dataframe(df.head(20))

    st.info(
        "En esta página se muestran ejemplos de **Pandas (Series y DataFrames)**, "
        "así como un resumen estadístico general del dataset utilizado durante el proyecto."
    )

elif seccion == "📊 Exploración general":
    col1, col2 = st.columns(2)
    with col1:
        show_figure(
            "01_distribucion_scores.png",
            "Distribución de Scores de Anime",
            "Histograma + boxplot que muestran cómo se concentran los scores alrededor de ~6.5.",
            """Distribución casi normal centrada en 6.5-7.0. La media (roja) y mediana (verde) coinciden, mostrando simetría perfecta."""
        )
    with col2:
        show_figure(
            "02_top20_scores.png",
            "Top 20 Animes por Score",
            "Gráfico de barras horizontales que resalta las producciones mejor calificadas del dataset.",
            """Los mejores 20 animes tienen scores entre 8.9-9.3. Lideran "Sousou no Frieren", "Fullmetal Alchemist: Brotherhood" y "Steins;Gate"."""
        )

    st.markdown("---")
    st.markdown("### 🏆 Top 20 Animes - Galería Interactiva")
    st.markdown("Desliza horizontalmente para explorar los mejores animes según MyAnimeList")
    create_anime_scrollbar(df, top_n=20)

    st.markdown("---")
    col3 = st.columns(1)[0]
    with col3:
        show_figure(
            "03_distribucion_tipo.png",
            "Distribución por Tipo de Anime",
            "Gráfico pastel + barras que muestran cómo se reparte la producción entre TV, OVA, ONA, películas y especiales.",
            """**TV** domina con 50%+ de producciones, seguido por **OVA**, **Movies**, **Specials** y **ONA**. La televisión sigue siendo el medio principal."""
        )

    st.markdown("---")
    show_figure(
        "04_animes_por_año.png",
        "Evolución de Animes Lanzados por Año",
        "Gráfico de área + línea que ilustra el crecimiento histórico de la industria del anime desde 1960.",
        """Crecimiento exponencial desde 1960. Los años 2015-2020 muestran el pico con 400-500 animes anuales por el auge del streaming."""
    )

elif seccion == "🎭 Géneros & Estudios":
    col1, col2 = st.columns(2)
    with col1:
        show_figure(
            "06_top_generos.png",
            "Top 15 Géneros Más Populares",
            "Barras horizontales que muestran qué géneros dominan el catálogo de MyAnimeList.",
            """**Comedy** lidera con 6,800+ apariciones, seguido por **Fantasy** y **Action**. Muchos animes combinan múltiples géneros."""
        )
    with col2:
        show_figure(
            "07_top_estudios.png",
            "Top 15 Estudios con Más Producciones",
            "Comparación de los estudios más prolíficos en la industria del anime.",
            """**Toei Animation** (Dragon Ball, One Piece), **Sunrise** (Gundam) y **J.C.Staff** lideran en producción. Cantidad ≠ calidad."""
        )

    st.markdown("---")
    show_figure(
        "08_distribucion_temporada.png",
        "Distribución por Temporada",
        "Combinación de gráfico pastel y barras que muestra en qué temporada se estrenan más animes.",
        """**Spring** lidera con ~30% de estrenos. La distribución refleja el calendario escolar japonés que inicia en abril."""
    )

elif seccion == "📈 Correlaciones & Seaborn":
    show_figure(
        "05_correlaciones.png",
        "Matriz de Correlación (Heatmap + Mapa de píxeles)",
        "Dos representaciones de la misma matriz de correlación usando diferentes técnicas de visualización.",
        """**Members vs Favorites (0.83)** tienen correlación muy fuerte. **Score vs Members (0.47)** moderada: popularidad no siempre implica calidad."""
    )

    st.markdown("### Gráficas avanzadas con Seaborn")

    c1, c2 = st.columns(2)
    with c1:
        show_figure(
            "seaborn_pairplot.png",
            "Pairplot de Variables Clave",
            "Relaciones bivariadas y distribuciones univariadas entre Score, Members y Favorites.",
            """Matriz de combinaciones entre Score, Members y Favorites. Los scatter plots muestran que mejores scores correlacionan con popularidad."""
        )
    with c2:
        show_figure(
            "seaborn_jointplot.png",
            "Jointplot: Members vs Score",
            "Análisis detallado de la relación entre popularidad (Members) y calificación (Score).",
            """Correlación ~0.47 entre Members y Score. Eje X en escala logarítmica. Identifica outliers: éxitos mainstream vs joyas ocultas."""
        )

    show_figure(
        "seaborn_violinplots.png",
        "Violin plots: Score por Tipo y Temporada",
        "Comparación de distribuciones de calificaciones según el formato y la temporada de estreno.",
        """**Movies** tienen scores más altos que **TV**. Las cuatro temporadas (Spring, Fall, etc.) muestran distribuciones similares centradas en 6.5-7.0."""
    )

elif seccion == "🧩 Dashboard Matplotlib":
    show_figure(
        "dashboard_completo.png",
        "Dashboard Completo: Análisis de MyAnimeList",
        "Dashboard integral con 10 visualizaciones diferentes en una sola figura.",
        """Composición de 10 gráficos diferentes (scatter, pie, heatmap, boxplot, etc.) en una sola figura. Ideal para reportes ejecutivos."""
    )

elif seccion == "🤖 Machine Learning":
    show_figure(
        "ml_prediccion_scores.png",
        "Modelo de Predicción de Scores (Random Forest)",
        "Modelo de machine learning que predice la calificación de un anime basándose en sus características.",
        """**Random Forest** predice Score con R² ~0.65-0.75. **Members** y **Favorites** son los predictores más importantes. Popularidad indica calidad."""
    )

    if summary.get("correlations"):
        st.markdown("#### Correlaciones clave utilizadas en el análisis")
        corr = summary["correlations"]
        st.write(corr)

elif seccion == "🎮 Sistema de recomendación":
    st.markdown("### Sistema de recomendación por género")
    st.markdown(
        "Selecciona un género y descubre los 10 animes mejor calificados de esa categoría. "
        "Cada barra muestra la portada oficial del anime."
    )
    
    # Extraer todos los géneros únicos
    all_genres = set()
    for genres_str in df['Genres'].dropna():
        if isinstance(genres_str, str):
            all_genres.update([g.strip() for g in genres_str.split(',')])
    all_genres = sorted(list(all_genres))
    
    # Selector de género
    selected_genre = st.selectbox("📚 Selecciona un género:", all_genres, index=0)
    
    # Filtrar animes por género
    genre_df = df[df['Genres'].str.contains(selected_genre, na=False, case=False)].copy()
    top_genre = genre_df.nlargest(10, 'Score')[['title', 'Score', 'image', 'Genres']].reset_index(drop=True)
    
    if len(top_genre) > 0:
        st.markdown(f"#### 🏆 Top 10 animes de **{selected_genre}**")
        
        # Crear barras horizontales con imágenes
        for idx, row in top_genre.iterrows():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Mostrar imagen del anime
                if pd.notna(row['image']) and row['image'].startswith('http'):
                    try:
                        st.image(row['image'], width=100)
                    except:
                        st.markdown("🖼️")
                else:
                    st.markdown("🖼️")
            
            with col2:
                # Mostrar título, score y barra
                st.markdown(f"**{idx + 1}. {row['title']}**")
                st.markdown(f"⭐ Score: **{row['Score']:.2f}**")
                
                # Barra de progreso basada en el score (normalizado 0-10)
                progress_value = row['Score'] / 10.0
                st.progress(progress_value)
                
                # Géneros
                genres_list = row['Genres'].split(', ') if pd.notna(row['Genres']) else []
                if len(genres_list) > 0:
                    st.caption(f"🏷️ {', '.join(genres_list[:3])}")
            
            st.markdown("---")
    else:
        st.warning(f"No se encontraron animes para el género **{selected_genre}**")

elif seccion == "🎬 Animaciones":
    st.markdown("### Animaciones estilo *race bar chart* y evolución temporal")
    st.markdown(
        "A continuación se muestran las animaciones generadas con Plotly: "
        "evolución de géneros, scores promedio y un scatter dinámico de `Members` vs `Score`."
    )

    st.markdown("#### Race chart de géneros")
    embed_html_chart("race_chart_generos.html", height=600)

    st.markdown("---")
    st.markdown("#### Evolución de scores promedio por género")
    embed_html_chart("evolucion_scores_generos.html", height=600)

    st.markdown("---")
    st.markdown("#### Scatter evolutivo: Members vs Score por año")
    embed_html_chart("scatter_evolutivo.html", height=600)