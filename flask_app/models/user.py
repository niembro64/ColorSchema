from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import schema
from flask import flash
import re


db_name = "color_schema"

class User:
    def __init__(self, data):
        self.id = data["id"]

        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.schema_id = 1



    @classmethod
    def save_user(cls, data):
        m = "save_user"
        User.p(m)        
        query = "INSERT INTO users (first_name, last_name, password, email, created_at, updated_at, schema_id) VALUES (%(first_name)s, %(last_name)s, %(password)s, %(email)s, NOW(), NOW(), 1);"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def get_user(cls, data):
        m = "get_user"
        User.p(m)        
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_users = []
        for row in results:
            one_user = cls(row)
            # all_users.append(one_user)
        return one_user

    @classmethod
    def get_user_by_email(cls, data):
        m = "get_user_by_email"
        User.p(m)        
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_users = []
        for row in results:
            one_user = cls(row)
            # all_users.append(one_user)
        return one_user

    @classmethod
    def get_id_from_email(cls, data):
        m = "get_id_from_email"
        User.p(m)        
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(
            db_name).query_db(query, data)
        all_users = []
        for row in results:
            # pass
            one_user = cls(row)
            all_users.append(one_user)
        # all_users = cls(results)
        user_id = all_users[0].id
        return user_id

    ####################################

    @staticmethod
    def l_email_exists(data):
        m = "l_email_exists"
        User.p(m)        
        exists = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(
            db_name).query_db(query, data)
        #all_users = []
        #for row in results:
        #    all_users.append(row)
        #    # all_users.append(one_user)

        #if all_users[0]["email"] == data["email"]:
        #if "niemeyer.eric@gmail.com" == data["email"]:
        #    exists = True
        
        if len(results) > 0:
            exists = True
        else:
            flash("Account doesn't exist.", "login")

        return exists

    @staticmethod
    def validate_register(reg_info):
        m = "validate_register"
        User.p(m)        
        is_valid = True

        # Is submitted
        # Don't know how to do this

        # Length checks
        if len(reg_info["r_first_name"]) < 3:
            flash("First Name must be at least 3 characters.", "register")
            is_valid = False
        if len(reg_info["r_last_name"]) < 3:
            flash("Last Name must be at least 3 characters.", "register")
            is_valid = False
        if len(reg_info["r_email"]) < 2:
            flash("Email must be at least 3 characters.", "register")
            is_valid = False
        if len(reg_info["r_password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if len(reg_info["r_confirm_password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False

        # Check Email Stuff
        snail = "@"
        dot = "."
        if not snail in reg_info["r_email"]:
            flash("@ must be in Email.", "register")
            is_valid = False
        if not dot in reg_info["r_email"]:
            flash(". must be in Email.", "register")
            is_valid = False

        # Check Matching Passwords
        if not reg_info["r_confirm_password"] == reg_info["r_password"]:
            flash("Passwords must match.", "register")
            is_valid = False

        # Regex Attempt
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(reg_info["r_email"]):
            flash("Email does not meet REGEX requirements.", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(log_info):
        m = "validate_login"
        User.p(m)        
        is_valid = True

        # Length checks
        if len(log_info["l_email"]) < 2:
            flash("Email is at least 2 characters.", "login")
            is_valid = False
        if len(log_info["l_password"]) < 8:
            flash("Password is at least 8 characters.", "login")
            is_valid = False

                # Check Email Stuff
        snail = "@"
        dot = "."
        if not snail in log_info["l_email"]:
            flash("@ must be in Email.", "login")
            is_valid = False
        if not dot in log_info["l_email"]:
            flash(". must be in Email.", "login")
            is_valid = False

        return is_valid



##########################################

    @staticmethod
    def p(l):
        print("------------------------------------------------")
        print(f"------------------------ {l}")
        print("------------------------------------------------")


