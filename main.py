import traceback
import sys
import datetime
import pyperclip
import logging
import argparse

from send_email import db
from send_email.database_tools import retrieve_data
from send_email.HTML_tools import create_email_HTML
from send_email.paper_tools import Journal
from send_email.email_tools import send_email
# from send_email.database_tools import initialize_user


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape journal papers.')
    parser.add_argument('--create-user', type=str,
                        help='Create a user in the database')
    parser.add_argument('--email', type=str, help='Use custom e-mail address')
    parser.add_argument('--update', help='Update journal last updated',
                        action='store_const', const=True)
    parsed_args = parser.parse_args()

    if parsed_args.create_user:
        db.create_all()
        quit()

    try:
        data = retrieve_data(db)

        journals = [Journal(**journal) for journal in data['journals']
                    if journal['enabled']]

        for journal in journals:
            journal.get_new_papers(authors=data['authors'],
                                   keywords=data['keywords'])

        total_papers = sum(len(journal.new_papers) for journal in journals)

        email_HTML = create_email_HTML(journals=journals)
        
        if parsed_args.update:
            for journal in journals:
                journal.update_database()
            db.session.commit()
    except:
        print(traceback.format_exc())

        db.session.rollback()
        email_HTML = traceback.format_exc()


    if parsed_args.email:
        date_string = datetime.datetime.now().strftime("%d %B %Y")
        send_email(email_address=parsed_args.email,
                  subject=f'{total_papers} new papers {date_string}',
                  html=email_HTML)
    else:
        try:
            pyperclip.copy(email_HTML)
        except:
            logger.error('Could not copy text')
            print(email_HTML)
