import feedparser
import logging
from pprint import pformat

from ..paper_tools import Paper, Author


logger = logging.getLogger(__name__)

def parse_nature_feed(url, journal):
    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
        try:
            if 'authors' in entry:
                authors = [Author(author['name']) for author in entry['authors']]
            else:
                authors = []

            date = entry['updated_parsed']
            paper = Paper(authors=authors,
                          title=entry['title'],
                          abstract=entry['summary'].split('</a></p>')[1],
                          link=entry['link'],
                          journal=journal,
                          pdf_link=entry['link'] + '.pdf',
                          date=date)
            papers.append(paper)
        except Exception:
            logger.error(f'Could not parse {journal} entry {pformat(entry)}')
    return papers
