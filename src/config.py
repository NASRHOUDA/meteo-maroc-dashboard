import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =============== API CONFIG ===============
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"
LANG = "fr"

# Villes du Maroc
VILLES = [
    "Casablanca", "Rabat", "Marrakech", "Fes", "Tangier",
    "Agadir", "Oujda", "Meknes", "Tetouan", "Safi",
    "El Jadida", "Nador", "Kenitra", "Beni Mellal", "Taza",
    "Ifrane", "Essaouira", "Chefchaouen", "Ouarzazate"
]

# =============== CHEMINS DE DONNÉES (TA STRUCTURE) ===============
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
OUTPUT_PATH = "data/output/"

# Créer les dossiers
for path in [RAW_DATA_PATH, PROCESSED_DATA_PATH, OUTPUT_PATH]:
    Path(path).mkdir(parents=True, exist_ok=True)

# =============== MONGODB CONFIG ===============
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DB = os.getenv("MONGODB_DB", "meteo_maroc")

# URI MongoDB
if MONGODB_USER and MONGODB_PASSWORD:
    MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/"
else:
    MONGODB_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/"

# Collections MongoDB
COLLECTION_RAW = "weather_raw"
COLLECTION_PROCESSED = "weather_processed"
COLLECTION_STATS = "weather_stats"
COLLECTION_ALERTS = "weather_alerts"

# =============== PARAMÈTRES PIPELINE ===============
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 1