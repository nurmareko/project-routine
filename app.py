from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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


@app.route("/edit")
def edit():
    return render_template("edit.html")


@app.route("/study", methods=["POST"])
def study():
    return render_template("study.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")
