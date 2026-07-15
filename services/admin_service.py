import time
from typing import Dict, List, Any

class AdminService:
    _lecturers: List[Dict[str, Any]] = [
        {"id": "L1", "name": "Dr. K. Prasannah", "department": "Information & Communication Technology", "email": "prasannah@vau.ac.lk", "designation": "Senior Lecturer"},
        {"id": "L2", "name": "Prof. T. Mangaleswaran", "department": "Financial Management", "email": "tmanga@vau.ac.lk", "designation": "Professor"},
        {"id": "L3", "name": "Mrs. S. Subathini", "department": "Department of Physical Science", "email": "suba@vau.ac.lk", "designation": "Senior Lecturer Grade II"}
    ]

    _courses: List[Dict[str, Any]] = [
        {"code": "ICT 2113", "name": "Object Oriented Programming", "department": "Information & Communication Technology", "credits": 3, "lecturer": "Dr. K. Prasannah"},
        {"code": "BST 1202", "name": "Financial Accounting", "department": "Financial Management", "credits": 2, "lecturer": "Prof. T. Mangaleswaran"},
        {"code": "AMT 2213", "name": "Linear Algebra", "department": "Department of Physical Science", "credits": 3, "lecturer": "Mrs. S. Subathini"}
    ]

    _buses: List[Dict[str, Any]] = [
        {"id": "B1", "bus_no": "PB-2918", "driver": "S. Ramanathan", "route": "Vavuniya Town <-> Pampaimadu Campus", "departure": "07:30 AM", "status": "On Time"},
        {"id": "B2", "bus_no": "PB-9021", "driver": "M. Perera", "route": "Railway Station <-> Pampaimadu Campus", "departure": "08:15 AM", "status": "Delayed"},
        {"id": "B3", "bus_no": "PB-1140", "driver": "K. Selvam", "route": "Vavuniya Town <-> Pampaimadu Campus", "departure": "01:30 PM", "status": "On Time"}
    ]

    _notices: List[Dict[str, Any]] = [
        {
            "id": "N1",
            "title": "End Semester Exams Schedule",
            "content": "The end semester examinations for all faculties will commence on July 10, 2026. Please collect admission cards from the admin branch.",
            "date": "2026-06-25",
            "category": "Academic"
        },
        {
            "id": "N2",
            "title": "Annual Sports Meet Registration",
            "content": "Registrations for athletic events at the Annual Sports Meet are now open. Register at the physical education office before July 5.",
            "date": "2026-06-26",
            "category": "General"
        }
    ]

    _notes: List[Dict[str, Any]] = [
        {"id": "H1", "title": "OOP Lecture 1 - Introduction to Classes", "subject": "Object Oriented Programming", "file_link": "https://vau.ac.lk/notes/oop-intro.pdf", "uploaded_by": "Dr. K. Prasannah"},
        {"id": "H2", "title": "Linear Algebra Sheet 1 - Systems of Linear Equations", "subject": "Linear Algebra", "file_link": "https://vau.ac.lk/notes/la-sheet1.pdf", "uploaded_by": "Mrs. S. Subathini"}
    ]

    # --- LECTURERS ---
    @classmethod
    def get_lecturers(cls) -> List[Dict[str, Any]]:
        return cls._lecturers

    @classmethod
    def add_lecturer(cls, name: str, department: str, email: str, designation: str) -> str:
        new_id = f"L{len(cls._lecturers) + 1}"
        cls._lecturers.append({
            "id": new_id,
            "name": name.strip(),
            "department": department.strip(),
            "email": email.strip().lower(),
            "designation": designation.strip()
        })
        return new_id

    @classmethod
    def delete_lecturer(cls, lecturer_id: str) -> bool:
        for lec in cls._lecturers:
            if lec["id"] == lecturer_id:
                cls._lecturers.remove(lec)
                return True
        return False

    # --- COURSES ---
    @classmethod
    def get_courses(cls) -> List[Dict[str, Any]]:
        return cls._courses

    @classmethod
    def add_course(cls, code: str, name: str, department: str, credits: int, lecturer: str) -> bool:
        # Check duplicate code
        for c in cls._courses:
            if c["code"].upper() == code.strip().upper():
                return False
        cls._courses.append({
            "code": code.strip().upper(),
            "name": name.strip(),
            "department": department.strip(),
            "credits": int(credits),
            "lecturer": lecturer.strip()
        })
        return True

    @classmethod
    def delete_course(cls, code: str) -> bool:
        for c in cls._courses:
            if c["code"] == code:
                cls._courses.remove(c)
                return True
        return False

    # --- BUSES ---
    @classmethod
    def get_buses(cls) -> List[Dict[str, Any]]:
        return cls._buses

    @classmethod
    def update_bus_status(cls, bus_id: str, status: str) -> bool:
        for b in cls._buses:
            if b["id"] == bus_id:
                b["status"] = status
                return True
        return False

    @classmethod
    def add_bus(cls, bus_no: str, driver: str, route: str, departure: str) -> str:
        new_id = f"B{len(cls._buses) + 1}"
        cls._buses.append({
            "id": new_id,
            "bus_no": bus_no.strip().upper(),
            "driver": driver.strip(),
            "route": route.strip(),
            "departure": departure.strip(),
            "status": "On Time"
        })
        return new_id

    @classmethod
    def delete_bus(cls, bus_id: str) -> bool:
        for b in cls._buses:
            if b["id"] == bus_id:
                cls._buses.remove(b)
                return True
        return False

    # --- NOTICES ---
    @classmethod
    def get_notices(cls) -> List[Dict[str, Any]]:
        return cls._notices

    @classmethod
    def add_notice(cls, title: str, content: str, category: str) -> str:
        new_id = f"N{len(cls._notices) + 1}"
        cls._notices.append({
            "id": new_id,
            "title": title.strip(),
            "content": content.strip(),
            "date": time.strftime("%Y-%m-%d"),
            "category": category.strip()
        })
        return new_id

    @classmethod
    def delete_notice(cls, notice_id: str) -> bool:
        for n in cls._notices:
            if n["id"] == notice_id:
                cls._notices.remove(n)
                return True
        return False

    # --- NOTES ---
    @classmethod
    def get_notes(cls) -> List[Dict[str, Any]]:
        return cls._notes

    @classmethod
    def add_note(cls, title: str, subject: str, file_link: str, uploaded_by: str) -> str:
        new_id = f"H{len(cls._notes) + 1}"
        cls._notes.append({
            "id": new_id,
            "title": title.strip(),
            "subject": subject.strip(),
            "file_link": file_link.strip(),
            "uploaded_by": uploaded_by.strip()
        })
        return new_id

    @classmethod
    def delete_note(cls, note_id: str) -> bool:
        for h in cls._notes:
            if h["id"] == note_id:
                cls._notes.remove(h)
                return True
        return False
