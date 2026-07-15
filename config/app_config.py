import os

class AppConfig:
    APP_NAME = "UniHub"
    APP_SUBTITLE = "AI Powered Smart University Student Super App"
    VERSION = "1.0.0"
    
    # Desktop window configuration
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 800
    WINDOW_MIN_WIDTH = 375
    WINDOW_MIN_HEIGHT = 650
    
    # Supported languages
    LANGUAGES = {
        "en": "English",
        "si": "Sinhala",
        "ta": "Tamil"
    }
    DEFAULT_LANGUAGE = "en"
    
    # Developer / Debug settings
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
