import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

sql = "INSERT INTO User_Answers (attempt_id, question_id, selected_answer, selected_answer_id, selected_answer_correct) VALUES (%s, %s, %s, %s, %s)"
val = [
    ("1", "1", "1", "1d", "1"),
    ("1", "2", "1", "2a", "0"),
    ("1", "3", "1", "3a", "1")
    ]

# Use this for 1 insertion
# cursor.execute(sql, val)

# Use this for many insertions
cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")