from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash
from flask_app.models.user_model import User
import re

class Meet:
    def __init__( self , data ):
        print(data)
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save_meet(cls, data):
        query = "INSERT INTO meets (location, description, date, user_id) VALUES ( %(location)s, %(description)s, %(date)s, %(user_id)s)"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all_meets(cls):
        query = "SELECT * FROM meets;"
        results = connectToMySQL(DB).query_db(query)

        meets = []
        for meet in results:
            meets.append( cls(meet) )
        return meets

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM meets WHERE meets.id = %(id)s;"
        results = connectToMySQL(DB).query_db( query, data)
        if results:
            return cls(results[0])

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM meets WHERE meets.id = %(id)s;"
        return connectToMySQL(DB).query_db( query, data )

# only returns the firts thing in the list, dictionary
        
    @classmethod
    def update(cls,data):
        query = "UPDATE meets SET location = %(location)s, description=%(description)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db( query, data)

    @staticmethod
    def validate_meet(data):
        errors = {}
        if len(data["location"]) < 3:
            errors["location"] = "Location should have at least 3 characters"
        if len(data["description"]) < 3:
            errors["description"] = "Description name should have at least 3 characters"
        for field,msg in errors.items():
            flash(msg,field)

        return len(errors) == 0

    # @staticmethod
    # def validate_new_tree(data):
    #     errors = {}
    #     if len(data["species"]) < 3:
    #         errors["species"] = "Species should have at least 3 characters"
    #     if len(data["location"]) < 3:
    #         errors["location"] = "Location name should have at least 3 characters"
    #     if len(data["reason"]) < 10:
    #         errors["reason"] = "Reason name should have at least 8 characters"
    #     for field,msg in errors.items():
    #         flash(msg,field)

    #     return len(errors) == 0

# query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, user_id=%(user_id)s,under_thirty_minutes=%(under_thirty_minutes)s WHERE id = %(id)s;"
