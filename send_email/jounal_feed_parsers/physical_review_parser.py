import feedparser
import re
import logging
from pprint import pformat


logger = logging.getLogger(__name__)


def parse_physical_review_feed(url, journal):
    from ..paper_tools import Paper, Author

    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
        try:
            # Extract authors
            author_entry = entry['author'].replace('\u2009', ' ')
            if '<em>et al.' in author_entry:
                author_entry = author_entry.split('</em>')[0]
                author_entry = author_entry.replace('<em>', ', ')
            author_strings = author_entry.split(', ')
            authors = [Author(author_string) for author_string in author_strings]

            title = entry['title'].split(' (arXiv')[0]
            if '<p>' in entry['summary']:
                abstract = entry['summary'].split('<p>')[1].split('</p>')[0]
            else:
                abstract = ''

            paper = Paper(authors=authors,
                          title=title,
                          abstract=abstract,
                          link=entry['link'],
                          journal=journal,
                          pdf_link=entry['link'].replace('/abs/', '/pdf/'),
                          date=rss_dict['updated_parsed'])
            papers.append(paper)
        except Exception as e:
            logger.error(f'Could not parse {journal} entry {pformat(entry)}')
            print(e)
    return papers
