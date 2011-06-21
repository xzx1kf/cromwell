# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from clublist import clublist

# configuration
DATABASE = './tmp/cromwell.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def show_players():
    cur = g.db.execute('select name, club, pos, pts, id from players \
            order by id asc')
    players = [dict(name=row[0], club=row[1], pos=row[2]) \
            for row in cur.fetchall()]
    return render_template('show_players.html', players=players)

#
@app.route('/club/<club>')
def show_club(club):
    cur = g.db.execute('select name, pos, pts, id from players where \
            club=? order by pts desc', [club])
    players = [dict(name=row[0], pos=row[1], id=row[3], pts=row[2]) \
            for row in cur.fetchall()]
    return render_template('show_club.html', players=players)

@app.route('/club', methods=['GET'])
def show_club_get():
    club = request.args.get('clubs')
    cur = g.db.execute('select name, pos, pts, id from players where \
            club=? order by pts desc', [club])
    players = [dict(name=row[0], pos=row[1], id=row[3], pts=row[2]) \
            for row in cur.fetchall()]

    selected_id = club

    return render_template('show_club.html', players=players, clubs=clublist, selected_id=selected_id)

@app.route('/add', methods=['POST'])
def add_player():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into players (name, pos) values (?, ?)',
                 [request.form['name'], request.form['pos']])
    g.db.commit()
    flash('New player was successfully posted')
    return redirect(url_for('show_players'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_players'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_players'))


if __name__ == '__main__':
    app.run()
