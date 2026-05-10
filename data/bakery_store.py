import json
from pathlib import Path

class BakeryStore:
    def __init__(self, data_folder: Path):
        self.inventory_path = data_folder / "inventory.json"
        self.orders_path = data_folder / "orders.json"
        self.users_path = data_folder / "users.json"


    # Inventory
    def load_inventory(self):

        if self.inventory_path.exists():
            with open(self.inventory_path, "r") as f:
                return json.load(f)
        return []
    
    def save_inventory(self, inventory):
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)


    # Orders
    def load_orders(self):
        if self.orders_path.exists():
            with open(self.orders_path, "r") as f:
                return json.load(f)
        return []
    
    def save_orders(self, orders):
        with open(self.orders_path, "w") as f:
            json.dump(orders, f, indent=4)


    # Users
    def load_users(self):

        if self.users_path.exists():
            with open(self.users_path, "r") as f:
                return json.load(f)
        return []
    
    def save_users(self, users):

        with open(self.users_path, "w") as f:
            json.dump(users, f, indent=4)