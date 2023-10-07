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

        return f"Order ID: {order_id}, Item ID: {item_id}, Quantity: {quantity}, Total Price: {total_price}"

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
    print(f"The result of insert_ order is {result}")

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1


def insert_order(order_data: list, session_id: str, current_order_id: int):
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
        # order_id = get_next_order_id()

        # print(f"The order id is {current_order_id}")
        # Insert a new order for the session and get the order ID
        # cursor.execute("INSERT INTO orders (session_id) VALUES (%s)", (session_id,))
        # Executing the SQL query to get the next available order_id
        
        for item in order_data:
            item_name = item['item_name']
            quantity = item['quantity']

            
            # print(item_name)
            # Retrieve the item_id based on the item_name
            cursor.execute("SELECT item_id, price FROM food_items WHERE name = %s", (item_name,))

            item_data = cursor.fetchone()

            print(f'here is item id ',item_data)
        

            if item_data:
                item_id = item_data['item_id']
                item_price = item_data['price']

                total_price = float(item_price) * int(quantity)  # Calculate the total price
                cursor.execute(
                    "INSERT INTO orders (order_id, item_id, session_id, quantity, total_price) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (int(current_order_id), item_id, session_id, quantity, float (total_price))
                )

                cnx.commit()
                # print('inside line 61')
                # item_id = item_id['item_id']
            
                # total_price = None  # You can calculate the total price based on item price and quantity here
                # print(current_order_id, item_id, session_id, quantity, total_price)
                # print("total cost ", quantity * total_price)
                
                # # Insert the item into the order
                # cursor.execute("INSERT INTO orders (order_id, item_id, session_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                #                (int(current_order_id), item_id, session_id, quantity))

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

import mysql.connector as mysql

def database_init():
    db_setup()

def delete_items_from_order(order_id, food_name):
    try:
        cnx = mysql.connect(
            user='user',
            password='password',
            database='mysql',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor()

        # Get the item_id of the food_name to be deleted
        cursor.execute("SELECT item_id FROM food_items WHERE name = %s", (food_name,))
        item_id = cursor.fetchone()

        if item_id:
            item_id = item_id[0]

            # Delete the item from the order
            cursor.execute("DELETE FROM orders WHERE order_id = %s AND item_id = %s", (order_id, item_id))
            cnx.commit()
            print(f"Deleted {food_name} from order {order_id}")
            return f"Deleted {food_name} from order {order_id}"

        else:
            print(f"{food_name} not found in food_items table")

        cursor.close()
        cnx.close()

    except mysql.Error as err:
        print(f"Error: {err}")



def db_setup():
    cnx = mysql.connect(
        user='user',
        password='password',
        database='mysql',
        host='127.0.0.1',
        port=3306
    )
    cursor = cnx.cursor()

    cursor.execute("DROP TABLE IF EXISTS `food_items`;")
    cursor.execute("DROP TABLE IF EXISTS `orders`;")

    cursor.execute("CREATE TABLE `food_items` ("
                   "item_id int PRIMARY KEY,"
                   "name VARCHAR(255) DEFAULT NULL,"
                   "price DECIMAL(10, 2) DEFAULT NULL"
                   ");")
    

    cursor.execute("INSERT INTO `food_items` (item_id, name, price) "
                   "VALUES (1, 'donuts', 2.50), (2, 'pig in blanket', 4.00), "
                   "(3, 'burrito', 5.50), (4, 'shake', 3.00), (5, 'sandwich', 4.50), (6, 'pancake', 3.25);")

    cursor.execute("CREATE TABLE `orders` ("
                   "order_id int NULL,"
                   "item_id int  NULL,"
                   "session_id TEXT NULL,"
                   "quantity int DEFAULT NULL,"
                   "total_price decimal(10,2) DEFAULT NULL"
                   ");")
            

    # Remove the code for fetching rows from the "orders" table
    cursor.execute("SELECT * FROM food_items")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    cnx.close()



print_all_items_in_orders()