import feedparser
import logging
from pprint import pformat



logger = logging.getLogger(__name__)


def parse_science_feed(url, journal):
    from ..paper_tools import Paper

    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
        try:
            first_names = entry['author'].split(', ')[1::2]
            last_names = entry['author'].split(', ')[::2]
            authors = [f'{first_name} {last_name}'
                       for first_name, last_name in zip(first_names, last_names)]
            date = entry['updated_parsed']
            paper = Paper(authors=authors,
                          title=entry['title'],
                          abstract=entry['summary'].lstrip('<p>').rstrip('</p>'),
                          link=entry['link'],
                          journal=journal,
                          date=date)
            papers.append(paper)
        except Exception:
            logger.error(f'Could not parse {journal} entry {pformat(entry)}')
    return papers
