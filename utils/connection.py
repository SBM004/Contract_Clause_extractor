import mysql.connector

conn=mysql.connector.connect(
    database="mydb",
    user="myuser",
    password="pass",
    host="localhost"
)


# cursor=conn.cursor(buffered=True)

# cursor.execute("SHOW TABLES")
# version = cursor.fetchone()
# print("Database version:", version)

# conn.close()