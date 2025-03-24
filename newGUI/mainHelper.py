from tkinter import *
from tkinter.ttk import Combobox

import mysql.connector


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
def create_dropdown_hor(parent, options, var, row, col, text="Select an option:"):
    """Creates a dropdown menu (Combobox) using a loop."""
    Label(parent, text=text).grid(row=row, column=col, padx=5, pady=5)
    dropdown = Combobox(parent, textvariable=var, values=options)
    dropdown.grid(row=row, column=col + 1, padx=5, pady=5)
    return dropdown


def create_dropdown_ver(parent, options, var, row, col, text="Select an option:"):
    """Creates a dropdown menu (Combobox) using a loop."""
    Label(parent, text=text).grid(row=row, column=col, padx=5, pady=5)
    dropdown = Combobox(parent, textvariable=var, values=options)
    dropdown.grid(row=row + 1, column=col, padx=5, pady=5)
    return dropdown
