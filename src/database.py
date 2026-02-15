"""
Module de connexion MongoDB
"""

import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnection:
    """Gestionnaire de connexion MongoDB"""
    
    def __init__(self, use_atlas: bool = False):
        """
        Initialise la connexion MongoDB
        use_atlas: True = MongoDB Atlas (Cloud), False = MongoDB local
        """
        self.use_atlas = use_atlas
        self.client = None
        self.db = None
        
    def connect(self):
        """Établit la connexion à MongoDB"""
        try:
            if self.use_atlas:
                # Connexion MongoDB Atlas (Cloud)
                uri = os.getenv("MONGODB_ATLAS_URI")
                self.client = MongoClient(uri, 
                                        maxPoolSize=50,
                                        minPoolSize=10,
                                        maxIdleTimeMS=45000,
                                        retryWrites=True)
                db_name = os.getenv("MONGODB_ATLAS_DB", "meteo_maroc")
            else:
                # Connexion MongoDB local
                host = os.getenv("MONGODB_HOST", "localhost")
                port = int(os.getenv("MONGODB_PORT", 27017))
                username = os.getenv("MONGODB_USER")
                password = os.getenv("MONGODB_PASSWORD")
                db_name = os.getenv("MONGODB_DB", "meteo_maroc")
                
                if username and password:
                    self.client = MongoClient(
                        f"mongodb://{username}:{password}@{host}:{port}/",
                        maxPoolSize=50
                    )
                else:
                    self.client = MongoClient(host, port, maxPoolSize=50)
            
            # Test de connexion
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            
            logger.info(f"✅ Connexion MongoDB réussie - {'Atlas' if self.use_atlas else 'Local'}")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"❌ Connexion MongoDB échouée: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur: {e}")
            return False
    
    def get_collection(self, collection_name: str):
        """Récupère une collection"""
        if self.db is None:
            self.connect()
        return self.db[collection_name]
    
    def close(self):
        """Ferme la connexion"""
        if self.client:
            self.client.close()
            logger.info("🔌 Connexion MongoDB fermée")

# Singleton pattern pour la connexion
_mongodb_connection = None

def get_mongodb_connection(use_atlas: bool = False) -> MongoDBConnection:
    """Retourne une instance unique de connexion MongoDB"""
    global _mongodb_connection
    if _mongodb_connection is None:
        _mongodb_connection = MongoDBConnection(use_atlas)
        _mongodb_connection.connect()
    return _mongodb_connection