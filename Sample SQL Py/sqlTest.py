import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

sql = "INSERT INTO Users (user_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
val = [
    ("3", "Mille", "Berg", "bergm1@findlay.edu"),
    ("4", "Person4", "Smith", "smithp4@findlay.edu"),
    ("5", "Person5", "Smith", "smithp5@findlay.edu")
    ]

# Use this for 1 insertion
# cursor.execute(sql, val)

# Use this for many insertions
cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")