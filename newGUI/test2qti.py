import os
import shutil
import subprocess
from collections import defaultdict
from tkinter import messagebox, filedialog

from mainHelper import *


def test2qti(createTest):
    if messagebox.askokcancel("Confirmation", f"Would you like to Export a QTI .zip file for Test ID: {createTest}?"):
        cnx = get_db_connection()

        cursor = cnx.cursor()

        cursor.execute("SELECT test_title FROM Test WHERE test_id = %s", (createTest,))
        result = cursor.fetchall()

        if len(result) == 0:
            messagebox.showerror("Error", f"{createTest} is not a valid Test ID.")
            return

        text_file_name = str(result[0][0]).strip()
        f = open(text_file_name + ".txt", "w")
        text_file_path = text_file_name.strip() + ".txt"

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
        tempQs = []
        for row in result:
            tempQs.append(row)

        testQuestions = [item[0] for item in tempQs]

        # Find all the actual questions for the test
        tempQ = []
        temp = []
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
        for x in testQuestions:
            cursor.execute("SELECT choice_id, choice_text, is_correct FROM Question_Choices WHERE question_id = %s",
                           (x,))
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

        # Open the directory selection dialog
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="Select a folder")

        # Create Solution File Name
        solution_file_path = text_file_name.strip() + " Solutions.pdf"

        # Runs the text2qti form the command line to create a QTI file and solutions PDF
        subprocess.run(['text2qti', text_file_path, '--solutions', solution_file_path])

        # Delete Text File because it has no use
        if os.path.exists(text_file_path):
            os.remove(text_file_path)

        # Find the generated .zip file (assuming text2qti creates a zip with the test name)
        zip_filename = text_file_name + ".zip"
        zip_source_path = os.path.join(os.getcwd(), zip_filename)  # Assuming it’s created in the current directory
        zip_dest_path = os.path.join(folder_path, zip_filename)  # Destination in selected folder

        # Move .zip file if it exists
        if os.path.exists(zip_source_path):
            shutil.move(zip_source_path, zip_dest_path)
            messagebox.showinfo("Success", f"QTI .zip File Exported to {zip_dest_path}")
        else:
            messagebox.showerror("Error", f"Could not find {zip_filename}.zip , Please Try Again.")

        # Find the generated solutions file
        pdf_filename = solution_file_path
        pdf_source_path = os.path.join(os.getcwd(), pdf_filename)  # Assuming it’s created in the current directory
        pdf_dest_path = os.path.join(folder_path, pdf_filename)  # Destination in selected folder

        # Move .zip file if it exists
        if os.path.exists(pdf_source_path):
            shutil.move(pdf_source_path, pdf_dest_path)

        return
    else:
        return
