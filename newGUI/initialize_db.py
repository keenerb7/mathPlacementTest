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

    # Insert data into Question_Categories
    c.executemany("""
        INSERT INTO Question_Categories (category_id, category_name)
        VALUES (?, ?)
    """, [
        (1, 'Reals Numbers'),
        (2, 'Solving Linear Equations'),
        (3, 'Exponents and Polynomials'),
        (4, 'Factoring'),
        (5, 'Rational Expressions and Equations'),
        (6, 'Inequalities'),
        (7, 'Quadractic Functions'),
        (8, 'Exponential and Logarithmic Functions')
    ])

    # Insert data into Questions
    c.executemany("""
        INSERT INTO Questions (question_id, question, category_id, question_difficulty)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 'Dr. Fun bought doughnuts for his math classes for their final exam reviews. Hi first class ate 32 doughnuts, his second ate 29, his third ate 36, and his fourth class ate 31 doughnuts. If he purchased 13 dozen doughnuts, how mnay did he have left over?', 1, 1),
        (2, 'On Angie\'s first five exams her grades were 75, 79, 86, 88, and 64. Find the (a.) mean and (b.) median of her grades.', 1, 3),
        (3, 'Evaluate $-5 + 3 \\cdot 4$. ', 1, 1),
        (4, 'Use the distributive property to simplify $-3(4-2x)$.', 2, 2),
        (5, 'Simplify $5x-8x+4$.', 2, 1),
        (6, 'Laura lent her sister $\\$2000$ for a period of 1 year. At the end of 1 year, her sister repaid the original amount plus $\\$80$ interest. What simple interest rate did her sister repay?', 2, 2),
        (7, 'Simplify the expression $5x^2 \\cdot 3x^2$.', 3, 4),
        (8, 'Calculate the following expression and express your answer in scientific notation: $(285000)(50000)$.', 3, 3),
        (9, 'Simplify $(6x-4)+(2x^2 - 5x - 3)$.', 3, 3),
        (10, 'Determine the greatest common factor of $9y^5$, $15y^3$, and $27y^4$.', 4, 4),
        (11, 'Solve $x^6 - 6x = 0$.', 4, 4),
        (12, 'The product of two positive integers is 36. Determine the two integers if the integer is 1 more than twice the smaller.', 4, 6),
        (13, 'Simplify $\\frac{-8+x}{x-8}$.', 5, 3),
        (14, 'Solve $2 + \\frac{8}{x} = 6$.', 5, 5),
        (15, 'The sum of a positive number and its reciprocal is 2. Determine the number.', 5, 5),
        (16, 'Solve the inequality $3z + 9 \\le 15$.', 6, 4),
        (17, 'Solve the the following inequaltiy and write the solution in interval notation: $1 < x - 4 < 7$.', 6, 5),
        (18, 'Micheal, a telephone operator, informs a customer in a phone booth that the charge for calling Omaha is $\\$4.50$ for the first 3 minutes and 95 cents for additional minute or any part therefor. How long can the customer talk if he has $\\$8.65$?', 6, 6),
        (19, 'Solve $x^2 + 2x -15 = 0$.', 7, 3),
        (20, 'Solve the formula $K = \\frac{1}{2}mv^2$ for $v$.', 7, 6),
        (21, 'Tom drove his 4-wheel-drive Jeep from Findlay, Ohio to Blackwater State Park, a distance of 520 miles. Had he averaged 15 miles per hour faster, the trip would have taken 2.4 hours less. Find the average speed that Tom drove.', 7, 7),
        (22, 'Write $\\log_5(125) = 3$ in exponential form.', 8, 5),
        (23, 'Find $N$, rounded to 4 decimal places, if $\\ln{N} = 2.79$', 8, 5),
        (24, 'Solve $10^{\\log_{10}(9)}$.', 8, 5)
    ])

    # Insert data into Question_Choices
    c.executemany("""
        INSERT INTO Question_Choices (choice_id, question_id, choice_text, is_correct)
        VALUES (?, ?, ?, ?)
    """, [
        ('10a', 10, '$3y^3$', 1),
        ('10b', 10, '$3y^4$', 0),
        ('10c', 10, '$3y^5$', 0),
        ('10d', 10, '$9y^3$', 0),
        ('10e', 10, '$9y^4$', 0),
        ('11a', 11, '0, 6', 1),
        ('11b', 11, '0', 0),
        ('11c', 11, '6', 0),
        ('11d', 11, '0, -6', 0),
        ('11e', 11, '-6', 0),
        ('12a', 12, '4, 9', 1),
        ('12b', 12, '3, 12', 0),
        ('12c', 12, '2, 18', 0),
        ('12d', 12, '1, 36', 0),
        ('12e', 12, '6, 6', 0),
        ('13a', 13, '1', 1),
        ('13b', 13, '-1', 0),
        ('13c', 13, '$\\frac{-8+x}{x-8}$', 0),
        ('13d', 13, '$\\frac{-8+x}{x}$', 0),
        ('13e', 13, '$-1 + x$', 0),
        ('14a', 14, '2', 1),
        ('14b', 14, '3', 0),
        ('14c', 14, '-2', 0),
        ('14d', 14, '1', 0),
        ('14e', 14, '-1', 0),
        ('15a', 15, '1', 1),
        ('15b', 15, '-1', 0),
        ('15c', 15, '0', 0),
        ('15d', 15, '2', 0),
        ('15e', 15, '-2', 0),
        ('16a', 16, '$z \\le 2$', 1),
        ('16b', 16, '$z < 2$', 0),
        ('16c', 16, '$z \\ge 2$', 0),
        ('16d', 16, '$z > 2$', 0),
        ('16e', 16, '$z \\le -2$', 0),
        ('17a', 17, '(5, 11)', 1),
        ('17b', 17, '[5, 11]', 0),
        ('17c', 17, '[-5, 11]', 0),
        ('17d', 17, '(5, -11)', 0),
        ('17e', 17, '(-5, -11)', 0),
        ('18a', 18, '7 min', 1),
        ('18b', 18, '5 min', 0),
        ('18c', 18, '6 min', 0),
        ('18d', 18, '8 min', 0),
        ('18e', 18, '9 min', 0),
        ('19a', 19, '3, -5', 1),
        ('19b', 19, '-3, -5', 0),
        ('19c', 19, '3, 5', 0),
        ('19d', 19, '-3, 5', 0),
        ('19e', 19, '0', 0),
        ('1a', 1, '28', 1),
        ('1b', 1, '27', 0),
        ('1c', 1, '29', 0),
        ('1d', 1, '31', 0),
        ('1e', 1, '24', 0),
        ('20a', 20, '$v = \\sqrt{\\frac{2K}{m}}$', 1),
        ('20b', 20, '$v = \\frac{2K}{m}$', 0),
        ('20c', 20, '$v = \\sqrt{\\frac{2}{Km}}$', 0),
        ('20d', 20, '$v = \\sqrt{\\frac{K}{m}}$', 0),
        ('20e', 20, '$v = \\sqrt{\\frac{K}{2m}}$', 0),
        ('21a', 21, '50 mph', 1),
        ('21b', 21, '55 mph', 0),
        ('21c', 21, '45 mph', 0),
        ('21d', 21, '40 mph', 0),
        ('21e', 21, '52 mph', 0),
        ('22a', 22, '$5^3 = 125$', 1),
        ('22b', 22, '$3^5 = 125$', 0),
        ('22c', 22, '$5^{125} = 3$', 0),
        ('22d', 22, '$3^{125} = 5$', 0),
        ('22e', 22, '$125^3 = 5$', 0),
        ('23a', 23, '16.2810', 1),
        ('23b', 23, '17.2810', 0),
        ('23c', 23, '16.5463', 0),
        ('23d', 23, '16.9876', 0),
        ('23e', 23, '16.1234', 0),
        ('24a', 24, '9', 1),
        ('24b', 24, '10', 0),
        ('24c', 24, '11', 0),
        ('24d', 24, '$10^{\\log_{10}(9)}$', 0),
        ('24e', 24, '$10^9$', 0),
        ('2a', 2, '(a.) 78.4 (b.) 79', 1),
        ('2b', 2, '(a.) 78.9 (b.) 86', 0),
        ('2c', 2, '(a.) 78.4 (b.) 75', 0),
        ('2d', 2, '(a.) 79.2 (b.) 64', 0),
        ('2e', 2, '(a.) 78.4 (b.) 86', 0),
        ('3a', 3, '7', 1),
        ('3b', 3, '-8', 0),
        ('3c', 3, '19', 0),
        ('3d', 3, '32', 0),
        ('3e', 3, '10', 0),
        ('4a', 4, '$6x-12$', 1),
        ('4b', 4, '$-6x-12$', 0),
        ('4c', 4, '$6x+12$', 0),
        ('4d', 4, '$2x-12$', 0),
        ('4e', 4, '$6x+4$', 0),
        ('5a', 5, '$-3x+4$', 1),
        ('5b', 5, '$3x+4$', 0),
        ('5c', 5, '$-3x-4$', 0),
        ('5d', 5, '$5x-8x+4$', 0),
        ('5e', 5, '$-4x+4$', 0),
        ('6a', 6, '4%', 1),
        ('6b', 6, '5%', 0),
        ('6c', 6, '4.5%', 0),
        ('6d', 6, '5.5%', 0),
        ('6e', 6, '3%', 0),
        ('7a', 7, '$15x^6$', 1),
        ('7b', 7, '$8x^6$', 0),
        ('7c', 7, '$-15x^6$', 0),
        ('7d', 7, '$15x^4$', 0),
        ('7e', 7, '$15x$', 0),
        ('8a', 8, '$1.425 \\cdot 10^{10}$', 1),
        ('8b', 8, '$1.25 \\cdot 10^{10}$', 0),
        ('8c', 8, '$1.5 \\cdot 10^{10}$', 0),
        ('8d', 8, '$1.425 \\cdot 10^{8}$', 0),
        ('8e', 8, '$1.425 \\cdot 10^{12}$', 0),
        ('9a', 9, '$2x^2 + x - 7$', 1),
        ('9b', 9, '$2x^2 - x - 7$', 0),
        ('9c', 9, '$2x^2 + x + 7$', 0),
        ('9d', 9, '$x^2 + x - 7$', 0),
        ('9e', 9, '$2x^2 - x + 7$', 0)
    ])

    # Insert data into Test
    c.executemany("""
        INSERT INTO Test (test_id, test_type, test_title, test_time)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 'Practice_Algebra_Exam_Spring25', 30)
    ])

    # Insert data into Test_Questions
    c.executemany("""
        INSERT INTO Test_Questions (test_id, question_id)
        VALUES (?, ?)
    """, [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11),
        (1, 12),
        (1, 13),
        (1, 14),
        (1, 15),
        (1, 16),
        (1, 17),
        (1, 18),
        (1, 19),
        (1, 20),
        (1, 21),
        (1, 22),
        (1, 23),
        (1, 24)
    ])

    # Insert data into Types_Of_Test
    c.executemany("""
        INSERT INTO Types_Of_Test (test_type, test_name)
        VALUES (?, ?)
    """, [
        (1, 'Algebra')
    ])

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()