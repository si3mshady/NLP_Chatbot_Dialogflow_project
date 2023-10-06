import mysql.connector as mysql
from fastapi.responses import JSONResponse

def insert_order(order_data: list):
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
        




        resp = {
            "fulfillmentText": f"Orders inserted successfully! -- all orders {str(inserted_orders)}"
        }

        return JSONResponse(content=resp)



        cnx.close()
        print("Orders inserted successfully!")

    except mysql.Error as err:
        print(f"Error: {err}")
        cnx.rollback()  # Rollback the transaction in case of an error

# if __name__ == "__main__":
 
 #need to modify this as each call shoud create 1 order not several 

#  What I am seeing currently 
#  Orders inserted successfully! -- all orders [{'order_id': 1, 'item_id': 6, 'quantity': 4, 'total_price': None}, {'order_id': 2, 'item_id': 6, 'quantity': 4, 'total_price': None}, {'order_id': 3, 'item_id': 6, 'quantity': 4, 'total_price': None}, {'order_id': 4, 'item_id': 6, 'quantity': 3, 'total_price': None}, {'order_id': 5, 'item_id': 5, 'quantity': 3, 'total_price': None}]