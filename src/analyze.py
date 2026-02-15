import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import logging
from config import PROCESSED_DATA_PATH, OUTPUT_PATH

logger = logging.getLogger(__name__)

class WeatherAnalyzer:
    """Analyse et visualisation des données météo"""
    
    def __init__(self):
        Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
        self.df = None
    
    def load_data(self, filepath):
        """Charger les données transformées"""
        if str(filepath).endswith('.parquet'):
            self.df = pd.read_parquet(filepath)
        else:
            self.df = pd.read_csv(filepath)
        return self.df
    
    def create_temperature_dashboard(self):
        """Graphique des températures"""
        fig = px.bar(self.df, 
                     x='Ville', 
                     y=['Température (°C)', 'Temp_min (°C)', 'Temp_max (°C)'],
                     title="🌡️ Températures par ville",
                     barmode='group',
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        
        fig.update_layout(xaxis_tickangle=-45)
        fig.write_html(Path(OUTPUT_PATH) / "temperature_dashboard.html")
        return fig
    
    def create_humidity_wind_chart(self):
        """Humidité vs Vent"""
        fig = px.scatter(self.df, 
                        x='Humidité (%)', 
                        y='Vent (m/s)',
                        size='Température (°C)',
                        color='Ville',
                        hover_data=['Description'],
                        title="💧 Humidité vs Vent (taille = température)")
        
        fig.write_html(Path(OUTPUT_PATH) / "humidity_wind.html")
        return fig
    
    def create_top_cities(self):
        """Top 5 des villes"""
        fig = go.Figure()
        
        top_chaud = self.df.nlargest(5, 'Température (°C)')
        fig.add_trace(go.Bar(
            x=top_chaud['Ville'],
            y=top_chaud['Température (°C)'],
            name='Plus chaudes',
            marker_color='crimson'
        ))
        
        top_froid = self.df.nsmallest(5, 'Température (°C)')
        fig.add_trace(go.Bar(
            x=top_froid['Ville'],
            y=top_froid['Température (°C)'],
            name='Plus froides',
            marker_color='skyblue'
        ))
        
        fig.update_layout(title="🏆 Top 5 villes - Plus chaudes vs Plus froides",
                         barmode='group')
        
        fig.write_html(Path(OUTPUT_PATH) / "top_cities.html")
        return fig
    
    def generate_summary_stats(self):
        """Statistiques descriptives"""
        stats = self.df[['Température (°C)', 'Humidité (%)', 'Vent (m/s)', 'Delta_Temp']].describe()
        stats.to_csv(Path(OUTPUT_PATH) / "summary_statistics.csv")
        return stats

if __name__ == "__main__":
    analyzer = WeatherAnalyzer()
    
    # Charger les dernières données
    processed_files = list(Path(PROCESSED_DATA_PATH).glob("*.parquet"))
    if processed_files:
        latest_file = max(processed_files, key=lambda p: p.stat().st_mtime)
        analyzer.load_data(latest_file)
        
        # Générer tous les graphiques
        analyzer.create_temperature_dashboard()
        analyzer.create_humidity_wind_chart()
        analyzer.create_top_cities()
        analyzer.generate_summary_stats()
        
        logger.info("✅ Analyses et graphiques générés")