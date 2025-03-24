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
root.geometry("1100x500")


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

    # Create Labels for the Columns of the Question Table
    Label(qviewFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    Label(qviewFrame, text="Question", anchor='w').grid(row=0, column=1, ipadx=215)
    Label(qviewFrame, text="Category ID").grid(row=0, column=2, ipadx=5)
    Label(qviewFrame, text="Question Difficulty").grid(row=0, column=3, ipadx=5)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("SELECT * FROM Questions")
    records = c.fetchall()

    print_qid, print_q, print_ctd, print_qd = '', '', '', ''
    num_rows = 0
    for row in records:
        print_qid += str(row[0]) + "\n"
        print_q += str(row[1]) + "\n"
        print_ctd += str(row[2]) + "\n"
        print_qd += str(row[3]) + "\n"
        num_rows += 1

    qid_label = Label(qviewFrame, text=print_qid, anchor='w')
    qid_label.grid(row=2, column=0, columnspan=1)
    q_label = Label(qviewFrame, text=print_q, anchor='w')
    q_label.grid(row=2, column=1, columnspan=1)
    ctd_label = Label(qviewFrame, text=print_ctd, anchor='w')
    ctd_label.grid(row=2, column=2, columnspan=1)
    qd_label = Label(qviewFrame, text=print_qd, anchor='w')
    qd_label.grid(row=2, column=3, columnspan=1)

    # Get all question IDs
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    question_ids = sorted(question_ids)

    selected_qid = StringVar()
    selected_qid.set(question_ids[0])   # Set first question ID as default

    text = "Select question ID to display answers:"
    question_dropdown = create_dropdown_ver(qviewFrame, question_ids, selected_qid, num_rows+2, 0, text)

    # Get answers for selected question ID
    def getAnswers(event=None):
        # Reconnect to the database
        cnx = get_db_connection()

        # Create cursor
        c = cnx.cursor()

        # Get the selected question ID
        selected_question_id = selected_qid.get()

        c.execute("SELECT choice_text FROM Question_Choices WHERE question_id = %s", (selected_question_id,))
        answers = [answer[0] for answer in c.fetchall()]

        # Clear previous answers
        for i in range(5):
            for answer in qviewFrame.grid_slaves(row=num_rows + 4 + i, column=1):
                answer.grid_forget()

        # Display answers
        j = num_rows + 4
        for answer in answers:
            Label(qviewFrame, text=answer, anchor='w', justify='left').grid(row=j, column=1, sticky="w")
            j += 1

        # Close connection and cursor
        c.close()
        cnx.close()

    question_dropdown.bind("<<ComboboxSelected>>", getAnswers)

    # Display Labels for answers
    Label(qviewFrame, text="(Correct) Answer Number 1:").grid(row=num_rows+4, column=0)
    Label(qviewFrame, text="Answer Number 2:").grid(row=num_rows+5, column=0)
    Label(qviewFrame, text="Answer Number 3:").grid(row=num_rows+6, column=0)
    Label(qviewFrame, text="Answer Number 4:").grid(row=num_rows+7, column=0)
    Label(qviewFrame, text="Answer Number 5:").grid(row=num_rows+8, column=0)

    # Show answers for the first question as default
    getAnswers()

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qview
    back_btn_qview = create_back_button(root, backQuestionView)
    return

    #Close the connection and cursor
    c.close()
    cnx.close()


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
        # Validate that there is a question in the form
        if not question.get().strip():
            messagebox.showerror("Error", "There is no Question submitted.")
            return

        # Validates that there is a selection in the dropdown box
        if len(var.get()) == 0:
            messagebox.showerror("Error", "There is no Question Category Selected.")
            return

        # Validate that there is a difficulty input
        if not difficulty.get().strip():
            messagebox.showerror("Error", "There is no Question Difficulty submitted.")
            return

        # Validate that Difficulty is a number
        if difficulty.get().isalpha():
            messagebox.showerror("Error", "Please enter an integer for Question Difficulty.")
            return

        # Validate that each answer is not empty
        for i in range(5):
            if not answers[i].get().strip():
                messagebox.showerror("Error", f"Answer {i + 1} is not submitted.")
                return

        # Connect to Database
        cnx = get_db_connection()

        # Create a Cursor
        c = cnx.cursor()

        # First Find the Last Used ID
        # Query Questions Table for all Questions
        c.execute("SELECT * FROM Questions")
        records = c.fetchall()
        newID = records[-1][0] + 1

        # Find Category ID for the selection Category
        c.execute("SELECT category_id FROM Question_Categories WHERE category_name= %s", (var.get(),))
        qcatResults = c.fetchone()
        cat_id = qcatResults[0]

        # Insert New Question into Questions Table
        c.execute(
            """INSERT INTO Questions (question_id, question, category_id, question_difficulty) 
               VALUES (%s, %s, %s, %s)""",
            (newID, question.get(), cat_id, difficulty.get())
        )

        # Insert New Question Choices into Question Choices Table
        letter = ['a', 'b', 'c', 'd', 'e']
        for i in range(5):
            if i == 0:
                c.execute("""INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct)
                    VALUES (%s, %s, %s, %s)""",
                          (str(f"{newID}{letter[i]}"), newID, answers[i].get(), '1'))
            else:
                c.execute("""INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct)
                                    VALUES (%s, %s, %s, %s)""",
                          (str(f"{newID}{letter[i]}"), newID, answers[i].get(), '0'))

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        # Clear Text Boxes
        question.delete(0, END)
        difficulty.delete(0, END)
        for i in range(5):
            answers[i].delete(0, END)

        return

    hide_main_menu()

    # Create a Frame this option
    global qaddFrame
    qaddFrame = Frame(root, bd=2)
    qaddFrame.grid(row=0, pady=10, padx=20)

    # Create Labels for the Text Input
    Label(qaddFrame, text="Question:").grid(row=0, column=1)
    question = Entry(qaddFrame, width=100)
    question.grid(row=0, column=2)

    # Create Dropdown Box for Question Categories
    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()
    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()
    question_categories = []
    var = StringVar()
    for row in results:
        question_categories.append(row[1])

    create_dropdown_ver(qaddFrame, question_categories, var, 2, 0, text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Label(qaddFrame, text="Question Category").grid(row=1, column=0, pady=10)
    Label(qaddFrame, text="Question Difficulty").grid(row=4, column=0, pady=10)
    difficulty = Entry(qaddFrame, width=30)
    difficulty.grid(row=5, column=0, padx=10, pady=10)

    # ANSWER SECTION
    # Create Labels for the Answer Choices and note the first one is always correct
    Label(qaddFrame, text="(Correct) Answer Number 1:").grid(row=2, column=1)
    Label(qaddFrame, text="Answer Number 2:").grid(row=3, column=1)
    Label(qaddFrame, text="Answer Number 3:").grid(row=4, column=1)
    Label(qaddFrame, text="Answer Number 4:").grid(row=5, column=1)
    Label(qaddFrame, text="Answer Number 5:").grid(row=6, column=1)

    # Create Text Boxes for Each Answer
    answers = []
    for i in range(5):
        entry = Entry(qaddFrame, width=100)
        entry.grid(row=2 + i, column=2)
        answers.append(entry)

    # Create Add Button to Trigger the Addition of the new Record
    add_btn = Button(qaddFrame, text="Add Question", command=addQuestion)
    add_btn.grid(row=6, column=0, padx=10, pady=10)

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

    # Simple Display of all the Questions
    # Create a Labels for the Columns of the Question Table
    Label(qmodifyFrame, text="Question ID").grid(row=0, column=1, sticky="")
    Label(qmodifyFrame, text="Questions", anchor='w').grid(row=0, column=2, sticky="")


    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("SELECT * FROM Questions")
    records = c.fetchall()
    print_qid, print_q, print_ctd, print_qd = '', '', '', ''
    num_rows = 0
    for row in records:
        print_qid += str(row[0]) + "\n"
        print_q += str(row[1]) + "\n"
        num_rows += 1

    qid_label = Label(qmodifyFrame, text=print_qid)
    qid_label.grid(row=2, column=1, sticky="ew")
    q_label = Label(qmodifyFrame, text=print_q)
    q_label.grid(row=2, column=2, sticky="ew")

    # Create a Dropdown option to select the Question to Edit
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    question_ids = sorted(question_ids)

    selected_qid = StringVar()
    # Set first question ID as default
    selected_qid.set(question_ids[0])

    text = "Select Question ID to be modified:"
    question_dropdown = create_dropdown_ver(qmodifyFrame, question_ids, selected_qid, 0, 0, text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Create the label and text boxes for the selected question
    # Create Labels for the Text Input
    Label(qmodifyFrame, text="Question:").grid(row=num_rows + 0, column=1)
    question = Entry(qmodifyFrame, width=100)
    question.grid(row=num_rows + 0, column=2)

    # Create Dropdown Box for Question Categories
    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()
    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()
    question_categories = []
    var = StringVar()
    for row in results:
        question_categories.append(row[1])

    cate_dropdown = create_dropdown_ver(qmodifyFrame, question_categories, var, num_rows + 2, 0, text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    Label(qmodifyFrame, text="Question Difficulty").grid(row=num_rows + 4, column=0, pady=10)
    difficulty = Entry(qmodifyFrame, width=30)
    difficulty.grid(row=num_rows + 5, column=0, padx=10, pady=10)

    # ANSWER SECTION
    # Create Labels for the Answer Choices and note the first one is always correct
    Label(qmodifyFrame, text="(Correct) Answer Number 1:").grid(row=num_rows + 2, column=1)
    Label(qmodifyFrame, text="Answer Number 2:").grid(row=num_rows + 3, column=1)
    Label(qmodifyFrame, text="Answer Number 3:").grid(row=num_rows + 4, column=1)
    Label(qmodifyFrame, text="Answer Number 4:").grid(row=num_rows + 5, column=1)
    Label(qmodifyFrame, text="Answer Number 5:").grid(row=num_rows + 6, column=1)

    # Create Text Boxes for Each Answer
    answers = []
    for i in range(5):
        entry = Entry(qmodifyFrame, width=100)
        entry.grid(row=num_rows + 2 + i, column=2)
        answers.append(entry)

    # Create Function to Fill in text boxes with current data given the Question ID
    def question_selection_dis(event=NONE):
        # Save the Question ID that we Want to change
        qID = question_dropdown.get()

        # Clear out the old results
        question.delete(0, END)
        cate_dropdown.delete(END)
        difficulty.delete(0, END)
        for i in range(5):
            answers[i].delete(0, END)

        # Save the Question, Category, and Difficulty from Questions Table
        # Connect to Database
        cnx = get_db_connection()
        # Create a Cursor
        c = cnx.cursor()

        c.execute("SELECT * FROM Questions WHERE question_id = %s", (qID,))
        questionInfo = c.fetchone()

        # Save the Answers from Question Choices Table
        c.execute("SELECT choice_text FROM Question_Choices WHERE question_id = %s", (qID,))
        questionAns = c.fetchall()

        # Commit Changes
        cnx.commit()
        # Close Connection
        cnx.close()

        # Update the Text Boxes and Other Widgets with the Question ID data
        question.insert(0, questionInfo[1])
        cate_dropdown.set(questionInfo[2])
        difficulty.insert(0, questionInfo[3])
        for i in range(5):
            answers[i].insert(0, questionAns[i])
        return

    # Create Function to Submit the Changes to the Database
    # MUST USE THE UPDATE SQL COMMANDS GOODLUCK BUDDY
    def submitChanges():
        return

    # Create a Binding for the Dropdown menu to change the Question ID
    question_dropdown.bind("<<ComboboxSelected>>", question_selection_dis)

    # Create Button to Trigger the Submission of Changes
    # Should probably have a message box saying that once these changes are made there is no going back
    # Create Add Button to Trigger the Addition of the new Record
    submit_btn = Button(qmodifyFrame, text="Submit Changes", command=submitChanges)
    submit_btn.grid(row=num_rows + 6, column=0, padx=10, pady=10)

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
    # and to Delete all the Questions Answers in Question Choices
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

            # Delete Answers for the same Question ID
            c.execute("DELETE FROM Question_Choices WHERE question_id= %s", (delete_box.get(),))
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

    # Create a Labels for the Columns of the Question Table
    Label(tviewFrame, text="Test ID").grid(row=0, column=0, ipadx=5)
    Label(tviewFrame, text="Type", anchor='w').grid(row=0, column=1, ipadx=5)
    Label(tviewFrame, text="Title").grid(row=0, column=2, ipadx=100)
    Label(tviewFrame, text="Time").grid(row=0, column=3, ipadx=10)
    Label(tviewFrame, text="# of Questions").grid(row=0, column=4, ipadx=10)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("SELECT * FROM Test")
    records = c.fetchall()
    print_tid, print_ttype, print_ttitle, print_ttime, print_qnum= '', '', '', '', ''
    num_rows = 0

    def countQuestions(t_id):
        # Query Test Questions table for count of questions
        c.execute("SELECT COUNT(question_id) AS num_questions FROM Test_Questions WHERE test_id = %s", (t_id,))

        # Get the result
        result = c.fetchone()

        # Get the count if any questions were found, else set to 0
        num_questions = result[0] if result else 0

        return num_questions

    for row in records:
        print_tid += str(row[0]) + "\n"
        print_ttype += str(row[1]) + "\n"
        print_ttitle += str(row[2]) + "\n"
        print_ttime += str(row[3]) + "\n"
        print_qnum += str(countQuestions(row[0])) + "\n"
        num_rows += 1

    tid_label = Label(tviewFrame, text=print_tid, anchor='w')
    tid_label.grid(row=2, column=0, columnspan=1)
    ttype_label = Label(tviewFrame, text=print_ttype, anchor='w')
    ttype_label.grid(row=2, column=1, columnspan=1)
    ttitle_label = Label(tviewFrame, text=print_ttitle, anchor='w')
    ttitle_label.grid(row=2, column=2, columnspan=1)
    ttime_label = Label(tviewFrame, text=print_ttime, anchor='w')
    ttime_label.grid(row=2, column=3, columnspan=1)
    qnum_label = Label(tviewFrame, text=print_qnum, anchor='w')
    qnum_label.grid(row=2, column=4, columnspan=1)

    # Get all test IDs
    c.execute("SELECT test_id FROM Test")
    test_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    test_ids = sorted(test_ids)

    selected_tid = StringVar()
    selected_tid.set(test_ids[0])  # Set first question ID as default

    text = "Select test ID to display question:"
    test_dropdown = create_dropdown_hor(tviewFrame, test_ids, selected_tid, num_rows + 2, 0, 2, text)

    # Get answers for selected question ID
    def getQuestions(event=None):
        # Reconnect to the database
        cnx = get_db_connection()

        # Create cursor
        c = cnx.cursor()

        # Get the selected question ID
        selected_test_id = selected_tid.get()

        query = (
            "SELECT q.question_id, q.question, q.category_id, q.question_difficulty "
            "FROM Questions q JOIN Test_Questions tq ON q.question_id = tq.question_ID "
            "WHERE tq.test_id = %s"
        )
        c.execute(query, (selected_test_id,))
        questions = c.fetchall()

        # Clear previous answers
        for question in tviewFrame.grid_slaves():
            if int(question.grid_info()["row"]) >= num_rows + 4:
                question.grid_forget()

        # Display questions
        j = num_rows + 4
        for question in questions:
            Label(tviewFrame, text=question[0], anchor ='center').grid(row=j, column=0, sticky="ew")
            Label(tviewFrame, text=question[1], anchor='w', justify='left', wraplength=400).grid(row=j, column=1, columnspan=3, rowspan=1, sticky="w")
            Label(tviewFrame, text=question[2], anchor ='center').grid(row=j, column=4, sticky="ew")
            Label(tviewFrame, text=question[3], anchor ='center').grid(row=j, column=5, sticky="ew")
            j += 1

        # Close connection and cursor
        c.close()
        cnx.close()

    #Display column headers
    Label(tviewFrame, text="Question ID").grid(row=num_rows + 3, column=0, ipadx=5)
    Label(tviewFrame, text="Question", anchor='w').grid(row=num_rows + 3, column=1, columnspan=3, ipadx=5, sticky="w")
    Label(tviewFrame, text="Category ID").grid(row=num_rows + 3, column=4, ipadx=5)
    Label(tviewFrame, text="Difficulty").grid(row=num_rows + 3, column=5, ipadx=5)

    test_dropdown.bind("<<ComboboxSelected>>", getQuestions)

    # Show questions for the first test as default
    getQuestions()

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
