from flask_app import app
from flask import render_template, request, redirect, flash, session

from flask_app.models.show import Show


# @app.route("/show_all")
# def ashow_all():
#     m = "show_all"
#     Show.p(m)
#     if not session['user_id'] > 0:
#         return redirect("/")

#     all_shows = Show.get_all_shows()

#     return render_template("show_all.html", all_shows=all_shows)
@app.route("/show_all")
def ashow_all():
    m = "show_all"
    Show.p(m)
    if not session['user_id'] > 0:
        return redirect("/")
    data = {
        "user_id": session['user_id']
    }

    all_shows = Show.get_all_shows_join_likes(data)

    return render_template("show_all.html", all_shows=all_shows)


# @app.route("/show_one/<int:show_id>")
# def ashow_one(show_id):
#     m = "show_one"
#     Show.p(m)
#     if not session['user_id'] > 0:
#         return redirect("/")
#     data = {
#       "id": show_id
#     }
#     one_show = Show.get_one_show(data)
#     return render_template("show_one.html", one_show = one_show)

@app.route("/show_one/<int:show_id>")
def ashow_one_joined(show_id):
    m = "show_one_joined"
    Show.p(m)
    if not session['user_id'] > 0:
        return redirect("/")
    data = {
      "id": show_id
    }
    one_show = Show.get_one_show_joined(data)
    num_likes = Show.num_likes(data)
    return render_template("show_one.html", one_show = one_show, num_likes = num_likes)

@app.route("/edit_one/<int:show_id>")
def aedit_one(show_id):
    m = "edit_one"
    Show.p(m)
    if not session['user_id'] > 0:
        return redirect("/")
    data = {
      "id": show_id
    }
    one_show = Show.get_one_show(data)    
    return render_template("edit_one.html", one_show = one_show)

@app.route("/add_one")
def add_one():
    m = "add_one"
    Show.p(m)
    if not session['user_id'] > 0:
        return redirect("/")
    return render_template("add_one.html")

#######################


@app.route("/fun_add_one", methods=["POST"])
def fun_add_one():
    m = "fun_add_one"
    Show.p(m)
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": session['user_id']
    }

    # VALIDATE SHOW
    valid_show = Show.validate_show(data)
    if not valid_show:
        return redirect("/add_one")


    Show.save_show(data)
    return redirect("/show_all")

@app.route("/fun_edit_one/<int:show_id>", methods=["POST"])
def fun_edit_one(show_id):
    m = "fun_edit_one"
    Show.p(m)
    data = {
        "id": show_id,
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": session['user_id']
    }

    # VALIDATE SHOW
    valid_show = Show.validate_show(data)
    if not valid_show:
        return redirect(f"/edit_one/{show_id}")

    Show.update_show(data)
    return redirect("/show_all")

@app.route("/fun_delete_one/<int:show_id>", methods=["POST"])
def fun_delete_one(show_id):
    m = "fun_delete_one"
    Show.p(m)
    data = {
        "id": show_id
    }
    Show.delete_show(data)
    return redirect("/show_all")

###

@app.route("/fun_like_show/<int:show_id>", methods=["POST"])
def fun_like_show(show_id):
    m = "fun_like"
    Show.p(m)
    data = {
        "show_id": show_id,
        "user_id": session["user_id"]
    }
    Show.like_show(data)
    return redirect("/show_all")

@app.route("/fun_unlike_show/<int:show_id>", methods=["POST"])
def fun_unlike_show(show_id):
    m = "fun_unlike"
    Show.p(m)
    data = {
        "show_id": show_id,
        "user_id": session["user_id"]
    }
    Show.unlike_show(data)
    return redirect("/show_all")









