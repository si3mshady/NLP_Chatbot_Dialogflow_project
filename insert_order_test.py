import mysql.connector as mysql
from fastapi.responses import JSONResponse

def print_all_items_in_orders():
    try:
        cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor(dictionary=True)

        # Retrieve all items from the orders table
        cursor.execute("SELECT * FROM orders")

        orders = cursor.fetchall()

        for order in orders:
            order_id = order['order_id']
            item_id = order['item_id']
            quantity = order['quantity']
            total_price = order['total_price']

            print(f"Order ID: {order_id}, Item ID: {item_id}, Quantity: {quantity}, Total Price: {total_price}")

        cursor.close()
        cnx.close()

    except mysql.Error as err:
        print(f"Error: {err}")


def insert_order(order_data: list, session_id: str):
    print(order_data)
    try:
        cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor()

        # Insert a new order for the session and get the order ID
        cursor.execute("INSERT INTO orders (session_id) VALUES (%s)", (session_id,))
        order_id = cursor.lastrowid  # Get the last inserted order ID

        for item in order_data:
            item_name = item['item_name']
            quantity = item['quantity']

            # Retrieve the item_id based on the item_name
            cursor.execute("SELECT item_id FROM food_items WHERE name = %s", (item_name,))
            item_id = cursor.fetchone()

            if item_id:
                item_id = item_id[0]
                total_price = None  # You can calculate the total price based on item price and quantity here

                # Insert the item into the order
                cursor.execute("INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                               (order_id, item_id, quantity, total_price))

                cnx.commit()  # Commit the transaction
        print_all_items_in_orders()
        cursor.close()
        cnx.close()

        resp = {
            "fulfillmentText": f"Order inserted successfully! Order ID: {order_id}"
        }

        return JSONResponse(content=resp)

    except mysql.Error as err:
        print(f"Error: {err}")
        cnx.rollback()  # Rollback the transaction in case of an error


print_all_items_in_orders()