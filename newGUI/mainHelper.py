from tkinter.ttk import Combobox

import mysql.connector
from tkinter import *
from tkinter import ttk


def get_db_connection():
    return mysql.connector.connect(
        user='sql5764680', password='yK8gNIyhZm',
        host='sql5.freesqldatabase.com', database='sql5764680'
    )


# Create a Function to Make the Back Button
def create_back_button(parent, command):
    btn = Button(parent, text="Back", command=command)
    btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    return btn


# Create a Dropdown with a Variable Length
def create_dropdown(parent, options, var, row, col, text = "Select an option:"):
    """Creates a dropdown menu (Combobox) using a loop."""
    Label(parent, text=text).grid(row=row, column=col, padx=5, pady=5)
    dropdown = Combobox(parent, textvariable=var, values=options)
    dropdown.grid(row=row, column=col + 1, padx=5, pady=5)
    return dropdown

# Get answers based on selected question ID
def get_answers(cnx, question_id):
    c = cnx.cursor()

    answer_ids = ['a', 'b', 'c', 'd', 'e']

    answers = []

    for answer_id in answer_ids:
        concatenated_id = f"{question_id}{answer_id}" #Concatenate question ID
        c.execute("SELECT choice_text FROM Question_Choices WHERE choice_id = %s", (concatenated_id,))
        answer = c.fetchone()

        if answer:
            answers.append(answer[0]) # Add answer to the list

    return answers
