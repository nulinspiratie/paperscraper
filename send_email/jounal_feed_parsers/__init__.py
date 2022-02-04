from .arxiv_parser import parse_arxiv_feed
from .nature_parser import parse_nature_feed
from .science_parser import parse_science_feed

RSS_feed_parsers = {
    'arXiv quant-ph': (parse_arxiv_feed, 'http://export.arxiv.org/rss/quant-ph'),
    'arXiv cond-mat': (parse_arxiv_feed, 'http://export.arxiv.org/rss/cond-mat'),

    'Nature': (parse_nature_feed, 'http://feeds.nature.com/nature/rss/current'),
    'Nature Chemistry': (parse_nature_feed, 'http://feeds.nature.com/nchem/rss/current'),
    'Nature Electronics': (parse_nature_feed, 'http://feeds.nature.com/natelectron/rss/current'),
    'Nature Materials': (parse_nature_feed, 'http://feeds.nature.com/nmat/rss/current'),
    'Nature Nanotechnology': (parse_nature_feed, 'http://feeds.nature.com/nnano/rss/current'),
    'Nature Physics': (parse_nature_feed, 'https://www.nature.com/nphys.rss'),
    'Nature Reviews Physics': (parse_nature_feed, 'http://feeds.nature.com/natrevphys/rss/current'),
    'Nature Communications': (parse_nature_feed, 'http://feeds.nature.com/ncomms/rss/current'),
    'npj Quantum Information': (parse_nature_feed, 'http://feeds.nature.com/npjqi/rss/current'),

    'Science': (parse_science_feed, 'http://science.sciencemag.org/rss/express.xml'),
    'Science Advances': (parse_science_feed, 'http://advances.sciencemag.org/rss/current.xml'),
}
