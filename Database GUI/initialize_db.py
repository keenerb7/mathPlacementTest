import sqlite3


def initialize_database():
    conn = sqlite3.connect("math_placement_test.db")
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


# if __name__ == "__main__":
#     initialize_database()
