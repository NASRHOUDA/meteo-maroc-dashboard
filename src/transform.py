import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH

class WeatherTransformer:
    """Transformation des données météo - Version CSV uniquement"""
    
    def __init__(self):
        Path(PROCESSED_DATA_PATH).mkdir(parents=True, exist_ok=True)
    
    def load_latest_raw(self) -> List[Dict]:
        """Charger le dernier fichier JSON brut"""
        raw_files = list(Path(RAW_DATA_PATH).glob("*.json"))
        
        if not raw_files:
            raise FileNotFoundError("❌ Aucun fichier JSON trouvé dans data/raw/")
        
        latest_file = max(raw_files, key=lambda p: p.stat().st_mtime)
        print(f"📂 Chargement: {latest_file.name}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def transform_to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """Convertir les données brutes en DataFrame"""
        records = []
        
        for ville_data in data:
            record = {
                "ville": ville_data["name"],
                "temperature": ville_data["main"]["temp"],
                "ressenti": ville_data["main"]["feels_like"],
                "temp_min": ville_data["main"]["temp_min"],
                "temp_max": ville_data["main"]["temp_max"],
                "pression": ville_data["main"]["pressure"],
                "humidite": ville_data["main"]["humidity"],
                "vent_vitesse": ville_data["wind"]["speed"],
                "conditions": ville_data["weather"][0]["description"],
                "timestamp": pd.to_datetime(ville_data["dt"], unit='s')
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # Features engineering simples
        df["delta_temp"] = df["temp_max"] - df["temp_min"]
        
        print(f"✅ DataFrame créé: {len(df)} lignes")
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Déjà fait dans transform_to_dataframe"""
        return df
    
    def save_processed(self, df: pd.DataFrame) -> str:
        """Sauvegarde en CSV uniquement (100% compatible)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        csv_path = Path(PROCESSED_DATA_PATH) / f"meteo_processed_{timestamp}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ Données sauvegardées: {csv_path}")
        
        return str(csv_path)

if __name__ == "__main__":
    transformer = WeatherTransformer()
    data = transformer.load_latest_raw()
    df = transformer.transform_to_dataframe(data)
    transformer.save_processed(df)
