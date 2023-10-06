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

    cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    cursor.execute("INSERT INTO test VALUES (2, 'bla')")
    cursor.execute("INSERT INTO test VALUES (3, 'blabla')")
    cursor.execute("INSERT INTO test VALUES (4, 'blablabla')")

    cursor.execute("SELECT * FROM test")
    for row in cursor.fetchall():
        print(row)
    
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()