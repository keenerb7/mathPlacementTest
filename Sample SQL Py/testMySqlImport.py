import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

cursor.execute("SELECT * FROM Users;")

file = open("testFile.txt", "w")

rows = cursor.fetchall()
for row in rows:
    # file.write(str(row))
    print(row)

file.close()
cursor.close()
cnx.close()