from flask import render_template, Blueprint, request, redirect, url_for
from .auth import login_required, get_articles, save_articles

main = Blueprint("main", __name__)


@main.route("/")
def index():
    articles = get_articles()
    sorted_articles = sorted(articles, key=lambda x: x["publish_date"], reverse=True)
    return render_template("index.html", articles=sorted_articles)


@login_required
@main.route("/admin/new_article")
def new_article():
    return render_template("admin/new_article.html")


@login_required
@main.route("/article/<string:article_id>")
def article(article_id):
    articles = get_articles()
    article = next((a for a in articles if a["id"] == article_id))
    if not article:
        return "Article not found", 404
    return render_template("article.html", article=article)


@login_required
@main.route("/admin/edit_article/<string:article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    articles = get_articles()
    article = next((a for a in articles if a["id"] == article_id), None)
    if not article:
        return "Article not found", 404
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        for i, a in enumerate(articles):
            if a["id"] == article_id:
                articles[i]["title"] = title
                articles[i]["content"] = content
                break
        save_articles(articles)
        return redirect(url_for("main.dashboard"))
    return render_template("admin/edit_article.html", article=article)


@login_required
@main.route("/admin/dashboard/")
def dashboard():
    articles = get_articles()
    sorted_articles = sorted(articles, key=lambda x: x["publish_date"], reverse=True)
    return render_template("admin/dashboard.html", articles=sorted_articles)


@login_required
@main.route("/admin/article/<string:article_id>", methods=["POST"])
def delete_article(article_id):
    articles = get_articles()
    article = next((a for a in articles if a["id"] == article_id), None)
    if not article:
        return "Article not found", 404

    for i, a in enumerate(articles):
        if a["id"] == article_id:
            del articles[i]
            break
    save_articles(articles)
    return redirect(url_for("main.dashboard"))
