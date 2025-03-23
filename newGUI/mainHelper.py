import mysql.connector
from tkinter import *


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

