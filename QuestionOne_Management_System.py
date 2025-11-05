# Maama Fina Restaurant Management System - OOP Professional
# Author: Gloria Nalubega Nambooze
# Date: 05-Nov-2025
# ---------------------------------------------
# This system manages menu items, orders (dining and takeout), payments, and inventory.
# Uses a menu-driven interface designed for clarity and ease of use.
# Ingredients are deducted from inventory per recipe when orders are placed.

class MenuItem:
    """Represents a single menu item with a name and price."""
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Menu:
    """Handles CRUD operations for the restaurant's menu."""
    def __init__(self):
        self.items = {}

    def display_menu(self):
        """Display all menu items with numeric indexing and prices."""
        if not self.items:
            print("Menu is currently empty.\n")
            return
        print("\n----- MENU -----")
        for i, (name, item) in enumerate(self.items.items(), start=1):
            print(f"{i}. {name}: UGX {item.price:.2f}")
        print(f"{len(self.items)+1}. Return to Main Menu")
        print("----------------")

    def select_item(self, action="select"):
        """Prompt user to select a menu item by number, or return None to go back."""
        if not self.items:
            print("Menu is empty.\n")
            return None
        while True:
            self.display_menu()
            choice = input(f"Select item number to {action}: ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.items):
                    return list(self.items.keys())[choice_num-1]
                elif choice_num == len(self.items)+1:
                    return None
            print("Invalid selection. Please enter a valid number.\n")

    def add_item(self):
        """Add a new meal to the menu."""
        print("\n--- Add New Meal ---")
        name = input("Enter new meal name (or '0' to cancel): ").strip()
        if name == "0":
            return
        if name in self.items:
            print("That meal already exists. Try updating it instead.\n")
            return
        while True:
            price_input = input("Enter price (UGX): ").strip()
            try:
                price = float(price_input)
                if price <= 0:
                    print("Price must be positive.\n")
                    continue
                break
            except ValueError:
                print("Invalid price. Please enter a numeric value.\n")
        self.items[name] = MenuItem(name, round(price, 2))
        print(f"'{name}' added successfully to the menu.\n")

    def update_item(self):
        """Update the price of an existing meal."""
        print("\n--- Update Meal Price ---")
        item_name = self.select_item("update")
        if not item_name:
            return
        while True:
            price_input = input(f"Enter new price for '{item_name}': ").strip()
            try:
                price = float(price_input)
                if price <= 0:
                    print("Price must be positive.\n")
                    continue
                break
            except ValueError:
                print("Invalid price. Please enter a numeric value.\n")
        self.items[item_name].price = round(price, 2)
        print(f"'{item_name}' price updated successfully.\n")

    def delete_item(self):
        """Delete a meal from the menu."""
        print("\n--- Delete Meal ---")
        item_name = self.select_item("delete")
        if not item_name:
            return
        confirm = input(f"Are you sure you want to delete '{item_name}'? (y/n): ").strip().lower()
        if confirm == "y":
            del self.items[item_name]
            print(f"'{item_name}' removed from the menu.\n")
        else:
            print("Deletion cancelled.\n")

class Inventory:
    """Manages raw materials stock and updates stock levels."""
    def __init__(self):
        self.stock = {
            "Rice (kg)": 10.0,
            "Beef (kg)": 5.0,
            "Eggs (units)": 30,
            "Chicken (kg)": 8.0,
            "Matooke (kg)": 10,
            "Posho (kg)": 7,
            "Beans (kg)": 6
        }

    def view_stock(self):
        """Display current inventory stock in a numbered list."""
        print("\n----- INVENTORY STOCK -----")
        for i, (item, qty) in enumerate(self.stock.items(), start=1):
            print(f"{i}. {item}: {qty}")
        print(f"{len(self.stock)+1}. Return to Main Menu")
        print("---------------------------")

    def select_item(self, action="restock"):
        """Enable selection of an inventory item by number."""
        while True:
            self.view_stock()
            choice = input(f"Select item number to {action}: ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.stock):
                    return list(self.stock.keys())[choice_num-1]
                elif choice_num == len(self.stock)+1:
                    return None
            print("Invalid selection. Please choose a valid number.\n")

    def restock_item(self):
        """Add quantity to existing stock with proper input validation."""
        print("\n--- Restock Inventory ---")
        item = self.select_item()
        if not item:
            return
        while True:
            qty_input = input(f"Enter quantity to add to '{item}': ").strip()
            try:
                qty = float(qty_input)
                if qty <= 0:
                    print("Quantity must be positive.\n")
                    continue
                self.stock[item] += qty
                print(f"'{item}' restocked successfully. New quantity: {self.stock[item]:.2f}\n")
                break
            except ValueError:
                print("Invalid quantity. Please enter a number.\n")

    def check_and_deduct(self, recipe):
        """
        Check if all ingredients are in stock for the given recipe.
        Deduct stock if sufficient; otherwise, notify user and cancel.
        """
        for ingredient, required_qty in recipe.items():
            if self.stock.get(ingredient, 0) < required_qty:
                print(f"Insufficient {ingredient}. Needed: {required_qty}, Available: {self.stock.get(ingredient, 0)}")
                return False
        # Deduct ingredients after confirmation
        for ingredient, required_qty in recipe.items():
            self.stock[ingredient] -= required_qty
        return True

class Order:
    """Represents a customer's order containing items and computing total cost."""
    def __init__(self, order_type):
        self.type = order_type  # 'dining' or 'takeout'
        self.items = {}  # {meal_name: quantity}
        self.total = 0.0

    def add_item(self, menu_item, quantity):
        """Add quantity of a menu item to the order and update total price."""
        self.items[menu_item.name] = self.items.get(menu_item.name, 0) + quantity
        self.total += menu_item.price * quantity

    def display(self, number):
        """Print details for a specific order."""
        print(f"Order {number} ({self.type.capitalize()}):")
        for name, qty in self.items.items():
            print(f"  {name}: {qty} unit(s)")
        print(f"  Total: UGX {self.total:.2f}\n")

class RestaurantSystem:
    """Main application class orchestrating menu, order, payment, and inventory management."""

    def __init__(self):
        self.menu = Menu()
        self.inventory = Inventory()
        self.orders = []

        # Initialize menu with sample meals
        initial_menu = {
            "Posho and Beans": 5000,
            "Chapati and Eggs": 4000,
            "Matooke and Beef": 7000,
            "Rice and Chicken": 8000
        }
        for name, price in initial_menu.items():
            self.menu.items[name] = MenuItem(name, price)

        # Define recipes used to track inventory usage per meal ordered
        self.recipes = {
            "Posho and Beans": {"Posho (kg)": 0.5, "Beans (kg)": 0.3},
            "Chapati and Eggs": {"Eggs (units)": 2, "Rice (kg)": 0.1},
            "Matooke and Beef": {"Matooke (kg)": 0.5, "Beef (kg)": 0.3},
            "Rice and Chicken": {"Rice (kg)": 0.5, "Chicken (kg)": 0.3}
        }

    def place_order(self):
        """Handle placement of dining or takeout orders with quantity and stock validation."""
        print("\n--- Place Order ---")
        while True:
            print("1. Dining")
            print("2. Takeout")
            print("3. Return to Main Menu")
            choice = input("Select order type: ").strip()
            if choice == "3":
                return
            elif choice == "1":
                order_type = "dining"
                break
            elif choice == "2":
                order_type = "takeout"
                break
            else:
                print("Invalid selection. Please try again.\n")

        order = Order(order_type)
        while True:
            item_name = self.menu.select_item("order")
            if not item_name:
                break

            while True:
                qty_input = input(f"Enter quantity for '{item_name}': ").strip()
                try:
                    qty = int(qty_input)
                    if qty <= 0:
                        print("Quantity must be greater than zero.\n")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Enter a whole number.\n")

            # Ensure sufficient inventory before adding items
            added_all = True
            if item_name in self.recipes:
                # Multiply recipe quantities by ordered amount
                required = {k: v * qty for k, v in self.recipes[item_name].items()}
                if not self.inventory.check_and_deduct(required):
                    print(f"Cannot add '{item_name}' - insufficient stock for requested quantity.\n")
                    added_all = False
            
            if added_all:
                order.add_item(self.menu.items[item_name], qty)
                print(f"Added {qty} x '{item_name}' to order.\n")

            cont = input("Add more items? (y/n): ").strip().lower()
            if cont != "y":
                break

        if order.items:
            self.orders.append(order)
            print("\n----- ORDER RECEIVED -----")
            for name, qty in order.items.items():
                price_each = self.menu.items[name].price
                print(f"{name}: {qty} unit(s) @ UGX {price_each:.2f} each")
            print(f"Total: UGX {order.total:.2f}")
            print("--------------------------\n")
        else:
            print("No valid items were added to the order.\n")

    def view_orders(self):
        """Display all active orders with details."""
        if not self.orders:
            print("No active orders at the moment.\n")
            return
        for i, order in enumerate(self.orders, start=1):
            order.display(i)

    def process_payment(self):
        """Allow user to select an active order to process payment and print receipt."""
        if not self.orders:
            print("No active orders available for payment.\n")
            return

        print("\n--- Process Payment ---")
        while True:
            for i, order in enumerate(self.orders, start=1):
                print(f"{i}. Order {i} ({order.type.capitalize()}), Total: UGX {order.total:.2f}")
            print(f"{len(self.orders)+1}. Return to Main Menu")
            choice = input("Select order number to process payment: ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.orders):
                    order = self.orders.pop(choice_num-1)
                    break
                elif choice_num == len(self.orders)+1:
                    return
            print("Invalid selection. Please choose a valid order number.\n")

        print("\n----- RECEIPT -----")
        print(f"Order Type: {order.type.capitalize()}")
        print(f"{'Item':20} {'Qty':>3} {'Unit Price':>12} {'Subtotal':>12}")
        for name, qty in order.items.items():
            unit_price = self.menu.items[name].price
            subtotal = unit_price * qty
            print(f"{name:20} {qty:>3} {unit_price:>12.2f} {subtotal:>12.2f}")
        print(f"{'Total':>49}: UGX {order.total:.2f}")

        while True:
            paid_input = input("Enter amount paid (UGX): ").strip()
            try:
                paid = float(paid_input)
                if paid < order.total:
                    print("Insufficient payment amount. Please enter at least the total.\n")
                    continue
                change = paid - order.total
                print(f"Payment accepted. Change: UGX {change:.2f}\n")
                break
            except ValueError:
                print("Invalid amount. Please enter a numeric value.\n")
        print("-------------------\n")

    def main_menu(self):
        """Main menu loop presenting options to the user with direct prompts."""
        while True:
            print("\n----- Maama Fina Restaurant System -----")
            print("1. View Menu")
            print("2. Add New Meal")
            print("3. Update Meal Price")
            print("4. Delete Meal")
            print("5. Place Order")
            print("6. View Orders")
            print("7. Process Payment")
            print("8. View Inventory Stock")
            print("9. Restock Inventory")
            print("0. Exit")
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.menu.display_menu()
            elif choice == "2":
                self.menu.add_item()
            elif choice == "3":
                self.menu.update_item()
            elif choice == "4":
                self.menu.delete_item()
            elif choice == "5":
                self.place_order()
            elif choice == "6":
                self.view_orders()
            elif choice == "7":
                self.process_payment()
            elif choice == "8":
                self.inventory.view_stock()
            elif choice == "9":
                self.inventory.restock_item()
            elif choice == "0":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid selection. Please choose a valid option.\n")

if __name__ == "__main__":
    system = RestaurantSystem()
    system.main_menu()
