from flask import Flask,render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('Login.html')

@app.route("/submit", methods=['POST'])
def submit():
    return render_template('Admin.html')
# @app.route("/home")

# @app.route("/admin")
# def admin():
#     return render_template('Admin.html')
@app.errorhandler(404)
def page_not_found(error):
    errortxt = "404 not found"
    return render_template('404.html',errortxt = errortxt), 404



SQLITE_DB_PATH = 'test.db'
SQLITE_DB_SCHEMA = 'test.sql'

with open(SQLITE_DB_SCHEMA) as f:
    create_db_sql = f.read()

db = sqlite3.connect(SQLITE_DB_PATH)

with db:
    db.executescript(create_db_sql)

with db:
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(
        'INSERT INTO members (account, password) VALUES ("user", "0000")'
    )


if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)
