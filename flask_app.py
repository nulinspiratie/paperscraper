
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from .source import *

app = Flask(__name__)
app.config["DEBUG"] = False

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="nulinspiratie",
    password="paperscraperpassword",
    hostname="paperscraperdb.cbyxywvwfrgo.us-east-2.rds.amazonaws.com",
    databasename="nulinspiratie$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))

class TitleKeyword(db.Model):
    __tablename__ = "title_keywords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))

class AbstractKeyword(db.Model):
    __tablename__ = "abstract_keywords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("main_page.html",
                               authors=Author.query.all(),
                               title_keywords=TitleKeyword.query.all(),
                               abstract_keywords=AbstractKeyword.query.all())

    else: # 'POST'
        name = request.form["contents"]

        if 'author_button' in request.form:
            existing_authors = Author.query.filter_by(name=name).all()
            if request.form['author_button'] == 'Add' and not existing_authors:
                # Add new author
                author = Author(name=name)
                db.session.add(author)
            elif request.form['author_button'] == 'Remove' and existing_authors:
                for existing_author in existing_authors:
                    db.session.delete(existing_author)
        elif 'title_keyword_button' in request.form:
            existing_title_keywords = TitleKeyword.query.filter_by(name=name).all()
            if request.form['title_keyword_button'] == 'Add' and not existing_title_keywords:
                # Add new title keyword
                title_keyword = TitleKeyword(name=name)
                db.session.add(title_keyword)
            elif request.form['title_keyword_button'] == 'Remove' and existing_title_keywords:
                for existing_title_keyword in existing_title_keywords:
                    db.session.delete(existing_title_keyword)
        elif 'abstract_keyword_button' in request.form:
            existing_abstract_keywords = AbstractKeyword.query.filter_by(name=name).all()
            if request.form['abstract_keyword_button'] == 'Add' and not existing_abstract_keywords:
                # Add new abstract keyword
                abstract_keyword = AbstractKeyword(name=name)
                db.session.add(abstract_keyword)
            elif request.form['abstract_keyword_button'] == 'Remove' and existing_abstract_keywords:
                for existing_abstract_keyword in existing_abstract_keywords:
                    db.session.delete(existing_abstract_keyword)
        db.session.commit()
        return redirect(url_for('index'))
