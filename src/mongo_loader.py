import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from pymongo.errors import BulkWriteError
from loguru import logger

from src.database import get_mongodb_connection
from src.config import (
    COLLECTION_RAW, COLLECTION_PROCESSED, 
    COLLECTION_STATS, COLLECTION_ALERTS
)

class MongoWeatherLoader:
    """Chargement des données météo vers MongoDB"""
    
    def __init__(self, use_atlas: bool = False):
        self.conn = get_mongodb_connection(use_atlas)
        self.db = self.conn.db
        
        # Collections
        self.raw_collection = self.db[COLLECTION_RAW]
        self.processed_collection = self.db[COLLECTION_PROCESSED]
        self.stats_collection = self.db[COLLECTION_STATS]
        self.alerts_collection = self.db[COLLECTION_ALERTS]
        
        # Création des index
        self._create_indexes()
    
    def _create_indexes(self):
        """Création des index pour optimiser les requêtes"""
        try:
            # Index pour les données brutes
            self.raw_collection.create_index([("name", 1)])
            self.raw_collection.create_index([("dt", -1)])
            self.raw_collection.create_index([("_extracted_at", -1)])
            
            # Index pour les données transformées
            self.processed_collection.create_index([("ville", 1)])
            self.processed_collection.create_index([("timestamp", -1)])
            self.processed_collection.create_index([
                ("ville", 1), 
                ("timestamp", -1)
            ])
            
            # Index texte pour la recherche
            self.processed_collection.create_index([
                ("ville", "text"),
                ("conditions", "text")
            ])
            
            logger.success("✅ Index MongoDB créés")
        except Exception as e:
            logger.warning(f"⚠️ Erreur création index: {e}")
    
    def insert_raw_data(self, data: List[Dict]) -> int:
        """Insertion des données brutes"""
        try:
            # Ajout de métadonnées
            for doc in data:
                doc["_loaded_at"] = datetime.now()
                doc["_source"] = "openweathermap_api"
            
            result = self.raw_collection.insert_many(data, ordered=False)
            logger.success(f"✅ {len(result.inserted_ids)} documents bruts insérés")
            return len(result.inserted_ids)
            
        except BulkWriteError as e:
            inserted = e.details['nInserted']
            logger.warning(f"⚠️ {inserted} documents bruts insérés (doublons ignorés)")
            return inserted
        except Exception as e:
            logger.error(f"❌ Erreur insertion données brutes: {e}")
            return 0
    
    def insert_processed_data(self, df: pd.DataFrame) -> int:
        """Insertion des données transformées"""
        try:
            # Conversion DataFrame -> Dict
            records = df.to_dict('records')
            
            # Ajout de métadonnées
            for record in records:
                record["_loaded_at"] = datetime.now()
                record["_version"] = "1.0"
            
            result = self.processed_collection.insert_many(records, ordered=False)
            logger.success(f"✅ {len(result.inserted_ids)} documents transformés insérés")
            return len(result.inserted_ids)
            
        except BulkWriteError as e:
            inserted = e.details['nInserted']
            logger.warning(f"⚠️ {inserted} documents transformés insérés")
            return inserted
        except Exception as e:
            logger.error(f"❌ Erreur insertion données transformées: {e}")
            return 0
    
    def get_latest_weather(self, limit: int = 20) -> List[Dict]:
        """Récupère les dernières données météo"""
        cursor = self.processed_collection.find(
            {},
            {"_id": 0, "ville": 1, "temperature": 1, "humidite": 1, 
             "vent_vitesse": 1, "conditions": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(limit)
        
        return list(cursor)
    
    def get_city_history(self, city: str, days: int = 7) -> List[Dict]:
        """Récupère l'historique d'une ville"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor = self.processed_collection.find(
            {
                "ville": city,
                "timestamp": {"$gte": cutoff_date}
            },
            {"_id": 0}
        ).sort("timestamp", 1)
        
        return list(cursor)

if __name__ == "__main__":
    # Test de connexion
    loader = MongoWeatherLoader(use_atlas=False)
    logger.success("✅ MongoWeatherLoader prêt à l'emploi!")
