from prometheus_client import Counter, Histogram, Gauge, start_http_server, REGISTRY
import time
import functools
import atexit

# ============================================
# MÉTRIQUES PROMETHEUS
# ============================================

# Compteurs
API_REQUESTS = Counter(
    'api_requests_total', 
    'Nombre total de requêtes API', 
    ['city', 'status']
)

PIPELINE_RUNS = Counter(
    'pipeline_runs_total', 
    'Nombre total d\'exécutions du pipeline'
)

PIPELINE_ERRORS = Counter(
    'pipeline_errors_total', 
    'Nombre total d\'erreurs', 
    ['stage']
)

# Histogrammes (temps)
EXTRACTION_TIME = Histogram(
    'extraction_duration_seconds', 
    'Temps d\'extraction des données'
)

TRANSFORM_TIME = Histogram(
    'transform_duration_seconds', 
    'Temps de transformation des données'
)

LOAD_TIME = Histogram(
    'load_duration_seconds', 
    'Temps de chargement dans MongoDB'
)

# Jauges (valeurs actuelles)
DATA_POINTS = Gauge(
    'data_points_total', 
    'Nombre de documents dans MongoDB'
)

CITIES_COUNT = Gauge(
    'cities_count_total', 
    'Nombre de villes traitées'
)

# ============================================
# DÉCORATEUR POUR MESURER LE TEMPS
# ============================================
def monitor_time(histogram):
    """Décorateur pour mesurer le temps d'exécution d'une fonction"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                histogram.observe(duration)
        return wrapper
    return decorator

# ============================================
# SERVEUR HTTP POUR PROMETHEUS (VERSION CORRIGÉE)
# ============================================
_metrics_server = None
_metrics_server_started = False

def start_metrics_server(port=8000):
    """Démarre un serveur HTTP pour que Prometheus scrape les métriques"""
    global _metrics_server_started, _metrics_server
    
    if not _metrics_server_started:
        try:
            # Démarrer le serveur
            start_http_server(port)
            _metrics_server_started = True
            print(f"✅ Serveur de métriques démarré sur le port {port}")
            
            # Optionnel : message à la sortie (mais ne ferme pas le serveur)
            # atexit.register(lambda: print("✅ Serveur de métriques arrêté"))
            
        except Exception as e:
            print(f"⚠️ Erreur au démarrage du serveur: {e}")
    else:
        print(f"ℹ️ Serveur de métriques déjà démarré sur le port {port}")

# ============================================
# FONCTION DE TEST
# ============================================
def test_metrics():
    """Fonction de test pour vérifier que les métriques fonctionnent"""
    PIPELINE_RUNS.inc()
    DATA_POINTS.set(42)
    print("✅ Métriques de test incrémentées")
    print(f"   pipeline_runs_total = {PIPELINE_RUNS._value.get()}")
    print(f"   data_points_total = {DATA_POINTS._value.get()}")

if __name__ == "__main__":
    # Test du module
    start_metrics_server(8000)
    test_metrics()
    print("\n📊 Métriques disponibles sur http://localhost:8000/metrics")
    print("Appuyez sur Ctrl+C pour arrêter")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Arrêt")