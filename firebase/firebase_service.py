import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from config.firebase_config import FirebaseConfig
from typing import Optional, Any

class FirebaseService:
    _admin_app = None
    _db = None
    _bucket = None
    _initialized = False

    @classmethod
    def initialize(cls) -> bool:
        """
        Initializes the Firebase Admin SDK safely.
        Returns: True if initialized successfully, False otherwise.
        """
        if cls._initialized:
            return True
            
        try:
            # Check if Firebase is already initialized by default
            if not firebase_admin._apps:
                if FirebaseConfig.is_admin_configured():
                    cred = credentials.Certificate(FirebaseConfig.SERVICE_ACCOUNT_JSON)
                    # Initialize with storage bucket mapping if bucket name is set
                    options = {}
                    if FirebaseConfig.STORAGE_BUCKET:
                        options['storageBucket'] = FirebaseConfig.STORAGE_BUCKET
                        
                    cls._admin_app = firebase_admin.initialize_app(cred, options)
                else:
                    # Fallback: attempt to initialize with application default credentials
                    try:
                        cls._admin_app = firebase_admin.initialize_app()
                    except Exception:
                        print("Warning: Firebase credentials not found. Firebase features will run in offline/mock mode.")
                        return False
            else:
                cls._admin_app = firebase_admin.get_app()
                
            cls._initialized = True
            return True
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            return False

    @classmethod
    def get_db(cls) -> Optional[firestore.firestore.Client]:
        """
        Returns Firestore Database Client.
        """
        if not cls._initialized and not cls.initialize():
            return None
        if cls._db is None:
            try:
                cls._db = firestore.client()
            except Exception as e:
                print(f"Error fetching Firestore client: {e}")
                return None
        return cls._db

    @classmethod
    def get_bucket(cls) -> Optional[Any]:
        """
        Returns default Firebase Cloud Storage Bucket.
        """
        if not cls._initialized and not cls.initialize():
            return None
        if cls._bucket is None:
            try:
                cls._bucket = storage.bucket()
            except Exception as e:
                print(f"Error fetching Firebase Storage bucket: {e}")
                return None
        return cls._bucket
        
    @classmethod
    def get_auth(cls):
        """
        Returns Firebase Admin Auth module reference.
        """
        return auth
