from flask import Flask
from flask_sqlalchemy import SQLAlchemy

RSS_urls = {'arXiv quant-ph': r'http://export.arxiv.org/rss/quant-ph',
            'Nature': 'http://feeds.nature.com/nature/rss/current',
            'Nature Chemistry': 'http://feeds.nature.com/nchem/rss/current',
            'Nature Electronics': 'http://feeds.nature.com/natelectron/rss/current',
            'Nature Materials': 'http://feeds.nature.com/nmat/rss/current',
            'Nature Nanotechnology': 'http://feeds.nature.com/nnano/rss/current',
            'Nature Physics': 'https://www.nature.com/nphys.rss',
            'Science': 'http://science.sciencemag.org/rss/express.xml',
            'Science Advances': 'http://advances.sciencemag.org/rss/current.xml'
            }
RSS_feed_parsers = {}

from . import feed_parsers

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