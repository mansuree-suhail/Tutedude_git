# imported modules needed for this task
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# this func. Loads environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'any_secret_key'  # -->> needed for flash messages

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

@app.route("/todo")
def todo():
    return render_template("todo.html")


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_desc = request.form.get("itemDescription")

    if not item_name or not item_desc:
        flash("All fields are required for To-Do.")
        return redirect(url_for("todo"))
    
    try:
        # Save the To-Do item in a separate collection
        mongo.db.todos.insert_one({
            "itemName": item_name,
            "itemDescription": item_desc
        })
        flash("To-Do item submitted successfully!")
        return redirect(url_for("todo"))
    except Exception as e:
        flash(f"Error saving To-Do item: {str(e)}")
        return redirect(url_for("todo"))

if __name__ == "__main__":
    app.run(debug=True)