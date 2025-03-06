import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

sql = "INSERT INTO User_Attempts (attempt_id, user_id, test_id, score, date_taken) VALUES (%s, %s, %s, %s, %s)"
val = [
    ("1", "1", "1", "66", "2025-03-06")
    ]

# Use this for 1 insertion
# cursor.execute(sql, val)

# Use this for many insertions
cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")