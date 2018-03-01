import sys
import datetime
from collections import OrderedDict
import pyperclip

from send_email import db
from send_email.database_tools import retrieve_data
from send_email.HTML_tools import create_email_HTML
from send_email.paper_tools import Journal
from send_email.email_tools import send_email

if __name__ == '__main__':
    data = retrieve_data(db)

    journals = [Journal(**journal) for journal in data['journals']
                if journal['enabled']]

    for journal in journals:
        journal.get_new_papers(authors=data['authors'],
                               keywords=data['keywords'])

    total_papers = sum(len(journal.sorted_papers) for journal in journals)

    email_HTML = create_email_HTML(journals=journals)


    if len(sys.argv) > 1:
        date_string = datetime.datetime.now().strftime("%d %B %Y")
        send_email(email_address='serwan.asaad@gmail.com',
                  subject=f'{total_papers} new papers {date_string}',
                  html=email_HTML)
    else:
        pyperclip.copy(email_HTML)