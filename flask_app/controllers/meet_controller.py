from flask import render_template, request, redirect, session

from flask_app.models.user_model import User
from flask_app.models.meet_model import Meet
from flask_app.controllers import user_controller
from flask_app import app, bcrypt

@app.route("/dashboard")
def dashboard():
    if "id" not in session:
        return redirect("/")
    user = User.retrieve_one(id = session["id"])
    meets = Meet.get_all_meets()
    return render_template("dashboard.html", user = user, meets = meets)

@app.route("/new_meet")
def new_meet():
    user = User.retrieve_one(id = session["id"])
    return render_template("new_meet.html", user = user)

@app.route("/user_account")
def user_account():
    user = User.retrieve_one(id = session["id"])
    meets = Meet.get_all_meets()
    return render_template("user_account.html", meets=meets, user = user)

@app.route("/edit_meet/<int:id>")
def edit_tree(id):
    user = User.retrieve_one(id = session["id"])
    data = {"id" : id}
    tree = Meet.get_one(data)
    return render_template("edit_meet.html", tree = tree, user = user)

@app.route("/show_meet/<int:id>")
def show_tree(id):
    data = {"id" : id}
    meet = Meet.get_one(data)
    user = User.retrieve_one(id = session["id"])
    return render_template("show_meet.html", meet = meet, user = user)

# Actioons
@app.route("/save_meet/<int:id>", methods = ["POST"])
def save_meet(id):
    if not Meet.validate_meet(request.form):
        return redirect("/new_meet")
    data = {
        **request.form,
        "user_id" : id 
    }
    Meet.save_meet(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    # We pass the data dictionary into the save method from the Friend class.
    Meet.remove({"id" : id})
    # Don't forget to redirect after saving to the database.
    return redirect("/user_account")

@app.route("/update_meet/<int:id>", methods = ["POST"])
def update_meet(id):
    if not Meet.validate_tree(request.form):
        return redirect(f"/edit_tree/{id}")
    data = {
        **request.form,
        "id" : id
    }
    Meet.update(data)

    return redirect("/dashboard")