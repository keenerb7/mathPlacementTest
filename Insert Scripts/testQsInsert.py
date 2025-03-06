import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

sql = "INSERT INTO Test_Questions (test_id, question_id) VALUES (%s, %s)"
val = [
    ("1", "1"),
    ("1", "2"),
    ("1", "3")
    ]

# Use this for 1 insertion
# cursor.execute(sql, val)

# Use this for many insertions
cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")