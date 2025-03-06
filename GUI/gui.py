'''import tkinter as tk
from tkinter import ttk, messagebox

class MathPlacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Placement Exam")
        self.root.geometry("800x600")
        
        # Navigation Bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        
        nav_menu = tk.Menu(menu_bar, tearoff=0)
        nav_menu.add_command(label="Add/Modify", command=self.show_add_modify)
        nav_menu.add_command(label="Make Test")
        menu_bar.add_cascade(label="Navigation", menu=nav_menu)
        
        # Layout Frames
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.center_frame = tk.Frame(root)
        self.center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Drop-down menu for categories
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.left_frame, textvariable=self.category_var, values=["Algebra", "Calculus", "Geometry", "Trigonometry"])
        self.category_menu.pack(pady=10)
        self.category_menu.bind("<<ComboboxSelected>>", self.load_questions)
        
        # Table for questions
        self.question_table = ttk.Treeview(self.center_frame, columns=("Question"), show='headings')
        self.question_table.heading("Question", text="Question")
        self.question_table.pack(fill=tk.BOTH, expand=True)
        
        self.question_table.bind("<Button-3>", self.right_click_menu)
        
        # Question input fields
        self.input_frame = tk.Frame(self.left_frame)
        self.input_frame.pack()
        
        tk.Label(self.input_frame, text="What is the Question?").pack()
        self.question_entry = tk.Entry(self.input_frame, width=50)
        self.question_entry.pack()
        
        tk.Label(self.input_frame, text="Answers").pack()
        self.answers = []
        for i in range(4):
            entry = tk.Entry(self.input_frame, width=50)
            entry.pack()
            self.answers.append(entry)
        
        # Buttons
        button_frame = tk.Frame(self.input_frame)
        button_frame.pack()
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_inputs)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(button_frame, text="Add Question", command=self.add_question)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Right-click menu
        self.right_click = tk.Menu(root, tearoff=0)
        self.right_click.add_command(label="Delete", command=self.delete_question)
        self.right_click.add_command(label="Modify", command=self.modify_question)
    
    def show_add_modify(self):
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    def load_questions(self, event=None):
        # Placeholder function for loading questions from a database
        pass
    
    def clear_inputs(self):
        self.question_entry.delete(0, tk.END)
        for entry in self.answers:
            entry.delete(0, tk.END)
    
    def add_question(self):
        question_text = self.question_entry.get()
        if question_text:
            self.question_table.insert("", "end", values=(question_text,))
            self.clear_inputs()
    
    def right_click_menu(self, event):
        item = self.question_table.identify_row(event.y)
        if item:
            self.right_click.post(event.x_root, event.y_root)
            self.selected_item = item
    
    def delete_question(self):
        if hasattr(self, 'selected_item') and self.selected_item:
            self.question_table.delete(self.selected_item)
    
    def modify_question(self):
        if hasattr(self, 'selected_item') and self.selected_item:
            values = self.question_table.item(self.selected_item, 'values')
            if values:
                self.question_entry.delete(0, tk.END)
                self.question_entry.insert(0, values[0])
                # Placeholder for populating answers
                for entry in self.answers:
                    entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathPlacementGUI(root)
    root.mainloop()
'''

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class MathPlacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Placement Exam Creator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f5f5")
        
        # Custom styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f5f5f5"
        self.primary_color = "#3498db"
        self.secondary_color = "#2980b9"
        self.accent_color = "#e74c3c"
        self.text_color = "#2c3e50"
        self.active_tab_color = "#2ecc71"  # Green color for active tab
        
        # Configure fonts
        self.default_font = tkfont.Font(family="Helvetica", size=10)
        self.header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.default_font)
        self.style.configure('TButton', background=self.primary_color, foreground='white', font=self.default_font)
        self.style.map('TButton', 
                       background=[('active', self.secondary_color), ('pressed', self.secondary_color)])
        self.style.configure('Header.TLabel', font=self.header_font)
        self.style.configure('Title.TLabel', font=self.title_font)
        self.style.configure('Accent.TButton', background=self.accent_color)
        self.style.map('Accent.TButton', 
                       background=[('active', '#c0392b'), ('pressed', '#c0392b')])
        
        # Create active tab style
        self.style.configure('Active.TButton', background=self.active_tab_color, foreground='white', font=self.default_font)
        self.style.map('Active.TButton', 
                       background=[('active', self.active_tab_color), ('pressed', self.active_tab_color)])
        
        # Configure Treeview style for tables
        self.style.configure("Treeview", 
                             background=self.bg_color,
                             foreground=self.text_color,
                             rowheight=25,
                             fieldbackground=self.bg_color,
                             font=self.default_font)
        self.style.configure("Treeview.Heading", 
                            font=self.header_font,
                            background=self.primary_color, 
                            foreground="white")
        self.style.map("Treeview", 
                      background=[('selected', self.primary_color)])
        
        # Menu bar
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_modify_btn = ttk.Button(self.menu_frame, text="Add/Modify", command=self.show_add_modify, style='Active.TButton')
        self.add_modify_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.make_test_btn = ttk.Button(self.menu_frame, text="Make Test", command=self.show_make_test, style='TButton')
        self.make_test_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Content frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Initially hide all frames
        self.current_frame = None
        
        # Create empty frames for different sections
        self.add_modify_frame = None
        self.make_test_frame = None
        
        # Categories
        self.categories = ["Algebra", "Calculus", "Geometry", "Trigonometry"]
        
        # Current selected category
        self.current_category = None
        
        # Show Add/Modify by default
        self.show_add_modify()
        
        # Set up right-click context menu for the table
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.bg_color, fg=self.text_color)
        self.context_menu.add_command(label="Modify", command=self.modify_question)
        self.context_menu.add_command(label="Delete", command=self.delete_question)
    
    def show_category_dropdown(self):
        # Category selection dropdown in add/modify frame
        category_label = ttk.Label(self.category_frame, text="Select Category:", style="Header.TLabel")
        category_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.category_frame, textvariable=self.category_var, 
                                             values=self.categories, state="readonly", width=15)
        self.category_dropdown.pack(side=tk.LEFT, padx=10, pady=10)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.on_category_selected)
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def update_tab_buttons(self, active_tab):
        # Update button styles based on which tab is active
        if active_tab == "add_modify":
            self.add_modify_btn.configure(style='Active.TButton')
            self.make_test_btn.configure(style='TButton')
        else:
            self.add_modify_btn.configure(style='TButton')
            self.make_test_btn.configure(style='Active.TButton')
    
    def show_add_modify(self):
        # Update tab buttons
        self.update_tab_buttons("add_modify")
        
        # Hide any current frame
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Create Add/Modify frame if it doesn't exist
        if not self.add_modify_frame:
            self.add_modify_frame = ttk.Frame(self.content_frame)
            
            # Top category selection frame
            self.category_frame = ttk.Frame(self.add_modify_frame)
            self.category_frame.pack(fill=tk.X, pady=(0, 10))
            
            self.show_category_dropdown()
            
            # Main content area - split into left panel and table
            self.main_panel = ttk.Frame(self.add_modify_frame)
            self.main_panel.pack(fill=tk.BOTH, expand=True)
            
            # Left panel (for adding/editing questions)
            self.left_panel = ttk.Frame(self.main_panel, width=400, height=600)
            self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
            self.left_panel.pack_propagate(False)  # Prevent shrinking
            
            # Table panel (center)
            self.table_panel = ttk.Frame(self.main_panel)
            self.table_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Create the initial empty left panel
            self.create_empty_left_panel()
            
            # Create the initial empty table panel
            self.create_empty_table_panel()
        
        # Show the Add/Modify frame
        self.add_modify_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.add_modify_frame
    
    def create_empty_left_panel(self):
        self.clear_frame(self.left_panel)
        
        # Empty state message
        empty_label = ttk.Label(self.left_panel, 
                               text="Select a category to add or modify questions", 
                               style="Header.TLabel", 
                               wraplength=380)
        empty_label.pack(expand=True)
    
    def create_empty_table_panel(self):
        self.clear_frame(self.table_panel)
        
        # Empty state message
        empty_label = ttk.Label(self.table_panel, 
                               text="Select a category to view questions", 
                               style="Header.TLabel")
        empty_label.pack(expand=True)
    
    def create_question_form(self):
        self.clear_frame(self.left_panel)
        
        # Question section
        question_label = ttk.Label(self.left_panel, text="What is the Question?", style="Header.TLabel")
        question_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.question_text = tk.Text(self.left_panel, height=5, width=40, 
                                   bg="white", fg=self.text_color,
                                   relief=tk.SOLID, bd=1)
        self.question_text.pack(fill=tk.X, pady=(0, 15))
        
        # Answers section
        answers_label = ttk.Label(self.left_panel, text="Answers", style="Header.TLabel")
        answers_label.pack(anchor=tk.W, pady=(5, 5))
        
        correct_answer_label = ttk.Label(self.left_panel, text="Correct Answer:")
        correct_answer_label.pack(anchor=tk.W, pady=(5, 2))
        
        self.answer1_text = tk.Text(self.left_panel, height=2, width=40, 
                                  bg="white", fg=self.text_color,
                                  relief=tk.SOLID, bd=1)
        self.answer1_text.pack(fill=tk.X, pady=(0, 10))
        
        # Incorrect answers
        incorrect_answers_label = ttk.Label(self.left_panel, text="Incorrect Answers:")
        incorrect_answers_label.pack(anchor=tk.W, pady=(5, 2))
        
        self.answer2_text = tk.Text(self.left_panel, height=2, width=40, 
                                  bg="white", fg=self.text_color,
                                  relief=tk.SOLID, bd=1)
        self.answer2_text.pack(fill=tk.X, pady=(0, 5))
        
        self.answer3_text = tk.Text(self.left_panel, height=2, width=40, 
                                  bg="white", fg=self.text_color,
                                  relief=tk.SOLID, bd=1)
        self.answer3_text.pack(fill=tk.X, pady=(0, 5))
        
        self.answer4_text = tk.Text(self.left_panel, height=2, width=40, 
                                  bg="white", fg=self.text_color,
                                  relief=tk.SOLID, bd=1)
        self.answer4_text.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.left_panel)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.clear_btn = ttk.Button(buttons_frame, text="Clear", style="Accent.TButton", 
                                   command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.add_btn = ttk.Button(buttons_frame, text="Add Question", 
                                 command=self.add_question)
        self.add_btn.pack(side=tk.LEFT)
        
        # Keep track of whether we're editing an existing question
        self.editing_id = None
    
    def create_questions_table(self):
        self.clear_frame(self.table_panel)
        
        # Table title
        title_label = ttk.Label(self.table_panel, 
                              text=f"{self.current_category} Questions", 
                              style="Title.TLabel")
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create treeview with scrollbar
        table_frame = ttk.Frame(self.table_panel)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview/Table
        columns = ("id", "question", "correct_answer")
        self.questions_table = ttk.Treeview(table_frame, columns=columns, show="headings",
                                          yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.questions_table.heading("id", text="ID")
        self.questions_table.heading("question", text="Question")
        self.questions_table.heading("correct_answer", text="Correct Answer")
        
        self.questions_table.column("id", width=50, stretch=False)
        self.questions_table.column("question", width=400)
        self.questions_table.column("correct_answer", width=200)
        
        self.questions_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.questions_table.yview)
        
        # Bind right-click context menu
        self.questions_table.bind("<Button-3>", self.show_context_menu)
        
        # Load sample data (in a real application, this would come from a database)
        self.load_sample_data()
    
    def on_category_selected(self, event):
        self.current_category = self.category_var.get()
        
        # Update both left panel and table panel with the selected category
        self.create_question_form()
        self.create_questions_table()
    
    def clear_form(self):
        # Clear all text fields
        self.question_text.delete("1.0", tk.END)
        self.answer1_text.delete("1.0", tk.END)
        self.answer2_text.delete("1.0", tk.END)
        self.answer3_text.delete("1.0", tk.END)
        self.answer4_text.delete("1.0", tk.END)
        
        # Reset editing state
        self.editing_id = None
        
        # Update button text if it was in editing mode
        self.add_btn.config(text="Add Question")
    
    def add_question(self):
        # Get values from the form
        question = self.question_text.get("1.0", "end-1c").strip()
        correct_answer = self.answer1_text.get("1.0", "end-1c").strip()
        incorrect1 = self.answer2_text.get("1.0", "end-1c").strip()
        incorrect2 = self.answer3_text.get("1.0", "end-1c").strip()
        incorrect3 = self.answer4_text.get("1.0", "end-1c").strip()
        
        # Basic validation
        if not question or not correct_answer or not incorrect1 or not incorrect2 or not incorrect3:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if self.editing_id is not None:
            # Update existing question
            for item in self.questions_table.get_children():
                if self.questions_table.item(item, "values")[0] == self.editing_id:
                    self.questions_table.item(item, values=(self.editing_id, question, correct_answer))
                    break
            messagebox.showinfo("Success", "Question updated successfully")
        else:
            # Add new question
            # Generate a simple ID (in a real app, this would be handled by the database)
            new_id = len(self.questions_table.get_children()) + 1
            self.questions_table.insert("", "end", values=(new_id, question, correct_answer))
            messagebox.showinfo("Success", "Question added successfully")
        
        # Clear the form
        self.clear_form()
    
    def show_context_menu(self, event):
        # Select the item the user right-clicked on
        item = self.questions_table.identify_row(event.y)
        if item:
            self.questions_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def modify_question(self):
        # Get the selected item
        selected_items = self.questions_table.selection()
        if not selected_items:
            return
        
        # Get the data from the selected item
        item = selected_items[0]
        values = self.questions_table.item(item, "values")
        
        # Set editing mode
        self.editing_id = values[0]
        
        # Fill the form with the selected question data
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert("1.0", values[1])
        
        self.answer1_text.delete("1.0", tk.END)
        self.answer1_text.insert("1.0", values[2])
        
        # For the incorrect answers, we'd normally fetch these from the database
        # For this example, we'll just fill in placeholders
        self.answer2_text.delete("1.0", tk.END)
        self.answer2_text.insert("1.0", "Incorrect answer 1")
        
        self.answer3_text.delete("1.0", tk.END)
        self.answer3_text.insert("1.0", "Incorrect answer 2")
        
        self.answer4_text.delete("1.0", tk.END)
        self.answer4_text.insert("1.0", "Incorrect answer 3")
        
        # Update button text
        self.add_btn.config(text="Update Question")
    
    def delete_question(self):
        # Get the selected item
        selected_items = self.questions_table.selection()
        if not selected_items:
            return
        
        # Ask for confirmation
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this question?"):
            self.questions_table.delete(selected_items)
            messagebox.showinfo("Success", "Question deleted successfully")
    
    def load_sample_data(self):
        # Load sample data (in a real application, this would come from a database)
        sample_data = []
        
        if self.current_category == "Algebra":
            sample_data = [
                (1, "Solve for x: 2x + 3 = 9", "x = 3"),
                (2, "Factor: x² - 9", "(x+3)(x-3)"),
                (3, "Solve the system: x + y = 5, 2x - y = 1", "x = 2, y = 3")
            ]
        elif self.current_category == "Calculus":
            sample_data = [
                (1, "Find the derivative of f(x) = x³", "f'(x) = 3x²"),
                (2, "Evaluate: ∫(2x + 3)dx", "x² + 3x + C")
            ]
        elif self.current_category == "Geometry":
            sample_data = [
                (1, "Area of a circle with radius 5", "25π"),
                (2, "Find the perimeter of a rectangle with length 8 and width 6", "28")
            ]
        elif self.current_category == "Trigonometry":
            sample_data = [
                (1, "sin(π/2) = ?", "1"),
                (2, "cos(0) = ?", "1")
            ]
        
        # Clear existing data
        for item in self.questions_table.get_children():
            self.questions_table.delete(item)
        
        # Insert sample data
        for item in sample_data:
            self.questions_table.insert("", "end", values=item)

    def show_make_test(self):
        # Update tab buttons
        self.update_tab_buttons("make_test")
        
        # Hide any current frame
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Create Make Test frame if it doesn't exist
        if not self.make_test_frame:
            self.make_test_frame = ttk.Frame(self.content_frame)
            
            # Split into left and right panels
            left_panel = ttk.Frame(self.make_test_frame, width=400)
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
            
            right_panel = ttk.Frame(self.make_test_frame)
            right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Left Panel - Test Selection
            test_frame = ttk.Frame(left_panel)
            test_frame.pack(fill=tk.X, pady=(0, 20))
            
            test_label = ttk.Label(test_frame, text="Existing Tests", style="Header.TLabel")
            test_label.pack(anchor=tk.W, pady=(0, 10))
            
            # Tests table
            test_table_frame = ttk.Frame(test_frame)
            test_table_frame.pack(fill=tk.X)
            
            # Scrollbar for tests table
            test_scrollbar = ttk.Scrollbar(test_table_frame)
            test_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Tests table
            columns = ("name",)
            self.tests_table = ttk.Treeview(test_table_frame, columns=columns, show="headings", 
                                           height=5, yscrollcommand=test_scrollbar.set)
            self.tests_table.heading("name", text="Test Name")
            self.tests_table.column("name", width=350)
            self.tests_table.pack(fill=tk.X)
            test_scrollbar.config(command=self.tests_table.yview)
            
            # Add sample tests
            self.tests_table.insert("", "end", values=("Test1",))
            self.tests_table.insert("", "end", values=("Test2",))
            
            # Buttons frame
            buttons_frame = ttk.Frame(left_panel)
            buttons_frame.pack(fill=tk.X, pady=10)
            
            self.add_test_btn = ttk.Button(buttons_frame, text="Add", command=self.start_add_test)
            self.add_test_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            self.modify_test_btn = ttk.Button(buttons_frame, text="Modify", command=self.modify_test)
            self.modify_test_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            self.delete_test_btn = ttk.Button(buttons_frame, text="Delete", command=self.delete_test)
            self.delete_test_btn.pack(side=tk.LEFT)
            
            # Test Configuration Frame (initially hidden)
            self.test_config_frame = ttk.Frame(left_panel)
            
            # Number of questions
            num_q_frame = ttk.Frame(self.test_config_frame)
            num_q_frame.pack(fill=tk.X, pady=10)
            
            num_q_label = ttk.Label(num_q_frame, text="Number of questions:")
            num_q_label.pack(side=tk.LEFT, padx=(0, 10))
            
            self.num_questions_var = tk.StringVar()
            self.num_questions_entry = ttk.Entry(num_q_frame, width=10, textvariable=self.num_questions_var)
            self.num_questions_entry.pack(side=tk.LEFT)
            
            # Apply button
            self.apply_num_btn = ttk.Button(num_q_frame, text="Apply", command=self.apply_question_count)
            self.apply_num_btn.pack(side=tk.LEFT, padx=10)
            
            # Section allocation frame
            self.section_frame = ttk.Frame(self.test_config_frame)
            
            section_title = ttk.Label(self.section_frame, text="Question Distribution", style="Header.TLabel")
            section_title.pack(anchor=tk.W, pady=(10, 5))
            
            # Will be filled dynamically when user enters question count
            self.section_entries = {}
            
            # Right Panel - Test Preview
            test_preview_frame = ttk.Frame(right_panel)
            test_preview_frame.pack(fill=tk.BOTH, expand=True)
            
            # Test name entry
            name_frame = ttk.Frame(test_preview_frame)
            name_frame.pack(fill=tk.X, pady=(0, 20))
            
            self.test_name_var = tk.StringVar(value="New Test")
            test_name_entry = ttk.Entry(name_frame, textvariable=self.test_name_var, font=self.header_font)
            test_name_entry.pack(side=tk.LEFT)
            
            # Questions table
            table_frame = ttk.Frame(test_preview_frame)
            table_frame.pack(fill=tk.BOTH, expand=True)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Questions table
            columns = ("id", "question", "section")
            self.test_questions_table = ttk.Treeview(table_frame, columns=columns, show="headings",
                                                   yscrollcommand=scrollbar.set)
            
            self.test_questions_table.heading("id", text="#")
            self.test_questions_table.heading("question", text="Question")
            self.test_questions_table.heading("section", text="Section")
            
            self.test_questions_table.column("id", width=50, stretch=False)
            self.test_questions_table.column("question", width=400)
            self.test_questions_table.column("section", width=100)
            
            self.test_questions_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.test_questions_table.yview)
            
            # Bind right-click menu
            self.test_questions_table.bind("<Button-3>", self.show_test_question_menu)
            
            # Bottom buttons
            bottom_frame = ttk.Frame(right_panel)
            bottom_frame.pack(fill=tk.X, pady=20)
            
            clear_btn = ttk.Button(bottom_frame, text="Clear", style="Accent.TButton", 
                                  command=self.clear_test)
            clear_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            download_btn = ttk.Button(bottom_frame, text="Download Script", 
                                     command=self.download_script)
            download_btn.pack(side=tk.LEFT)
            
            # Test question context menu
            self.test_question_menu = tk.Menu(self.root, tearoff=0, bg=self.bg_color, fg=self.text_color)
            self.test_question_menu.add_command(label="Change with random question of same section", 
                                              command=self.change_with_same_section)
            self.test_question_menu.add_command(label="Change with random of different section", 
                                              command=self.show_section_selection)
            self.test_question_menu.add_command(label="Change manually", 
                                              command=self.change_manually)
            self.test_question_menu.add_separator()
            self.test_question_menu.add_command(label="Delete", 
                                              command=self.delete_test_question)
            
            # Section selection submenu (for changing section)
            self.section_menu = tk.Menu(self.root, tearoff=0, bg=self.bg_color, fg=self.text_color)
            for section in self.categories:
                self.section_menu.add_command(label=section, 
                                            command=lambda s=section: self.change_with_different_section(s))
        
        # Show the Make Test frame
        self.make_test_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.make_test_frame

    def start_add_test(self):
        # Show test configuration frame
        self.test_config_frame.pack(fill=tk.X, pady=10)
        self.section_frame.pack(fill=tk.X, pady=10)
        
        # Clear any existing data
        self.clear_test()
        
        # Set focus to the number of questions field
        self.num_questions_entry.focus()

    def apply_question_count(self):
        try:
            num_questions = int(self.num_questions_var.get())
            if num_questions <= 0:
                raise ValueError("Number must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of questions")
            return
        
        # Clear section frame
        for widget in self.section_frame.winfo_children():
            if widget != self.section_frame.winfo_children()[0]:  # Keep the title
                widget.destroy()
        
        # Create section allocation inputs
        self.section_entries = {}
        self.remaining_var = tk.StringVar(value=f"Remaining: {num_questions}")
        
        # Remaining label
        remaining_label = ttk.Label(self.section_frame, textvariable=self.remaining_var)
        remaining_label.pack(anchor=tk.W, pady=(5, 10))
        
        for section in self.categories:
            section_frame = ttk.Frame(self.section_frame)
            section_frame.pack(fill=tk.X, pady=2)
            
            section_label = ttk.Label(section_frame, text=section, width=15)
            section_label.pack(side=tk.LEFT)
            
            section_var = tk.StringVar(value="0")
            section_entry = ttk.Entry(section_frame, textvariable=section_var, width=10)
            section_entry.pack(side=tk.LEFT, padx=5)
            
            # Track changes to update remaining
            section_var.trace_add("write", lambda name, index, mode, sv=section_var, s=section: 
                                 self.update_remaining(sv, s))
            
            self.section_entries[section] = section_var
        
        # Generate button
        generate_btn = ttk.Button(self.section_frame, text="Generate Test", 
                                command=self.generate_test)
        generate_btn.pack(anchor=tk.E, pady=10)

    def update_remaining(self, var, section):
        try:
            total_questions = int(self.num_questions_var.get())
            allocated = 0
            for s, sv in self.section_entries.items():
                try:
                    allocated += int(sv.get())
                except ValueError:
                    pass
            
            remaining = total_questions - allocated
            self.remaining_var.set(f"Remaining: {remaining}")
        except ValueError:
            pass

    def generate_test(self):
        # Validate totals
        try:
            total_questions = int(self.num_questions_var.get())
            allocated = 0
            for section, var in self.section_entries.items():
                try:
                    allocated += int(var.get())
                except ValueError:
                    messagebox.showerror("Error", f"Invalid number for {section}")
                    return
            
            if allocated != total_questions:
                messagebox.showerror("Error", 
                                  f"Total questions must equal {total_questions}. Currently allocated: {allocated}")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return
        
        # Clear existing questions
        for item in self.test_questions_table.get_children():
            self.test_questions_table.delete(item)
        
        # Generate random questions for each section
        question_id = 1
        
        for section, var in self.section_entries.items():
            section_count = int(var.get())
            for i in range(section_count):
                # In a real app, these would be pulled from the database
                question_text = f"Random {section} Question {i+1}"
                self.test_questions_table.insert("", "end", 
                                               values=(question_id, question_text, section))
                question_id += 1
        
        # Add the test to the tests table if it's new
        if self.test_name_var.get() not in [self.tests_table.item(item)["values"][0] 
                                         for item in self.tests_table.get_children()]:
            self.tests_table.insert("", "end", values=(self.test_name_var.get(),))

    def modify_test(self):
        selected = self.tests_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a test to modify")
            return
        
        # Get the test name
        test_name = self.tests_table.item(selected[0], "values")[0]
        self.test_name_var.set(test_name)
        
        # In a real app, we would load the test's questions and configuration
        # For this demo, let's just show some sample data
        
        # Clear existing questions
        for item in self.test_questions_table.get_children():
            self.test_questions_table.delete(item)
        
        # Sample questions for the selected test
        if test_name == "Test1":
            question_data = [
                (1, "Solve for x: 2x + 3 = 9", "Algebra"),
                (2, "Find the derivative of f(x) = x³", "Calculus"),
                (3, "Find the perimeter of a rectangle with length 8 and width 6", "Geometry")
            ]
        else:  # Test2
            question_data = [
                (1, "Factor: x² - 9", "Algebra"),
                (2, "Evaluate: ∫(2x + 3)dx", "Calculus")
            ]
        
        # Load the questions
        for item in question_data:
            self.test_questions_table.insert("", "end", values=item)
        
        # Show configuration panel
        self.test_config_frame.pack(fill=tk.X, pady=10)
        self.section_frame.pack(fill=tk.X, pady=10)
        
        # Set question count
        self.num_questions_var.set(str(len(question_data)))
        
        # Apply to generate the section allocation fields
        self.apply_question_count()
        
        # Set the section allocations based on the questions
        section_counts = {}
        for _, _, section in question_data:
            section_counts[section] = section_counts.get(section, 0) + 1
        
        for section, count in section_counts.items():
            if section in self.section_entries:
                self.section_entries[section].set(str(count))

    def delete_test(self):
        selected = self.tests_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a test to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this test?"):
            self.tests_table.delete(selected)
            self.clear_test()

    def show_test_question_menu(self, event):
        # Select the item the user right-clicked on
        item = self.test_questions_table.identify_row(event.y)
        if item:
            self.test_questions_table.selection_set(item)
            self.selected_question_id = item
            self.test_question_menu.post(event.x_root, event.y_root)

    def change_with_same_section(self):
        if not hasattr(self, 'selected_question_id'):
            return
        
        item = self.selected_question_id
        values = self.test_questions_table.item(item, "values")
        if not values:
            return
        
        id_num, _, section = values
        
        # Generate a new random question from the same section
        new_question = f"New Random {section} Question"
        self.test_questions_table.item(item, values=(id_num, new_question, section))

    def show_section_selection(self):
        if not hasattr(self, 'selected_question_id'):
            return
        
        # Show the section selection menu
        self.section_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def change_with_different_section(self, new_section):
        if not hasattr(self, 'selected_question_id'):
            return
        
        item = self.selected_question_id
        values = self.test_questions_table.item(item, "values")
        if not values:
            return
        
        id_num, _, old_section = values
        
        # Update counts in section allocation
        if hasattr(self, 'section_entries') and old_section in self.section_entries and new_section in self.section_entries:
            try:
                old_count = int(self.section_entries[old_section].get())
                new_count = int(self.section_entries[new_section].get())
                
                if old_count > 0:
                    self.section_entries[old_section].set(str(old_count - 1))
                    self.section_entries[new_section].set(str(new_count + 1))
            except ValueError:
                pass
        
        # Generate a new random question from the different section
        new_question = f"New Random {new_section} Question"
        self.test_questions_table.item(item, values=(id_num, new_question, new_section))

    def change_manually(self):
        if not hasattr(self, 'selected_question_id'):
            return
        
        messagebox.showinfo("Info", "This would open a dialog to select a specific question from the database")

    def delete_test_question(self):
        if not hasattr(self, 'selected_question_id'):
            return
        
        item = self.selected_question_id
        values = self.test_questions_table.item(item, "values")
        if not values:
            return
        
        _, _, section = values
        
        # Update section count
        if hasattr(self, 'section_entries') and section in self.section_entries:
            try:
                count = int(self.section_entries[section].get())
                if count > 0:
                    self.section_entries[section].set(str(count - 1))
                    
                    # Update total questions
                    total = int(self.num_questions_var.get())
                    self.num_questions_var.set(str(total - 1))
                    
                    # Update remaining count
                    self.update_remaining(None, None)
            except ValueError:
                pass
        
        # Delete the question
        self.test_questions_table.delete(item)
        
        # Renumber remaining questions
        for i, item in enumerate(self.test_questions_table.get_children(), 1):
            current_values = self.test_questions_table.item(item, "values")
            if current_values:
                self.test_questions_table.item(item, values=(i, current_values[1], current_values[2]))

    def clear_test(self):
        # Clear test name
        self.test_name_var.set("New Test")
        
        # Clear questions
        for item in self.test_questions_table.get_children():
            self.test_questions_table.delete(item)
        
        # Clear configuration
        self.num_questions_var.set("")
        if hasattr(self, 'section_entries'):
            for section, var in self.section_entries.items():
                var.set("0")

    def download_script(self):
        messagebox.showinfo("Info", "This would generate and download a script for the test")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathPlacementGUI(root)
    root.mainloop()