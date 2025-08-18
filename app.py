from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///routine.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    tasks = db.execute("SELECT * FROM tasks")

    if request.method == "POST":
        return render_template("index.html", tasks=tasks)

    else:
        return render_template("index.html", tasks=tasks)


@app.route("/tasks")
def tasks():
    tasks = db.execute("SELECT * FROM tasks")
    return render_template("tasks.html", tasks=tasks)


@app.route("/study", methods=["POST"])
def study():
    return render_template("study.html")


@app.route("/statistics")
def statistics():
    studies = db.execute('SELECT * FROM studies')
    return render_template("statistics.html", studies=studies)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        name = request.form.get("name")
        db.execute("DELETE FROM tasks WHERE name=?", name)
        flash(name + " deleted!")
        return redirect("/tasks")
    else:
        name = request.args.get("name")
        return render_template("delete.html", name=name)
    

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        id = request.form.get("id")
        new_name = request.form.get("name")
        new_work_time = request.form.get("work-time")
        new_rest_time = request.form.get("rest-time")
        new_repetition = request.form.get("repetition")
        db.execute("UPDATE tasks SET name=?, work_time=?, rest_time=?, repetition=? WHERE id=?", new_name, new_work_time, new_rest_time, new_repetition, id)

        flash(new_name + " edited!")
        return redirect("/tasks")
    else:
        task = {
            "id": request.args.get("id"),
            "name": request.args.get("name"),
            "work": request.args.get("work-time"),
            "rest": request.args.get("rest-time"),
            "repetition": request.args.get("repetition")
        }
        return render_template("edit.html", task=task)
    

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        work_time = request.form.get("work-time")
        rest_time = request.form.get("rest-time")
        repetition = request.form.get("repetition")
        db.execute("INSERT INTO tasks (name, work_time, rest_time, repetition) values (?, ?, ?, ?)", name, work_time, rest_time, repetition)
        flash(name + " created!");
        return redirect("/tasks")
    else:
        return render_template("add.html")