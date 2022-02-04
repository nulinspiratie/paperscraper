from .arxiv_parser import parse_arxiv_feed
from .nature_parser import parse_nature_feed
from .science_parser import parse_science_feed
from .physical_review_parser import parse_physical_review_feed

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

    'Physical Review Letters': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prl.xml'),
    'Physical Review X': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prx.xml'),
    'Physical Review Quantum': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prxquantum.xml'),
    'Reviews of Modern Physics': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/rmp.xml'),
    'Physical Review Applied': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prapplied.xml'),
    'Physical Review Materials': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prmaterials.xml'),
    'Physical Review Research': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prresearch.xml'),
    'Physical Review A': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/pra.xml'),
    'Physical Review B': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prb.xml'),
    'Physical Review C': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prc.xml'),
    'Physical Review D': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/prd.xml'),
    'Physical Review E': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/pre.xml'),
    'Physical Review Physics': (parse_physical_review_feed, 'http://feeds.aps.org/rss/recent/physics.xml'),
}
