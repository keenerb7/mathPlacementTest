import mysql.connector

cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm',
                              host='sql5.freesqldatabase.com',
                              database='sql5764680')

cursor = cnx.cursor()

'''
sql = "INSERT INTO Question_Categories (category_id, category_name) VALUES (%s, %s)"
val = [
    ("1", "Algebra Test")
]

cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")

sql = "INSERT INTO Questions (question_id, question, category_id, question_difficulty) VALUES (%s, %s, %s, %s)"
val = [
    ("1", "Solve the equation $5y-2 = 2x+3$ for $y$.", "1", "3"),
    ("2", "Find the slope and the y-intercept of the line $3x-5y-9=0$.", "1", "4"),
    ("3", "In a calculus class, 15 of the students play soccer. Find the total number of students in the class if 3 out of every 5 play soccer.", "1", "4")
    ]

# Use this for 1 insertion
# cursor.execute(sql, val)

# Use this for many insertions
cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")

cursor.execute("ALTER TABLE Question_Choices MODIFY choice_id VARCHAR(3)")

sql = "INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct) VALUES (%s, %s, %s, %s)"
val = [
    ("1a", "1", "$y = 2x$", "FALSE"),
    ("1b", "1", "$y = 2/5 x + 2/5$", "FALSE"),
    ("1c", "1", "$y = 2x + 1$" , "FALSE"),
    ("1d", "1", "$y = 2/5 x + 1$", "TRUE"),
    ("1e", "1", "$y = 1", "FALSE"),
    ("2a", "2", "$m = 5/3, b = 3$", "FALSE"),
    ("2b", "2", "$m = -3, b = 4$", "FALSE"),
    ("2c", "2", "$m = 3, b = -14$" , "FALSE"),
    ("2d", "2", "$m = 5/3, b = 9/5$", "FALSE"),
    ("2e", "2", "$m = 5/3, b = -9/5", "TRUE"),
    ("3a", "3", "$25$", "TRUE"),
    ("3b", "3", "$9$", "FALSE"),
    ("3c", "3", "$45/8" , "FALSE"),
    ("3d", "3", "$40$", "FALSE"),
    ("3e", "3", "$21", "FALSE"),
    ]

cursor.executemany(sql, val)

cnx.commit()

print(cursor.rowcount, "record inserted.")
'''

sql = "UPDATE Question_Choices SET is_correct = 1 WHERE choice_id = '1d';"
cursor.execute(sql)
cnx.reconnect(attempts=3, delay=2)
cnx.commit()
print(cursor.rowcount, "record(s) affected")