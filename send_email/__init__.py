from flask import Flask
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__, template_folder='../templates')
application.config.from_object('config')

db = SQLAlchemy(application)


class AuthorDB(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))


class KeywordDB(db.Model):
    __tablename__ = "keywords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))


class JournalDB(db.Model):
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    enabled = db.Column(db.Boolean)
    summary = db.Column(db.Boolean)
    order = db.Column(db.Integer)
    last_update = db.Column(db.String(4096))
