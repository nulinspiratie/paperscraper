from flask import Flask
from flask_sqlalchemy import SQLAlchemy

RSS_urls = {'arXiv quant-ph': r'http://export.arxiv.org/rss/quant-ph'}
RSS_feed_parsers = {}

from . import feed_parsers

application = Flask(__name__, template_folder='../templates')
application.config.from_object('config')

db = SQLAlchemy(application)