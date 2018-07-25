# A very simple Flask Hello World app for you to get started with...
import argparse
from flask import redirect, render_template, request, url_for
from send_email import RSS_urls
import logging
from datetime import datetime

from send_email import application, db, AuthorDB, KeywordDB, JournalDB

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
fh = logging.FileHandler('flask.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


db.create_all()

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("main.html",
                               authors=AuthorDB.query.all(),
                               keywords=KeywordDB.query.all(),
                               journals=JournalDB.query.all())
    else: # 'POST'
        logger.info(f'Request.form: {request.form}')

        if 'author_button' in request.form:
            name = request.form["contents"]
            existing_authors = AuthorDB.query.filter_by(name=name).all()
            if request.form['author_button'] == 'Add':
                logger.info(f'Adding new author: {name}')
                if existing_authors:
                    logger.warning('Author already exists')
                else:
                    author = AuthorDB(name=name)
                    db.session.add(author)
            elif request.form['author_button'] == 'Remove' and existing_authors:
                logger.info(f'Removing authors with name: {name}')
                for existing_author in existing_authors:
                    logger.info(f'Removing existing author {existing_author}')
                    db.session.delete(existing_author)
        elif 'keyword_button' in request.form:
            name = request.form["contents"]
            existing_keywords = KeywordDB.query.filter_by(name=name).all()
            if request.form['keyword_button'] == 'Add' and not existing_keywords:
                logger.info(f'Adding new keyword: {name}')
                keyword = KeywordDB(name=name)
                db.session.add(keyword)
            elif request.form['keyword_button'] == 'Remove' and existing_keywords:
                logger.info(f'Removing keywords with name: {name}')
                for existing_keyword in existing_keywords:
                    logger.info(f'Removing existing keyword: {existing_keyword}')
                    db.session.delete(existing_keyword)
        elif 'journal_button' in request.form:
            total_journals = JournalDB.query.all()
            logger.info(f'Journals: {[journal.name for journal in total_journals]}')
            if request.form['journal_button'] == 'Save':
                logger.info('clicked save')
                orders = [int(request.form[f'{journal.name}-order'])
                          for journal in total_journals]
                if not all(k in orders for k in range(1, len(total_journals)+1)):
                    logger.warning(f'Orders not incrementing from 1: {orders}')
                    return redirect(url_for('index'))
                else:
                    logger.info('Updating existing journals')
                    for journal in total_journals:
                        journal.enabled = f'{journal.name}-enabled' in request.form
                        journal.summary = f'{journal.name}-summary' in request.form
                        journal.order = int(request.form[f'{journal.name}-order'])
                        logger.info(f'Updated {journal.name}\t'
                                    f'enabled: {journal.enabled}\t'
                                    f'order: {journal.order}')
            else:
                name = request.form["contents"]
                try:
                    journal = next(journal for journal in RSS_urls
                                   if name.lower() == journal.lower())
                    existing_journals = JournalDB.query.filter_by(name=journal).all()
                    if request.form['journal_button'] == 'Add':
                        if not existing_journals:
                            logger.info(f'Adding journal: {name}')
                            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            journal = JournalDB(name=journal, enabled=True, summary=True,
                                              order=len(total_journals)+1,
                                              last_update=date)
                            db.session.add(journal)
                    elif request.form['journal_button'] == 'Remove':
                        for existing_journal in existing_journals:
                            logger.info(f'Removing existing journal: {existing_journal}')
                            db.session.delete(existing_journal)
                except StopIteration:
                    logger.warning(f'Could not find journal {name} in {RSS_urls}')

        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run paperscraper website')
    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=str)
    parser.add_argument('--public', action='store_const', const=True)
    parsed_args = parser.parse_args()
    if parsed_args.public:
        parsed_args.ip = '155.143.13.171'

    application.run(host=parsed_args.ip, port=parsed_args.port)
