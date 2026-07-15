import time
from typing import Dict, List, Any

class CafeteriaService:
    _menu: List[Dict[str, Any]] = [
        {"id": "m1", "name": "Chicken Rice & Curry", "category": "Lunch", "price": 350.0, "available": True},
        {"id": "m2", "name": "Vegetarian Rice & Curry", "category": "Lunch", "price": 250.0, "available": True},
        {"id": "m3", "name": "Egg Hopper", "category": "Breakfast", "price": 50.0, "available": True},
        {"id": "m4", "name": "Kiribath (Milk Rice) with Lunu Miris", "category": "Breakfast", "price": 120.0, "available": True},
        {"id": "m5", "name": "Samosa", "category": "Snacks", "price": 40.0, "available": True},
        {"id": "m6", "name": "Milk Tea", "category": "Beverages", "price": 70.0, "available": True},
        {"id": "m7", "name": "Plain Coffee", "category": "Beverages", "price": 60.0, "available": True}
    ]

    _orders: List[Dict[str, Any]] = []
    _feedback: List[Dict[str, Any]] = [
        {"id": "f1", "student_name": "Jane Doe", "rating": 5, "comment": "Great food and quick pickup service!", "timestamp": int(time.time()) - 3600}
    ]

    @classmethod
    def get_menu(cls) -> List[Dict[str, Any]]:
        return cls._menu

    @classmethod
    def update_menu_item(cls, item_id: str, name: str, category: str, price: float, available: bool) -> bool:
        for item in cls._menu:
            if item["id"] == item_id:
                item["name"] = name.strip()
                item["category"] = category.strip()
                item["price"] = float(price)
                item["available"] = bool(available)
                return True
        return False

    @classmethod
    def add_menu_item(cls, name: str, category: str, price: float) -> str:
        new_id = f"m{len(cls._menu) + 1}"
        cls._menu.append({
            "id": new_id,
            "name": name.strip(),
            "category": category.strip(),
            "price": float(price),
            "available": True
        })
        return new_id

    @classmethod
    def delete_menu_item(cls, item_id: str) -> bool:
        for item in cls._menu:
            if item["id"] == item_id:
                cls._menu.remove(item)
                return True
        return False

    @classmethod
    def place_pre_order(cls, student_uid: str, items: List[Dict[str, Any]], total_price: float, pickup_time: str) -> Dict[str, Any]:
        new_id = f"ord_{len(cls._orders) + 1001}"
        order = {
            "id": new_id,
            "student_uid": student_uid,
            "items": items,
            "total_price": total_price,
            "pickup_time": pickup_time,
            "status": "Pending",
            "timestamp": int(time.time())
        }
        cls._orders.append(order)
        return order

    @classmethod
    def get_student_orders(cls, student_uid: str) -> List[Dict[str, Any]]:
        return [ord for ord in cls._orders if ord["student_uid"] == student_uid]

    @classmethod
    def get_all_orders(cls) -> List[Dict[str, Any]]:
        return cls._orders

    @classmethod
    def update_order_status(cls, order_id: str, status: str) -> bool:
        for ord in cls._orders:
            if ord["id"] == order_id:
                ord["status"] = status
                return True
        return False

    @classmethod
    def submit_feedback(cls, student_name: str, rating: int, comment: str):
        cls._feedback.append({
            "id": f"f{len(cls._feedback) + 1}",
            "student_name": student_name.strip() or "Anonymous Student",
            "rating": int(rating),
            "comment": comment.strip(),
            "timestamp": int(time.time())
        })

    @classmethod
    def get_all_feedback(cls) -> List[Dict[str, Any]]:
        return cls._feedback
