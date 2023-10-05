class OrderSystem:
    def __init__(self):
        self.food_items = {
            'Donut': 2.50,
            'Pigs in a Blanket': 4.00,
            'Burrito': 5.50,
            'Shake': 3.00,
            'Sandwich': 4.50,
            'Pancake': 3.25,
        }
        self.orders = {}  # Dictionary to store orders with session IDs as keys

    def process_order(self, session_id, food_items, quantities):
        if session_id not in self.orders:
            self.orders[session_id] = {}  # Create a new session if it doesn't exist

        total = 0.0
        message = "Order Summary:\n"

        for item, quantity in zip(food_items, quantities):
            if item in self.food_items and quantity > 0:
                price = self.food_items[item]
                total += price * quantity

                # Update or create the order for the session
                self.orders[session_id][item] = {
                    'quantity': quantity,
                    'price': price,
                }

                message += f"{quantity} {item}(s) - ${price * quantity:.2f}\n"
            else:
                return "Invalid item or quantity."

        message += f"Total: ${total:.2f}"
        return message

    def update_order(self, session_id, item, new_quantity):
        if session_id in self.orders and item in self.orders[session_id]:
            if new_quantity > 0:
                price = self.food_items[item]
                self.orders[session_id][item]['quantity'] = new_quantity
                self.orders[session_id][item]['price'] = price * new_quantity
                return f"Updated {item} quantity to {new_quantity}."
            else:
                return "Quantity must be greater than 0."
        else:
            return f"{item} not found in the order."

    def delete_order(self, session_id, item):
        if session_id in self.orders and item in self.orders[session_id]:
            del self.orders[session_id][item]
            return f"Removed {item} from the order."
        else:
            return f"{item} not found in the order."

    def get_order_summary(self, session_id):
        if session_id in self.orders:
            order_details = self.orders[session_id]
            total = sum(order['price'] for order in order_details.values())
            message = "Order Summary:\n"
            for item, details in order_details.items():
                message += f"{details['quantity']} {item}(s) - ${details['price']:.2f}\n"
            message += f"Total: ${total:.2f}"
            return message
        else:
            return "No orders yet for this session."


# Example usage:
order_system = OrderSystem()
session_id = "2dd4ba28-bb88-ee42-a23c-13cc189b4b3d"

# Process an order
food_items = ["Donut", "Shake", "Sandwich"]
quantities = [3, 3, 3]
print(order_system.process_order(session_id, food_items, quantities))

# Update an order
new_quantity = 2
item_to_update = "Donut"
print(order_system.update_order(session_id, item_to_update, new_quantity))

# Delete an order
item_to_delete = "Shake"
print(order_system.delete_order(session_id, item_to_delete))

# Get the order summary
print(order_system.get_order_summary(session_id))
