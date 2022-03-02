from flask_app import app
from flask import render_template, request, redirect, flash, session

from flask_app.models.user import User
from flask_app.models.show import Show


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def root():
    m = "root"
    User.p(m)
    return redirect("/user_login")


@app.route("/index")
def index():
    m = "index"
    User.p(m)
    return redirect("/user_login")


@app.route("/user_login")
def user_login():
    m = "user_login"
    User.p(m)
    return render_template("user_login.html")


########################

@app.route("/login_user", methods=["POST"])
def fun_login():
    m = "fun_login"
    User.p(m)

    data = {
        "email": request.form["l_email"]
    }

    if not User.l_email_exists(data):
        return redirect("/")

    one_user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(one_user.password, request.form['l_password']):
        flash("Bad Password.", "login")
        return redirect("/")

    if not User.validate_login(request.form):
        return redirect("/")

    data = {
        "email": request.form["l_email"]
    }

    user_id = User.get_id_from_email(data)

    data = {
        "id": user_id
    }

    one_user = User.get_user(data)

    session['user_id'] = one_user.id
    session['first_name'] = one_user.first_name
    session['last_name'] = one_user.last_name
    session['password'] = one_user.password
    session['email'] = one_user.email

    return redirect("/show_all")


@app.route("/register_user", methods=["POST"])
def fun_register():
    m = "fun_register"
    User.p(m)

    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['r_password'])

    data = {
        "first_name": request.form["r_first_name"],
        "last_name": request.form["r_last_name"],
        "password": pw_hash,
        "email": request.form["r_email"]
    }

    user_id = User.save_user(data)
    session['user_id'] = user_id

    session['first_name'] = data["first_name"]
    session['last_name'] = data["last_name"]
    session['password'] = data["password"]
    session['email'] = data["email"]

    User.p(session)

    return redirect("/show_all")

@app.route("/log_out", methods=["POST"])
def fun_log_out():
    session['user_id'] = 0
    session['first_name'] = ""
    session['last_name'] = ""
    session['password'] = ""
    session['email'] = ""
    return redirect("/")