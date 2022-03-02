from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect, flash, session


from flask_app.models import user

db_name = "python_exam_3"

class Show:
    def __init__(self, data):
        self.id = data["id"]

        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.description = data["description"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user_id = data["user_id"]

    @classmethod
    def get_all_shows(cls):
        m = "get_all_shows"
        Show.p(m)       
        query = "SELECT * FROM shows;"
        results = connectToMySQL(db_name).query_db(query)
        all_shows = []
        for show in results:
            all_shows.append(cls(show))
        return all_shows
    
    @classmethod
    def get_all_shows_join_likes(cls, data):
        m = "get_all_shows_join_likes"
        Show.p(m)       
        # query = "SELECT * FROM likes LEFT JOIN shows ON likes.show_id = shows.id WHERE likes.user_id NOT Null;"
        query = "SELECT * FROM shows LEFT JOIN likes ON likes.show_id = shows.id LEFT JOIN users ON users.id = %(user_id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_shows_and_user_like = []
        for row in results:
            Show.p(row)
            one_show = cls(row)
            # if row.user_id != NULL:
            #     user_data = {
            #         "like": False
            #     }
            # else:
            #     user_data = {
            #         "like": True
            #     }
            # user_data = {
            #     "id": row["likes.user_id"],
            #     "first_name": row["first_name"],
            #     "last_name": row["last_name"],
            #     "password": row["password"],
            #     "email": row["email"],
            #     "created_at": row["users.created_at"],
            #     "updated_at": row["users.updated_at"]
            # }

            if row["likes.user_id"] == session["user_id"]:
                one_show.like = 1
            else:
                one_show.like = 0
            all_shows_and_user_like.append(one_show)
        return all_shows_and_user_like

    @classmethod
    def get_one_show(cls, data):
        m = "get_one_show"
        Show.p(m)  
        query = "SELECT * FROM shows WHERE %(id)s = shows.id;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_shows = []
        for show in results:
            all_shows.append(cls(show))
        return all_shows[0]

    @classmethod
    def get_one_show_joined(cls, data):
        m = "get_one_show_joined"
        Show.p(m)  
        query = "SELECT * FROM shows LEFT JOIN users ON users.id = shows.user_id WHERE %(id)s = shows.id;"
        results = connectToMySQL(db_name).query_db(query, data)
        all_shows = []
        for row in results:
            one_show = Show(row)
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
            all_shows. append(one_show)
        return all_shows[0]

    @classmethod
    def save_show(cls, data):
        m = "save_show"
        Show.p(m)  
        query = "INSERT INTO shows (title, network, release_date, description, user_id, created_at, updated_at) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s, NOW(), NOW());"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def update_show(cls, data):
        m = "update_show"
        Show.p(m)  
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def delete_show(cls, data):
        m = "delete_show"
        Show.p(m)  
        query = "DELETE FROM shows WHERE id = %(id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def like_show(cls, data):
        m = "like_show"
        Show.p(m)  
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s);"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def unlike_show(cls, data):
        m = "like_show"
        Show.p(m)  
        query = "DELETE FROM likes WHERE show_id = %(show_id)s and user_id = %(user_id)s;"
        new_id = connectToMySQL(db_name).query_db(query, data)
        return new_id

    @classmethod
    def num_likes(cls, data):
        m = "num_likes"
        query = "SELECT * FROM likes WHERE likes.show_id = %(id)s;"
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
            flash("Title is at least 3 characters.", "show")
            is_valid = False
        if len(show_info["network"]) < 3:
            flash("Network is at least 3 characters.", "show")
            is_valid = False
        if len(show_info["description"]) < 3:
            flash("Description is at least 3 characters.", "show")
            is_valid = False

        return is_valid
