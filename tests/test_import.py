def test_import_extract():
    """Test que le module extract peut être importé"""
    try:
        from src.extract import WeatherExtractor
        assert True
    except ImportError:
        assert False

def test_import_transform():
    """Test que le module transform peut être importé"""
    try:
        from src.transform import WeatherTransformer
        assert True
    except ImportError:
        assert False

def test_import_loader():
    """Test que le module mongo_loader peut être importé"""
    try:
        from src.mongo_loader import MongoWeatherLoader
        assert True
    except ImportError:
        assert False