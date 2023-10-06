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

def get_next_order_id():
    cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
    # cursor = cnx.cursor(dictionary=True)
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1


def insert_order(order_data: list, session_id: str):
    # print(order_data)
    try:
        cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor(dictionary=True)
        order_id = get_next_order_id()

        print(f"The order id is {order_id}")
        # Insert a new order for the session and get the order ID
        # cursor.execute("INSERT INTO orders (session_id) VALUES (%s)", (session_id,))
        # Executing the SQL query to get the next available order_id
        
        for item in order_data:
            item_name = item['item_name']
            quantity = item['quantity']
            print(item_name)
            # Retrieve the item_id based on the item_name
            cursor.execute("SELECT item_id FROM food_items WHERE name = %s", (item_name,))
            item_id = cursor.fetchone()
            print(item_id)
        

            if item_id:
                print('inside line 61')
                item_id = item_id['item_id']
            
                total_price = None  # You can calculate the total price based on item price and quantity here
                print(order_id, item_id, session_id, quantity, total_price)
                # Insert the item into the order
                cursor.execute("INSERT INTO orders (order_id, item_id, session_id, quantity) VALUES (%s, %s, %s, %s)",
                               (order_id, item_id, session_id, quantity))

                cnx.commit()  # Commit the transaction
        print_all_items_in_orders()
        cursor.close()
        cnx.close()

        resp = {
            "fulfillmentText": f"Order inserted successfully! Order ID: {session_id}"
        }

        return JSONResponse(content=resp)

    except mysql.Error as err:
        print(f"Error: {err}")
        cnx.rollback()  # Rollback the transaction in case of an error


print_all_items_in_orders()