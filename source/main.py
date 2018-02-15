import datetime

from database_tools import get_entries
from HTML_tools import create_email_HTML
from feed_parsers import parse_arXiv_feed
from paper_tools import filter_papers, sort_papers
from email_tools import send_email


filter_keywords = get_entries()

papers = parse_arXiv_feed(r'http://export.arxiv.org/rss/quant-ph')
print('Total papers from arXiv:', len(papers))
filtered_papers = filter_papers(papers, **filter_keywords)
sorted_papers = sort_papers(papers,
                            sort_order=['authors', 'title_keywords', 'abstract_keywords'],
                            **filter_keywords)
print('Total filtered_papers:', len(sorted_papers))

# date_string = datetime.datetime.now().strftime("%d %B %Y")
# send_email(email_address='serwan.asaad@gmail.com',
#           subject=f'{len(sorted_papers)} new papers {date_string}',
#           html=create_email_HTML(papers))