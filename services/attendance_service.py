import os

class AttendanceService:
    """Mock service for attendance data.
    In a real deployment this would query a database (e.g., Firestore).
    """
    _attendance = {}

    @classmethod
    def get_attendance(cls, student_uid: str) -> dict:
        """Return mock attendance data for a student.
        The dict maps subject name to a tuple (attended_sessions, total_sessions).
        """
        if student_uid not in cls._attendance:
            cls._attendance[student_uid] = {
                "Mathematics": (28, 30),
                "Physics": (25, 30),
                "Computer Science": (27, 30),
                "Chemistry": (20, 30),
                "English": (30, 30),
            }
        return cls._attendance[student_uid]

    @classmethod
    def update_attendance(cls, student_uid: str, subject: str, attended: int, total: int):
        """Update attendance record for a student's subject."""
        # Ensure student entry exists
        cls.get_attendance(student_uid)
        cls._attendance[student_uid][subject] = (attended, total)

    @staticmethod
    def calculate_percentage(attendance_dict: dict) -> float:
        total_attended = sum(v[0] for v in attendance_dict.values())
        total_sessions = sum(v[1] for v in attendance_dict.values())
        if total_sessions == 0:
            return 0.0
        return (total_attended / total_sessions) * 100

    @staticmethod
    def subjects_at_risk(attendance_dict: dict, threshold: float = 75.0) -> list:
        at_risk = []
        for subject, (attended, total) in attendance_dict.items():
            if total == 0:
                continue
            percent = (attended / total) * 100
            if percent < threshold:
                at_risk.append({"subject": subject, "percentage": percent})
        return at_risk
