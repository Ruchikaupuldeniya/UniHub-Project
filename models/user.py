from typing import Any, Dict

class User:
    def __init__(self, uid: str, email: str, role: str, created_at: int):
        self.uid = uid
        self.email = email
        self.role = role
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            uid=data.get("uid", ""),
            email=data.get("email", ""),
            role=data.get("role", "student"),
            created_at=data.get("created_at", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }
