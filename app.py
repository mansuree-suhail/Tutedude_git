# imported modules needed for this task
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# this func. Loads environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'any_secret_key'  # -->> needed for flash messages

@app.route("/todo")
def todo():
    return render_template("todo.html")

#  for Set up MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if not name or not email:
            flash("All fields are required.")
            return render_template("index.html")
        try:
            mongo.db.submissions.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return render_template("index.html")
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
