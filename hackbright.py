"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])
    return (row[0], row[1], row[2])

# QUERY FOR STUDENTS BY TITLE
def get_projects_by_title(title):
    """Given a title, print project and description from Projects table."""

    QUERY = """
        SELECT title, description
        FROM Projects
        WHERE title = ?
        """

    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project: %s\nDescription: %s" % (
        row[0], row[1])

def get_student_grade(github, project_title):
    """Given a github account and project title, print grade from Grades table."""

    QUERY = """
        SELECT student_github, project_title, grade
        FROM Grades
        WHERE student_github = ? AND project_title = ? 
        """

    db_cursor.execute(QUERY, (github, project_title))
    row = db_cursor.fetchone()
    print "Github Account: %s\nProject Title: %s\nGrade: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO Students (first_name, last_name, github)
        VALUES (?, ?, ?)"""

    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)
    return (first_name, last_name)

def update_grade(github, project_title, grade):
    """Given a github and project title, assign a new grade."""

    QUERY = """
        UPDATE Grades SET grade = ?
        WHERE student_github = ? AND project_title = ?
        """

    db_cursor.execute(QUERY, (grade, github, project_title))
    db_connection.commit()
    print "Successfully updated %s's grade for project, %s to %s." % (
        github, project_title, grade)


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "project_title":
            project_title = args[0]
            get_projects_by_title(project_title)

        elif command == "grade_request":
            github = args[0]
            project_title = args[1]
            get_student_grade(github, project_title)

        elif command == "update_grade":
            github, project_title, grade = args
            update_grade(github, project_title, grade)
        
        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
