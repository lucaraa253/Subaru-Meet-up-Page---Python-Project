from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash
# from flask_app.models.tree_model import Tree
# from flask_app.models import tree_model
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# from flask_app.models import IMPORT OTHER MODEL HERE IF NEEDED

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# ---------------Create----------------
    @classmethod
    def create(cls, data):
        query = '''
                INSERT INTO users 
                (first_name,last_name, email, password) 
                VALUES 
                (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                '''
        return connectToMySQL(DB).query_db(query,data)


# ---------------Retreive----------------

    @classmethod
    def retrieve_one(cls, **data):
        query = "SELECT * FROM users WHERE "
        # wheres = []
        # for key in data:
        #     wheres. append(f"{key} = %({key})s")
        where_str = " AND " . join(f"{key} = %({key})s" for key in data)
        query += where_str + ";"
        results = connectToMySQL(DB).query_db(query,data)
        print(results)
        if results:
            return cls(results[0])

# ---------------Validation---------Static method-------

    @staticmethod
    def validate_register(data):
        errors = {}
        if len(data["first_name"]) < 3:
            errors["first_name"] = "First name should be at least 3 characters"
        if len(data["last_name"]) < 3:
            errors["last_name"] = "Last name should be at least 3 characters"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Email format is invalid"
        elif User.retrieve_one(email=data["email"]):
            errors["email"] = "Email is already in use"
        if len(data["password"]) < 8:
            errors["password"] = "Password name should be at least 8 characters"
        elif data["password"] != data["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match"
        
        for field,msg in errors.items():
            flash(msg,field)

        return len(errors) == 0


    @staticmethod
    def validate_login(data):
        errors = {}
        user = User.retrieve_one(email=data["login_email"])
        if not user:
            errors["login"] = "Invalid credentials"
        elif not bcrypt.check_password_hash(user.password,data["login_password"]):
            errors["login"] = "Invalid credentials"

        for field,msg in errors.items():
            flash(msg,field)

        return len(errors) == 0


    # @classmethod
    # def get_user_with_tree(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN trees ON trees.user_id = users.id WHERE users.id = %(id)s;"
    #     results = connectToMySQL(DB).query_db( query, data)
    #     user = cls( results[0])
    #     user.trees= []
    #     for row_from_db in results:
    #         tree_data = {
    #             "user_id" : row_from_db["user_id"],
    #             "id" : row_from_db["trees.id"],
    #             "species" : row_from_db["species"],
    #             "location" : row_from_db["location"],
    #             "reason" : row_from_db["reason"],
    #             "date_planted" : row_from_db["date_planted"],
    #             "created_at" : row_from_db["ninjas.created_at"],
    #             "updated_at" : row_from_db["ninjas.updated_at"],
    #         }
    #         user.trees.append(tree_model.Tree( tree_data ) )
    #     return user


