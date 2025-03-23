import mysql.connector
from test2qti import *

# Connect to Database
cnx = get_db_connection()
# Create a Cursor
c = cnx.cursor()
# Commit Changes
cnx.commit()
# Close Connection
cnx.close()

# Create the main window
root = Tk()
root.title("University of Findlay Math Department")
root.iconbitmap(r"C:\university_findlay_logo_32d_icon.ico")
root.geometry("1000x500")


# Create a Main Menu Display Functions for Show and Hide
def show_main_menu():
    viewQuest_btn.grid(row=0, column=0, padx=10, pady=10, ipadx=50)
    addQuest_btn.grid(row=0, column=1, padx=10, pady=10, ipadx=50)
    modifyQuest_btn.grid(row=0, column=2, padx=10, pady=10, ipadx=50)
    deleteQuest_btn.grid(row=0, column=3, padx=10, pady=10, ipadx=50)
    viewTest_btn.grid(row=2, column=0, columnspan=1, pady=10, padx=10, ipadx=50)
    makeTest_btn.grid(row=2, column=1, columnspan=1, pady=10, padx=10, ipadx=50)
    modifyTest_btn.grid(row=2, column=2, columnspan=1, pady=10, padx=10, ipadx=50)
    deleteTest_btn.grid(row=2, column=3, columnspan=1, pady=10, padx=10, ipadx=50)
    extractTest_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=10, ipadx=50)


def hide_main_menu():
    # Hide Current Buttons
    viewQuest_btn.grid_forget()
    addQuest_btn.grid_forget()
    modifyQuest_btn.grid_forget()
    deleteQuest_btn.grid_forget()
    viewTest_btn.grid_forget()
    makeTest_btn.grid_forget()
    modifyTest_btn.grid_forget()
    deleteTest_btn.grid_forget()
    extractTest_btn.grid_forget()


# Create a Function to Return to Original View from Question View Page
def backQuestionView():
    show_main_menu()
    qviewFrame.grid_forget()
    back_btn_qview.grid_forget()
    return


# Create Question View Function To Query From Questions Table
def questionView():
    hide_main_menu()

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
    back_btn_qview = create_back_button(root, backQuestionView)
    return


# Create a Function to Return to Original View
def backQuestionAdd():
    show_main_menu()
    qaddFrame.grid_forget()
    back_btn_qadd.grid_forget()
    return


# Create Question Add Function to Add Records to Questions Table
def questionAdd():
    # Create a Function to Add a Question to the Question Table
    def addQuestion():
        # Connect to Database
        cnx = get_db_connection()

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

    hide_main_menu()

    # Create a Frame this option
    global qaddFrame
    qaddFrame = Frame(root, bd=2)
    qaddFrame.grid(row=0, pady=10, padx=20)

    # Create Labels for the Text Input
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
    back_btn_qadd = create_back_button(root, backQuestionAdd)
    return


# Create Function to Return to Original View
def backQuestionModify():
    show_main_menu()
    qmodifyFrame.grid_forget()
    back_btn_qmodify.grid_forget()
    return


# Create Question Modify Function to Update Records in Question Table
def questionModify():
    hide_main_menu()

    # Create a Frame this option
    global qmodifyFrame
    qmodifyFrame = Frame(root, bd=2)
    qmodifyFrame.grid(row=0, pady=10, padx=20)

    global back_btn_qmodify
    back_btn_qmodify = create_back_button(root, backQuestionModify)
    return


# Create a Function to Return to Original View
def backQuestionDelete():
    show_main_menu()
    qdeleteFrame.grid_forget()
    back_btn_qdelete.grid_forget()
    return


# Create Question Delete Function to Delete a Record in Question Table
def questionDelete():
    hide_main_menu()

    # Create a Frame this option
    global qdeleteFrame
    qdeleteFrame = Frame(root, bd=2)
    qdeleteFrame.grid(row=0, pady=10, padx=20)

    # Create a Labels for the Columns of the Question Table
    Label(qdeleteFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    Label(qdeleteFrame, text="Question", anchor='w').grid(row=0, column=1, ipadx=215)

    def showQuestionsForDelete():
        # Connect to Database
        cnx = get_db_connection()
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
        question_id = delete_box.get()
        if messagebox.askyesno("Question",
                               "Are you sure you would like to delete Question ID: " + str(question_id)):
            # Connect to Database
            cnx = get_db_connection()
            # Create a Cursor
            c = cnx.cursor()

            # Data Validation to Ensure Proper Question ID
            c.execute("SELECT * FROM Questions WHERE question_id= %s", (question_id,))
            results = c.fetchall()
            if len(results) == 0:
                messagebox.showerror("Error", f"{question_id} is not a valid Question ID.")
                return

            # Delete Proper Question ID From Questions Table
            c.execute("DELETE from Questions WHERE question_id= %s", (delete_box.get(),))
            # Commit Changes
            cnx.commit()
            # Close Connection
            cnx.close()
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
    back_btn_qdelete = create_back_button(root, backQuestionDelete)
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


################################### This Section is the Test Section ###################################################
def backTestView():
    show_main_menu()
    tviewFrame.grid_forget()
    back_btn_tview.grid_forget()
    return


# Create Function to View a Test
def testView():
    hide_main_menu()

    # Create a Frame this option
    global tviewFrame
    tviewFrame = Frame(root, bd=2)
    tviewFrame.grid(row=0, pady=10, padx=20)

    global back_btn_tview
    back_btn_tview = create_back_button(root, backTestView)
    return


def backTestMake():
    show_main_menu()
    tmakeFrame.grid_forget()
    back_btn_tmake.grid_forget()
    return


# Create Function to Make a Test
def testMake():
    hide_main_menu()

    # Create a Frame this option
    global tmakeFrame
    tmakeFrame = Frame(root, bd=2)
    tmakeFrame.grid(row=0, pady=10, padx=20)

    global back_btn_tmake
    back_btn_tmake = create_back_button(root, backTestMake)
    return


def backTestModify():
    show_main_menu()
    tmodifyFrame.grid_forget()
    back_btn_tmodify.grid_forget()
    return


# Create Function to Modify a Test
def testModify():
    hide_main_menu()

    # Create a Frame this option
    global tmodifyFrame
    tmodifyFrame = Frame(root, bd=2)
    tmodifyFrame.grid(row=0, pady=10, padx=20)

    global back_btn_tmodify
    back_btn_tmodify = create_back_button(root, backTestModify)

    return


def backTestDelete():
    show_main_menu()
    tdeleteFrame.grid_forget()
    back_btn_tdelete.grid_forget()
    return


# Create Function to Delete a Test
def testDelete():
    hide_main_menu()

    # Create a Frame this option
    global tdeleteFrame
    tdeleteFrame = Frame(root, bd=2)
    tdeleteFrame.grid(row=0, pady=10, padx=20)

    global back_btn_tdelete
    back_btn_tdelete = create_back_button(root, backTestDelete)

    return


# Create a Function to Return to Original View
def backTestExtract():
    show_main_menu()
    testExtractFrame.grid_forget()
    back_btn_testExtract.grid_forget()
    return


# Create Function to Extract a Test
def testExtract():
    hide_main_menu()

    # Display a list of Test and Their Names
    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT test_id, test_title, test_type FROM Test")
    results = c.fetchall()

    # Create a Frame this option
    global testExtractFrame
    testExtractFrame = Frame(root, bd=2)
    testExtractFrame.grid(row=0, pady=10, padx=20)

    # Create a Labels for the Columns of the Question Table
    Label(testExtractFrame, text="Test ID").grid(row=0, column=0, ipadx=5)
    Label(testExtractFrame, text="Test Title", anchor='w').grid(row=0, column=1, ipadx=100)
    Label(testExtractFrame, text="Test Type").grid(row=0, column=2, ipadx=5)

    # Display the Current Tests Available
    print_tid, print_t, print_tt = '', '', ''
    for row in results:
        print_tid += str(row[0]) + "\n"
        print_t += str(row[1]) + "\n"
        print_tt += str(row[2]) + "\n"

    tid_label = Label(testExtractFrame, text=print_tid, anchor='w')
    tid_label.grid(row=2, column=0, columnspan=1)
    t_label = Label(testExtractFrame, text=print_t, anchor='w')
    t_label.grid(row=2, column=1, columnspan=1)
    tt_label = Label(testExtractFrame, text=print_tt, anchor='w')
    tt_label.grid(row=2, column=2, columnspan=1)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Create a Selection Section for the Test
    Label(testExtractFrame, text="Test ID for QTI Extraction: ").grid(row=3, column=0)
    select_box = Entry(testExtractFrame, width=10)
    select_box.grid(row=3, column=1)
    extract_btn = Button(testExtractFrame, text="Extract QTI File for Test", command=lambda: test2qti(select_box.get()))
    extract_btn.grid(row=4, column=1)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_testExtract
    back_btn_testExtract = create_back_button(root, backTestExtract)

    return


# Create View Test Button
viewTest_btn = Button(root, text="View Test", command=testView)
viewTest_btn.grid(row=2, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Add Test Button
makeTest_btn = Button(root, text="Make Test", command=testMake)
makeTest_btn.grid(row=2, column=1, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Modify Test Button
modifyTest_btn = Button(root, text="Modify Test", command=testModify)
modifyTest_btn.grid(row=2, column=2, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Delete Test Button
deleteTest_btn = Button(root, text="Delete Test", command=testDelete)
deleteTest_btn.grid(row=2, column=3, columnspan=1, pady=10, padx=10, ipadx=50)

# Create Extract Test Button
extractTest_btn = Button(root, text="Extract Test", command=testExtract)
extractTest_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=10, ipadx=50)

# Run the main event loop
root.mainloop()
