from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect, flash, session
from flask_app.models import user

db_name = "color_schema"

class Schema:
    def __init__(self, data):
        self.id = data["id"]

        self.title = data["title"]
        self.description = data["description"]
        self.color_main = data["color_main"]
        self.color_secondary = data["color_secondary"]
        self.color_accent = data["color_accent"]
        self.color_text = data["color_text"]
        self.color_background = data["color_background"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user_id = data["user_id"]

    @classmethod
    def get_all_schemas(cls):
        m = "get_all_schemas"
        Schema.p(m)       
        query = "SELECT * FROM schemas;"
        results = connectToMySQL(db_name).query_db(query)
        all_schemas = []
        for schema in results:
            all_schemas.append(cls(schema))
        return all_schemas

    @classmethod
    def get_one_schema(cls, data):
        m = "get_one_schema"
        Schema.p(m)  
        query = "SELECT * FROM schemas WHERE %(id)s = schemas.id;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_schemas = []
        for schema in results:
            all_schemas.append(cls(schema))
        return all_schemas[0]

    @classmethod
    def get_one_show_joined(cls, data):
        m = "get_one_show_joined"
        Schema.p(m)  
        query = "SELECT * FROM schemas LEFT JOIN users ON users.id = schemas.user_id WHERE %(id)s = schemas.id;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_schemas = []
        for row in results:
            one_show = Schema(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            one_show.user = user.User(user_data)
            all_schemas. append(one_show)
        return all_schemas[0]

    @classmethod
    def save_show(cls, data):
        m = "save_show"
        Schema.p(m)  
        query = "INSERT INTO schemas (title, network, release_date, description, user_id, created_at, updated_at) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s, NOW(), NOW());"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def update_show(cls, data):
        m = "update_show"
        Schema.p(m)  
        query = "UPDATE schemas SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def delete_show(cls, data):
        m = "delete_show"
        Schema.p(m)  
        query = "DELETE FROM schemas WHERE id = %(id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def like_show(cls, data):
        m = "like_show"
        Schema.p(m)  
        query = "INSERT INTO likes (user_id, schema_id) VALUES (%(user_id)s, %(schema_id)s);"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def unlike_show(cls, data):
        m = "like_show"
        Schema.p(m)  
        query = "DELETE FROM likes WHERE schema_id = %(schema_id)s and user_id = %(user_id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def num_likes(cls, data):
        m = "num_likes"
        query = "SELECT * FROM likes WHERE likes.schema_id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        count = 0
        for row in results:
            count += 1        
        return count


##########################################

    @staticmethod
    def p(l):
        print("------------------------------------------------")
        print(f"------------------------ {l}")
        print("------------------------------------------------")

    @staticmethod
    def validate_show(show_info):
        is_valid = True

        # Length checks
        if len(show_info["title"]) < 3:
            flash("Title is at least 3 characters.", "schema")
            is_valid = False
        if len(show_info["network"]) < 3:
            flash("Network is at least 3 characters.", "schema")
            is_valid = False
        if len(show_info["description"]) < 3:
            flash("Description is at least 3 characters.", "schema")
            is_valid = False

        return is_valid
