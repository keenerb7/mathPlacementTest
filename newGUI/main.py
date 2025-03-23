import mysql.connector
from tkinter import *
from tkinter import messagebox

# Connect to Database
cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm', host='sql5.freesqldatabase.com',
                              database='sql5764680')

# Create a Cursor
c = cnx.cursor()

# Commit Changes
cnx.commit()

# Close Connection
cnx.close()

# Create the main window
root = Tk()
root.title("University of Findlay Math Department")
root.geometry("1000x500")


# Create a Function to Return to Original View
def backQuestionView():
    viewQuest_btn.grid(row=0, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    addQuest_btn.grid(row=0, column=1, columnspan=1, pady=10, padx=10, ipadx=50)
    modifyQuest_btn.grid(row=0, column=2, columnspan=1, pady=10, padx=10, ipadx=50)
    deleteQuest_btn.grid(row=0, column=3, columnspan=1, pady=10, padx=10, ipadx=50)
    qviewFrame.grid_forget()
    back_btn_qview.grid_forget()
    return


# Create Question View Function To Query From Questions Table
def questionView():
    # Hide Current Buttons
    viewQuest_btn.grid_forget()
    addQuest_btn.grid_forget()
    modifyQuest_btn.grid_forget()
    deleteQuest_btn.grid_forget()

    # Create a Frame this option
    global qviewFrame
    qviewFrame = Frame(root, bd=2)
    qviewFrame.grid(row=0, pady=10, padx=20)

    # Create a Labels for the Columns of the Question Table
    Label(qviewFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    Label(qviewFrame, text="Question", anchor='w').grid(row=0, column=1, ipadx=215)
    Label(qviewFrame, text="Category ID").grid(row=0, column=2, ipadx=5)
    Label(qviewFrame, text="Question Difficulty").grid(row=0, column=3, ipadx=5)

    # Connect to Database
    cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm', host='sql5.freesqldatabase.com',
                                  database='sql5764680')

    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("SELECT * FROM Questions")
    records = c.fetchall()
    print_qid, print_q, print_ctd, print_qd = '', '', '', ''
    for row in records:
        print_qid += str(row[0]) + "\n"
        print_q += str(row[1]) + "\n"
        print_ctd += str(row[2]) + "\n"
        print_qd += str(row[3]) + "\n"

    qid_label = Label(qviewFrame, text=print_qid, anchor='w')
    qid_label.grid(row=2, column=0, columnspan=1)
    q_label = Label(qviewFrame, text=print_q, anchor='w')
    q_label.grid(row=2, column=1, columnspan=1)
    ctd_label = Label(qviewFrame, text=print_ctd, anchor='w')
    ctd_label.grid(row=2, column=2, columnspan=1)
    qd_label = Label(qviewFrame, text=print_qd, anchor='w')
    qd_label.grid(row=2, column=3, columnspan=1)

    # Commit Changes
    cnx.commit()

    # Close Connection
    cnx.close()

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qview
    back_btn_qview = Button(root, text="Back", command=backQuestionView)
    back_btn_qview.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    return


# Create a Function to Return to Original View
def backQuestionAdd():
    viewQuest_btn.grid(row=0, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    addQuest_btn.grid(row=0, column=1, columnspan=1, pady=10, padx=10, ipadx=50)
    modifyQuest_btn.grid(row=0, column=2, columnspan=1, pady=10, padx=10, ipadx=50)
    deleteQuest_btn.grid(row=0, column=3, columnspan=1, pady=10, padx=10, ipadx=50)
    qaddFrame.grid_forget()
    back_btn_qadd.grid_forget()
    return


# Create Question Add Function to Add Records to Questions Table
def questionAdd():
    # Create a Function to Add a Question to the Question Table
    def addQuestion():
        # Connect to Database
        cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm', host='sql5.freesqldatabase.com',
                                      database='sql5764680')

        # Create a Cursor
        c = cnx.cursor()

        # First Find the Last Used ID
        # Query Questions Table for all Questions
        c.execute("SELECT * FROM Questions")
        records = c.fetchall()
        newID = records[-1][0] + 1

        # SOME TYPE OF INPUT VALIDATION FOR AT LEAST LATEX PURPOSES AND INTEGERS
        # USE THE MESSAGE BOXES TO SEND BACK TO FORM BEFORE CLEARING

        # Insert New Question into Questions Table
        c.execute(
            """INSERT INTO Questions (question_id, question, category_id, question_difficulty) 
               VALUES (%s, %s, %s, %s)""",
            (newID, question.get(), category.get(), difficulty.get())
        )

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        # Clear Text Boxes
        question.delete(0, END)
        category.delete(0, END)
        difficulty.delete(0, END)

        return

    # Hide Current Buttons
    viewQuest_btn.grid_forget()
    addQuest_btn.grid_forget()
    modifyQuest_btn.grid_forget()
    deleteQuest_btn.grid_forget()

    # Create a Frame this option
    global qaddFrame
    qaddFrame = Frame(root, bd=2)
    qaddFrame.grid(row=0, pady=10, padx=20)

    # Create Labels for the Text Input
    # NOT SURE IF THEY SHOULD HAVE CONTROL OVER QUESTION ID
    # I AM CURRENTLY ASSUMING NO
    Label(qaddFrame, text="Question").grid(row=0, column=0, pady=10)
    question = Entry(qaddFrame, width=100)
    question.grid(row=0, column=1, padx=10, pady=10)
    Label(qaddFrame, text="Category ID").grid(row=1, column=0, pady=10)
    category = Entry(qaddFrame, width=30)
    category.grid(row=1, column=1, padx=10, pady=10)
    Label(qaddFrame, text="Question Difficulty").grid(row=2, column=0, pady=10)
    difficulty = Entry(qaddFrame, width=30)
    difficulty.grid(row=2, column=1, padx=10, pady=10)

    # Create Add Button to Trigger the Addition of the new Record
    add_btn = Button(qaddFrame, text="Add Question", command=addQuestion)
    add_btn.grid(row=4, column=1, padx=10, pady=10)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qadd
    back_btn_qadd = Button(root, text="Back", command=backQuestionAdd)
    back_btn_qadd.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    return


# Create Question Modify Function to Update Records in Question Table
def questionModify():
    return


# Create a Function to Return to Original View
def backQuestionDelete():
    viewQuest_btn.grid(row=0, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    addQuest_btn.grid(row=0, column=1, columnspan=1, pady=10, padx=10, ipadx=50)
    modifyQuest_btn.grid(row=0, column=2, columnspan=1, pady=10, padx=10, ipadx=50)
    deleteQuest_btn.grid(row=0, column=3, columnspan=1, pady=10, padx=10, ipadx=50)
    qdeleteFrame.grid_forget()
    back_btn_qdelete.grid_forget()
    return


# Create Question Delete Function to Delete a Record in Question Table
def questionDelete():
    # Hide Current Buttons
    viewQuest_btn.grid_forget()
    addQuest_btn.grid_forget()
    modifyQuest_btn.grid_forget()
    deleteQuest_btn.grid_forget()

    # Create a Frame this option
    global qdeleteFrame
    qdeleteFrame = Frame(root, bd=2)
    qdeleteFrame.grid(row=0, pady=10, padx=20)

    # Create a Labels for the Columns of the Question Table
    Label(qdeleteFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    Label(qdeleteFrame, text="Question", anchor='w').grid(row=0, column=1, ipadx=215)
    # Label(qdeleteFrame, text="Category ID").grid(row=0, column=2, ipadx=5)
    # Label(qdeleteFrame, text="Question Difficulty").grid(row=0, column=3, ipadx=5)

    def showQuestionsForDelete():
        # Connect to Database
        cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm', host='sql5.freesqldatabase.com',
                                      database='sql5764680')

        # Create a Cursor
        c = cnx.cursor()

        # Query Questions Table for all Questions
        c.execute("SELECT * FROM Questions")
        records = c.fetchall()
        print_qid, print_q, print_ctd, print_qd = '', '', '', ''
        for row in records:
            print_qid += str(row[0]) + "\n"
            print_q += str(row[1]) + "\n"

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        qid_label = Label(qdeleteFrame, text=print_qid, anchor='w')
        qid_label.grid(row=2, column=0, columnspan=1)
        q_label = Label(qdeleteFrame, text=print_q, anchor='w')
        q_label.grid(row=2, column=1, columnspan=1)

    # Create a Function to Delete the Typed Question ID From the Question Table
    def deleteQuestion():
        if messagebox.askyesno("Question",
                               "Are you sure you would like to delete Question ID: " + str(delete_box.get())):
            # Connect to Database
            cnx = mysql.connector.connect(user='sql5764680', password='yK8gNIyhZm', host='sql5.freesqldatabase.com',
                                          database='sql5764680')

            # Create a Cursor
            c = cnx.cursor()

            c.execute("DELETE from Questions WHERE question_id= %s", (delete_box.get(),))

            # Commit Changes
            cnx.commit()

            # Close Connection
            cnx.close()

            # This is a temporary fix to force refresh the
            # backQuestionDelete()
        else:
            return

        showQuestionsForDelete()


    showQuestionsForDelete()
    Label(qdeleteFrame, text="Question ID to Delete: ").grid(row=3, column=0)
    delete_box = Entry(qdeleteFrame, width=10)
    delete_box.grid(row=3, column=1)
    deleteQuestion_btn = Button(qdeleteFrame, text="Delete Question", command=deleteQuestion)
    deleteQuestion_btn.grid(row=4, column=1)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qdelete
    back_btn_qdelete = Button(root, text="Back", command=backQuestionDelete)
    back_btn_qdelete.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    return


# Create View Question Button
viewQuest_btn = Button(root, text="View Questions", command=questionView)
viewQuest_btn.grid(row=0, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Add Question Button
addQuest_btn = Button(root, text="Add Questions", command=questionAdd)
addQuest_btn.grid(row=0, column=1, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Modify Question Button
modifyQuest_btn = Button(root, text="Modify Questions", command=questionModify)
modifyQuest_btn.grid(row=0, column=2, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Delete Question Button
deleteQuest_btn = Button(root, text="Delete Questions", command=questionDelete)
deleteQuest_btn.grid(row=0, column=3, columnspan=1, pady=10, padx=10, ipadx=50)

# Run the main event loop
root.mainloop()
