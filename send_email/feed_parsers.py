import feedparser
import re
from .paper_tools import Paper, Author
from . import RSS_feed_parsers


def parse_arXiv_feed(url, journal):
    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
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
    return papers
RSS_feed_parsers['arXiv quant-ph'] = parse_arXiv_feed



def parse_nature_feed(url, journal):
    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
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
    return papers
RSS_feed_parsers['Nature'] = parse_nature_feed
RSS_feed_parsers['Nature Chemistry'] = parse_nature_feed
RSS_feed_parsers['Nature Electronics'] = parse_nature_feed
RSS_feed_parsers['Nature Materials'] = parse_nature_feed
RSS_feed_parsers['Nature Nanotechnology'] = parse_nature_feed
RSS_feed_parsers['Nature Physics'] = parse_nature_feed


def parse_science_feed(url, journal):
    rss_dict = feedparser.parse(url)
    papers = []
    for entry in rss_dict['entries']:
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
    return papers
RSS_feed_parsers['Science'] = parse_science_feed
RSS_feed_parsers['Science Advances'] = parse_science_feed