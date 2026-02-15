import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
from datetime import datetime
import pytz
import time

# ============================================
# CONFIGURATION PAGE
# ============================================
st.set_page_config(
    page_title="Météo Maroc • Dashboard Premium",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# INITIALISATION SESSION STATE
# ============================================
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now(pytz.timezone('Africa/Casablanca'))

# Installation et import de streamlit-autorefresh
try:
    from streamlit_autorefresh import st_autorefresh
    # Auto-refresh toutes les 60 secondes (60000ms) pour mettre à jour l'heure actuelle
    count = st_autorefresh(interval=60000, limit=None, key="fizzbuzzcounter")
except ImportError:
    # Si streamlit-autorefresh n'est pas installé, continuer sans auto-refresh
    pass

# ============================================
# CSS - FOND DARK + BLEU CLAIR AU LIEU DU VIOLET
# ============================================
st.markdown("""
<style>
    /* ===== TOOLBAR AVEC DÉGRADÉ BLEU CLAIR ===== */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%) !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Cacher tous les éléments blancs */
    .stApp header:before,
    .stApp header:after,
    .stApp header > div,
    .stApp header [data-testid="stDecoration"],
    .stApp header [data-testid="stStatusWidget"],
    .stApp header [data-testid="stToolbar"],
    .stApp header [data-testid="baseButton-header"],
    .stApp header button,
    .stApp header div[role="status"],
    .stApp header div[class*="StatusWidget"],
    .stApp header div[class*="Toolbar"] {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Forcer toutes les icônes en blanc */
    .stApp header svg,
    .stApp header path,
    .stApp header line,
    .stApp header polygon {
        stroke: white !important;
        fill: white !important;
        color: white !important;
    }
    
    /* Menu déroulant */
    div[data-testid="stStatusWidget"] {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 50px !important;
    }
    
    /* ===== RESTE DU CSS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(191, 223, 255, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    /* Titres et labels visibles */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white !important;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #e8e8e8 !important;
    }
    
    /* Labels des inputs */
    label, .stSelectbox label, .stMultiselect label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Boutons visibles dès le début - BLEU CLAIR */
    .stButton > button {
        color: white !important;
        font-weight: 600 !important;
        border: 1px solid rgba(191, 223, 255, 0.5) !important;
        background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        border-color: #64b5f6 !important;
        box-shadow: 0 4px 15px rgba(191, 223, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%) !important;
        color: #01579B !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #1e2a3a 0%, #1a1f2e 100%) !important;
        color: white !important;
        border: 1px solid rgba(191, 223, 255, 0.3) !important;
    }
    
    /* Tabs - BLEU CLAIR */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a8b2d1 !important;
        background-color: rgba(30, 42, 58, 0.5) !important;
        border: 1px solid rgba(191, 223, 255, 0.2) !important;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #01579B !important;
        background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%) !important;
        border-color: transparent !important;
    }
    
    /* Multiselect - BLEU CLAIR */
    .stMultiSelect [data-baseweb="select"] {
        background-color: rgba(30, 42, 58, 0.8) !important;
        border: 1px solid rgba(191, 223, 255, 0.3) !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #90CAF9 !important;
        color: #01579B !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%);
        padding: 2rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(191, 223, 255, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-header h1 {
        color: #01579B !important;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: #0277BD !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .badge-container {
        display: flex;
        gap: 0.8rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    
    .badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: white !important;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .badge-mongo { 
        background: linear-gradient(135deg, #00ed64 0%, #00c853 100%); 
        color: #1a1a2e !important; 
        border: none;
    }
    .badge-api { 
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
        border: none;
    }
    .badge-streamlit { 
        background: linear-gradient(135deg, #ff4b4b 0%, #ff3838 100%); 
        border: none;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #1a1f2e 100%);
        border: 1px solid rgba(191, 223, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card:hover {
        border-color: #BFDFFF;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(191, 223, 255, 0.4);
    }
    
    .metric-label {
        color: #a8b2d1 !important;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin: 0;
    }
    
    .metric-value {
        color: white !important;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
        margin: 0.3rem 0 0.1rem 0;
    }
    
    .metric-delta {
        color: #90CAF9 !important;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .footer {
        text-align: center;
        color: #a8b2d1 !important;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(191, 223, 255, 0.2);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUSEAU HORAIRE MAROC (UTC+1)
# ============================================
def get_maroc_time():
    """Retourne l'heure actuelle au Maroc (UTC+1)"""
    maroc_tz = pytz.timezone('Africa/Casablanca')
    return datetime.now(maroc_tz)

def convert_to_maroc_time(utc_dt):
    """Convertit une date UTC en heure marocaine"""
    if pd.isna(utc_dt):
        return None
    maroc_tz = pytz.timezone('Africa/Casablanca')
    if utc_dt.tzinfo is None:
        utc_dt = pytz.UTC.localize(utc_dt)
    return utc_dt.astimezone(maroc_tz)

# ============================================
# CONNEXION MONGODB
# ============================================
@st.cache_resource(ttl=300)
def init_mongodb():
    try:
        client = MongoClient(
            'mongodb://meteo_user:meteo_password@mongodb:27017/',
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000
        )
        client.admin.command('ping')
        db = client['meteo_maroc']
        return db['weather_processed']
    except Exception as e:
        st.error(f"❌ **Erreur MongoDB** : {str(e)}")
        return None

collection = init_mongodb()

# ============================================
# CHARGEMENT ET NETTOYAGE DES DONNÉES
# ============================================
@st.cache_data(ttl=60, show_spinner="📡 Chargement des données...")
def load_and_clean_data():
    if collection is None:
        return pd.DataFrame()
    
    try:
        pipeline = [
            {"$sort": {"timestamp": -1}},
            {"$group": {
                "_id": "$ville",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}}
        ]
        
        cursor = collection.aggregate(pipeline)
        df = pd.DataFrame(list(cursor))
        
        if df.empty:
            return df
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Convertir en heure marocaine
            df['timestamp_maroc'] = df['timestamp'].apply(convert_to_maroc_time)
        
        df = df.drop_duplicates(subset=['ville'], keep='first')
        df = df.sort_values('temperature', ascending=False)
        
        return df
        
    except Exception as e:
        st.error(f"❌ **Erreur chargement** : {str(e)}")
        return pd.DataFrame()

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🌤️ Météo Maroc • Dashboard</h1>
    <p>Analyse météo en temps réel • 19 villes • Heure marocaine (UTC+1)</p>
    <div class="badge-container">
        <span class="badge badge-mongo">🍃 MongoDB</span>
        <span class="badge badge-api">⚡ OpenWeatherMap</span>
        <span class="badge badge-streamlit">📊 Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e2a3a 0%, #1a1f2e 100%); padding: 1.5rem; border-radius: 20px; border: 1px solid rgba(191, 223, 255, 0.3); margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h2 style="color: white; margin:0; font-size: 1.5rem;">🎛️ Contrôle</h2>
        <p style="color: #a8b2d1; margin:0.3rem 0 0 0;">Sélection et filtrage</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_and_clean_data()
    
    if not df.empty:
        villes_uniques = sorted(df['ville'].unique())
        
        col1, col2 = st.columns(2)
        with col1:
            select_all = st.button("📌 Toutes", use_container_width=True, type="primary")
        with col2:
            clear_all = st.button("🧹 Effacer", use_container_width=True, type="secondary")
        
        if select_all:
            selected_villes = villes_uniques
        elif clear_all:
            selected_villes = []
        else:
            selected_villes = st.multiselect(
                "Sélectionner des villes",
                options=villes_uniques,
                default=villes_uniques[:6] if len(villes_uniques) > 6 else villes_uniques,
                label_visibility="collapsed"
            )
        
        if not selected_villes:
            selected_villes = villes_uniques[:3] if len(villes_uniques) >= 3 else villes_uniques
        
        # ===== STATISTIQUES AVEC HEURE MAROC =====
        st.markdown('<hr style="margin: 1.5rem 0; border-color: rgba(191, 223, 255, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 1rem;">📊 Statistiques</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="sidebar-stat">
                <p class="sidebar-stat-label">🏙️ Villes</p>
                <p class="sidebar-stat-value">{len(villes_uniques)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            temp_moyenne = df['temperature'].mean()
            st.markdown(f"""
            <div class="sidebar-stat">
                <p class="sidebar-stat-label">🌡️ Moyenne</p>
                <p class="sidebar-stat-value">{temp_moyenne:.1f}°C</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== DERNIER RAFRAÎCHISSEMENT =====
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e2a3a 0%, #1a1f2e 100%); padding: 1.2rem; border-radius: 16px; margin-top: 1rem; border: 1px solid rgba(191, 223, 255, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <p style="color: #a8b2d1; font-size:0.7rem; margin:0; text-transform: uppercase;">⏱️ DERNIER RAFRAÎCHISSEMENT</p>
            <p style="color: white; font-size:1.1rem; font-weight:600; margin:0.2rem 0 0 0;">{st.session_state.last_refresh.strftime('%d/%m/%Y • %H:%M:%S')}</p>
            <p style="color: #90CAF9; font-size:0.75rem; margin:0.2rem 0 0 0;">Heure du Maroc (UTC+1)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== HEURE ACTUELLE MAROC - BLEU CLAIR =====
        current_time = get_maroc_time()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%); padding: 1rem; border-radius: 16px; margin-top: 1rem; border: 1px solid rgba(255,255,255,0.2); text-align: center; box-shadow: 0 4px 15px rgba(191, 223, 255, 0.3);">
            <p style="color: #01579B; font-size:0.7rem; margin:0;">🕐 HEURE ACTUELLE (MAROC)</p>
            <p style="color: #01579B; font-size:1.3rem; font-weight:700; margin:0.2rem 0 0 0;">{current_time.strftime('%H:%M')}</p>
            <p style="color: #0277BD; font-size:0.75rem; margin:0.2rem 0 0 0;">{current_time.strftime('%d %B %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr style="margin: 1.5rem 0; border-color: rgba(191, 223, 255, 0.2);">', unsafe_allow_html=True)
        
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.session_state.last_refresh = get_maroc_time()
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    else:
        st.warning("⚠️ **Aucune donnée**")
        selected_villes = []

# ============================================
# MAIN CONTENT
# ============================================
if not df.empty and selected_villes:
    df_filtered = df[df['ville'].isin(selected_villes)].copy()
    
    if not df_filtered.empty:
        # ===== KPIs =====
        st.markdown('<p style="color: white; font-size: 1.4rem; font-weight: 700; margin: 0 0 1rem 0;">📌 Indicateurs clés</p>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        with cols[0]:
            temp_moy = df_filtered['temperature'].mean()
            temp_max = df_filtered['temperature'].max()
            ville_max = df_filtered.loc[df_filtered['temperature'].idxmax(), 'ville']
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">🌡️ TEMPÉRATURE</p>
                <p class="metric-value">{temp_moy:.1f}°C</p>
                <p class="metric-delta">Max: {temp_max:.1f}°C ({ville_max})</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            humidite_moy = df_filtered['humidite'].mean()
            humidite_max = df_filtered['humidite'].max()
            ville_humid = df_filtered.loc[df_filtered['humidite'].idxmax(), 'ville']
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">💧 HUMIDITÉ</p>
                <p class="metric-value">{humidite_moy:.0f}%</p>
                <p class="metric-delta">Max: {humidite_max:.0f}% ({ville_humid})</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            vent_moy = df_filtered['vent_vitesse'].mean()
            vent_max = df_filtered['vent_vitesse'].max()
            ville_vent = df_filtered.loc[df_filtered['vent_vitesse'].idxmax(), 'ville']
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">💨 VENT</p>
                <p class="metric-value">{vent_moy:.1f} m/s</p>
                <p class="metric-delta">Max: {vent_max:.1f} m/s ({ville_vent})</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">📊 ANALYSE</p>
                <p class="metric-value">{df_filtered['ville'].nunique()}</p>
                <p class="metric-delta">{len(df_filtered)} mesures • {len(selected_villes)} sélectionnées</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== HEURE MAROC DANS LES TABS - BLEU CLAIR =====
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0 0.5rem 0;">
            <p style="color: white; font-size: 1.1rem; font-weight: 600; margin:0;">📊 Visualisations</p>
            <div style="background: linear-gradient(135deg, #BFDFFF 0%, #90CAF9 100%); padding: 0.5rem 1rem; border-radius: 50px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 15px rgba(191, 223, 255, 0.3);">
                <span style="color: #01579B; font-size:0.8rem;">🕐 </span>
                <span style="color: #01579B; font-weight:600;">{get_maroc_time().strftime('%H:%M')}</span>
                <span style="color: #0277BD; font-size:0.7rem; margin-left:0.5rem;">UTC+1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🌡️ Températures", "💧 Humidité & Vent", "📋 Données"])
        
        with tab1:
            fig_temp = px.bar(
                df_filtered.sort_values('temperature', ascending=False),
                x='ville',
                y='temperature',
                color='temperature',
                color_continuous_scale=['#BFDFFF', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5', '#1565C0'],
                title=None,
                labels={'temperature': '°C', 'ville': ''},
                text_auto='.1f',
                height=500
            )
            
            fig_temp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=20, b=50),
                xaxis=dict(tickfont_color='white', tickangle=45, gridcolor='rgba(191, 223, 255, 0.1)'),
                yaxis=dict(tickfont_color='white', gridcolor='rgba(191, 223, 255, 0.1)')
            )
            
            fig_temp.update_traces(textfont_color='white', textposition='outside')
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hum = px.bar(
                    df_filtered.sort_values('humidite', ascending=False),
                    x='ville',
                    y='humidite',
                    color='humidite',
                    color_continuous_scale=['#F0F7FF', '#BFDFFF', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5'],
                    title="💧 Humidité (%)",
                    labels={'humidite': '%', 'ville': ''},
                    text_auto='.0f',
                    height=450
                )
                fig_hum.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font_color='white',
                    xaxis=dict(gridcolor='rgba(191, 223, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(191, 223, 255, 0.1)')
                )
                fig_hum.update_traces(textfont_color='white', textposition='outside')
                st.plotly_chart(fig_hum, use_container_width=True)
            
            with col2:
                fig_wind = px.bar(
                    df_filtered.sort_values('vent_vitesse', ascending=False),
                    x='ville',
                    y='vent_vitesse',
                    color='vent_vitesse',
                    color_continuous_scale=['#F0F7FF', '#BFDFFF', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5'],
                    title="💨 Vent (m/s)",
                    labels={'vent_vitesse': 'm/s', 'ville': ''},
                    text_auto='.1f',
                    height=450
                )
                fig_wind.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font_color='white',
                    xaxis=dict(gridcolor='rgba(191, 223, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(191, 223, 255, 0.1)')
                )
                fig_wind.update_traces(textfont_color='white', textposition='outside')
                st.plotly_chart(fig_wind, use_container_width=True)
        
        with tab3:
            df_display = df_filtered[['ville', 'temperature', 'humidite', 'vent_vitesse', 'conditions']].copy()
            df_display.columns = ['Ville', 'Température', 'Humidité', 'Vent', 'Conditions']
            
            st.dataframe(
                df_display.style.format({
                    'Température': '{:.1f}°C',
                    'Humidité': '{:.0f}%',
                    'Vent': '{:.1f} m/s'
                }),
                use_container_width=True,
                height=400
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("🔥 **Plus chaudes**")
                top_hot = df_filtered.nlargest(3, 'temperature')[['ville', 'temperature']]
                for _, row in top_hot.iterrows():
                    st.write(f"- {row['ville']}: {row['temperature']:.1f}°C")
            
            with col2:
                st.markdown("💨 **Plus ventées**")
                top_wind = df_filtered.nlargest(3, 'vent_vitesse')[['ville', 'vent_vitesse']]
                for _, row in top_wind.iterrows():
                    st.write(f"- {row['ville']}: {row['vent_vitesse']:.1f} m/s")
            
            with col3:
                st.markdown("💧 **Plus humides**")
                top_humid = df_filtered.nlargest(3, 'humidite')[['ville', 'humidite']]
                for _, row in top_humid.iterrows():
                    st.write(f"- {row['ville']}: {row['humidite']:.0f}%")

# ============================================
# FOOTER
# ============================================
current_time = get_maroc_time()
st.markdown(f"""
<div class="footer">
    <p style="margin-bottom: 0.5rem;">🌤️ <strong>Météo Maroc • Dashboard Premium</strong></p>
    <p style="font-size: 0.75rem;">Données météo en direct des 19 villes du Maroc • Source: OpenWeatherMap • Mise à jour quotidienne"</p>
    <p style="font-size: 0.7rem; margin-top: 1rem; color: #90CAF9;">Dernier rafraîchissement: {current_time.strftime('%d/%m/%Y • %H:%M')}</p>
</div>
""", unsafe_allow_html=True)