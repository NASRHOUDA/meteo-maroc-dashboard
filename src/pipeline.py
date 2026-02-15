"""
Pipeline complet : API → JSON → DataFrame → MongoDB
Avec métriques Prometheus pour monitoring
"""

import sys
import time
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent))

from extract import WeatherExtractor
from transform import WeatherTransformer
from mongo_loader import MongoWeatherLoader

# Importer les métriques
from src.metrics import (
    PIPELINE_RUNS,
    PIPELINE_ERRORS,
    EXTRACTION_TIME,
    TRANSFORM_TIME,
    LOAD_TIME,
    DATA_POINTS,
    CITIES_COUNT,
    API_REQUESTS
)

def run_pipeline(use_atlas: bool = False):
    """Exécute le pipeline complet avec métriques Prometheus"""
    
    print(f"Valeur initiale pipeline_runs: {PIPELINE_RUNS._value.get()}")
    
    # Incrémenter le compteur d'exécutions
    PIPELINE_RUNS.inc()
    
    print("\n" + "="*50)
    print("🚀 PIPELINE MÉTÉO MAROC - MONGODB")
    print("="*50 + "\n")
    
    # ============================================
    # ÉTAPE 1: EXTRACTION
    # ============================================
    print("📡 ÉTAPE 1: Extraction des données API...")
    extractor = WeatherExtractor()
    
    # Mesurer le temps d'extraction manuellement
    start_time = time.time()
    data = extractor.extract_all()
    extraction_duration = time.time() - start_time
    EXTRACTION_TIME.observe(extraction_duration)
    print(f"⏱️ Temps d'extraction: {extraction_duration:.2f} secondes")
    
    if not data:
        print("❌ Aucune donnée extraite. Arrêt du pipeline.")
        PIPELINE_ERRORS.labels(stage='extract').inc()
        return
    
    # Enregistrer les requêtes API par ville
    for ville in data:
        ville_nom = ville.get('name', 'unknown')
        API_REQUESTS.labels(city=ville_nom, status='success').inc()
    
    extractor.save_raw(data)
    print(f"✅ Extraction terminée: {len(data)} villes\n")
    
    # ============================================
    # ÉTAPE 2: TRANSFORMATION
    # ============================================
    print("🔄 ÉTAPE 2: Transformation des données...")
    transformer = WeatherTransformer()
    
    # Mesurer le temps de transformation manuellement
    start_time = time.time()
    df = transformer.transform_to_dataframe(data)
    df = transformer.engineer_features(df)
    transform_duration = time.time() - start_time
    TRANSFORM_TIME.observe(transform_duration)
    print(f"⏱️ Temps de transformation: {transform_duration:.2f} secondes")
    
    transformer.save_processed(df)
    print(f"✅ Transformation terminée: {len(df)} lignes\n")
    
    # ============================================
    # ÉTAPE 3: CHARGEMENT MONGODB
    # ============================================
    print("🍃 ÉTAPE 3: Chargement vers MongoDB...")
    
    # Mesurer le temps de chargement manuellement
    start_time = time.time()
    try:
        loader = MongoWeatherLoader(use_atlas=use_atlas)
        
        # Insertion des données brutes
        raw_count = loader.insert_raw_data(data)
        print(f"   - Documents bruts: {raw_count}")
        
        # Insertion des données transformées
        processed_count = loader.insert_processed_data(df)
        print(f"   - Documents transformés: {processed_count}")
        
        load_duration = time.time() - start_time
        LOAD_TIME.observe(load_duration)
        print(f"⏱️ Temps de chargement: {load_duration:.2f} secondes")
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        PIPELINE_ERRORS.labels(stage='load').inc()
        return
    
    # Mettre à jour les jauges
    DATA_POINTS.set(processed_count)
    CITIES_COUNT.set(len(df['ville'].unique()))
    
    # Vérification
    try:
        latest = loader.get_latest_weather(5)
        print(f"\n✅ Pipeline terminé avec succès!")
        print(f"📊 Dernières mesures:")
        for doc in latest:
            print(f"   - {doc['ville']}: {doc['temperature']}°C, {doc['conditions']}")
    except:
        pass
    
    print(f"\n🌐 Interface MongoDB Express: http://localhost:8081")
    print(f"📊 Métriques: http://localhost:8000/metrics")
    
    return {
        "raw_count": raw_count,
        "processed_count": processed_count,
        "data": data,
        "df": df
    }

if __name__ == "__main__":
    # Exécuter le pipeline
    # Mettre use_atlas=True pour MongoDB Atlas (Cloud)
    run_pipeline(use_atlas=False)