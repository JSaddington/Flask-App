from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        u = request.form["nm"]
        session["user"] = u
        flash("Login successful!")
        return redirect(url_for("home"), user=u)
    else:
        if "user" in session:
            flash("already logged in")
            return redirect(url_for("home"))
        else:
            return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        u = session["user"]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        u = session["user"]
        flash(f"logged out {u}", "info")
        session.pop("user", None)

    flash("No user logged in at the moment")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
