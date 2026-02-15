import requests
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

from src.config import (
    OPENWEATHER_API_KEY, VILLES, BASE_URL, UNITS, LANG,
    RAW_DATA_PATH, REQUEST_TIMEOUT, MAX_RETRIES
)

load_dotenv()

class WeatherExtractor:
    """Extraction des données météo depuis OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.villes = VILLES
        self.session = requests.Session()
    
    def extract_city(self, ville: str) -> Optional[Dict]:
        """Extraction pour une seule ville"""
        try:
            url = f"{BASE_URL}?q={ville},MA&appid={self.api_key}&units={UNITS}&lang={LANG}"
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                # Ajouter des métadonnées
                data['_extracted_at'] = datetime.now().isoformat()
                data['_extraction_version'] = '1.0'
                print(f"✅ {ville}: {data['main']['temp']}°C - {data['weather'][0]['description']}")
                return data
            else:
                print(f"❌ {ville}: Erreur {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ {ville}: Exception - {str(e)}")
            return None
    
    def extract_all(self) -> List[Dict]:
        """Extraction pour toutes les villes"""
        all_data = []
        for ville in self.villes:
            data = self.extract_city(ville)
            if data:
                all_data.append(data)
        
        print(f"\n✅ Extraction terminée: {len(all_data)}/{len(self.villes)} villes")
        return all_data
    
    def save_raw(self, data: List[Dict]) -> str:
        """Sauvegarde des données brutes en JSON"""
        # Créer le dossier raw s'il n'existe pas
        Path(RAW_DATA_PATH).mkdir(parents=True, exist_ok=True)
        
        # Générer le nom du fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meteo_maroc_{timestamp}.json"
        filepath = Path(RAW_DATA_PATH) / filename
        
        # Sauvegarder en JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"💾 Données sauvegardées: {filepath}")
        return str(filepath)

if __name__ == "__main__":
    # Test
    extractor = WeatherExtractor()
    data = extractor.extract_all()
    if data:
        filepath = extractor.save_raw(data)
        print(f"\n✅ Fichier créé: {filepath}")