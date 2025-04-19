from tkinter import filedialog
import json
import os
import sqlite3
CONFIG_FILE = "config.json"


def initialize_database(file=None):

    if file is None:
        conn = sqlite3.connect("default.db")
    else:
        conn = sqlite3.connect(file)
    c = conn.cursor()

    # Create tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS Question_Categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            question_id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            question_difficulty INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES Question_Categories (category_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Question_Choices (
            choice_id TEXT PRIMARY KEY,
            question_id INTEGER NOT NULL,
            choice_text TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES Questions (question_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Test (
            test_id INTEGER PRIMARY KEY,
            test_type INTEGER NOT NULL,
            test_title TEXT NOT NULL,
            test_time REAL NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Test_Questions (
            test_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            PRIMARY KEY (test_id, question_id),
            FOREIGN KEY (test_id) REFERENCES Test (test_id),
            FOREIGN KEY (question_id) REFERENCES Questions (question_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Types_Of_Test (
            test_type INTEGER PRIMARY KEY,
            test_name TEXT NOT NULL
        )
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()


def connect_to_database(database_file):
    return sqlite3.connect(database_file)


def select_database(save=False):
    if save:
        filepath = filedialog.asksaveasfilename(
            title="Create or Overwrite SQLite Database",
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db"), ("All Files", "*.*")]
        )
    else:
        filepath = filedialog.askopenfilename(
            title="Select SQLite Database File",
            filetypes=[("SQLite DB", "*.db"), ("All Files", "*.*")]
        )

    if filepath:
        save_last_db_path(filepath)
        connect_to_database(filepath)

    return filepath


def save_last_db_path(path):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"last_db_path": path}, f)


def load_last_db_path():
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) != 0:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_db_path")
    return None


def startup_database():
    last_db = load_last_db_path()
    if last_db and os.path.exists(last_db):
        connect_to_database(last_db)
        return last_db
    else:
        initialize_database()
        filename = "default.db"
        filepath = os.path.abspath(filename)
        save_last_db_path(filepath)
        return filepath


def get_current_db_info():
    if not os.path.exists(CONFIG_FILE):
        return "No database file has been selected yet.", "temp"

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        db_path = data.get("last_db_path")

    if db_path and os.path.exists(db_path):
        file_name = os.path.basename(db_path)
        return db_path, file_name
    else:
        return "Saved database path is missing or invalid.", "temp"
