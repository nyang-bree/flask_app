from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re




class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at,updated_at) VALUES (%(name)s,%(email)s,%(dob)s,%(password)s, NOW(),NOW())"
        return connectToMySQL('users_schema').query_db(query,data)
    


    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('users_schema').query_db(query, user)
        if len(result) >= 1:
            flash('Email already has an account', 'register')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First_name must be at least 3 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last_name must be at least 3 characters.", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Password doesn't match", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'register')
            is_valid = False
        return is_valid