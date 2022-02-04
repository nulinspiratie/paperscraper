import feedparser
import re
import logging
from pprint import pformat

from ..paper_tools import Paper, Author


logger = logging.getLogger(__name__)


def parse_arxiv_feed(url, journal):
    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
        try:
            author_strings = re.findall('>([A-Z][^<]+)<\/a>', entry['author'])
            authors = [Author(author_string) for author_string in author_strings]
            title = entry['title'].split(' (arXiv')[0]
            paper = Paper(authors=authors,
                          title=title,
                          abstract=entry['summary'].strip('<p>').strip('</p'),
                          link=entry['link'],
                          journal=journal,
                          pdf_link=entry['link'].replace('/abs/', '/pdf/'),
                          date=rss_dict['updated_parsed'])
            papers.append(paper)
        except Exception:
            logger.error(f'Could not parse {journal} entry {pformat(entry)}')
    return papers
