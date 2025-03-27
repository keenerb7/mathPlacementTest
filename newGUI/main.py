from test2qti import *
from tkinter import ttk

# Create the main window
root = Tk()
root.title("University of Findlay Math Department")
root.iconbitmap(r"university_findlay_logo_32d_icon.ico")

root.tk.call("source", r"azure.tcl")
root.tk.call("set_theme", "light")

notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, rowspan=5, columnspan=4)
notebook.grid_columnconfigure(0, weight=1, uniform="equal")
notebook.grid_columnconfigure(1, weight=1, uniform="equal")
notebook.grid_columnconfigure(2, weight=1, uniform="equal")
notebook.grid_columnconfigure(3, weight=1, uniform="equal")
quest_frame = ttk.Frame(notebook)
test_frame = ttk.Frame(notebook)
questType_frame = ttk.Frame(notebook)
testType_frame = ttk.Frame(notebook)

notebook.add(quest_frame, text="Question Options")
notebook.add(test_frame, text="Test Options")
notebook.add(questType_frame, text="Question Type Options")
notebook.add(testType_frame, text="Test Type Options")


# I think we should ask if they want a consistent size or variable zie
# Without setting the size beforehand it is variable
# root.geometry("1100x500")

########################################Helper function that need to be in main#########################################
# Create a Main Menu Display Functions for Show and Hide
def show_main_menu():
    notebook.grid(row=1, column=0, rowspan=5, columnspan=4)
    mainMenu_lbl.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipadx=50, ipady=10)

    viewQuest_btn.grid(row=2, column=0, padx=10, pady=10, ipadx=50, ipady=10, sticky='ew')
    addQuest_btn.grid(row=2, column=1, padx=10, pady=10, ipadx=50, ipady=10, sticky='ew')
    modifyQuest_btn.grid(row=2, column=2, padx=10, pady=10, ipadx=50, ipady=10, sticky='ew')
    deleteQuest_btn.grid(row=2, column=3, padx=10, pady=10, ipadx=50, ipady=10, sticky='ew')

    # Test buttons in row 3
    viewTest_btn.grid(row=2, column=0, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')
    makeTest_btn.grid(row=2, column=1, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')
    modifyTest_btn.grid(row=2, column=2, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')
    deleteTest_btn.grid(row=2, column=3, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')
    extractTest_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=10, ipadx=50, ipady=10)


def hide_main_menu():
    mainMenu_lbl.grid_forget()
    notebook.grid_forget()
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


######################################Question View#####################################################################
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
    ttk.Label(qviewFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    ttk.Label(qviewFrame, text="Question", anchor='w').grid(row=0, column=1, columnspan=2, ipadx=215, sticky='w')
    ttk.Label(qviewFrame, text="Category").grid(row=0, column=3, ipadx=5)
    ttk.Label(qviewFrame, text="Question Difficulty").grid(row=0, column=4, ipadx=5)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("""
        SELECT 
            q.question_id,
            q.question,
            qc.category_name,
            q.question_difficulty
        FROM 
            Questions q
        JOIN
            Question_Categories qc ON q.category_id = qc.category_id
            """)
    records = c.fetchall()

    num_qrows = 0

    # Loop through and display each question
    for row in records:
        qid_lbl = ttk.Label(qviewFrame, text=str(row[0]), anchor='w')
        qid_lbl.grid(row=num_qrows + 2, column=0, columnspan=1)

        q_lbl = Label(qviewFrame, text=str(row[1]), anchor='w', justify='left')
        q_lbl.grid(row=num_qrows + 2, column=1, columnspan=2, sticky='w')

        ctd_lbl = Label(qviewFrame, text=str(row[2]), anchor='w')
        ctd_lbl.grid(row=num_qrows + 2, column=3, columnspan=1)

        qd_lbl = Label(qviewFrame, text=str(row[3]), anchor='w')
        qd_lbl.grid(row=num_qrows + 2, column=4, columnspan=1)

        num_qrows += 1

    # Get all question IDs
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    question_ids = sorted(question_ids)

    selected_qid = StringVar()
    selected_qid.set(question_ids[0])  # Set first question ID as default

    text = "Select question ID to display answers:"
    question_dropdown = create_dropdown_hor(qviewFrame, question_ids, selected_qid, num_qrows + 2, 0, 2, text)

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
            for answer in qviewFrame.grid_slaves(row=num_qrows + 4 + i, column=2):
                answer.grid_forget()

        # Display answers
        j = num_qrows + 4
        for answer in answers:
            Label(qviewFrame, text=answer, anchor='w', justify='left').grid(row=j, column=2, sticky="w")
            j += 1

        # Close connection and cursor
        c.close()
        cnx.close()

    question_dropdown.bind("<<ComboboxSelected>>", getAnswers)

    # Display Labels for answers
    ttk.Label(qviewFrame, text="(Correct) Answer Number 1:").grid(row=num_qrows + 4, column=0, columnspan=2, sticky="w")
    ttk.Label(qviewFrame, text="Answer Number 2:").grid(row=num_qrows + 5, column=0, columnspan=2, sticky="w")
    ttk.Label(qviewFrame, text="Answer Number 3:").grid(row=num_qrows + 6, column=0, columnspan=2, sticky="w")
    ttk.Label(qviewFrame, text="Answer Number 4:").grid(row=num_qrows + 7, column=0, columnspan=2, sticky="w")
    ttk.Label(qviewFrame, text="Answer Number 5:").grid(row=num_qrows + 8, column=0, columnspan=2, sticky="w")

    # Show answers for the first question as default
    getAnswers()

    # Close the connection and cursor
    c.close()
    cnx.close()

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qview
    back_btn_qview = create_back_button(root, backQuestionView)
    return


####################################Question Add########################################################################
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

        try:
            # Find the highest existing question ID and increment
            c.execute("SELECT COALESCE(MAX(question_id), 0) + 1 FROM Questions")
            newID = c.fetchone()[0]

            # Find Category ID for the selected Category
            c.execute("SELECT category_id FROM Question_Categories WHERE category_name = %s", (var.get(),))
            qcatResults = c.fetchone()

            if not qcatResults:
                messagebox.showerror("Error", "Selected category not found.")
                cnx.close()
                return

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
                choice_id = f"{newID}{letter[i]}"
                is_correct = '1' if i == 0 else '0'
                c.execute("""INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct)
                            VALUES (%s, %s, %s, %s)""",
                          (choice_id, newID, answers[i].get(), is_correct))

            # Commit Changes
            cnx.commit()

            # Clear Text Boxes
            question.delete(0, END)
            cate_drop.set('')
            difficulty.delete(0, END)
            for i in range(5):
                answers[i].delete(0, END)

            messagebox.showinfo("Success", "Question added successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
            cnx.rollback()
        finally:
            # Close Connection
            cnx.close()

        return

    hide_main_menu()

    # Create a Frame for this option
    global qaddFrame
    qaddFrame = Frame(root, bd=2)
    qaddFrame.grid(row=0, pady=10, padx=20)

    # Create Labels for the Text Input
    ttk.Label(qaddFrame, text="Question:").grid(row=0, column=2)
    question = ttk.Entry(qaddFrame, width=100)
    question.grid(row=0, column=3)

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

    cate_drop = create_dropdown_ver(qaddFrame, question_categories, var, 2, 0, 1, text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Label(qaddFrame, text="Question Category").grid(row=1, column=0, pady=10)
    ttk.Label(qaddFrame, text="Question Difficulty").grid(row=4, column=0, pady=10)
    difficulty = ttk.Entry(qaddFrame, width=30)
    difficulty.grid(row=5, column=0, padx=10, pady=10)

    # ANSWER SECTION
    # Create Labels for the Answer Choices and note the first one is always correct
    ttk.Label(qaddFrame, text="(Correct) Answer Number 1:").grid(row=2, column=2)
    ttk.Label(qaddFrame, text="Answer Number 2:").grid(row=3, column=2)
    ttk.Label(qaddFrame, text="Answer Number 3:").grid(row=4, column=2)
    ttk.Label(qaddFrame, text="Answer Number 4:").grid(row=5, column=2)
    ttk.Label(qaddFrame, text="Answer Number 5:").grid(row=6, column=2)

    # Create Text Boxes for Each Answer
    answers = []
    for i in range(5):
        entry = ttk.Entry(qaddFrame, width=100)
        entry.grid(row=2 + i, column=3)
        answers.append(entry)

    # Create Add Button to Trigger the Addition of the new Record
    add_btn = ttk.Button(qaddFrame, text="Add Question", command=addQuestion, width=30)
    add_btn.grid(row=8, column=3, padx=10, pady=10)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qadd
    back_btn_qadd = create_back_button(root, backQuestionAdd)
    return


###############################################Question Modify##########################################################
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
    question_dropdown = create_dropdown_ver(qmodifyFrame, question_ids, selected_qid, 1, 0, 1, text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Create the label and text boxes for the selected question
    # Create Labels for the Text Input
    Label(qmodifyFrame, text="Question:").grid(row=num_rows + 0, column=1)
    question = ttk.Entry(qmodifyFrame, width=100)
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

    cate_dropdown = create_dropdown_ver(qmodifyFrame, question_categories, var, num_rows + 2, 0, 1,
                                        text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    Label(qmodifyFrame, text="Question Difficulty").grid(row=num_rows + 4, column=0, pady=10, sticky='w')
    difficulty = ttk.Entry(qmodifyFrame, width=30)
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
        entry = ttk.Entry(qmodifyFrame, width=100)
        entry.grid(row=num_rows + 2 + i, column=2)
        answers.append(entry)

    def question_selection_dis(event=None):
        # Save the Question ID that we want to change
        qID = question_dropdown.get()

        # Clear out the old results
        question.delete(0, END)
        cate_dropdown.set('')  # Corrected clearing method for dropdown
        difficulty.delete(0, END)
        for i in range(5):
            answers[i].delete(0, END)

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        # Fetch question details
        c.execute("SELECT * FROM Questions WHERE question_id = %s", (qID,))
        questionInfo = c.fetchone()

        # Fetch answers for the selected question
        c.execute("SELECT choice_text FROM Question_Choices WHERE question_id = %s", (qID,))
        questionAns = c.fetchall()

        # Close database connection
        cnx.close()

        if questionInfo:
            # Get Category Name for Drop Down
            cat_name = str(getCategoryName(questionInfo[2])) # Fetch category name
            cat_name = cat_name.strip("(),''")
            cate_dropdown.set(cat_name)  # Correctly update dropdown value

            # Update the text fields with the retrieved data
            question.insert(0, questionInfo[1])  # Question text
            difficulty.insert(0, questionInfo[3])  # Difficulty level

            # Update answer choices
            for i, ans in enumerate(questionAns):
                answers[i].insert(0, ans[0])  # Insert the actual text value

    # Create Function to Submit the Changes to the Database
    # MUST USE THE UPDATE SQL COMMANDS GOODLUCK BUDDY
    def submitChanges():
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

        # FInd new ID for the New Question
        newID = countQuestionsTotal()

        # Find Category ID for the selection Category
        c.execute("SELECT category_id FROM Question_Categories WHERE category_name= %s", (var.get(),))
        qcatResults = c.fetchone()
        cat_id = qcatResults[0]

        # Update existing question in the Questions Table
        c.execute(
            """UPDATE Questions 
               SET question = %s, category_id = %s, question_difficulty = %s 
               WHERE question_id = %s""",
            (question.get(), cat_id, difficulty.get(), newID)
        )

        # Update existing question choices in the Question_Choices Table
        letter = ['a', 'b', 'c', 'd', 'e']
        for i in range(5):
            if i == 0:
                c.execute(
                    """UPDATE Question_Choices 
                       SET choice_text = %s, is_correct = %s 
                       WHERE choice_id = %s AND question_id = %s""",
                    (answers[i].get(), '1', str(f"{newID}{letter[i]}"), newID)
                )
            else:
                c.execute(
                    """UPDATE Question_Choices 
                       SET choice_text = %s, is_correct = %s 
                       WHERE choice_id = %s AND question_id = %s""",
                    (answers[i].get(), '0', str(f"{newID}{letter[i]}"), newID)
                )


        print("Supposed to be Updated.")
        print()

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        # Clear Text Boxes
        question.delete(0, END)
        cate_dropdown.set('')
        difficulty.delete(0, END)
        for i in range(5):
            answers[i].delete(0, END)
        question_dropdown.set('')
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


############################################Question Delete#############################################################
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
    ttk.Label(qdeleteFrame, text="Question ID").grid(row=0, column=0, ipadx=5)
    ttk.Label(qdeleteFrame, text="Question", anchor='w').grid(row=0, column=1, ipadx=215)

    global num_rows_qdelete
    num_rows_qdelete = 0

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("SELECT * FROM Questions")
    records = c.fetchall()

    for row in records:
        qid_lbl = ttk.Label(qdeleteFrame, text=str(row[0]), anchor='w')
        qid_lbl.grid(row=num_rows_qdelete + 2, column=0, columnspan=1)

        q_lbl = Label(qdeleteFrame, text=str(row[1]), anchor='w', justify='left')
        q_lbl.grid(row=num_rows_qdelete + 2, column=1, columnspan=2, sticky='w')

        num_rows_qdelete += 1

    # Commit Changes
    cnx.commit()

    # Close Connection
    cnx.close()

    # Create a Function to Delete the Typed Question ID From the Question Table
    # and to Delete all the Questions Answers in Question Choices
    def deleteQuestion():
        question_id = question_dropdown.get()
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

            # Query Questions in the Test questions table to see if the Question is apart a test
            c.execute("SELECT question_id FROM Test_Questions")
            usedQuesitons = c.fetchall()
            if question_id in usedQuesitons:
                messagebox.showerror("Error", f"{question_id} is apart of a current Test.")
                return

            try:
                # Delete Answers for the same Question ID
                c.execute("DELETE FROM Question_Choices WHERE question_id= %s", (question_id,))
                # Delete Proper Question ID From Questions Table
                c.execute("DELETE from Questions WHERE question_id= %s", (question_id,))

                # Commit Changes
                cnx.commit()

            except Exception as e:
                # Rollback changes if there's an error
                cnx.rollback()

                # Display an error message
                messagebox.showerror("ERROR", f"{question_id} is unable to be deleted. {question_id} is in a test.")
                # print(f"Error occurred: {e}")

            # Close Connection
            cnx.close()
        else:
            return

        # Explicitly remove the back button before refreshing the UI
        back_btn_qdelete.grid_forget()

        # Refresh the UI to show updated list of questions
        qdeleteFrame.destroy()
        questionDelete()

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Create a Dropdown option to select the Question to Edit
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    question_ids = sorted(question_ids)

    selected_qid = StringVar()
    # Set first question ID as default
    selected_qid.set(question_ids[0])

    text = "Select Question ID to be Deleted:"
    question_dropdown = create_dropdown_hor(qdeleteFrame, question_ids, selected_qid, num_rows_qdelete + 4, 0, 1, text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()
    # ttk.Label(qdeleteFrame, text="Question ID to Delete: ").grid(row=num_rows_qdelete + 2, column=0, columnspan=2, sticky='w')
    # delete_box = ttk.Entry(qdeleteFrame, width=10)
    # delete_box.grid(row=num_rows_qdelete + 2, column=1)
    deleteQuestion_btn = ttk.Button(qdeleteFrame, text="Delete Question", command=deleteQuestion)
    deleteQuestion_btn.grid(row=num_rows_qdelete + 4, column=1)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qdelete
    back_btn_qdelete = create_back_button(root, backQuestionDelete)
    return


######################################Question Buttons##################################################################
# Create Main Menu Label
mainMenu_lbl = ttk.Label(root, text="Math Placement Test", font=('Verdana', 20), anchor="center")
mainMenu_lbl.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipadx=50, ipady=10)
# Create View Question Button
viewQuest_btn = ttk.Button(quest_frame, text="View Questions", command=questionView, width=13)
viewQuest_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Add Question Button
addQuest_btn = ttk.Button(quest_frame, text="Add Questions", command=questionAdd, width=13)
addQuest_btn.grid(row=1, column=1, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Modify Question Button
modifyQuest_btn = ttk.Button(quest_frame, text="Modify Questions", command=questionModify, width=13)
modifyQuest_btn.grid(row=1, column=2, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Delete Question Button
deleteQuest_btn = ttk.Button(quest_frame, text="Delete Questions", command=questionDelete, width=13)
deleteQuest_btn.grid(row=1, column=3, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)


########################################################################################################################
################################### This Section is the Test Section ###################################################
########################################################################################################################

################################################Test View###############################################################
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
    c.execute("""
        SELECT 
            t.test_id,
            tot.test_name,
            t.test_title,
            t.test_time
        FROM 
            Test t
        JOIN
            Types_Of_Test tot ON t.test_type = tot.test_type
            """)
    records = c.fetchall()
    print_tid, print_ttype, print_ttitle, print_ttime, print_qnum = '', '', '', '', ''
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

    tid_label = ttk.Label(tviewFrame, text=print_tid, anchor='w')
    tid_label.grid(row=2, column=0, columnspan=1)
    ttype_label = ttk.Label(tviewFrame, text=print_ttype, anchor='w')
    ttype_label.grid(row=2, column=1, columnspan=1)
    ttitle_label = ttk.Label(tviewFrame, text=print_ttitle, anchor='w')
    ttitle_label.grid(row=2, column=2, columnspan=1)
    ttime_label = ttk.Label(tviewFrame, text=print_ttime, anchor='w')
    ttime_label.grid(row=2, column=3, columnspan=1)
    qnum_label = ttk.Label(tviewFrame, text=print_qnum, anchor='w')
    qnum_label.grid(row=2, column=4, columnspan=1)

    # Get all test IDs
    c.execute("SELECT test_id FROM Test")
    test_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    test_ids = sorted(test_ids)

    selected_tid = StringVar()
    selected_tid.set(test_ids[0])  # Set first question ID as default

    text = "Select test ID to display question: "
    test_dropdown = create_dropdown_hor(tviewFrame, test_ids, selected_tid, num_rows + 2, 0, 2, text)

    # Get answers for selected question ID
    def getQuestions(event=None):
        # Reconnect to the database
        cnx = get_db_connection()

        # Create cursor
        c = cnx.cursor()

        # Get the selected question ID
        selected_test_id = selected_tid.get()

        query = ("""
            SELECT 
                q.question_id, 
                q.question, 
                qc.category_name, 
                q.question_difficulty 
            FROM 
                Questions q 
            JOIN 
                Test_Questions tq ON q.question_id = tq.question_id 
            JOIN 
                Question_Categories qc ON q.category_id = qc.category_id 
            WHERE 
                tq.test_id = %s
        """)
        c.execute(query, (selected_test_id,))
        questions = c.fetchall()

        # Clear previous answers
        for question in tviewFrame.grid_slaves():
            if int(question.grid_info()["row"]) >= num_rows + 4:
                question.grid_forget()

        # Display questions
        j = num_rows + 4
        for question in questions:
            Label(tviewFrame, text=question[0], anchor='center').grid(row=j, column=0, sticky="ew")
            Label(tviewFrame, text=question[1], anchor='w', justify='left', wraplength=400).grid(row=j, column=1,
                                                                                                 columnspan=3,
                                                                                                 rowspan=1, sticky="w")
            Label(tviewFrame, text=question[2], anchor='center').grid(row=j, column=4, sticky="ew")
            Label(tviewFrame, text=question[3], anchor='center').grid(row=j, column=5, sticky="ew")
            j += 1

        # Close connection and cursor
        c.close()
        cnx.close()

    #Display column headers
    Label(tviewFrame, text="Question ID").grid(row=num_rows + 3, column=0, ipadx=5)
    Label(tviewFrame, text="Question", anchor='w').grid(row=num_rows + 3, column=1, columnspan=3, ipadx=5, sticky="w")
    Label(tviewFrame, text="Category").grid(row=num_rows + 3, column=4, ipadx=5)
    Label(tviewFrame, text="Difficulty").grid(row=num_rows + 3, column=5, ipadx=5)

    test_dropdown.bind("<<ComboboxSelected>>", getQuestions)

    # Show questions for the first test as default
    getQuestions()

    global back_btn_tview
    back_btn_tview = create_back_button(root, backTestView)
    return


###################################################Test Make############################################################
def backTestMake():
    show_main_menu()
    tmakeFrame.grid_forget()
    back_btn_tmake.grid_forget()
    return


# Create Function to Make a Test
def testMake():
    def addTest():
        # Validate inputs
        if not ttype_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Test Type.")
            return

        if not ttitle_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Test Title.")
            return

        try:
            test_time = float(ttime_entry.get())
            num_questions = int(tnumquestion_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Time and Number of Questions must be numeric values.")
            return

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Find the last Test ID and increment
            c.execute("SELECT MAX(test_id) FROM Test")
            last_test_id = c.fetchone()[0]
            new_test_id = last_test_id + 1 if last_test_id else 1

            # Insert New Test
            c.execute(
                """INSERT INTO Test (test_id, test_type, test_title, test_time) 
                   VALUES (%s, %s, %s, %s)""",
                (new_test_id, ttype_entry.get(), ttitle_entry.get(), test_time)
            )

            # Randomly select questions for the test based on the specified number
            c.execute("""
                SELECT question_id FROM Questions 
                ORDER BY RAND() 
                LIMIT %s
            """, (num_questions,))

            selected_questions = c.fetchall()

            # Insert selected questions into Test_Questions
            for question in selected_questions:
                c.execute(
                    """INSERT INTO Test_Questions (test_id, question_id) 
                       VALUES (%s, %s)""",
                    (new_test_id, question[0])
                )

            # Commit Changes
            cnx.commit()
            messagebox.showinfo("Success", f"Test {new_test_id} created successfully!")

            # Clear input fields
            ttype_entry.delete(0, END)
            ttitle_entry.delete(0, END)
            ttime_entry.delete(0, END)
            tnumquestion_entry.delete(0, END)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            cnx.rollback()
        finally:
            cnx.close()

    hide_main_menu()

    # Create a Frame for this option
    global tmakeFrame
    tmakeFrame = Frame(root, bd=2)
    tmakeFrame.grid(row=0, pady=10, padx=20)

    # Labels for Test Creation
    Label(tmakeFrame, text="Test ID").grid(row=0, column=0, ipadx=5)
    Label(tmakeFrame, text="Type", anchor='w').grid(row=0, column=1, ipadx=5)
    Label(tmakeFrame, text="Title").grid(row=0, column=2, ipadx=100)
    Label(tmakeFrame, text="Time (minutes)").grid(row=0, column=3, ipadx=5)
    Label(tmakeFrame, text="# of Questions").grid(row=0, column=4, ipadx=5)

    # New Test ID will be current number of tests + 1
    tid_label = Label(tmakeFrame, text=(countTests() + 1), anchor='w')
    tid_label.grid(row=2, column=0, columnspan=1)

    # MAYBE USE A DROPDOWN WITH TEST TYPES SO NO GUESSING
    # Test type input
    ttype_entry = ttk.Entry(tmakeFrame, width=8)
    ttype_entry.grid(row=2, column=1)

    # Test Name input
    ttitle_entry = ttk.Entry(tmakeFrame, width=50)
    ttitle_entry.grid(row=2, column=2)

    # Test Time input
    ttime_entry = ttk.Entry(tmakeFrame, width=8)
    ttime_entry.grid(row=2, column=3)

    # Number of questions input
    tnumquestion_entry = ttk.Entry(tmakeFrame, width=8)
    tnumquestion_entry.grid(row=2, column=4)

    # Add Test Button
    add_test_btn = ttk.Button(tmakeFrame, text="Create Test", command=addTest)
    add_test_btn.grid(row=4, column=2, pady=10)

    # Back Button
    global back_btn_tmake
    back_btn_tmake = create_back_button(root, backTestMake)

    return


#################################################Test Modify############################################################
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


###################################################Test Delete##########################################################
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

    # Create a Labels for the Columns of the Question Table
    Label(tdeleteFrame, text="Test ID").grid(row=0, column=0, ipadx=5)
    Label(tdeleteFrame, text="Test", anchor='w').grid(row=0, column=1)

    def showTestForDelete():
        # Connect to Database
        cnx = get_db_connection()
        # Create a Cursor
        c = cnx.cursor()
        # Query Questions Table for all Questions
        c.execute("SELECT * FROM Test")
        records = c.fetchall()
        print_tid, print_t, print_ttd, print_td = '', '', '', ''
        num_rows = 0
        for row in records:
            print_tid += str(row[0]) + "\n"
            print_t += str(row[2]) + "\n"
            num_rows += 1

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        qid_label = Label(tdeleteFrame, text=print_tid, anchor='w')
        qid_label.grid(row=2, column=0, columnspan=1)
        q_label = Label(tdeleteFrame, text=print_t, anchor='w')
        q_label.grid(row=2, column=1, columnspan=1)

        return num_rows

    # Create a Function to Delete the Typed Question ID From the Question Table
    # and to Delete all the Questions Answers in Question Choices
    def deleteQuestion():
        question_id = test_dropdown.get()
        # question_id = delete_box.get()
        if messagebox.askyesno("Question",
                               "Are you sure you would like to delete Test ID: " + str(question_id)):
            # Connect to Database
            cnx = get_db_connection()
            # Create a Cursor
            c = cnx.cursor()

            # Data Validation to Ensure Proper Question ID
            c.execute("SELECT * FROM Test WHERE test_id= %s", (question_id,))
            results = c.fetchall()
            if len(results) == 0:
                messagebox.showerror("Error", f"{question_id} is not a valid Test ID.")
                return

            # Delete Answers for the same Question ID
            c.execute("DELETE FROM Test_Questions WHERE test_id= %s", (question_id,))
            # Delete Proper Question ID From Questions Table
            c.execute("DELETE from Test WHERE test_id= %s", (question_id,))

            # Commit Changes
            cnx.commit()
            # Close Connection
            cnx.close()
        else:
            return

        showTestForDelete()

    num_rows = showTestForDelete()
    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()
    # Get all test IDs
    c.execute("SELECT test_id FROM Test")
    test_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    test_ids = sorted(test_ids)

    selected_tid = StringVar()
    selected_tid.set(test_ids[0])  # Set first question ID as default

    text = "Select test ID to delete: "
    test_dropdown = create_dropdown_hor(tdeleteFrame, test_ids, selected_tid, num_rows + 2, 0, 2, text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Label(tdeleteFrame, text="Test ID to Delete: ").grid(row=3, column=0)
    # delete_box = ttk.Entry(tdeleteFrame, width=10)
    # delete_box.grid(row=3, column=1)
    deleteQuestion_btn = ttk.Button(tdeleteFrame, text="Delete Test", command=deleteQuestion)
    deleteQuestion_btn.grid(row=num_rows + 4, column=1)

    global back_btn_tdelete
    back_btn_tdelete = create_back_button(root, backTestDelete)

    return


##############################################Test Extract##############################################################
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

    c.execute("""
        SELECT 
            t.test_id, 
            t.test_title, 
            tot.test_name 
        FROM 
            Test t
        JOIN 
             Types_Of_Test tot ON t.test_type = tot.test_type
            """)
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
    num_rows = 0
    for row in results:
        print_tid += str(row[0]) + "\n"
        print_t += str(row[1]) + "\n"
        print_tt += str(row[2]) + "\n"
        num_rows += 1

    tid_label = ttk.Label(testExtractFrame, text=print_tid, anchor='w')
    tid_label.grid(row=2, column=0, columnspan=1)
    t_label = ttk.Label(testExtractFrame, text=print_t, anchor='w')
    t_label.grid(row=2, column=1, columnspan=1)
    tt_label = ttk.Label(testExtractFrame, text=print_tt, anchor='w')
    tt_label.grid(row=2, column=2, columnspan=1)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Create a Selection Section for the Test
    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()
    # Get all test IDs
    c.execute("SELECT test_id FROM Test")
    test_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    test_ids = sorted(test_ids)

    selected_tid = StringVar()
    selected_tid.set(test_ids[0])  # Set first question ID as default

    text = "Select test ID to Export to QTI .zip file: "
    test_dropdown = create_dropdown_hor(testExtractFrame, test_ids, selected_tid, num_rows + 2, 0, 2, text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()
    # Label(testExtractFrame, text="Test ID for QTI Extraction: ").grid(row=3, column=0)
    # select_box = ttk.Entry(testExtractFrame, width=10)
    # select_box.grid(row=3, column=1)
    extract_btn = ttk.Button(testExtractFrame, text="Export QTI .zip File for Test", command=lambda: test2qti(test_dropdown.get()))
    extract_btn.grid(row=num_rows + 4, column=1)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_testExtract
    back_btn_testExtract = create_back_button(root, backTestExtract)

    return


##############################################Test Buttons##############################################################
# Create View Test Button
viewTest_btn = ttk.Button(test_frame, text="View Test", command=testView, width=13)
viewTest_btn.grid(row=1, column=0, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Add Test Button
makeTest_btn = ttk.Button(test_frame, text="Make Test", command=testMake, width=13)
makeTest_btn.grid(row=1, column=1, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Modify Test Button
modifyTest_btn = ttk.Button(test_frame, text="Modify Test", command=testModify, width=13)
modifyTest_btn.grid(row=1, column=2, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Delete Test Button
deleteTest_btn = ttk.Button(test_frame, text="Delete Test", command=testDelete, width=13)
deleteTest_btn.grid(row=1, column=3, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Extract Test Button
extractTest_btn = ttk.Button(test_frame, text="Extract Test", command=testExtract, width=13)
extractTest_btn.grid(row=2, column=1, columnspan=2, pady=10, padx=10, ipadx=50, ipady=10)

########################################################################################################################
# Run the main event loop
root.mainloop()
