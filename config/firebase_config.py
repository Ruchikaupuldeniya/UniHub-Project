import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class FirebaseConfig:
    # Client Config (used for REST client operations if Pyrebase or custom client REST requests are used)
    API_KEY = os.getenv("FIREBASE_API_KEY", "")
    AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
    PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
    STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
    APP_ID = os.getenv("FIREBASE_APP_ID", "")
    MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID", "")
    DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", f"https://{PROJECT_ID}.firebaseio.com" if PROJECT_ID else "")
    
    # Firebase Admin SDK Credentials Path
    # This can point to a local JSON file for the service account
    SERVICE_ACCOUNT_JSON = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "config/serviceAccountKey.json")

    @classmethod
    def is_client_configured(cls) -> bool:
        return bool(cls.API_KEY and cls.PROJECT_ID)

    @classmethod
    def is_admin_configured(cls) -> bool:
        # Check if the service account file exists or if credentials are set as environment variables
        return os.path.exists(cls.SERVICE_ACCOUNT_JSON)
