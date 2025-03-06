import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

cursor. execute("SELECT * FROM `Test`")


# This is used to fetch all of the results
result = cursor.fetchall()

# This is used to fecth one of the results
# result = cursor.fetchone()

for x in result:
    print(x)

# How to Delete records from the database
# sql = "DELETE FROM Users WHERE first_name = 'Person5'"

# cursor.execute(sql)

# cnx.commit()

# print(cursor.rowcount, "record(s) deleted")