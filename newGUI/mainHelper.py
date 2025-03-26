from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk

import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        user='sql5764680', password='yK8gNIyhZm',
        host='sql5.freesqldatabase.com', database='sql5764680'
    )


# Create a Function to Make the Back Button
def create_back_button(parent, command):
    btn = ttk.Button(parent, text="Back", command=command)
    btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    return btn


# Create a Dropdown with a Variable Length
def create_dropdown_hor(parent, options, var, row, col, cspan, text="Select an option:"):
    """Creates a dropdown menu (Combobox) using a loop."""
    ttk.Label(parent, text=text, anchor='w').grid(row=row, column=col, columnspan=cspan, padx=5, pady=5, sticky="w")
    dropdown = ttk.Combobox(parent, textvariable=var, values=options)
    dropdown.grid(row=row, column=col + cspan, columnspan=cspan, padx=5, pady=5, sticky='w')
    return dropdown


def create_dropdown_ver(parent, options, var, row, col, cspan, text="Select an option:"):
    """Creates a dropdown menu (Combobox) using a loop."""
    ttk.Label(parent, text=text).grid(row=row, column=col, padx=5, pady=5, sticky="w")
    dropdown = ttk.Combobox(parent, textvariable=var, values=options)
    dropdown.grid(row=row + 1, column=col, columnspan=cspan, padx=5, pady=5, sticky="w")
    return dropdown


def countQuestionsTestID(t_id):
    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Test Questions table for count of questions
    c.execute("SELECT COUNT(question_id) AS num_questions FROM Test_Questions WHERE test_id = %s", (t_id,))

    # Get the result
    result = c.fetchone()

    # Get the count if any questions were found, else set to 0
    num_questions = result[0] if result else 0

    # Close the connection
    cnx.close()

    return num_questions


def countTests():
    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Test table for count of Test ID
    c.execute("SELECT COUNT(test_id) AS num_tests FROM Test")

    # Get the result
    result = c.fetchone()

    # Get the count if any test were found, else set to 0
    num_tests = result[0] if result else 0

    # Close the connection
    cnx.close()

    return num_tests


def countQuestionsTotal():
    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Test Questions table for count of questions
    c.execute("SELECT COUNT(question_id) AS num_questions FROM Questions")

    # Get the result
    result = c.fetchone()

    # Get the count if any questions were found, else set to 0
    num_questions = result[0] if result else 0

    # Close the connection
    cnx.close()

    return num_questions


def getCategoryName(cat_id):
    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Test table for count of Test ID
    c.execute("SELECT category_name FROM Question_Categories WHERE category_id = %s", (cat_id,))

    # Get the result
    result = c.fetchone()

    # Close the connection
    cnx.close()

    return result
