import os
import sys
from dotenv import load_dotenv
from config.firebase_config import FirebaseConfig
from firebase.firebase_service import FirebaseService

load_dotenv()
print("API_KEY:", FirebaseConfig.API_KEY)
print("Admin Configured:", FirebaseConfig.is_admin_configured())
res = FirebaseService.initialize()
print("Initialize Result:", res)
