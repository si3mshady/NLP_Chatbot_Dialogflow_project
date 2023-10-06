import mysql.connector as mysql

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
                   "VALUES (1, 'Donut', 2.50), (2, 'Pigs in a Blanket', 4.00), "
                   "(3, 'Burrito', 5.50), (4, 'Shake', 3.00), (5, 'Sandwich', 4.50), (6, 'Pancake', 3.25);")

    cursor.execute("CREATE TABLE `orders` ("
                   "order_id int AUTO_INCREMENT PRIMARY KEY,"
                   "item_id int NULL,"
                   "session_id VARCHAR(255),"
                   "quantity int DEFAULT NULL,"
                   "total_price decimal(10,2) DEFAULT NULL"
                   ");")

    # Remove the code for fetching rows from the "orders" table
    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    db_setup()