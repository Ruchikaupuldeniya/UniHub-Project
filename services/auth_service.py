import requests
import time
from typing import Any, Dict, Optional, List
from config.firebase_config import FirebaseConfig
from firebase.firebase_service import FirebaseService
from models.user import User
from models.student import Student

class AuthService:
    # REST API endpoints
    SIGN_IN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key="
    SIGN_UP_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key="
    RESET_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="
    
    # In-memory mock database for offline/no-credential development
    _mock_users: Dict[str, Dict[str, Any]] = {
        "mock_admin_uid": {"uid": "mock_admin_uid", "email": "admin@vau.ac.lk", "role": "administrator", "password": "Password123!", "created_at": int(time.time())},
        "mock_student_uid": {"uid": "mock_student_uid", "email": "student@vau.ac.lk", "role": "student", "password": "Password123!", "created_at": int(time.time())}
    }
    _mock_students: Dict[str, Dict[str, Any]] = {
        "mock_student_uid": {
            "uid": "mock_student_uid",
            "reg_num": "2021/ICT/80",
            "name": "Jane Doe",
            "faculty": "Applied Science",
            "department": "Physical Science",
            "is_active": True,
            "profile_pic": ""
        }
    }

    @classmethod
    def sign_in(cls, email: str, password: str) -> Dict[str, Any]:
        """
        Signs in a user.
        Returns user details dict: {"uid": ..., "email": ..., "role": ..., "token": ...}
        Raises Exception if credentials/account is invalid.
        """
        email_clean = email.strip().lower()
        
        # Check if Firebase live credentials are set
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            url = f"{cls.SIGN_IN_URL}{FirebaseConfig.API_KEY}"
            payload = {
                "email": email_clean,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            res_data = response.json()
            
            if response.status_code != 200:
                error_msg = res_data.get("error", {}).get("message", "INVALID_CREDENTIALS")
                raise Exception(cls._translate_error(error_msg))
                
            uid = res_data["localId"]
            id_token = res_data["idToken"]
            
            # Fetch user role from Firestore
            db = FirebaseService.get_db()
            if db:
                user_doc = db.collection("users").document(uid).get()
                if not user_doc.exists:
                    # Fallback role if auth exists but no Firestore doc
                    role = "student"
                else:
                    role = user_doc.to_dict().get("role", "student")
                
                # If student, verify if active
                if role == "student":
                    student_doc = db.collection("students").document(uid).get()
                    if student_doc.exists and not student_doc.to_dict().get("is_active", True):
                        raise Exception("Your account has been deactivated. Please contact an administrator.")
            else:
                role = "student"
                
            return {
                "uid": uid,
                "email": email_clean,
                "role": role,
                "token": id_token
            }
        else:
            # Offline Mock Fallback Mode
            # Check mock db
            match_uid = None
            for uid, user_data in cls._mock_users.items():
                if user_data["email"] == email_clean:
                    match_uid = uid
                    break
                    
            if match_uid:
                user_data = cls._mock_users[match_uid]
                stored_password = user_data.get("password", "Password123!")
                if password == stored_password:
                    role = user_data["role"]
                    
                    if role == "student":
                        student_data = cls._mock_students.get(match_uid, {})
                        if not student_data.get("is_active", True):
                            raise Exception("Your account has been deactivated. Please contact an administrator.")
                            
                    return {
                        "uid": match_uid,
                        "email": email_clean,
                        "role": role,
                        "token": "mock_session_token"
                    }
            
            raise Exception("Invalid email or password.")

    @classmethod
    def sign_up(cls, email: str, password: str, reg_num: str, name: str, faculty: str, department: str) -> Dict[str, Any]:
        """
        Registers a new student user.
        """
        email_clean = email.strip().lower()
        
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            # 1. Sign up on Firebase Auth
            url = f"{cls.SIGN_UP_URL}{FirebaseConfig.API_KEY}"
            payload = {
                "email": email_clean,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            res_data = response.json()
            
            if response.status_code != 200:
                error_msg = res_data.get("error", {}).get("message", "EMAIL_EXISTS")
                raise Exception(cls._translate_error(error_msg))
                
            uid = res_data["localId"]
            id_token = res_data["idToken"]
            
            # 2. Write details to Firestore
            db = FirebaseService.get_db()
            if db:
                user = User(uid=uid, email=email_clean, role="student", created_at=int(time.time()))
                student = Student(
                    uid=uid,
                    reg_num=reg_num,
                    name=name,
                    faculty=faculty,
                    department=department,
                    is_active=True
                )
                
                # Perform batch write/set
                batch = db.batch()
                user_ref = db.collection("users").document(uid)
                student_ref = db.collection("students").document(uid)
                
                batch.set(user_ref, user.to_dict())
                batch.set(student_ref, student.to_dict())
                batch.commit()
                
            return {
                "uid": uid,
                "email": email_clean,
                "role": "student",
                "token": id_token
            }
        else:
            # Offline Mock Mode
            # Verify if email exists
            for user_data in cls._mock_users.values():
                if user_data["email"] == email_clean:
                    raise Exception("The email address is already in use by another account.")
                    
            uid = f"mock_uid_{int(time.time())}"
            # Save in mock database
            cls._mock_users[uid] = {
                "uid": uid,
                "email": email_clean,
                "role": "student",
                "created_at": int(time.time())
            }
            cls._mock_students[uid] = {
                "uid": uid,
                "reg_num": reg_num.upper(),
                "name": name,
                "faculty": faculty,
                "department": department,
                "is_active": True,
                "profile_pic": ""
            }
            
            return {
                "uid": uid,
                "email": email_clean,
                "role": "student",
                "token": "mock_session_token"
            }

    @classmethod
    def reset_password(cls, email: str) -> bool:
        """
        Sends password reset link.
        """
        email_clean = email.strip().lower()
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            url = f"{cls.RESET_URL}{FirebaseConfig.API_KEY}"
            payload = {
                "requestType": "PASSWORD_RESET",
                "email": email_clean
            }
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                error_msg = response.json().get("error", {}).get("message", "EMAIL_NOT_FOUND")
                raise Exception(cls._translate_error(error_msg))
            return True
        else:
            # Mock reset password success
            # Check if email is registered in mock database
            found = any(user_data["email"] == email_clean for user_data in cls._mock_users.values())
            if not found:
                raise Exception("There is no user record corresponding to this identifier. The user may have been deleted.")
            return True

    @classmethod
    def change_password(cls, uid: str, id_token: str, new_password: str) -> bool:
        """
        Changes the user's password.
        """
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={FirebaseConfig.API_KEY}"
            payload = {
                "idToken": id_token,
                "password": new_password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            res_data = response.json()
            if response.status_code != 200:
                error_msg = res_data.get("error", {}).get("message", "FAILED_TO_UPDATE_PASSWORD")
                raise Exception(cls._translate_error(error_msg))
            return True
        else:
            # Mock mode: update local database password
            if uid in cls._mock_users:
                cls._mock_users[uid]["password"] = new_password
                return True
            raise Exception("User session has expired or user is not found.")

    @classmethod
    def _translate_error(cls, error_msg: str) -> str:
        """
        Helper to translate Firebase Auth REST API error messages to human readable strings.
        """
        if "EMAIL_EXISTS" in error_msg:
            return "The email address is already in use by another account."
        elif "INVALID_EMAIL" in error_msg:
            return "The email address is badly formatted."
        elif "EMAIL_NOT_FOUND" in error_msg or "INVALID_PASSWORD" in error_msg:
            return "Invalid email address or password."
        elif "USER_DISABLED" in error_msg:
            return "The user account has been disabled by an administrator."
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_msg:
            return "Access to this account has been temporarily disabled due to many failed login attempts."
        return f"Authentication failed: {error_msg}"

    @classmethod
    def get_student_profile(cls, uid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves student profile by UID.
        """
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            db = FirebaseService.get_db()
            if db:
                doc = db.collection("students").document(uid).get()
                if doc.exists:
                    return doc.to_dict()
            return None
        else:
            return cls._mock_students.get(uid)

    @classmethod
    def update_student_profile(cls, uid: str, updates: Dict[str, Any]) -> bool:
        """
        Updates student profile.
        """
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            db = FirebaseService.get_db()
            if db:
                db.collection("students").document(uid).update(updates)
                return True
            return False
        else:
            if uid in cls._mock_students:
                cls._mock_students[uid].update(updates)
                return True
            return False

    @classmethod
    def get_all_students(cls) -> List[Dict[str, Any]]:
        """
        Retrieves all student profiles (for admin panel).
        """
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            db = FirebaseService.get_db()
            if db:
                docs = db.collection("students").stream()
                return [doc.to_dict() for doc in docs]
            return []
        else:
            return list(cls._mock_students.values())

    @classmethod
    def toggle_student_status(cls, uid: str) -> bool:
        """
        Toggles active status of a student.
        """
        if FirebaseConfig.is_client_configured() and FirebaseService.initialize():
            db = FirebaseService.get_db()
            if db:
                doc_ref = db.collection("students").document(uid)
                doc = doc_ref.get()
                if doc.exists:
                    new_status = not doc.to_dict().get("is_active", True)
                    doc_ref.update({"is_active": new_status})
                    # Also disable/enable in mock users for sync
                    user_ref = db.collection("users").document(uid)
                    user_ref.update({"role": "student"}) # Retain role
                    # Firebase Admin Auth toggle
                    try:
                        auth = FirebaseService.get_auth()
                        auth.update_user(uid, disabled=not new_status)
                    except Exception as e:
                        print(f"Error updating Firebase Auth user disabled status: {e}")
                    return True
            return False
        else:
            if uid in cls._mock_students:
                new_status = not cls._mock_students[uid].get("is_active", True)
                cls._mock_students[uid]["is_active"] = new_status
                return True
            return False
