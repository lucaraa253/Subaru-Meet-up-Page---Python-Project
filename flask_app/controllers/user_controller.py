from flask import render_template, request, redirect, session

from flask_app.models.user_model import User

# from flask_app.models.recipe_model import Recipe
# from flask_app.models import recipe_model
# from flask_app.controllers import recipe_controller
from flask_app import app, bcrypt
from flask_app.models.meet_model import Meet

@app.route("/")
def index():
    return render_template("index.html")



# updated this for redirect to dashboard instead of template

@app.route("/register", methods = ["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    user_data = {
        **request.form,
        "password" : bcrypt.generate_password_hash(request.form["password"])
    }
    session["id"] = User.create(user_data)
    return redirect("/dashboard")

@app.route("/login", methods = ["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    user = User.retrieve_one(email = request.form["login_email"])
    session ["id"] = user.id
    return redirect("/dashboard")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")