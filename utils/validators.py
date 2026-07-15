import re

class Validators:
    # Student registration number pattern: e.g. 2021/ICT/80 or 2019/BS/01
    REG_NUM_PATTERN = re.compile(r"^\d{4}/[A-Z]{2,4}/\d+$")
    
    # Standard email validation pattern
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    
    # Vavuniya University student email domain
    UNI_STUDENT_DOMAIN = "@vau.ac.lk"
    
    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        if not email or not cls.EMAIL_PATTERN.match(email):
            return False
        return True
        
    @classmethod
    def is_student_email(cls, email: str) -> bool:
        if not cls.is_valid_email(email):
            return False
        return email.lower().endswith(cls.UNI_STUDENT_DOMAIN)
        
    @classmethod
    def is_valid_password(cls, password: str) -> tuple[bool, str]:
        """
        Validates password strength.
        Returns: (bool, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit."
        if not any(c.isalpha() for c in password):
            return False, "Password must contain at least one letter."
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
            return False, "Password must contain at least one special character."
        return True, "Password is strong."
        
    @classmethod
    def is_valid_registration_number(cls, reg_num: str) -> bool:
        """
        Validates University of Vavuniya registration numbers (e.g. '2021/ICT/80')
        """
        if not reg_num:
            return False
        return bool(cls.REG_NUM_PATTERN.match(reg_num.strip().upper()))
        
    @classmethod
    def is_valid_gpa(cls, gpa_str: str) -> bool:
        try:
            val = float(gpa_str)
            return 0.0 <= val <= 4.0
        except ValueError:
            return False
            
    @classmethod
    def is_non_empty(cls, value: str) -> bool:
        return bool(value and value.strip())
