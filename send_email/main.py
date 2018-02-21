import datetime
from send_email import db
from send_email.database_tools import get_entries
from send_email.HTML_tools import create_email_HTML
from send_email.feed_parsers import parse_arXiv_feed
from send_email.paper_tools import filter_papers, sort_papers
from send_email.email_tools import send_email

if __name__ == '__main__':
    filter_keywords = get_entries(db)

    papers = parse_arXiv_feed(r'http://export.arxiv.org/rss/quant-ph')
    print('Total papers from arXiv:', len(papers))
    filtered_papers = filter_papers(papers, **filter_keywords)
    print('Total filtered_papers:', len(filtered_papers))
    sorted_filtered_papers = sort_papers(filtered_papers,
                                         sort_order=['authors', 'title_keywords', 'abstract_keywords'],
                                         **filter_keywords)

    date_string = datetime.datetime.now().strftime("%d %B %Y")
    send_email(email_address='serwan.asaad@gmail.com',
              subject=f'{len(sorted_filtered_papers)} new papers {date_string}',
              html=create_email_HTML(sorted_filtered_papers))