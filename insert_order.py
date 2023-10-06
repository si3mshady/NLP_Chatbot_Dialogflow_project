import mysql.connector as mysql

def insert_order(order_data):
    try:
        cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor()

        for item in order_data:
            item_name = item['item_name']
            quantity = item['quantity']

            # Retrieve the item_id based on the item_name
            cursor.execute("SELECT item_id FROM food_items WHERE name = %s", (item_name,))
            item_id = cursor.fetchone()

            if item_id:
                item_id = item_id[0]
                total_price = None  # You can calculate the total price based on item price and quantity here

                # Insert the order into the orders table
                cursor.execute("INSERT INTO orders (item_id, quantity, total_price) VALUES (%s, %s, %s)",
                               (item_id, quantity, total_price))

                cnx.commit()  # Commit the transaction

        cursor.close()

        # Fetch and display the inserted orders
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        inserted_orders = cursor.fetchall()

        for order in inserted_orders:
            print(f"Order ID: {order['order_id']}, Item ID: {order['item_id']}, Quantity: {order['quantity']}, Total Price: {order['total_price']}")

        cnx.close()
        print("Orders inserted successfully!")

    except mysql.Error as err:
        print(f"Error: {err}")
        cnx.rollback()  # Rollback the transaction in case of an error

if __name__ == "__main__":
    order_data = [{'item_name': 'shakes', 'quantity': 4.0}, {'item_name': 'pancake', 'quantity': 4.0}]
    insert_order(order_data)
