
# A very simple Flask Hello World app for you to get started with...
from flask import redirect, render_template, request, url_for
import logging

from send_email import application, db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
fh = logging.FileHandler('flask.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))

class Keyword(db.Model):
    __tablename__ = "keywords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))

class Journal(db.Model):
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    enabled = db.Column(db.Boolean)
    summary = db.Column(db.Boolean)
    order = db.Column(db.Integer)

db.create_all()

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("main.html",
                               authors=Author.query.all(),
                               keywords=Keyword.query.all(),
                               journals=Journal.query.all())
    else: # 'POST'
        logger.info(f'Request.form: {request.form}')

        if 'author_button' in request.form:
            name = request.form["contents"]
            existing_authors = Author.query.filter_by(name=name).all()
            if request.form['author_button'] == 'Add':
                logger.info(f'Adding new author: {name}')
                if existing_authors:
                    logger.warning('Author already exists')
                else:
                    author = Author(name=name)
                    db.session.add(author)
            elif request.form['author_button'] == 'Remove' and existing_authors:
                logger.info(f'Removing authors with name: {name}')
                for existing_author in existing_authors:
                    logger.info(f'Removing existing author {existing_author}')
                    db.session.delete(existing_author)
        elif 'keyword_button' in request.form:
            name = request.form["contents"]
            existing_keywords = Keyword.query.filter_by(name=name).all()
            if request.form['keyword_button'] == 'Add' and not existing_keywords:
                logger.info(f'Adding new keyword: {name}')
                keyword = Keyword(name=name)
                db.session.add(keyword)
            elif request.form['keyword_button'] == 'Remove' and existing_keywords:
                logger.info(f'Removing keywords with name: {name}')
                for existing_keyword in existing_keywords:
                    logger.info(f'Removing existing keyword: {existing_keyword}')
                    db.session.delete(existing_keyword)
        elif 'journal_button' in request.form:
            total_journals = Journal.query.all()
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
                existing_journals = Journal.query.filter_by(name=name).all()
                if request.form['journal_button'] == 'Add':
                    if not existing_journals:
                        logger.info(f'Adding journal: {name}')
                        journal = Journal(name=name, enabled=True, summary=True,
                                          order=len(total_journals)+1)
                        db.session.add(journal)
                elif request.form['journal_button'] == 'Remove':
                    for existing_journal in existing_journals:
                        logger.info(f'Removing existing journal: {existing_journal}')
                        db.session.delete(existing_journal)

        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    application.run(host='0.0.0.0')