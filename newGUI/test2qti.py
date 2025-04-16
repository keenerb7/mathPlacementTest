import os
import shutil
import subprocess
import re
from collections import defaultdict
from tkinter import messagebox, filedialog

from mainHelper import *


def test2qti(createTest):
    if messagebox.askokcancel("Confirmation", f"Would you like to Export a QTI .zip file for Test ID: {createTest}?"):
        cnx = get_db_connection()

        cursor = cnx.cursor()

        # Fetch the test title
        cursor.execute("SELECT test_title FROM Test WHERE test_id = ?", (createTest,))
        result = cursor.fetchall()

        if len(result) == 0:
            messagebox.showerror("Error", f"{createTest} is not a valid Test ID.")
            return

        text_file_name = str(result[0][0]).strip()
        f = open(text_file_name + ".txt", "w")
        text_file_path = text_file_name.strip() + ".txt"

        # Write the test title to the text file
        for row in result:
            f.write(f"Quiz Title: {row[0]}\n")

        # Write quiz options
        f.write(f"shuffle answers: true\n")
        f.write(f"shuffle questions: true\n")
        # f.write(f"show correct answers: true\n")
        f.write(f"one question at a time: true\n")
        f.write(f"can't go back: true\n")

        # Fetch all question IDs for the test
        cursor.execute("SELECT question_id FROM Test_Questions WHERE test_id = ?", (createTest,))
        result = cursor.fetchall()
        testQuestions = [row[0] for row in result]

        # Fetch all questions for the test
        questionsText = []
        for x in testQuestions:
            cursor.execute("SELECT question_id, question FROM Questions WHERE question_id = ?", (x,))
            result = cursor.fetchall()
            questionsText.extend(result)

        # Fetch all answer choices for each question
        questionAnswers = []
        for x in testQuestions:
            cursor.execute("SELECT choice_id, choice_text, is_correct FROM Question_Choices WHERE question_id = ?", (x,))
            result = cursor.fetchall()
            questionAnswers.extend(result)

        # Write questions and answers to the text file
        grouped_answers = defaultdict(list)
        for ans in questionAnswers:
            match = re.match(r"(\d+)", ans[0])  # Extract full question number at the start
            if match:
                q_num = int(match.group(1))
                grouped_answers[q_num].append(ans)
            else:
                print(f"Could not extract question number from: {ans[0]}")

        for q in questionsText:
            q_num, q_text = q
            f.write(f"{q_num}. {q_text}\n")

            for ans in grouped_answers[q_num]:
                match = re.match(r"(\d+)([a-eA-E])", ans[0])  # Assuming labels are A–E
                if match:
                    ans_label = match.group(2).lower()
                else:
                    print(f"Couldn't extract answer label from: {ans[0]}")
                    ans_label = "?"

                ans_text = ans[1]
                is_correct = "*" if ans[2] == 1 else ""  # Space if not correct

                f.write(f"{is_correct}{ans_label}) {ans_text}\n")

        # Close the connections
        cnx.close()
        f.close()

        # Open the directory selection dialog
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="Select a folder")

        # Ensure that a folder path is selected
        if not folder_path:
            return

        # Create Solution File Name
        solution_file_path = text_file_name.strip() + " Solutions.pdf"

        # Run the text2qti command-line tool to create a QTI file and solutions PDF
        subprocess.run(['text2qti', text_file_path, '--solutions', solution_file_path])

        # Delete the text file because it has no further use
        if os.path.exists(text_file_path):
            os.remove(text_file_path)

        # Find the generated .zip file (assuming text2qti creates a zip with the test name)
        zip_filename = text_file_name + ".zip"
        zip_source_path = os.path.join(os.getcwd(), zip_filename)  # Assuming it’s created in the current directory
        zip_dest_path = os.path.join(folder_path, zip_filename)  # Destination in the selected folder

        # Move the .zip file if it exists
        if os.path.exists(zip_source_path):
            shutil.move(zip_source_path, zip_dest_path)
            messagebox.showinfo("Success", f"QTI .zip File Exported to {zip_dest_path}")
        else:
            messagebox.showerror("Error", f"Could not find {zip_filename}.zip. Please Try Again.\n"
                                          f"Double Check for duplicate questions and answers in the test.")

        # Find the generated solutions file
        pdf_filename = solution_file_path
        pdf_source_path = os.path.join(os.getcwd(), pdf_filename)  # Assuming it’s created in the current directory
        pdf_dest_path = os.path.join(folder_path, pdf_filename)  # Destination in the selected folder

        # Move the solutions file if it exists
        if os.path.exists(pdf_source_path):
            shutil.move(pdf_source_path, pdf_dest_path)

        return
    else:
        return
