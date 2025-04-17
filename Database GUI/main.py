import os
from initialize_db import initialize_database
from test2qti import *
from tkinter import ttk
from latexCheck import *

# Check if the database file exists
db_file = "math_placement_test.db"
if not os.path.exists(db_file):
    initialize_database()


# Create the main window
root = Tk()
root.title("University of Findlay Math Department")
root.iconbitmap(r"university_findlay_logo_32d_icon.ico")

root.tk.call("source", r"azure.tcl")
root.tk.call("set_theme", "light")

notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, rowspan=5, columnspan=4)
quest_frame = ttk.Frame(notebook)
test_frame = ttk.Frame(notebook)
questType_frame = ttk.Frame(notebook)
testType_frame = ttk.Frame(notebook)

notebook.add(quest_frame, text="Question Options")
notebook.add(test_frame, text="Test Options")
notebook.add(questType_frame, text="Question Category Options")
notebook.add(testType_frame, text="Test Category Options")

# I think we should ask if they want a consistent size or variable zie
# Without setting the size beforehand it is variable
root.geometry("1200x600")
root.columnconfigure(0, weight=1)


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
def back_question_view():
    show_main_menu()
    qviewFrame.grid_forget()
    back_btn_qview.grid_forget()
    header_qview.grid_forget()
    return


# Create Question View Function To Query From Questions Table
def question_view():
    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "q.question_id"
        elif sort_order == "Title":
            order_by = "q.question"
        elif sort_order == "Category":
            order_by = "qc.category_name"
        elif sort_order == "Difficulty":
            order_by = "q.question_difficulty"
        else:
            order_by = "q.question_id"  # Fallback

        c.execute(f"""
            SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
            FROM Questions q
            JOIN Question_Categories qc ON q.category_id = qc.category_id
            ORDER BY {order_by}
        """)
        results = c.fetchall()

        for row in results:
            tree.insert("", "end", values=row)

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Show header
    global header_qview
    header_qview = create_header_label(root, "Question Overview")

    # Create a Frame this option
    global qviewFrame
    qviewFrame = Frame(root, bd=2)
    qviewFrame.grid(row=1, pady=10, padx=20)

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(qviewFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown = create_dropdown_hor(sortFrame, ["ID", "Title", "Category", "Difficulty"], sort_var, row=0, col=0,
                                        cspan=2, state="readonly",
                                        text="Sort questions by:")
    sort_dropdown.grid(padx=10)

    # Create a Frame for the treeview
    treeFrame = Frame(qviewFrame, bd=5)
    treeFrame.grid(row=1, column=0, sticky="nsew")

    # Define columns for the treeview
    columns = ("qid", "q", "qcat", "qdif")

    # Create a treeview with the defined columns
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=8)

    # Set headers
    tree.heading("qid", text="ID", anchor="w")
    tree.heading("q", text="Question", anchor="w")
    tree.heading("qcat", text="Category", anchor="w")
    tree.heading("qdif", text="Difficulty", anchor="w")

    # Set the columns
    tree.column("qid", width=40, anchor="w")
    tree.column("q", width=750, anchor="w")
    tree.column("qcat", width=230, anchor="w")
    tree.column("qdif", width=60, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    # Create scrollbar for treeview
    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("""
        SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
        FROM Questions q
        JOIN Question_Categories qc ON q.category_id = qc.category_id
        ORDER BY q.question_id
            """)
    records = c.fetchall()

    # Loop through and display each question
    for row in records:
        tree.insert("", "end", values=row)

    # Create a Frame inside the qview Frame to display answers
    answerFrame = Frame(qviewFrame, bd=2)
    answerFrame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

    # Get all question IDs
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    question_ids = sorted(question_ids)

    selected_qid = StringVar()
    # selected_qid.set(question_ids[0])  # Set the first question ID as default

    text = "Select question ID to display answers: "
    question_dropdown = create_dropdown_hor(answerFrame, question_ids, selected_qid, 1, 1, 2, "normal", text)
    question_dropdown.grid(pady=10)

    # Get answers for selected question ID
    def getAnswers(event=None):
        # Reconnect to the database
        cnx = get_db_connection()

        # Create cursor
        c = cnx.cursor()

        # Get the selected question ID
        selected_question_id = selected_qid.get()

        c.execute("SELECT choice_text FROM Question_Choices WHERE question_id = ?", (selected_question_id,))
        answers = [answer[0] for answer in c.fetchall()]

        # Clear previous answers
        for i in range(5):
            for answer in answerFrame.grid_slaves(row=4 + i, column=4):
                answer.grid_forget()

        # Display answers
        j = 4
        for answer in answers:
            Label(answerFrame, text=answer, anchor='w', justify="left").grid(row=j, column=4, sticky="w")
            j += 1

        # Close connection and cursor
        c.close()
        cnx.close()

    question_dropdown.bind("<<ComboboxSelected>>", getAnswers)

    # Display Labels for answers
    ttk.Label(answerFrame, text="(Correct) Answer Number 1:", font=("Arial", 10, "bold")).grid(row=4, column=1,
                                                                                               columnspan=1, sticky="e",
                                                                                               pady=5)
    ttk.Label(answerFrame, text="Answer Number 2:").grid(row=5, column=1, columnspan=1, sticky="e", pady=5)
    ttk.Label(answerFrame, text="Answer Number 3:").grid(row=6, column=1, columnspan=1, sticky="e", pady=5)
    ttk.Label(answerFrame, text="Answer Number 4:").grid(row=7, column=1, columnspan=1, sticky="e", pady=5)
    ttk.Label(answerFrame, text="Answer Number 5:").grid(row=8, column=1, columnspan=1, sticky="e", pady=5)

    # Show answers for the first question as default
    getAnswers()

    # Close the connection and cursor
    c.close()
    cnx.close()

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qview
    back_btn_qview = create_back_button(root, back_question_view)
    return


####################################Question Add########################################################################
# Create a Function to Return to Original View
def back_question_add():
    show_main_menu()
    qaddFrame.grid_forget()
    back_btn_qadd.grid_forget()
    header_qadd.grid_forget()
    return


# Create Question Add Function to Add Records to Questions Table
def question_add():
    # Create a Function to Add a Question to the Question Table
    def addQuestion():
        # Validate that there is a question in the form
        if not question.get().strip():
            messagebox.showerror("Error", "There is no Question submitted.")
            return

        valid, texResult = check_latex_validity(f'{question.get()}')
        if not valid:
            messagebox.showerror("LaTeX is not valid.", f"Error: {texResult}\nCheck Question.")
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

        # Validate that each answer is not empty and properly latex formatted
        for i in range(5):
            answer = answers[i].get()
            if not answer.strip():
                messagebox.showerror("Error", f"Answer {i + 1} is not submitted.")
                return

            valid, texResult = check_latex_validity(f'{answer}')
            if not valid:
                messagebox.showerror("LaTeX is not valid.", f"Error: {texResult}\nCheck Answer {i + 1}")
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
            c.execute("SELECT category_id FROM Question_Categories WHERE category_name = ?", (var.get(),))
            qcatResults = c.fetchone()

            if not qcatResults:
                messagebox.showerror("Error", "Selected category not found.")
                cnx.close()
                return

            cat_id = qcatResults[0]

            # Insert New Question into Questions Table
            c.execute(
                """INSERT INTO Questions (question_id, question, category_id, question_difficulty) 
                   VALUES (?, ?, ?, ?)""",
                (newID, question.get(), cat_id, difficulty.get())
            )

            # Insert New Question Choices into Question Choices Table
            letter = ['a', 'b', 'c', 'd', 'e']
            for i in range(5):
                choice_id = f"{newID}{letter[i]}"
                is_correct = '1' if i == 0 else '0'
                c.execute("""
                        INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct)
                        VALUES (?, ?, ?, ?)""",
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

        except sql.connector.Error as err:
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
    qaddFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_qadd
    header_qadd = create_header_label(root, "Add Questions")

    # Create Labels for the Text Input
    ttk.Label(qaddFrame, text="Question: ", font=("Arial", 10, "bold"), foreground="#047bf9").grid(row=0, column=2,
                                                                                                   sticky="e")
    question = ttk.Entry(qaddFrame, width=99)
    question.grid(row=0, column=3, padx=10, pady=15)

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

    cate_drop = create_dropdown_ver(qaddFrame, question_categories, var, 2, 0, 1, "readonly", text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Label(qaddFrame, text="Question Category").grid(row=1, column=0, pady=10)
    ttk.Label(qaddFrame, text="Question Difficulty").grid(row=4, column=0, sticky="w", padx=0, pady=5)
    difficulty = ttk.Entry(qaddFrame, width=30)
    difficulty.grid(row=5, column=0, padx=0, pady=5)

    # ANSWER SECTION
    # Create Labels for the Answer Choices and note the first one is always correct
    ttk.Label(qaddFrame, text="Answer Number 1 (Correct): ", font=("Arial", 10, "bold")).grid(row=2, column=2,
                                                                                              sticky="e", pady=10)
    ttk.Label(qaddFrame, text="Answer Number 2: ").grid(row=3, column=2, sticky="e", pady=10)
    ttk.Label(qaddFrame, text="Answer Number 3: ").grid(row=4, column=2, sticky="e", pady=10)
    ttk.Label(qaddFrame, text="Answer Number 4: ").grid(row=5, column=2, sticky="e", pady=10)
    ttk.Label(qaddFrame, text="Answer Number 5: ").grid(row=6, column=2, sticky="e", pady=10)

    # Create Text Boxes for Each Answer
    answers = []
    for i in range(5):
        entry = ttk.Entry(qaddFrame, width=99)
        entry.grid(row=2 + i, column=3, padx=5)
        answers.append(entry)

    # Create Add Button to Trigger the Addition of the new Record
    add_btn = ttk.Button(qaddFrame, text="Add Question", command=addQuestion, width=30, style="Accent.TButton")
    add_btn.grid(row=8, column=3, padx=10, pady=10)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qadd
    back_btn_qadd = create_back_button(root, back_question_add)
    return


###############################################Question Modify##########################################################
# Create Function to Return to Original View
def back_question_modify():
    show_main_menu()
    qmodifyFrame.grid_forget()
    back_btn_qmodify.grid_forget()
    header_qmodify.grid_forget()
    return


# Create Question Modify Function to Update Records in Question Table
def question_modify():
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
        c.execute("SELECT * FROM Questions WHERE question_id = ?", (qID,))
        questionInfo = c.fetchone()

        # Fetch answers for the selected question
        c.execute("SELECT choice_text FROM Question_Choices WHERE question_id = ?", (qID,))
        questionAns = c.fetchall()

        # Close database connection
        cnx.close()

        if questionInfo:
            # Get Category Name for Drop Down
            cat_name = str(get_category_name(questionInfo[2]))  # Fetch category name
            cat_name = cat_name.strip("(),''")
            cate_dropdown.set(cat_name)  # Correctly update dropdown value

            # Update the text fields with the retrieved data
            question.insert(0, questionInfo[1])  # Question text
            difficulty.insert(0, questionInfo[3])  # Difficulty level

            # Update answer choices
            for i, ans in enumerate(questionAns):
                answers[i].insert(0, ans[0])  # Insert the actual text value

    def refresh_tree():
        # Clear existing treeview
        for item in tree.get_children():
            tree.delete(item)

        # Connect to database and create cursor
        cnx = get_db_connection()
        c = cnx.cursor()

        c.execute("""
                SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
                FROM Questions q
                JOIN Question_Categories qc ON q.category_id = qc.category_id
                ORDER BY q.question_id
                            """)

        records = c.fetchall()

        # Insert updated records into the treeview
        for row in records:
            tree.insert("", "end", values=row)

        # Close connection
        cnx.close()

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

        valid, texResult = check_latex_validity(f'{question.get()}')
        if not valid:
            messagebox.showerror("LaTeX is not valid.", f"Error: {texResult}\nCheck Question.")
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
            answer = answers[i].get()
            if not answers[i].get().strip():
                messagebox.showerror("Error", f"Answer {i + 1} is not submitted.")
                return

            valid, texResult = check_latex_validity(f'{answer}')
            if not valid:
                messagebox.showerror("LaTeX is not valid.", f"Error: {texResult}\nCheck Answer {i + 1}")
                return

        # Connect to Database
        cnx = get_db_connection()

        # Create a Cursor
        c = cnx.cursor()

        # FInd new ID for the New Question
        # newID = countQuestionsTotal()
        qid = question_dropdown.get()

        # Find Category ID for the selection Category
        c.execute("SELECT category_id FROM Question_Categories WHERE category_name= ?", (var.get(),))
        qcatResults = c.fetchone()
        cat_id = qcatResults[0]

        # Update existing question in the Questions Table
        c.execute(
            """UPDATE Questions 
               SET question = ?, category_id = ?, question_difficulty = ? 
               WHERE question_id = ?""",
            (question.get(), cat_id, difficulty.get(), qid)
        )

        # Update existing question choices in the Question_Choices Table
        letter = ['a', 'b', 'c', 'd', 'e']
        for i in range(5):
            if i == 0:
                c.execute(
                    """UPDATE Question_Choices 
                       SET choice_text = ?, is_correct = ? 
                       WHERE choice_id = ? AND question_id = ?""",
                    (answers[i].get(), '1', str(f"{qid}{letter[i]}"), qid)
                )
            else:
                c.execute(
                    """UPDATE Question_Choices 
                       SET choice_text = ?, is_correct = ? 
                       WHERE choice_id = ? AND question_id = ?""",
                    (answers[i].get(), '0', str(f"{qid}{letter[i]}"), qid)
                )

        print("Supposed to be updated.")
        print()

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        # Clear Text Boxes and Dropdown
        question.delete(0, END)
        cate_dropdown.set('')
        difficulty.delete(0, END)

        for i in range(5):
            answers[i].delete(0, END)

        question_dropdown.set('')

        refresh_tree()

        return

    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "q.question_id"
        elif sort_order == "Title":
            order_by = "q.question"
        elif sort_order == "Category":
            order_by = "qc.category_name"
        elif sort_order == "Difficulty":
            order_by = "q.question_difficulty"
        else:
            order_by = "q.question_id"  # Fallback

        c.execute(f"""
            SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
            FROM Questions q
            JOIN Question_Categories qc ON q.category_id = qc.category_id
            ORDER BY {order_by}
        """)
        results = c.fetchall()

        for row in results:
            tree.insert("", "end", values=row)

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global qmodifyFrame
    qmodifyFrame = Frame(root, bd=2)
    qmodifyFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_qmodify
    header_qmodify = create_header_label(root, "Modify Questions")

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(qmodifyFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown = create_dropdown_hor(sortFrame, ["ID", "Title", "Category", "Difficulty"], sort_var, row=0, col=0,
                                        cspan=2, state="readonly",
                                        text="Sort questions by:")

    treeFrame = Frame(qmodifyFrame, bd=5)
    treeFrame.grid(row=1, column=0, sticky="nsew")

    # Define columns for the treeview
    columns = ("qid", "q", "qcat", "qdif")

    # Create a treeview with the defined columns
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=5)

    # Set headers
    tree.heading("qid", text="ID", anchor="w")
    tree.heading("q", text="Question", anchor="w")
    tree.heading("qcat", text="Category", anchor="w")
    tree.heading("qdif", text="Difficulty", anchor="w")

    # Set the columns
    tree.column("qid", width=40, anchor="w")
    tree.column("q", width=750, anchor="w")
    tree.column("qcat", width=230, anchor="w")
    tree.column("qdif", width=60, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Create treeview
    refresh_tree()

    modFrame = Frame(qmodifyFrame, bd=2)
    modFrame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

    modFrame.grid_columnconfigure(1, weight=1)  # Expands second column

    # Create a Dropdown option to select the Question to Edit
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    question_ids = sorted(question_ids)

    selected_qid = StringVar()

    # Set the first question ID as default
    # selected_qid.set(question_ids[0])

    text = "Select Question ID to be modified:"
    question_dropdown = create_dropdown_ver(modFrame, question_ids, selected_qid, 0, 0, 1, "normal", text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Create the label and text boxes for the selected question
    # Create Labels for the Text Input
    Label(modFrame, text="Question: ", foreground="#047bf9", font=("Arial", 10, "bold")).grid(row=0, column=3,
                                                                                              sticky='w')
    question = ttk.Entry(modFrame, width=110)
    question.grid(row=0, column=4, columnspan=3, sticky='e')

    # Create Dropdown Box for Question Categories
    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Retrieve question categories
    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()
    question_categories = []
    var = StringVar()

    for row in results:
        question_categories.append(row[1])

    cate_dropdown = create_dropdown_ver(modFrame, question_categories, var, 2, 0, 1, "readonly",
                                        text="Question Category")
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    Label(modFrame, text="Question Difficulty").grid(row=4, column=0, pady=5, padx=0, sticky='w')
    difficulty = ttk.Entry(modFrame, width=30)
    difficulty.grid(row=5, column=0, padx=0, pady=5)

    # ANSWER SECTION
    # Create Labels for the Answer Choices and note the first one is always correct
    Label(modFrame, text="Answer Number 1 (Correct): ", font=("Arial", 10, "bold")).grid(row=1, column=4, sticky='e')
    Label(modFrame, text="Answer Number 2: ").grid(row=2, column=4, sticky='e')
    Label(modFrame, text="Answer Number 3: ").grid(row=3, column=4, sticky='e')
    Label(modFrame, text="Answer Number 4: ").grid(row=4, column=4, sticky='e')
    Label(modFrame, text="Answer Number 5: ").grid(row=5, column=4, sticky='e')

    # Create Text Boxes for Each Answer
    answers = []
    for i in range(5):
        entry = ttk.Entry(modFrame, width=70)
        entry.grid(row=1 + i, column=5, columnspan=3, sticky='e')
        answers.append(entry)

    # Create a Binding for the Dropdown menu to change the Question ID
    question_dropdown.bind("<<ComboboxSelected>>", question_selection_dis)

    # Create Button to Trigger the Submission of Changes
    # Should probably have a message box saying that once these changes are made, there is no going back
    # Create Add Button to Trigger the Addition of the new Record
    submit_btn = ttk.Button(modFrame, text="Submit Changes", command=submitChanges, style='Accent.TButton', width=25)
    submit_btn.grid(row=6, column=6, padx=10, pady=10, sticky='e')

    global back_btn_qmodify
    back_btn_qmodify = create_back_button(root, back_question_modify)
    return


############################################Question Delete#############################################################
# Create a Function to Return to Original View
def back_question_delete():
    show_main_menu()
    qdeleteFrame.grid_forget()
    back_btn_qdelete.grid_forget()
    header_qdelete.grid_forget()
    return


# Create Question Delete Function to Delete a Record in Question Table
def question_delete():
    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "q.question_id"
        elif sort_order == "Title":
            order_by = "q.question"
        elif sort_order == "Category":
            order_by = "qc.category_name"
        elif sort_order == "Difficulty":
            order_by = "q.question_difficulty"
        else:
            order_by = "q.question_id"  # Fallback

        c.execute(f"""
                SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
                FROM Questions q
                JOIN Question_Categories qc ON q.category_id = qc.category_id
                ORDER BY {order_by}
            """)
        results = c.fetchall()

        for row in results:
            tree.insert("", "end", values=row)

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global qdeleteFrame
    qdeleteFrame = Frame(root, bd=2)
    qdeleteFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_qdelete
    header_qdelete = create_header_label(root, "Delete Questions")

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(qdeleteFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown = create_dropdown_hor(sortFrame, ["ID", "Title", "Category", "Difficulty"], sort_var, row=0,
                                        col=0,
                                        cspan=2, state="readonly",
                                        text="Sort questions by:")

    treeFrame = Frame(qdeleteFrame, bd=10)
    treeFrame.grid(row=1, column=0, sticky="nsew")

    # Define columns for the treeview
    columns = ("qid", "q", "qcat", "qdif")

    # Create a treeview with the defined columns
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=15)

    # Set headers
    tree.heading("qid", text="ID", anchor="w")
    tree.heading("q", text="Question", anchor="w")
    tree.heading("qcat", text="Category", anchor="w")
    tree.heading("qdif", text="Difficulty", anchor="w")

    # Set the columns
    tree.column("qid", width=40, anchor="w")
    tree.column("q", width=750, anchor="w")
    tree.column("qcat", width=230, anchor="w")
    tree.column("qdif", width=60, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Connect to Database
    cnx = get_db_connection()
    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("""
                SELECT q.question_id, q.question, qc.category_name, q.question_difficulty
                FROM Questions q
                JOIN Question_Categories qc ON q.category_id = qc.category_id
                ORDER BY q.question_id
                    """)
    records = c.fetchall()

    # Loop through and display each question
    for row in records:
        tree.insert("", "end", values=row)

    delFrame = Frame(qdeleteFrame, bd=2)
    delFrame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

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
            c.execute("SELECT * FROM Questions WHERE question_id= ?", (question_id,))
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

            # noinspection PyBroadException
            try:
                # Delete Answers for the same Question ID
                c.execute("DELETE FROM Question_Choices WHERE question_id= ?", (question_id,))
                # Delete Proper Question ID From Questions Table
                c.execute("DELETE from Questions WHERE question_id= ?", (question_id,))

                # Commit Changes
                cnx.commit()

            except Exception as e:
                # Rollback changes if there's an error
                cnx.rollback()

                # Display an error message
                messagebox.showerror("ERROR", f"Question #{question_id} is part of a test and cannot be deleted.")
                # print(f"Error occurred: {e}")

            # Close Connection
            cnx.close()
        else:
            return

        # Explicitly remove the back button before refreshing the UI
        back_btn_qdelete.grid_forget()

        # Refresh the UI to show an updated list of questions
        qdeleteFrame.destroy()
        back_btn_qdelete.grid_forget()
        header_qdelete.grid_forget()
        question_delete()

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Create a Dropdown option to select the Question to Edit
    c.execute("SELECT question_id FROM Questions")
    question_ids = [row[0] for row in c.fetchall()]

    question_ids = sorted(question_ids)

    selected_qid = StringVar()

    # Set the first question ID as default
    # selected_qid.set(question_ids[0])

    text = "Select Question ID to be deleted: "
    question_dropdown = create_dropdown_hor(delFrame, question_ids, selected_qid, 0, 0, 2,
                                            "normal", text)

    # Commit Changes
    cnx.commit()

    # Close Connection
    cnx.close()

    # ttk.Label(qdeleteFrame, text="Question ID to Delete: ").grid(row=num_rows_qdelete + 2, column=0, columnspan=2, sticky='w')
    # delete_box = ttk.Entry(qdeleteFrame, width=10)
    # delete_box.grid(row=num_rows_qdelete + 2, column=1)
    deleteQuestion_btn = ttk.Button(delFrame, text="Delete Question", command=deleteQuestion, style="Accent.TButton")
    deleteQuestion_btn.grid(row=0, column=5, sticky='e', padx=10, ipadx=20)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_qdelete
    back_btn_qdelete = create_back_button(root, back_question_delete)

    return


######################################Question Buttons##################################################################
# Create Main Menu Label
mainMenu_lbl = ttk.Label(root, text="Math Placement Test", font=('Verdana', 20), anchor="center")
mainMenu_lbl.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipadx=50, ipady=10)
# Create View Question Button
viewQuest_btn = ttk.Button(quest_frame, text="View Questions", command=question_view, width=13)
viewQuest_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Add Question Button
addQuest_btn = ttk.Button(quest_frame, text="Add Questions", command=question_add, width=13)
addQuest_btn.grid(row=1, column=1, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Modify Question Button
modifyQuest_btn = ttk.Button(quest_frame, text="Modify Questions", command=question_modify, width=13)
modifyQuest_btn.grid(row=1, column=2, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)

# Create Delete Question Button
deleteQuest_btn = ttk.Button(quest_frame, text="Delete Questions", command=question_delete, width=13)
deleteQuest_btn.grid(row=1, column=3, columnspan=1, pady=10, padx=10, ipadx=50, ipady=10)


########################################################################################################################
################################### This Section is the Test Section ###################################################
########################################################################################################################

################################################Test View###############################################################
def back_test_view():
    show_main_menu()
    tviewFrame.grid_forget()
    back_btn_tview.grid_forget()
    header_tview.grid_forget()
    return


# Create Function to View a Test
def test_view():
    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "t.test_id"
        elif sort_order == "Type":
            order_by = "tot.test_name"
        elif sort_order == "Title":
            order_by = "t.test_title"
        elif sort_order == "Time":
            order_by = "t.test_time"
        else:
            order_by = "t.test_id"  # Fallback

        c.execute(f"""
                SELECT t.test_id, tot.test_name, t.test_title, t.test_time
                FROM Test t
                JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                ORDER BY {order_by}
            """)
        results = c.fetchall()

        for row in results:
            num_questions = count_questions_test_id(row[0])
            tree.insert("", "end", values=row + (num_questions,))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global tviewFrame
    tviewFrame = Frame(root, bd=2)
    tviewFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_tview
    header_tview = create_header_label(root, "Test Overview")

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(tviewFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown_test = create_dropdown_hor(sortFrame, ["ID", "Type", "Title", "Time"], sort_var, 0, 0, 2,
                                             state="readonly",
                                             text="Sort test by:")

    #Create a Frame for the treeview
    treeFrame = Frame(tviewFrame, bd=5)
    treeFrame.grid(row=1, column=0, sticky="nsew")

    # Define columns for the treeview
    columns = ("tid", "ttype", "ttitle", "ttime", "numq")

    # Create a treeview with the defined columns
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=6)

    # Set headers
    tree.heading("tid", text="ID", anchor="w")
    tree.heading("ttype", text="Type", anchor="w")
    tree.heading("ttitle", text="Title", anchor="w")
    tree.heading("ttime", text="Time", anchor="w")
    tree.heading("numq", text="# of Questions", anchor="w")

    # Set the columns
    tree.column("tid", width=40, anchor="w")
    tree.column("ttype", width=200, anchor="w")
    tree.column("ttitle", width=620, anchor="w")
    tree.column("ttime", width=100, anchor="w")
    tree.column("numq", width=100, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("""
        SELECT t.test_id, tot.test_name, t.test_title, t.test_time
        FROM Test t
        JOIN Types_Of_Test tot ON t.test_type = tot.test_type
        ORDER BY t.test_id
            """)

    records = c.fetchall()

    def countQuestions(t_id):
        # Query Test Questions table for count of questions
        c.execute("SELECT COUNT(question_id) AS num_questions FROM Test_Questions WHERE test_id = ?", (t_id,))

        # Get the result
        result = c.fetchone()

        # Get the count if any questions were found, else set to 0
        num_questions = result[0] if result else 0

        return num_questions

    # Loop through and display each question in the treeview
    for row in records:
        num_questions = countQuestions(row[0])
        tree.insert("", "end", values=row + (num_questions,))

    # Create a Frame for displaying questions
    questionFrame = Frame(tviewFrame, bd=2)
    questionFrame.grid(row=2, column=0, pady=5, padx=5, sticky='nsew')

    # Get all test IDs
    c.execute("SELECT test_id FROM Test")
    test_ids = [row[0] for row in c.fetchall()]

    # Sort IDs in ascending order
    test_ids = sorted(test_ids)

    selected_tid = StringVar()
    # selected_tid.set(test_ids[0])  # Set the first question ID as default

    text = "Select test ID to display questions: "
    test_dropdown = create_dropdown_hor(questionFrame, test_ids, selected_tid, 0, 0, 2, "normal", text)

    # Get answers for selected question ID
    def getQuestions(event=None):
        # Reconnect to the database
        cnx = get_db_connection()

        # Create cursor
        c = cnx.cursor()

        qTreeFrame = Frame(questionFrame, bd=10)
        qTreeFrame.grid(row=1, column=0, sticky="nsew", columnspan=5)

        qColumns = ("qid", "q", "qcat", "qdif")

        qTree = ttk.Treeview(qTreeFrame, columns=qColumns, show="headings", height=5)

        # Set headers
        qTree.heading("qid", text="ID", anchor="w")
        qTree.heading("q", text="Question", anchor="w")
        qTree.heading("qcat", text="Category", anchor="w")
        qTree.heading("qdif", text="Difficulty", anchor="w")

        # Set the columns
        qTree.column("qid", width=40, anchor="w")
        qTree.column("q", width=800, anchor="w")
        qTree.column("qcat", width=120, anchor="w")
        qTree.column("qdif", width=100, anchor="w")

        qTree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(qTreeFrame, orient="vertical", command=qTree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        qTree.configure(yscrollcommand=scrollbar.set)

        # Get the selected question ID
        selected_test_id = selected_tid.get()

        query = ("""
            SELECT q.question_id, q.question, qc.category_name, q.question_difficulty 
            FROM Questions q 
            JOIN Test_Questions tq ON q.question_id = tq.question_id 
            JOIN Question_Categories qc ON q.category_id = qc.category_id 
            WHERE tq.test_id = ?
        """)
        c.execute(query, (selected_test_id,))
        questions = c.fetchall()

        for row in qTree.get_children():
            qTree.delete(row)

        for item in questions:
            qTree.insert("", "end", values=item)

        # Close connection and cursor
        c.close()
        cnx.close()

    test_dropdown.bind("<<ComboboxSelected>>", getQuestions)

    # Show questions for the first test as default
    getQuestions()

    global back_btn_tview
    back_btn_tview = create_back_button(root, back_test_view)
    return


###################################################Test Make############################################################
def back_test_make():
    show_main_menu()
    tmakeFrame.grid_forget()
    back_btn_tmake.grid_forget()
    header_tmake.grid_forget()
    return


# Create Function to Make a Test
def test_make():
    # Variables to track selected questions
    selected_questions = set()

    # Realtime counter of selected questions
    def updateQuestionCounter():
        question_counter_label.config(text=f"Questions selected: {len(selected_questions)}")

    # Load all questions for each category on screen
    def loadQuestionsForCategory(event=None):
        # Clear previous questions
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if category_names:
            selected_category_id = category_ids[category_dropdown.current()]
        else:
            selected_category_id = 0

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        # Get questions for the selected category
        c.execute("""
            SELECT question_id, question, category_id, question_difficulty
            FROM Questions
            WHERE category_id = ?
            ORDER BY question_difficulty
        """, (selected_category_id,))

        questions = c.fetchall()
        cnx.close()

        # Create headers for a question list
        Label(question_frame, text="Question", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=W, padx=5)
        Label(question_frame, text="Difficulty", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=W, padx=5)

        checkbox_vars.clear()

        # Add questions in a list format
        def toggle_question(qid, var):
            if var.get():
                selected_questions.add(qid)
            else:
                selected_questions.discard(qid)
            updateQuestionCounter()

        for i, (q_id, q_text, qc_id, q_diff) in enumerate(questions, start=1):
            var = IntVar(value=1 if q_id in selected_questions else 0)

            # Keep track of checkboxes
            checkbox_vars.append(var)

            ttk.Checkbutton(scrollable_frame, text=q_text, variable=var,
                            command=lambda q=q_id, v=var: toggle_question(q, v)).grid(row=i, column=0, columnspan=4,
                                                                                      sticky="w", padx=10)
            Label(scrollable_frame, text=q_diff, anchor="e").grid(row=i, column=4, sticky="e", padx=15)

    def addTest():
        if not var.get().strip():
            messagebox.showerror("Error", "Please enter a Test Type.")
            return

        if not ttitle_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Test Title.")
            return

        if not selected_questions:
            messagebox.showerror("Error", "Please select at least one question.")
            return

        try:
            test_time = float(ttime_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Time must be a numeric value.")
            return

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Get new test ID
            c.execute("SELECT COALESCE(MAX(test_id), 0) +1 FROM Test")
            new_test_id = c.fetchone()[0]

            # Get test type ID
            c.execute("SELECT test_type FROM Types_Of_Test WHERE test_name = ?", (var.get(),))
            test_type_id = c.fetchone()[0]

            # Insert new test
            c.execute("""
                INSERT INTO Test (test_id, test_type, test_title, test_time) 
                VALUES (?, ?, ?, ?)""",
                      (new_test_id, test_type_id, ttitle_entry.get(), test_time))

            # Insert selected questions
            for question_id in selected_questions:
                c.execute("""
                    INSERT INTO Test_Questions (test_id, question_id) 
                    VALUES (?, ?)""",
                          (new_test_id, question_id))

            cnx.commit()
            messagebox.showinfo("Success",
                                f"Test {new_test_id} created successfully with {len(selected_questions)} questions!")

            # Reset fields
            cate_drop.set('')
            ttitle_entry.delete(0, END)
            ttime_entry.delete(0, END)
            selected_questions.clear()
            updateQuestionCounter()

            # Reset all checkboxes
            for box in checkbox_vars:
                box.set(0)


        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            cnx.rollback()
        finally:
            cnx.close()

    hide_main_menu()

    global tmakeFrame
    tmakeFrame = Frame(root, bd=2)
    tmakeFrame.grid(row=1, pady=10, padx=20)

    global header_tmake
    header_tmake = create_header_label(root, "Create Tests")

    test_frame = Frame(tmakeFrame)
    test_frame.grid(row=0, column=0, sticky="nsew")
    test_frame.columnconfigure(5, weight=1)

    question_frame = LabelFrame(tmakeFrame, text="")
    question_frame.grid(row=2, column=0, sticky="nsew")

    canvas = Canvas(question_frame, width=1000)
    canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")
    scrollbar = ttk.Scrollbar(question_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=4, sticky="ns")

    # Create scrollable frame inside canvas
    global scrollable_frame
    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1000)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    def on_frame_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    question_frame.grid_rowconfigure(0, weight=1)  # Make sure row 0 (where canvas is) expands
    question_frame.grid_columnconfigure(0, weight=1)

    Label(test_frame, text="Test ID").grid(row=0, column=0)
    Label(test_frame, text="Title").grid(row=0, column=3, sticky="w")
    Label(test_frame, text="Time (minutes)").grid(row=0, column=6, sticky="w")

    checkbox_vars = []

    # Finding the test ID

    # Connect to database
    cnx = get_db_connection()
    c = cnx.cursor()

    # Get new test ID
    c.execute("SELECT COALESCE(MAX(test_id), 0) +1 FROM Test")
    new_test_id = c.fetchone()[0]

    # Close database
    cnx.close()

    tid_label = Label(test_frame, text=new_test_id)
    tid_label.grid(row=1, column=0, sticky="w")

    # Connect to Database
    cnx = get_db_connection()
    c = cnx.cursor()
    c.execute("""
        SELECT * FROM Types_Of_Test
        ORDER BY test_name """)
    test_types = [row[1] for row in c.fetchall()]
    cnx.close()

    # Make the drop-down menu with all the test types
    var = StringVar()
    cate_drop = create_dropdown_ver(test_frame, test_types, var, 0, 1, 2, "normal", text="Type")
    cate_drop.grid(ipadx=25)

    # Label for test title
    ttitle_entry = ttk.Entry(test_frame)
    ttitle_entry.grid(row=1, column=3, columnspan=3, sticky="ew", padx=2)

    # Label for test time
    ttime_entry = ttk.Entry(test_frame)
    ttime_entry.grid(row=1, column=6, sticky="ew", padx=2)

    # Label that tells the user how many questions are
    # currently selected
    question_counter_label = Label(test_frame, text="Questions selected: 0", font=("Arial", 10, "bold"), anchor="e")
    question_counter_label.grid(row=2, column=4, columnspan=3, sticky="e")

    cnx = get_db_connection()
    c = cnx.cursor()
    c.execute("""SELECT category_id, category_name 
                 FROM Question_Categories 
                 ORDER BY category_name""")
    categories = c.fetchall()

    # Initialize empty lists
    category_ids = []
    category_names = []

    # Populate lists using a loop
    for category in categories:
        category_ids.append(category[0])
        category_names.append(category[1])

    # Close the database
    cnx.close()

    # Create a dropdown for selecting the question category
    category_var = StringVar()

    # Set the first category as default
    # category_var.set(category_names[0])

    category_dropdown = create_dropdown_hor(test_frame, category_names, category_var, 2, 0, 2, "readonly",
                                            "Select question category: ")
    category_dropdown.grid(pady=10)

    category_dropdown.bind("<<ComboboxSelected>>", loadQuestionsForCategory)
    if category_names:
        category_dropdown.current(0)
    else:
        category_dropdown.set("")

    loadQuestionsForCategory()

    ttk.Button(tmakeFrame, text="Create Test", command=addTest, style="Accent.TButton", width=20).grid(row=3, column=0,
                                                                                                       sticky="e",
                                                                                                       pady=15)

    global back_btn_tmake
    back_btn_tmake = create_back_button(root, back_test_make)

    return


#################################################Test Modify############################################################
def back_test_modify():
    show_main_menu()
    tmodifyFrame.grid_forget()
    back_btn_tmodify.grid_forget()
    header_tmodify.grid_forget()
    return


def test_modify():
    # When refreshing the page, destroy the previous frame
    if 'tmodifyFrame' in globals():
        back_test_modify()

    # Variables to track selected questions
    selected_questions = set()

    # Define tree at the function level, so it's accessible to all nested functions
    tree = None

    # Sort the tree view
    def load_categories(sort_order):
        # Use the tree variable from the outer scope
        nonlocal tree

        if tree:  # Make sure tree is defined before trying to use it
            for item in tree.get_children():
                tree.delete(item)

            cnx = get_db_connection()
            c = cnx.cursor()

            # Build the ORDER BY clause based on the selected sort order
            if sort_order == "ID":
                order_by = "t.test_id"
            elif sort_order == "Type":
                order_by = "tot.test_name"
            elif sort_order == "Title":
                order_by = "t.test_title"
            elif sort_order == "Time":
                order_by = "t.test_time"
            else:
                order_by = "t.test_id"  # Fallback

            c.execute(f"""
                        SELECT t.test_id, tot.test_name, t.test_title, t.test_time
                        FROM Test t
                        JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                        ORDER BY {order_by}
                    """)
            results = c.fetchall()

            for row in results:
                tree.insert("", "end", values=row)

            cnx.commit()
            cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    # Realtime counter of selected questions
    def updateQuestionCounter():
        question_counter_label.config(text=f"Questions selected: {len(selected_questions)}")

    def submitChange():
        # Validate that the title is entered
        if not title.get().strip():
            messagebox.showerror("Error", "There is no title submitted.")
            return

        # Validate a test is selected in the dropdown menu
        if len(var.get()) == 0:
            messagebox.showerror("Error", "No test is selected.")
            return

        # Validate a time is entered
        if not time.get().strip():
            messagebox.showerror("Error", "There is no time submitted.")
            return

        # Validate the time is a number
        if not time.get().isdigit():
            messagebox.showerror("Error", "Please enter a number for the time.")
            return

        # New inputs

        # Get the selected test from dropdown
        selected_test_title = var.get().strip()

        # Get new title input
        new_test_title = title.get().strip()

        # Convert input to float
        new_test_time = int(time.get().strip())

        # Get the new test type
        new_test_type_name = type_var.get().strip()

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Fetch test_id
            c.execute("SELECT test_id FROM Test WHERE test_id = ?", (selected_test_title,))
            test_info = c.fetchone()

            if not test_info:
                messagebox.showerror("Error", "Selected test does not exist.")
                return

            # Extract test_id
            test_id = test_info[0]

            # Fetch test_type ID based on selected test type name
            c.execute("SELECT test_type FROM Types_Of_Test WHERE test_name = ?", (new_test_type_name,))
            test_type_info = c.fetchone()

            if not test_type_info:
                messagebox.showerror("Error", "Selected test type does not exist.")
                return

            new_test_type = test_type_info[0]

            # Update test title, time and type
            c.execute("""
                    UPDATE Test 
                    SET test_title = ?, test_time = ?, test_type = ?
                    WHERE test_id = ?
                """, (new_test_title, new_test_time, new_test_type, test_id))

            # Clear existing questions for this test
            c.execute("DELETE FROM Test_Questions WHERE test_id = ?", (test_id,))

            # Insert newly selected questions
            for qid in selected_questions:
                c.execute("INSERT INTO Test_Questions (test_id, question_id) VALUES (?, ?)", (test_id, qid))

            # Commit changes
            cnx.commit()
            messagebox.showinfo("Success", "Test has been successfully updated.")

            test_modify()

        except Exception as e:
            cnx.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

        finally:
            cnx.close()

    def question_canvas():
        # Clear previous questions
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        # Fetch all the question
        c.execute("""
                    SELECT question_id, question, question_difficulty
                    FROM Questions
                    ORDER BY question_difficulty
                        """)
        all_questions_in_cat = c.fetchall()

        # Create headers for the question list
        Label(question_frame, text="Question", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        Label(question_frame, text="Difficulty", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", padx=5)

        # Display questions in the question frame
        def toggle_question(qid, var):
            if var.get():
                selected_questions.add(qid)
            else:
                selected_questions.discard(qid)
            updateQuestionCounter()

        for i, (q_id, q_text, q_diff) in enumerate(all_questions_in_cat, start=1):
            var = IntVar(value=1 if q_id in all_questions_in_cat else 0)

            # Cut the question length to 70 characters
            shortened_qtitle = q_text[:70] + "..." if len(q_text) > 70 else q_text

            ttk.Checkbutton(scrollable_frame, text=shortened_qtitle, variable=var,
                            command=lambda q=q_id, v=var: toggle_question(q, v)).grid(row=i, column=0, sticky="w",
                                                                                      padx=5)
            Label(scrollable_frame, text=q_diff).grid(row=i, column=1, sticky="e", padx=5)

        cnx.close()

        return

    def test_selection_dis(event=None):
        # Get the selected test id
        selected_test_id = test_drop.get()

        # Clear out the old results
        title.delete(0, END)
        test_type_dropdown.set('')
        time.delete(0, END)

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        # Fetch test details using the selected title
        c.execute("""
            SELECT test_id, test_type, test_title, test_time 
            FROM Test 
            WHERE test_id = ?""",
                  (selected_test_id,))

        test_info = c.fetchone()

        if not test_info:
            cnx.close()
            return  # Exit if no test is found

        test_id, test_type, test_title_value, test_time_value = test_info

        # Update UI elements
        title.insert(0, test_title_value)
        time.insert(0, str(test_time_value))

        # Get Category Name for Dropdown
        c.execute("SELECT test_name FROM Types_Of_Test WHERE test_type = ?", (test_type,))
        category_name = c.fetchone()

        if category_name:
            test_type_dropdown.set(category_name[0])

        # Fetch only the selected questions
        c.execute("""
            SELECT q.question_id
            FROM Questions q
            JOIN Test_Questions tq ON q.question_id = tq.question_id
            WHERE tq.test_id = ?
        """, (test_id,))
        selected_question_ids = {qid for (qid,) in c.fetchall()}  # Store selected questions in a set

        # Fetch all available questions (not just selected ones)
        c.execute("""
            SELECT question_id, question, question_difficulty
            FROM Questions
            ORDER BY question_difficulty
        """)
        all_questions = c.fetchall()

        # Clear previous questions
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Clear and update selected questions
        selected_questions.clear()

        def toggle_question(qid, var):
            if var.get():
                selected_questions.add(qid)
            else:
                selected_questions.discard(qid)
            updateQuestionCounter()

        # Display all questions but check only the selected ones
        for i, (q_id, q_text, q_diff) in enumerate(all_questions, start=1):
            is_selected = q_id in selected_question_ids
            var = IntVar(value=1 if is_selected else 0)

            if is_selected:
                selected_questions.add(q_id)  # Track initially selected questions

            # Cut the question length to 70 characters
            shortened_qtitle = q_text[:70] + "..." if len(q_text) > 70 else q_text

            ttk.Checkbutton(scrollable_frame, text=shortened_qtitle, variable=var,
                            command=lambda q=q_id, v=var: toggle_question(q, v)).grid(row=i, column=0, sticky="w",
                                                                                      padx=5)
            Label(scrollable_frame, text=q_diff).grid(row=i, column=3, sticky="e", padx=5)

        # Update question counter to reflect initially selected questions
        updateQuestionCounter()

        # Close database connection
        cnx.close()

    def test_treeview():
        # Define columns for the treeview
        columns = ("tid", "ttype", "ttitle")

        # Create a treeview with the defined columns
        nonlocal tree  # Use the tree from the outer scope
        tree = ttk.Treeview(modify_frame, columns=columns, show="headings", height=6)

        # Set headers
        tree.heading("tid", text="ID", anchor="w")
        tree.heading("ttype", text="Type", anchor="w")
        tree.heading("ttitle", text="Title", anchor="w")

        # Set the columns
        tree.column("tid", width=50, anchor="w")
        tree.column("ttype", width=220, anchor="w")
        tree.column("ttitle", width=250, anchor="w")

        tree.grid(row=0, column=0, sticky="nsew", columnspan=3, rowspan=5)

        scrollbar = ttk.Scrollbar(modify_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=2, sticky="nse", rowspan=5)
        tree.configure(yscrollcommand=scrollbar.set)

        # Connect to Database
        cnx = get_db_connection()

        # Create a Cursor
        c = cnx.cursor()

        # Query Questions Table for all Questions
        c.execute("""
                    SELECT t.test_id, tot.test_name, t.test_title
                    FROM Test t
                    JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                    ORDER BY t.test_id
                        """)

        records = c.fetchall()
        ids = []

        # Loop through and display each question in the treeview
        for row in records:
            ids.append(row[0])
            tree.insert("", "end", values=row)

        cnx.commit()
        cnx.close()

        return ids

    hide_main_menu()

    # Number of rows
    global num_rows_qdelete
    num_rows_qdelete = 0

    # Create a Frame
    global tmodifyFrame
    tmodifyFrame = Frame(root, bd=2)
    tmodifyFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_tmodify
    header_tmodify = create_header_label(root, "Modify Tests")

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(tmodifyFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown_test = create_dropdown_hor(sortFrame, ["ID", "Type", "Title", "Time"], sort_var, 0, 0, 2,
                                             state="readonly",
                                             text="Sort test by:")

    modify_frame = Frame(tmodifyFrame, bd=2)
    modify_frame.grid(row=1, column=0, sticky="nsew")

    # Create a Frame for question category dropdown
    question_category_frame = Frame(tmodifyFrame, bd=2)
    question_category_frame.grid(row=2, column=0)

    # Create a Frame for a scrollable canvas with questions
    question_frame = LabelFrame(tmodifyFrame, text="")
    question_frame.grid(row=3, column=0, sticky="nw", columnspan=2)

    # Create Canvas
    canvas = Canvas(question_frame, width=600, height=200)
    canvas.grid(row=1, column=0, columnspan=4, sticky="nw")
    scrollbar = ttk.Scrollbar(question_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=4, sticky="ns")

    # Create scrollable frame inside canvas
    global scrollable_frame
    scrollable_frame = Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=600)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    def on_frame_configure(event):
        canvas.config(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Ensure row 0 expands
    question_frame.grid_rowconfigure(0, weight=1)
    question_frame.grid_columnconfigure(0, weight=1)

    question_canvas()

    test_ids = test_treeview()

    var = StringVar()

    # Dropdown positioned right after the list of tests
    test_drop = create_dropdown_hor(modify_frame, test_ids, var, 0, 3, 2, "normal",
                                    text="   Select test by ID:")

    # Create a Binding for the Dropdown menu to change the Question ID
    test_drop.bind("<<ComboboxSelected>>", test_selection_dis)

    # Label that tells the user how many questions are
    # currently selected
    question_counter_label = Label(modify_frame, text="Questions selected: 0", font=("Arial", 10, "bold"))
    question_counter_label.grid(row=7, column=0, columnspan=1, sticky="w", pady=10)

    # QUESTIONS FRAME

    category_frame = Frame(tmodifyFrame)
    category_frame.grid(row=1, column=3, columnspan=1, sticky="w")

    cnx = get_db_connection()
    c = cnx.cursor()
    c.execute("""SELECT test_type, test_name 
                 FROM Types_Of_Test 
                 ORDER BY test_name""")
    types = c.fetchall()

    # Initialize empty lists
    test_type = []
    test_name = []

    # Populate lists using a loop
    for type in types:
        test_type.append(type[0])
        test_name.append(type[1])

    # Close the database
    cnx.close()

    # Create a dropdown for selecting the Test Type
    type_var = StringVar()
    test_type_dropdown = create_dropdown_hor(modify_frame, test_name, type_var, 1, 3, 3, "readonly",
                                             "   Current test type: ")

    # Label and text box for test title
    Label(modify_frame, text="Test Title:").grid(row=2, column=3, sticky="w", padx=10)
    title = ttk.Entry(modify_frame, width=50)
    title.grid(row=2, column=4, columnspan=3, sticky="e", padx=10)

    Label(modify_frame, text="Test Time:").grid(row=4, column=3, sticky="w", padx=10)
    time = ttk.Entry(modify_frame, width=10)
    time.grid(row=4, column=4, columnspan=2, sticky="e")

    ttk.Button(modify_frame, text="Modify Test", command=submitChange, style="Accent.TButton").grid(row=4, column=6,
                                                                                                    pady=10)

    global back_btn_tmodify
    back_btn_tmodify = create_back_button(root, back_test_modify)

    # Load the initial sorted data
    load_categories(sort_var.get())

    return


###################################################Test Delete##########################################################

def back_test_delete():
    show_main_menu()
    tdeleteFrame.grid_forget()
    back_btn_tdelete.grid_forget()
    header_tdelete.grid_forget()
    return


# Create Function to Delete a Test
def test_delete():
    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "t.test_id"
        elif sort_order == "Type":
            order_by = "tot.test_name"
        elif sort_order == "Title":
            order_by = "t.test_title"
        elif sort_order == "Time":
            order_by = "t.test_time"
        else:
            order_by = "t.test_id"  # Fallback

        c.execute(f"""
                    SELECT t.test_id, tot.test_name, t.test_title, t.test_time
                    FROM Test t
                    JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                    ORDER BY {order_by}
                """)
        results = c.fetchall()

        for row in results:
            num_questions = count_questions_test_id(row[0])
            tree.insert("", "end", values=row + (num_questions,))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global tdeleteFrame

    # Destroy existing frame to prevent duplicates
    if 'tdeleteFrame' in globals() and tdeleteFrame.winfo_exists():
        tdeleteFrame.destroy()

    tdeleteFrame = Frame(root, bd=2)
    tdeleteFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_tdelete
    header_tdelete = create_header_label(root, "Delete Tests")

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(tdeleteFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown_test = create_dropdown_hor(sortFrame, ["ID", "Type", "Title", "Time"], sort_var, 0, 0, 2,
                                             state="readonly",
                                             text="Sort test by:")

    # Create a Frame for the treeview
    treeFrame = Frame(tdeleteFrame, bd=10)
    treeFrame.grid(row=1, column=0, sticky="nsew", columnspan=5)

    # Define columns for the treeview
    columns = ("tid", "ttype", "ttitle", "ttime", "numq")

    # Create a treeview with the defined columns
    global tree
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=6)

    # Set headers
    tree.heading("tid", text="ID", anchor="w")
    tree.heading("ttype", text="Type", anchor="w")
    tree.heading("ttitle", text="Title", anchor="w")
    tree.heading("ttime", text="Time", anchor="w")
    tree.heading("numq", text="# of Questions", anchor="w")

    # Set the columns
    tree.column("tid", width=40, anchor="w")
    tree.column("ttype", width=200, anchor="w")
    tree.column("ttitle", width=620, anchor="w")
    tree.column("ttime", width=100, anchor="w")
    tree.column("numq", width=100, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    def showTestForDelete():
        # Clear the tree completely before inserting new data
        tree.delete(*tree.get_children())

        # Connect to Database
        cnx = get_db_connection()

        # Create a Cursor
        c = cnx.cursor()

        # Query Questions Table for all Questions
        c.execute("""
                SELECT t.test_id, tot.test_name, t.test_title, t.test_time
                FROM Test t
                JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                    """)

        records = c.fetchall()

        def countQuestions(t_id):
            # Query Test Questions table for count of questions
            c.execute("SELECT COUNT(question_id) AS num_questions FROM Test_Questions WHERE test_id = ?", (t_id,))

            # Get the result
            result = c.fetchone()

            # Get the count if any questions were found, else set to 0
            num_questions = result[0] if result else 0

            return num_questions

        # Loop through and display each question in the treeview
        for row in records:
            num_questions = countQuestions(row[0])
            tree.insert("", "end", values=row + (num_questions,))

        # Commit Changes
        cnx.commit()

        # Close Connection
        cnx.close()

        return

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
            c.execute("SELECT * FROM Test WHERE test_id= ?", (question_id,))
            results = c.fetchall()
            if len(results) == 0:
                messagebox.showerror("Error", f"{question_id} is not a valid Test ID.")
                return

            # Delete Answers for the same Question ID
            c.execute("DELETE FROM Test_Questions WHERE test_id= ?", (question_id,))
            # Delete Proper Question ID From Questions Table
            c.execute("DELETE from Test WHERE test_id= ?", (question_id,))

            # Commit Changes
            cnx.commit()
            # Close Connection
            cnx.close()

            tdeleteFrame.grid_forget()
            back_btn_tdelete.grid_forget()
            header_tdelete.grid_forget()
            test_delete()
        else:
            return

        showTestForDelete()

    showTestForDelete()
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
    # selected_tid.set(test_ids[0])  # Set the first question ID as default

    text = "Select test ID to delete: "
    test_dropdown = create_dropdown_hor(tdeleteFrame, test_ids, selected_tid, 2, 0, 1, "normal", text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Label(tdeleteFrame, text="Test ID to Delete: ").grid(row=3, column=0)
    # delete_box = ttk.Entry(tdeleteFrame, width=10)
    # delete_box.grid(row=3, column=1)
    deleteQuestion_btn = ttk.Button(tdeleteFrame, text="Delete Test", command=deleteQuestion, style="Accent.TButton")
    deleteQuestion_btn.grid(row=2, column=1, sticky="e", padx=10, ipadx=20)

    global back_btn_tdelete
    back_btn_tdelete = create_back_button(root, back_test_delete)

    return


##############################################Test Extract##############################################################
# Create a Function to Return to Original View
def back_test_extract():
    show_main_menu()
    textractFrame.grid_forget()
    back_btn_textract.grid_forget()
    header_textract.grid_forget()
    return


# Create Function to Extract a Test
def test_extract():
    # Sort the tree view
    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        # Build the ORDER BY clause based on the selected sort order
        if sort_order == "ID":
            order_by = "t.test_id"
        elif sort_order == "Type":
            order_by = "tot.test_name"
        elif sort_order == "Title":
            order_by = "t.test_title"
        elif sort_order == "Time":
            order_by = "t.test_time"
        else:
            order_by = "t.test_id"  # Fallback

        c.execute(f"""
                        SELECT t.test_id, tot.test_name, t.test_title, t.test_time
                        FROM Test t
                        JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                        ORDER BY {order_by}
                    """)
        results = c.fetchall()

        for row in results:
            num_questions = count_questions_test_id(row[0])
            tree.insert("", "end", values=row + (num_questions,))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Show header
    global header_textract
    header_textract = create_header_label(root, "Export Tests")

    # Create a Frame this option
    global textractFrame
    textractFrame = Frame(root, bd=2)
    textractFrame.grid(row=1, pady=10, padx=20)

    # Create a Frame for the sort dropdown menu
    sortFrame = Frame(textractFrame, bd=1)
    sortFrame.grid(row=0, column=0, padx=10, sticky="nsew")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown_test = create_dropdown_hor(sortFrame, ["ID", "Type", "Title", "Time"], sort_var, 0, 0, 2,
                                             state="readonly",
                                             text="Sort test by:")

    # Create a Frame for the treeview
    treeFrame = Frame(textractFrame, bd=10)
    treeFrame.grid(row=1, column=0, sticky="nsew")

    # Define columns for the treeview
    columns = ("tid", "ttype", "ttitle", "ttime", "numq")

    # Create a treeview with the defined columns
    tree = ttk.Treeview(treeFrame, columns=columns, show="headings", height=6)

    # Set headers
    tree.heading("tid", text="ID", anchor="w")
    tree.heading("ttype", text="Type", anchor="w")
    tree.heading("ttitle", text="Title", anchor="w")
    tree.heading("ttime", text="Time", anchor="w")
    tree.heading("numq", text="# of Questions", anchor="w")

    # Set the columns
    tree.column("tid", width=40, anchor="w")
    tree.column("ttype", width=200, anchor="w")
    tree.column("ttitle", width=620, anchor="w")
    tree.column("ttime", width=100, anchor="w")
    tree.column("numq", width=100, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    # Query Questions Table for all Questions
    c.execute("""
            SELECT t.test_id, tot.test_name, t.test_title, t.test_time
            FROM Test t
            JOIN Types_Of_Test tot ON t.test_type = tot.test_type
                """)

    records = c.fetchall()

    def countQuestions(t_id):
        # Query Test Questions table for count of questions
        c.execute("SELECT COUNT(question_id) AS num_questions FROM Test_Questions WHERE test_id = ?", (t_id,))

        # Get the result
        result = c.fetchone()

        # Get the count if any questions were found, else set to 0
        num_questions = result[0] if result else 0

        return num_questions

    # Loop through and display each question in the treeview
    for row in records:
        num_questions = countQuestions(row[0])
        tree.insert("", "end", values=row + (num_questions,))

    # Commit Changes
    cnx.commit()

    # Close Connection
    cnx.close()

    #Create a Frame for extract button and dropdown
    butFrame = Frame(textractFrame, bd=2)
    butFrame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

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
    # selected_tid.set(test_ids[0])  # Set the first question ID as default

    text = "Select test ID to Export to QTI .zip file: "
    test_dropdown = create_dropdown_hor(butFrame, test_ids, selected_tid, 1, 0, 2, "normal", text)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()
    # Label(butFrame, text="Test ID for QTI Extraction: ").grid(row=3, column=0)
    # select_box = ttk.Entry(butFrame, width=10)
    # select_box.grid(row=3, column=1)
    extract_btn = ttk.Button(butFrame, text="Export QTI .zip File for Test",
                             command=lambda: test2qti(test_dropdown.get()), style="Accent.TButton")
    extract_btn.grid(row=2, column=4, sticky='e', padx=10)

    # Create a Back Button to Hide Current View and Reshow Original View
    global back_btn_textract
    back_btn_textract = create_back_button(root, back_test_extract)

    return


##############################################Test Buttons##############################################################
# Create View Test Button
viewTest_btn = ttk.Button(test_frame, text="View Test", command=test_view, width=13)
viewTest_btn.grid(row=1, column=0, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Add Test Button
makeTest_btn = ttk.Button(test_frame, text="Make Test", command=test_make, width=13)
makeTest_btn.grid(row=1, column=1, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Modify Test Button
modifyTest_btn = ttk.Button(test_frame, text="Modify Test", command=test_modify, width=13)
modifyTest_btn.grid(row=1, column=2, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Delete Test Button
deleteTest_btn = ttk.Button(test_frame, text="Delete Test", command=test_delete, width=13)
deleteTest_btn.grid(row=1, column=3, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Extract Test Button
extractTest_btn = ttk.Button(test_frame, text="Extract Test", command=test_extract, width=13)
extractTest_btn.grid(row=2, column=1, columnspan=2, pady=10, padx=10, ipadx=50, ipady=10)


########################################################################################################################
################################### This Section is Question Type Options ##############################################
########################################################################################################################
######################################## Question Option Add ###########################################################
def back_quest_cat_add():
    show_main_menu()
    questCatAddFrame.grid_forget()
    back_btn_questCatAdd.grid_forget()
    header_qcatadd.grid_forget()
    return


def quest_cat_add():
    # When refreshing the page, destroy the previous frame
    if 'questCatAddFrame' in globals():
        back_quest_cat_add()

    def addNewQuestCat():

        # Making sure the user input a Question Category Title
        if not qctitle_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Question Category Title.")
            return

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Find the last Category ID and increment
            c.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM Question_Categories")
            new_questCat_id = c.fetchone()[0]

            # Insert New Category
            c.execute(
                """INSERT INTO Question_Categories (category_id, category_name) 
                   VALUES (?, ?)""",
                (new_questCat_id, qctitle_entry.get())
            )

            # Commit Changes
            cnx.commit()
            messagebox.showinfo("Success", f"Question category {new_questCat_id} added successfully!")

            # Clear input field
            qctitle_entry.delete(0, END)

            # Refresh the UI
            quest_cat_add()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            cnx.rollback()
        finally:
            cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_id")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global questCatAddFrame
    questCatAddFrame = Frame(root, bd=2)
    questCatAddFrame.grid(row=1, pady=10, padx=20)

    # Show header
    global header_qcatadd
    header_qcatadd = create_header_label(root, "Add Question Categories")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    sort_dropdown = create_dropdown_ver(questCatAddFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2,
                                        state="readonly", text="Sort categories by:")

    # Create a treeview for displaying categories
    tree = ttk.Treeview(questCatAddFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(questCatAddFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()

    for row in results:
        tree.insert("", "end", values=(row[0], row[1]))

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    Label(questCatAddFrame, text="Question Category Name").grid(row=3, column=0, ipadx=5)

    # If we have time, they would like to have a comment section next to the category name
    # this means editing the database and adding category_label in the Questions_Categories table

    #Label(questCatAddFrame, text="Question Type Comment").grid(row=0, column=0, ipadx=5)

    # Test Name input
    qctitle_entry = ttk.Entry(questCatAddFrame, width=50)
    qctitle_entry.grid(row=4, column=0)

    # Add Test Button
    add_questCat_btn = ttk.Button(questCatAddFrame, text="Add New Category", command=addNewQuestCat,
                                  style="Accent.TButton")
    add_questCat_btn.grid(row=5, column=0, pady=10)

    global back_btn_questCatAdd
    back_btn_questCatAdd = create_back_button(root, back_quest_cat_add)

    return


######################################## Question Option Modify ########################################################


def back_quest_cat_modify():
    show_main_menu()
    questCatModifyFrame.grid_forget()
    back_btn_questCatModify.grid_forget()
    header_qcatmodify.grid_forget()
    return


def quest_cat_modify():
    # When refreshing the page, destroy the previous frame
    if 'questCatModifyFrame' in globals():
        back_quest_cat_modify()

    def submitChanges():

        # Get the selected category and new title
        selected_category = var.get()
        new_title = qctitle_entry.get().strip()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category")
            return

        if not new_title:
            messagebox.showerror("Error", "Please write a title")

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Update the category title in the database
            c.execute("UPDATE Question_Categories SET category_name = ? WHERE category_name = ?",
                      (new_title, selected_category))
            cnx.commit()
            messagebox.showinfo("Success", f"Category '{selected_category}' updated to '{new_title}'")

            # Refresh the UI
            quest_cat_modify()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update category: {str(e)}")
        finally:
            # Close Connection
            cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_id")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global questCatModifyFrame
    questCatModifyFrame = Frame(root, bd=2)
    questCatModifyFrame.grid(row=1, pady=10, padx=20)

    global header_qcatmodify
    header_qcatmodify = create_header_label(root, "Modify Question Categories")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    create_dropdown_ver(questCatModifyFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2, state="readonly",
                        text="Sort categories by:")

    # Create a treeview for displaying categories
    tree = ttk.Treeview(questCatModifyFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(questCatModifyFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Create Dropdown Box for Question Category

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()
    cat_name = []
    var = StringVar()

    # Insert categories into treeview
    for row in results:
        cat_name.append(row[1])
        tree.insert("", "end", values=(row[0], row[1]))

    # Create dropdown for category selection
    def on_category_select(event):
        # When a category is selected, populate the entry with its current title
        selected_category = var.get()
        qctitle_entry.delete(0, END)
        qctitle_entry.insert(0, selected_category)

    cate_drop = create_dropdown_hor(questCatModifyFrame, cat_name, var, 4, 0, 1, "normal",
                                    text="Select a Question Category")
    cate_drop.bind('<<ComboboxSelected>>', on_category_select)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Test Name input
    qctitle_entry = ttk.Entry(questCatModifyFrame, width=50)
    qctitle_entry.grid(row=6, column=0, columnspan=2)

    # Button to modify
    modify_questCat_btn = ttk.Button(questCatModifyFrame, text="Modify Question Category Title", command=submitChanges,
                                     style="Accent.TButton")
    modify_questCat_btn.grid(row=7, column=0, columnspan=2, pady=10)

    global back_btn_questCatModify
    back_btn_questCatModify = create_back_button(root, back_quest_cat_modify)

    return


######################################## Question Option Delete ########################################################


def back_quest_cat_delete():
    show_main_menu()
    questCatDeleteFrame.grid_forget()
    back_btn_questCatDelete.grid_forget()
    header_qcatdelete.grid_forget()
    return


def quest_cat_delete():
    # When refreshing the page, destroy the previous frame
    if 'questCatDeleteFrame' in globals():
        back_quest_cat_delete()

    def deleteQuestCat():

        # Get the selected category
        selected_category = var.get()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category to delete.")
            return

        # Confirmation Dialog
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the category '{selected_category}'?\n\nThis will remove the category and any associated questions."
        )

        if confirm:
            # Connect to Database
            cnx = get_db_connection()
            c = cnx.cursor()

            try:
                # First, get the category_id for the selected category
                c.execute("SELECT category_id FROM Question_Categories WHERE category_name = ?", (selected_category,))
                category_id = c.fetchone()[0]

                # Delete questions associated with this category
                c.execute("DELETE FROM Questions WHERE category_id = ?", (category_id,))

                # Then delete the category from Question_Categories
                c.execute("DELETE FROM Question_Categories WHERE category_id = ?", (category_id,))

                # Commit changes
                cnx.commit()

                # Show a success message
                messagebox.showinfo("Success", f"Category '{selected_category}' has been deleted.")

                # Clear the current selection
                var.set('')

                # Refresh the UI
                quest_cat_delete()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                cnx.rollback()
            finally:
                cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_id")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Question_Categories ORDER BY category_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global questCatDeleteFrame
    questCatDeleteFrame = Frame(root, bd=2)
    questCatDeleteFrame.grid(row=1, pady=10, padx=20)

    global header_qcatdelete
    header_qcatdelete = create_header_label(root, "Delete Question Categories")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    create_dropdown_ver(questCatDeleteFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2, state="readonly",
                        text="Sort categories by:")

    # Create Dropdown Box for Test Category

    # Create a treeview for displaying categories
    tree = ttk.Treeview(questCatDeleteFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(questCatDeleteFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Question_Categories")
    results = c.fetchall()
    cat_name = []

    var = StringVar()

    for row in results:
        cat_name.append(row[1])
        tree.insert("", "end", values=(row[0], row[1]))

    cate_drop = create_dropdown_hor(questCatDeleteFrame, cat_name, var, 4, 0, 1, "normal",
                                    text="Select a question category")
    cate_drop.grid(padx=10)
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Adjust button position
    delete_questCat_btn = ttk.Button(questCatDeleteFrame, text="Delete Question Category", command=deleteQuestCat,
                                     style="Accent.TButton")
    delete_questCat_btn.grid(row=5, column=0, columnspan=2, pady=10)

    global back_btn_questCatDelete
    back_btn_questCatDelete = create_back_button(root, back_quest_cat_delete)

    return


################################################ Question Options Buttons ##############################################

# Create Add Question Option Button
addQuestCat_btn = ttk.Button(questType_frame, text="Add Question Category", command=quest_cat_add, width=13)
addQuestCat_btn.grid(row=1, column=0, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Modify Question Option Button
modifyQuestCat_btn = ttk.Button(questType_frame, text="Modify Question Category", command=quest_cat_modify, width=13)
modifyQuestCat_btn.grid(row=1, column=1, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Delete Question Option Button
deleteQuestCat_btn = ttk.Button(questType_frame, text="Delete Question Category", command=quest_cat_delete, width=13)
deleteQuestCat_btn.grid(row=1, column=2, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')


########################################################################################################################
################################### This Section is Test Type Options ##################################################
########################################################################################################################


######################################## Test Option Add ###############################################################


def back_test_cat_add():
    show_main_menu()
    testCatAddFrame.grid_forget()
    back_btn_testCatAdd.grid_forget()
    header_tcatadd.grid_forget()
    return


def test_cat_add():
    # When refreshing the page, destroy the previous frame
    if 'testCatAddFrame' in globals():
        back_test_cat_add()

    def addNewTestCat():
        # Making sure the user input a Question Category Title
        if not tctitle_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Test Category Title.")
            return

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Find the last Category ID and increment
            c.execute("SELECT COALESCE(MAX(test_type), 0) + 1 FROM Types_Of_Test")
            new_testCat_id = c.fetchone()[0]

            # Insert New Category
            c.execute(
                """INSERT INTO Types_Of_Test (test_type, test_name) 
                   VALUES (?, ?)""",
                (new_testCat_id, tctitle_entry.get())
            )

            # Commit Changes
            cnx.commit()
            messagebox.showinfo("Success", f"Question category {new_testCat_id} added successfully!")

            # Clear input field
            tctitle_entry.delete(0, END)

            # Refresh the UI
            test_cat_add()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            cnx.rollback()
        finally:
            cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_type")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global testCatAddFrame
    testCatAddFrame = Frame(root, bd=2)
    testCatAddFrame.grid(row=1, pady=10, padx=20)

    global header_tcatadd
    header_tcatadd = create_header_label(root, "Add Test Category")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    create_dropdown_ver(testCatAddFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2, state="readonly",
                        text="Sort categories by:")

    # Create a treeview for displaying categories
    tree = ttk.Treeview(testCatAddFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(testCatAddFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Types_Of_Test")
    results = c.fetchall()

    for row in results:
        tree.insert("", "end", values=(row[0], row[1]))

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    Label(testCatAddFrame, text="Enter new test category title:").grid(row=4, column=0, ipadx=5)

    # If we have time, they would like to have a comment section next to the category name
    # this means editing the database and adding category_label in the Questions_Categories table

    #Label(questCatAddFrame, text="Question Type Comment").grid(row=0, column=0, ipadx=5)

    # Test Name input
    tctitle_entry = ttk.Entry(testCatAddFrame, width=50)
    tctitle_entry.grid(row=6, column=0)

    # Add Test Button
    add_testCat_btn = ttk.Button(testCatAddFrame, text="Add New Category", command=addNewTestCat,
                                 style="Accent.TButton")
    add_testCat_btn.grid(row=8, column=0, pady=10)

    global back_btn_testCatAdd
    back_btn_testCatAdd = create_back_button(root, back_test_cat_add)

    return


######################################## Test Option Modify ############################################################


def back_test_cat_modify():
    show_main_menu()
    testCatModifyFrame.grid_forget()
    back_btn_testCatModify.grid_forget()
    header_tcatadd.grid_forget()
    return


def test_cat_modify():
    # When refreshing the page, destroy the previous frame
    if 'testCatModifyFrame' in globals():
        back_test_cat_modify()

    def submitChanges():
        # Get the selected category and new title
        selected_category = var.get()
        new_title = qctitle_entry.get().strip()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category")
            return

        if not new_title:
            messagebox.showerror("Error", "Please write a title")

        # Connect to Database
        cnx = get_db_connection()
        c = cnx.cursor()

        try:
            # Update the category title in the database
            c.execute("UPDATE Types_Of_Test SET test_name = ? WHERE test_name = ?", (new_title, selected_category))
            cnx.commit()
            messagebox.showinfo("Success", f"Test Category '{selected_category}' updated to '{new_title}'")

            # Refresh the UI
            test_cat_modify()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update test category: {str(e)}")
        finally:
            # Close Connection
            cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_type")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global testCatModifyFrame
    testCatModifyFrame = Frame(root, bd=2)
    testCatModifyFrame.grid(row=1, pady=10, padx=20)

    global header_tcatadd
    header_tcatadd = create_header_label(root, "Modify Test Category")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    create_dropdown_ver(testCatModifyFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2, state="readonly",
                        text="Sort categories by:")

    # Create a treeview for displaying categories
    tree = ttk.Treeview(testCatModifyFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(testCatModifyFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Types_Of_Test")
    results = c.fetchall()
    cat_name = []
    var = StringVar()

    # Insert categories into treeview
    for row in results:
        cat_name.append(row[1])
        tree.insert("", "end", values=(row[0], row[1]))

    # Create dropdown for category selection
    def on_category_select(event):
        # When a category is selected, populate the entry with its current title
        selected_category = var.get()
        qctitle_entry.delete(0, END)
        qctitle_entry.insert(0, selected_category)

    cate_drop = create_dropdown_hor(testCatModifyFrame, cat_name, var, 4, 0, 1, "normal",
                                    text="Select a Test Category")
    cate_drop.grid(pady=15)

    cate_drop.bind('<<ComboboxSelected>>', on_category_select)

    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    # Test Name input
    qctitle_entry = ttk.Entry(testCatModifyFrame, width=50)
    qctitle_entry.grid(row=6, column=0, columnspan=2)

    # Button to modify
    modify_testCat_btn = ttk.Button(testCatModifyFrame, text="Modify Test Category Title", command=submitChanges,
                                    style="Accent.TButton")
    modify_testCat_btn.grid(row=7, column=0, columnspan=2, pady=10)

    global back_btn_testCatModify
    back_btn_testCatModify = create_back_button(root, back_test_cat_modify)

    return


######################################## Test Option Delete ############################################################


def back_test_cat_delete():
    show_main_menu()
    testCatDeleteFrame.grid_forget()
    back_btn_testCatDelete.grid_forget()
    header_tcatdelete.grid_forget()
    return


def test_cat_delete():
    # When refreshing the page, destroy the previous frame
    if 'testCatDeleteFrame' in globals():
        back_test_cat_delete()

    def deleteTestCat():

        # Get the selected category
        selected_category = var.get()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category to delete.")
            return

        # Confirmation Dialog
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the category '{selected_category}'?\n\nThis will remove the category and any associated tests."
        )

        if confirm:
            # Connect to Database
            cnx = get_db_connection()
            c = cnx.cursor()

            try:
                # First, get the test_type for the selected category
                c.execute("SELECT test_type FROM Types_Of_Test WHERE test_name = ?", (selected_category,))
                category_id = c.fetchone()[0]

                # Delete tests associated with this category
                c.execute("DELETE FROM Test WHERE test_type = ?", (category_id,))

                # Then delete the category from Question_Categories
                c.execute("DELETE FROM Types_Of_Test WHERE test_type = ?", (category_id,))

                # Commit changes
                cnx.commit()

                # Show a success message
                messagebox.showinfo("Success", f"Category '{selected_category}' has been deleted.")

                # Clear the current selection
                var.set('')

                # Refresh the UI
                test_cat_delete()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                cnx.rollback()
            finally:
                cnx.close()

    def load_categories(sort_order):
        for item in tree.get_children():
            tree.delete(item)

        cnx = get_db_connection()
        c = cnx.cursor()

        if sort_order == "ID":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_type")
        elif sort_order == "Title":
            c.execute("SELECT * FROM Types_Of_Test ORDER BY test_name")

        results = c.fetchall()
        for row in results:
            tree.insert("", "end", values=(row[0], row[1]))

        cnx.commit()
        cnx.close()

    def on_sort_change(*args):
        selected_sort = sort_var.get()
        load_categories(selected_sort)

    hide_main_menu()

    # Create a Frame this option
    global testCatDeleteFrame
    testCatDeleteFrame = Frame(root, bd=2)
    testCatDeleteFrame.grid(row=1, pady=10, padx=20)

    global header_tcatdelete
    header_tcatdelete = create_header_label(root, "Delete Test Category")

    # DROPDOWN: Add sorting selection
    sort_var = StringVar()
    sort_var.set("ID")  # default sort
    sort_var.trace("w", on_sort_change)

    create_dropdown_ver(testCatDeleteFrame, ["ID", "Title"], sort_var, row=0, col=0, cspan=2, state="readonly",
                        text="Sort categories by:")

    # Create Dropdown Box for Test Category

    # Create a treeview for displaying categories
    tree = ttk.Treeview(testCatDeleteFrame, columns=("tcid", "tcat"), show="headings", height=5)
    tree.heading("tcid", text="Test Category ID", anchor="w")
    tree.heading("tcat", text="Test Category Title", anchor="w")

    # Define column width
    tree.column("tcid", width=100)
    tree.column("tcat", width=300)

    # Add a scrollbar to the treeview
    scrollbar = ttk.Scrollbar(testCatDeleteFrame, orient="vertical", command=tree.yview)

    # Configure tree to use the scrollbar
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=2, column=0, columnspan=2, pady=10)
    scrollbar.grid(row=2, column=2, sticky="ns", pady=10)

    # Connect to Database
    cnx = get_db_connection()

    # Create a Cursor
    c = cnx.cursor()

    c.execute("SELECT * FROM Types_Of_Test")
    results = c.fetchall()
    cat_name = []

    var = StringVar()

    for row in results:
        cat_name.append(row[1])
        tree.insert("", "end", values=(row[0], row[1]))

    cate_drop = create_dropdown_hor(testCatDeleteFrame, cat_name, var, 4, 0, 1, "normal",
                                    text="Select a test category: ")
    cate_drop.grid(padx=10)
    # Commit Changes
    cnx.commit()
    # Close Connection
    cnx.close()

    delete_testCat_btn = ttk.Button(testCatDeleteFrame, text="Delete Question Category", command=deleteTestCat,
                                    style="Accent.TButton")
    delete_testCat_btn.grid(row=5, column=0, pady=10, columnspan=2)

    global back_btn_testCatDelete
    back_btn_testCatDelete = create_back_button(root, back_test_cat_delete)

    return


################################################ Test Options Buttons ##################################################

# Create Add Question Option Button
addTestCat_btn = ttk.Button(testType_frame, text="Add Test Category", command=test_cat_add, width=13)
addTestCat_btn.grid(row=1, column=0, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Delete Question Option Button
deleteTestCat_btn = ttk.Button(testType_frame, text="Modify Test Category", command=test_cat_modify, width=13)
deleteTestCat_btn.grid(row=1, column=1, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

# Create Delete Question Option Button
deleteTestCat_btn = ttk.Button(testType_frame, text="Delete Test Category", command=test_cat_delete, width=13)
deleteTestCat_btn.grid(row=1, column=2, pady=10, padx=10, ipadx=50, ipady=10, sticky='ew')

########################################################################################################################


# Run the main event loop
root.mainloop()
