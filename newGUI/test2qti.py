import mysql.connector
import subprocess
from collections import defaultdict
from mainHelper import *

cnx = get_db_connection()

cursor = cnx.cursor()

# Determine the Test that we want to pull from the database
# Note this value will be hardcoded now but should be able to be changed from
# the professor GUI most likely
createTest = 1

f = open("sampleTest.txt", "w")

cursor.execute("SELECT test_title FROM Test WHERE test_id = %s", (createTest,))
result = cursor.fetchall()

# Making the Test Title in the text file
for row in result:
    f.write(f"Quiz Title: {row[0]}\n")

# This section is for quiz options
# Should have a way from GUI to change these values
f.write(f"shuffle answers: true\n")
f.write(f"show correct answers: true\n")
f.write(f"one question at a time: true\n")
f.write(f"can't go back: true\n")

# Find all the question ids for the test
cursor.execute("SELECT question_id FROM Test_Questions WHERE test_id = %s", (createTest,))
result = cursor.fetchall()
testQuestions = []
tempQs = []
for row in result:
    tempQs.append(row)

testQuestions = [item[0] for item in tempQs]

# Find all the actual questions for the test
tempQ = []
temp = []
questionsText = []
for x in testQuestions:
    cursor.execute("SELECT question_id, question FROM Questions WHERE question_id = %s", (x,))
    result = cursor.fetchall()
    for row in result:
        temp.append(row)
        tempQ.append(temp)
        temp = []

questionsText = [list(item) for sublist in tempQ for item in sublist]

# Find all the answer choices for each of the questions
tempAs = []
temp = []
questionAnswers = []
for x in testQuestions:
    cursor.execute("SELECT choice_id, choice_text, is_correct FROM Question_Choices WHERE question_id = %s", (x,))
    result = cursor.fetchall()
    for row in result:
        temp.append(row)
        tempAs.append(temp)
        temp = []

questionAnswers = [list(item) for sublist in tempAs for item in sublist]

# Write out the questions to the text file
grouped_answers = defaultdict(list)
for ans in questionAnswers:
    q_num = int(ans[0][0])  # Extract the question number
    grouped_answers[q_num].append(ans)

# Formatting
for q in questionsText:
    q_num, q_text = q
    f.write(f"{q_num}. {q_text}\n")

    for ans in grouped_answers[q_num]:
        ans_label = ans[0][1]  # extract the letter
        ans_text = ans[1]  # answer text
        is_correct = "*" if ans[2] == 1 else ""  # mark correct answers

        f.write(f"{is_correct}{ans_label}) {ans_text}\n")

    # f.write("\n") # For spacing maybe

# Close the connections
cnx.close()
f.close()

# Open and read the file after appending
# f = open("sampleTest.txt", "r")
# print(f.read())

# Runs the text2qti form the command line to create a QTI file and solutions PDF
subprocess.run(['text2qti', 'sampleTest.txt', '--solutions', 'sampleTestSolutions.pdf'])
