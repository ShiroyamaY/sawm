import os
import sqlite3
from pathlib import Path
from flask import Flask, request, render_template, redirect, url_for, session, g, flash

APP_SECRET = os.environ.get("APP_SECRET", "dev-secret-change-me")
DB_PATH = os.environ.get("DB_PATH", "app.db")

app = Flask(__name__)
app.config.update(SECRET_KEY=APP_SECRET)


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(DB_PATH)
		g.db.row_factory = sqlite3.Row
	return g.db


@app.teardown_appcontext
def close_db(exc):
	db = g.pop('db', None)
	if db is not None:
		db.close()


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	login TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);
"""

SEED_USERS = [
	("alice", "password1"),
	("bob", "password2"),
	("charlie", "password3"),
	("dave", "password4"),
	("eve", "password5"),
	("mallory", "password6"),
	("trent", "password7"),
]


@app.route('/init')
def init_db():
	db = get_db()
	db.executescript(SCHEMA_SQL)
	# insert users if not exists
	for login, password in SEED_USERS:
		try:
			db.execute("INSERT INTO user (login, password) VALUES (?, ?)", (login, password))
		except sqlite3.IntegrityError:
			pass
	db.commit()
	return "DB initialized and seeded with 7 users."


@app.route('/')
def index():
	return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')


@app.route('/login-vuln', methods=['POST'])
def login_vuln():
	# DELIBERATELY VULNERABLE: string concatenation into SQL
	username = request.form.get('login', '')
	password = request.form.get('password', '')
	query = f"SELECT id, login FROM user WHERE login = '{username}' AND password = '{password}'"
	try:
		row = get_db().execute(query).fetchone()
	except sqlite3.Error as e:
		flash(f"SQL error: {e}", "error")
		return redirect(url_for('login'))
	if row:
		session['user'] = dict(row)
		return redirect(url_for('admin'))
	flash("Invalid credentials (vulnerable).", "error")
	return redirect(url_for('login'))


@app.route('/login-safe', methods=['POST'])
def login_safe():
	# SAFE: parameterized query + server-side validation
	username = request.form.get('login', '')
	password = request.form.get('password', '')
	if not validate_input(username) or not validate_input(password):
		flash("Invalid input format.", "error")
		return redirect(url_for('login'))
	row = get_db().execute(
		"SELECT id, login FROM user WHERE login = ? AND password = ?",
		(username, password)
	).fetchone()
	if row:
		session['user'] = dict(row)
		return redirect(url_for('admin'))
	flash("Invalid credentials (safe).", "error")
	return redirect(url_for('login'))


def validate_input(value: str) -> bool:
	# simple whitelist: letters, digits, underscore, 3-32 chars
	import re
	return bool(re.fullmatch(r"[A-Za-z0-9_]{3,32}", value or ""))


@app.route('/admin')
def admin():
	if 'user' not in session:
		flash("Please login first.", "error")
		return redirect(url_for('login'))
	return render_template('admin.html', user=session['user'])


@app.route('/logout')
def logout():
	session.clear()
	flash("Logged out.")
	return redirect(url_for('login'))


if __name__ == '__main__':
	# ensure templates/static dirs exist
	Path('templates').mkdir(exist_ok=True)
	Path('static').mkdir(exist_ok=True)
	app.run(host='127.0.0.1', port=5000, debug=True)

