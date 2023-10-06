import mysql.connector as mysql

def main():
    cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='127.0.0.1', 
        port=3306
    )
    cursor = cnx.cursor()

    cursor.execute("CREATE TABLE food_items (  id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, price DECIMAL(10, 2) NOT NULL);")

    cursor.execute("INSERT INTO food_items (name, price) VALUES ('Donut', 2.50), ('Pigs in a Blanket', 4.00),('Burrito', 5.50),('Shake', 3.00),('Sandwich', 4.50), ('Pancake', 3.25);")
    

    cursor.execute("SELECT * FROM food_items")
    for row in cursor.fetchall():
        print(row)
    
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()