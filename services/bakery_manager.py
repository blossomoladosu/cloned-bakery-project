import uuid
from typing import List, Dict, Optional


class BakeryManager:
    def __init__(self, inventory: List[Dict], users: List[Dict], orders: List[Dict]) -> None:
        self.inventory = inventory
        self.users = users
        self.orders = orders

    def find_user(self, email: str, password: str) -> Optional[Dict]:
        for user in self.users:
            if user["email"].strip().lower() == email.strip().lower() and user["password"] == password:
                return user
        return None

    def register_customer(self, full_name: str, email: str, password: str):
        if not full_name or not email or not password:
            return "Please fill in all fields."

        for user in self.users:
            if user["email"].lower() == email.lower():
                return "An account with that email already exists."

        new_user = {
            "id": str(uuid.uuid4()),
            "full_name": full_name,
            "email": email,
            "password": password,
            "role": "Customer"
        }

        self.users.append(new_user)
        return "Success"

    def all_inventory(self) -> List[Dict]:
        return list(self.inventory)

    def all_orders(self) -> List[Dict]:
        return list(self.orders)

    def find_item_by_id(self, item_id: str) -> Optional[Dict]:
        for item in self.inventory:
            if item["item_id"] == item_id:
                return item
        return None

    def find_item_by_name(self, item_name: str) -> Optional[Dict]:
        for item in self.inventory:
            if item["name"] == item_name:
                return item
        return None

    def add_to_cart(self, cart: List[Dict], selected_item: Dict, quantity: int):
        if quantity > selected_item["stock"]:
            return "Not enough stock available."

        cart.append({
            "item_id": selected_item["item_id"],
            "item_name": selected_item["name"],
            "price": selected_item["price"],
            "quantity": quantity
        })

        return "Success"

    def checkout(self, cart: List[Dict], user_email: str):
        for cart_item in cart:
            item = self.find_item_by_id(cart_item["item_id"])

            if item is None:
                return "Item not found."

            if cart_item["quantity"] > item["stock"]:
                return "Not enough stock available."

            item["stock"] -= cart_item["quantity"]

            self.orders.append({
                "id": str(uuid.uuid4()),
                "customer_email": user_email,
                "item_id": cart_item["item_id"],
                "item_name": cart_item["item_name"],
                "quantity": cart_item["quantity"],
                "status": "Placed",
                "total": round(cart_item["price"] * cart_item["quantity"], 2)
            })

        return "Success"

    def find_orders_by_customer(self, email: str) -> List[Dict]:
        return [order for order in self.orders if order["customer_email"] == email]

    def find_placed_orders_by_customer(self, email: str) -> List[Dict]:
        return [
            order for order in self.orders
            if order["customer_email"] == email and order["status"] == "Placed"
        ]

    def update_order_quantity(self, order_id: str, new_quantity: int):
        for order in self.orders:
            if order["id"] == order_id:
                item = self.find_item_by_name(order["item_name"])

                if item is None:
                    return "Item not found."

                item["stock"] += order["quantity"]

                if new_quantity > item["stock"]:
                    item["stock"] -= order["quantity"]
                    return "Not enough stock available."

                item["stock"] -= new_quantity
                order["quantity"] = new_quantity
                order["total"] = round(new_quantity * item["price"], 2)

                return "Success"

        return "Order not found."

    def cancel_order(self, order_id: str):
        for order in self.orders:
            if order["id"] == order_id:
                order["status"] = "Cancelled"

                item = self.find_item_by_name(order["item_name"])
                if item:
                    item["stock"] += order["quantity"]

                return "Success"

        return "Order not found."

    def restock_inventory(self, item_name: str, add_quantity: int):
        item = self.find_item_by_name(item_name)

        if item is None:
            return "Item not found."

        item["stock"] += add_quantity

        return "Success"

    def update_order_status(self, order_id: str, new_status: str):
        for order in self.orders:
            if order["id"] == order_id:
                order["status"] = new_status
                return "Success"

        return "Order not found."