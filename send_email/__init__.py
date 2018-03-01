from flask import Flask
from flask_sqlalchemy import SQLAlchemy

RSS_urls = {'arXiv quant-ph': r'http://export.arxiv.org/rss/quant-ph',
            'Nature': 'http://feeds.nature.com/nature/rss/current',
            'Nature Chemistry': 'http://feeds.nature.com/nchem/rss/current',
            'Nature Electronics': 'http://feeds.nature.com/natelectron/rss/current',
            'Nature Materials': 'http://feeds.nature.com/nmat/rss/current',
            'Nature Nanotechnology': 'http://feeds.nature.com/nnano/rss/current',
            'Nature Physics': 'https://www.nature.com/nphys.rss',
            }
RSS_feed_parsers = {}

from . import feed_parsers

application = Flask(__name__, template_folder='../templates')
application.config.from_object('config')

db = SQLAlchemy(application)