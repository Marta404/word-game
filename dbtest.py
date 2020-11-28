from flask import Flask, g
import sqlite3

from flask import Flask
app = Flask(__name__)
db_location = 'var/gamedb.db'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db in not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/")
def root():
    db = get_db()
    db.cursor().exctute(
        'insert into questions values ( NULL, "What is the name of the biggest part of the human brain?". "The cerebrum", "1")')
    db.commit()

    page = []
    page.append('<html><ul>')
    sql = "SELECT rowid, * FROM questions ORDER BY week"
    for row in db.cursor().execute(sql):
        page.append('<li>')
        page.append(str(row))
        page.append('</li>')

    page.append('</ul></html>')
    return ''.join(page)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)