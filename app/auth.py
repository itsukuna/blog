from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import json
import os
import uuid
from datetime import datetime

auth = Blueprint("auth", __name__)

# temporary username and password
username = "admin"
password = "admin"

article_file = "articles.json"


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        if user == username and pwd == password:
            session["user"] = user
            return redirect(url_for("main.index"))
        else:
            return "Invalid username or password"
    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def get_articles():
    if os.path.exists(article_file):
        with open(article_file, "r") as file:
            articles = json.load(file)
        return articles
    else:
        return []


def save_articles(articles):
    with open(article_file, "w") as file:
        json.dump(articles, file, indent=4)


@auth.route("/admin/article", methods=["GET", "POST"])
def article():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        articles = get_articles()
        articles.append(
            {
                "id": str(uuid.uuid4()),
                "title": title,
                "content": content,
                "publish_date": datetime.now().strftime("%d/%M/%Y"),
            }
        )
        save_articles(articles)
        return redirect(url_for("main.dashboard"))
    return render_template("admin/dashboard.html")
