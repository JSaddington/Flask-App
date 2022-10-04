from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)


db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password



db.create_all()



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hash(request.form["password"])
        session["user"] = email
        found = users.query.filter_by(email = email, password = password).first()
        if found:
            session.permanent = True
            session["email"] = found.email
            flash("Login successful!")
            return redirect(url_for("home"))

        else:
            flash("You do not exist, register here.")
            return redirect(url_for("register"))
    else:
        if "user" in session:
            flash("You are already logged in")
            return redirect(url_for("home"))
        else:
            return render_template("login.html")


# @app.route("/user", methods=["POST", "GET"])
# def user():
#     email = None
#     if "user" in session:
#         u = session["user"]
#         if request.method == "POST":
#             email = request.form["email"]
#             session["email"] = email
#             found = users.query.filter_by(name = u).first()
#             found.email = email
#             db.session.commit()
#             flash("Email saved")
#         else: 
#             if "email" in session:
#                 email = session["email"]

#         return render_template("user.html", email=email)
#     else:
#         flash("You are not logged in")
#         return redirect(url_for("login"))
        
@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        e = request.form["email"]
        p = hash(request.form["password"])
        if users.query.all() is None:
            usr = users(e, p)
            db.session.add(usr)
            db.session.commit()
            flash("Registered successfully, now please log in.")
            return redirect(url_for("login"))
        else:
            found = users.query.filter_by(email = e, password = p).first()
            if found:
                flash("This email is already registered; please use a different email.")
                return redirect(url_for("login"))
            else:
                usr = users(e, p)
                db.session.add(usr)
                db.session.commit()
                flash("Registered successfully, now please log in.")
                return redirect(url_for("login"))
    else:
        return render_template("register.html")




@app.route("/logout")
def logout():
    flash("logged out")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
