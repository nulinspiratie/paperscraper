import feedparser
import re
from .paper_tools import Author, Paper


def parse_arXiv_feed(url):
    rss_dict = feedparser.parse(url)
    print(rss_dict)
    papers = []
    for entry in rss_dict['entries']:
        author_strings = re.findall('>([A-Z][^<]+)<\/a>', entry['author'])
        authors = [Author(author_string) for author_string in author_strings]
        title = entry['title'].split(' (arXiv')[0]
        paper = Paper(authors=authors,
                      title=title,
                      abstract=entry['summary'].strip('<p>').strip('</p'),
                      link=entry['link'],
                      journal='arXiv',
                      pdf_link=entry['link'].replace('/abs/', '/pdf/'))
        papers.append(paper)
    return papers