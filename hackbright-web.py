from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add")
def student_add():
    """Adds a student."""

    return render_template("student_add.html")

@app.route("/added-student", methods=['POST'])
def added_student():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    github = request.form["github"]

    print request.form

    first_name, last_name = hackbright.make_new_student(firstname, lastname, github)

    return render_template("added_student.html",
                            firstname=first_name,
                            lastname=last_name,
                            github=github)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github)
    return html

if __name__ == "__main__":
    app.run(debug=True)