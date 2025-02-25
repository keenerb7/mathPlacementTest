CREATE DATABASE MathTestPlacementDB;
USE MathTestPlacementDB;

# DROP DATABASE MathTestPlacementDB;

CREATE TABLE Question_Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(255) NOT NULL,
    category_id INT,
    question_difficulty INT,
    FOREIGN KEY (category_id) REFERENCES Question_Categories(category_id)
);

CREATE TABLE Question_Choices (
    choice_id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT,
    choice_text VARCHAR(255) NOT NULL,
    is_correct BOOLEAN,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Types_Of_Test (
    test_type INT PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL
);

CREATE TABLE Test (
    test_id INT PRIMARY KEY AUTO_INCREMENT,
    test_type INT,
    test_title VARCHAR(255) NOT NULL,
    test_time FLOAT,
    FOREIGN KEY (test_type) REFERENCES Types_Of_Test(test_type)
);

CREATE TABLE Test_Questions (
    test_id INT,
    question_id INT,
    PRIMARY KEY (test_id, question_id),
    FOREIGN KEY (test_id) REFERENCES Test(test_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE User_Attempts (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    test_id INT,
    score INT,
    date_taken DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (test_id) REFERENCES Test(test_id)
);

CREATE TABLE User_Answers (
    attempt_id INT,
    question_id INT,
    selected_answer BOOLEAN,
    selected_answer_id INT,
    selected_answer_correct BOOLEAN,
    PRIMARY KEY (attempt_id, question_id),
    FOREIGN KEY (attempt_id) REFERENCES User_Attempts(attempt_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

CREATE TABLE User_Test_Assignment (
    user_id INT,
    test_id INT,
    attempt_id INT,
    user_attempted BOOLEAN,
    PRIMARY KEY (user_id, test_id, attempt_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (test_id) REFERENCES Test(test_id),
    FOREIGN KEY (attempt_id) REFERENCES User_Attempts(attempt_id)
);
