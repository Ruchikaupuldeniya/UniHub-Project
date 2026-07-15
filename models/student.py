from typing import Any, Dict

class Student:
    def __init__(self, uid: str, reg_num: str, name: str, faculty: str, department: str, is_active: bool = True, profile_pic: str = ""):
        self.uid = uid
        self.reg_num = reg_num.strip().upper()
        self.name = name.strip()
        self.faculty = faculty.strip()
        self.department = department.strip()
        self.is_active = is_active
        self.profile_pic = profile_pic

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        return cls(
            uid=data.get("uid", ""),
            reg_num=data.get("reg_num", ""),
            name=data.get("name", ""),
            faculty=data.get("faculty", ""),
            department=data.get("department", ""),
            is_active=data.get("is_active", True),
            profile_pic=data.get("profile_pic", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "reg_num": self.reg_num,
            "name": self.name,
            "faculty": self.faculty,
            "department": self.department,
            "is_active": self.is_active,
            "profile_pic": self.profile_pic
        }
