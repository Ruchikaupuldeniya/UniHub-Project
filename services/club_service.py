import os
from typing import Dict, List, Any

class ClubService:
    _clubs: List[Dict[str, Any]] = [
        {
            "id": "c1",
            "name": "IEEE Student Branch",
            "description": "Advancing technology for humanity through engineering workshops and projects.",
            "members": ["mock_student_uid"]
        },
        {
            "id": "c2",
            "name": "ACM Student Chapter",
            "description": "Fostering computing science research, hackathons, and programming contests.",
            "members": ["mock_student_uid"]
        },
        {
            "id": "c3",
            "name": "Rotaract Club of Vavuniya",
            "description": "Selfless service above self. Leadership development and community outreach.",
            "members": []
        },
        {
            "id": "c4",
            "name": "Gavel Club",
            "description": "Improving public speaking, communication, and leadership skills for students.",
            "members": []
        },
        {
            "id": "c5",
            "name": "Leo Club",
            "description": "Leadership, Experience, Opportunity. Community empowerment through charity work.",
            "members": []
        }
    ]

    _events: List[Dict[str, Any]] = [
        {
            "id": "e1",
            "title": "Tech Hackathon 2026",
            "description": "24-hour coding hackathon to solve real-world problems in student logistics and campus services.",
            "date": "2026-07-15",
            "time": "09:00 AM",
            "location": "ICT Lab 1, Pampaimadu Campus",
            "club": "ACM Student Chapter",
            "image": "/assets/tech_hackathon.png",
            "registered_users": ["mock_student_uid"],
            "reminders_enabled": []
        },
        {
            "id": "e2",
            "title": "UniHub Music Night",
            "description": "Annual acoustic and musical concert featuring student bands, choir, and cultural dances.",
            "date": "2026-08-10",
            "time": "06:00 PM",
            "location": "Main Auditorium, Vavuniya",
            "club": "Art & Music Society",
            "image": "/assets/music_night.png",
            "registered_users": [],
            "reminders_enabled": []
        },
        {
            "id": "e3",
            "title": "Annual Sports Meet",
            "description": "Inter-faculty athletics, track & field events, football, and cricket championship games.",
            "date": "2026-09-22",
            "time": "08:00 AM",
            "location": "University Main Grounds",
            "club": "Sports Club",
            "image": "/assets/sports_meet.png",
            "registered_users": [],
            "reminders_enabled": []
        }
    ]

    @classmethod
    def get_clubs(cls) -> List[Dict[str, Any]]:
        return cls._clubs

    @classmethod
    def get_events(cls) -> List[Dict[str, Any]]:
        return cls._events

    @classmethod
    def toggle_club_membership(cls, user_uid: str, club_id: str) -> bool:
        for club in cls._clubs:
            if club["id"] == club_id:
                if user_uid in club["members"]:
                    club["members"].remove(user_uid)
                else:
                    club["members"].append(user_uid)
                return True
        return False

    @classmethod
    def toggle_event_registration(cls, user_uid: str, event_id: str) -> bool:
        for event in cls._events:
            if event["id"] == event_id:
                if user_uid in event["registered_users"]:
                    event["registered_users"].remove(user_uid)
                else:
                    event["registered_users"].append(user_uid)
                return True
        return False

    @classmethod
    def toggle_event_reminder(cls, user_uid: str, event_id: str) -> bool:
        for event in cls._events:
            if event["id"] == event_id:
                if user_uid in event["reminders_enabled"]:
                    event["reminders_enabled"].remove(user_uid)
                else:
                    event["reminders_enabled"].append(user_uid)
                return True
        return False

    @classmethod
    def add_club(cls, name: str, description: str) -> str:
        new_id = f"c{len(cls._clubs) + 1}"
        cls._clubs.append({
            "id": new_id,
            "name": name.strip(),
            "description": description.strip(),
            "members": []
        })
        return new_id

    @classmethod
    def delete_club(cls, club_id: str) -> bool:
        for club in cls._clubs:
            if club["id"] == club_id:
                cls._clubs.remove(club)
                return True
        return False

    @classmethod
    def add_event(cls, title: str, description: str, date: str, time: str, location: str, club: str) -> str:
        new_id = f"e{len(cls._events) + 1}"
        cls._events.append({
            "id": new_id,
            "title": title.strip(),
            "description": description.strip(),
            "date": date.strip(),
            "time": time.strip(),
            "location": location.strip(),
            "club": club.strip(),
            "image": "/assets/tech_hackathon.png", # Default/placeholder asset
            "registered_users": [],
            "reminders_enabled": []
        })
        return new_id

    @classmethod
    def delete_event(cls, event_id: str) -> bool:
        for event in cls._events:
            if event["id"] == event_id:
                cls._events.remove(event)
                return True
        return False
