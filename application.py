
# A very simple Flask Hello World app for you to get started with...
from flask import redirect, render_template, request, url_for

from send_email import application, db


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
    enabled = db.Column(db.Boolean())
    order = db.Column(db.Integer())

db.create_all()

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("main.html",
                               authors=Author.query.all(),
                               keywords=Keyword.query.all())
    else: # 'POST'
        name = request.form["contents"]

        if 'author_button' in request.form:
            existing_authors = Author.query.filter_by(name=name).all()
            if request.form['author_button'] == 'Add' and not existing_authors:
                # Add new author
                author = Author(name=name)
                db.session.add(author)
            elif request.form['author_button'] == 'Remove' and existing_authors:
                for existing_author in existing_authors:
                    db.session.delete(existing_author)
        elif 'keyword_button' in request.form:
            existing_keywords = Keyword.query.filter_by(name=name).all()
            if request.form['keyword_button'] == 'Add' and not existing_keywords:
                # Add new keyword
                keyword = Keyword(name=name)
                db.session.add(keyword)
                print('Adding keyword', name)
            elif request.form['keyword_button'] == 'Remove' and existing_keywords:
                for existing_keyword in existing_keywords:
                    db.session.delete(existing_keyword)
                print('Removing keyword', name)
        elif 'save_button' in request.form:
            pass
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    application.run(host='0.0.0.0')