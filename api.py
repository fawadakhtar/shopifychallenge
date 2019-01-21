import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to my bike store</h1>
<p>Hi Quality used bikes and a reasonable price.</p>'''


@app.route('/bikes/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('bikes1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM bikes where inventory_count > 0;').fetchall()

    return jsonify(all_books)
	
@app.route('/bikes/select', methods=['GET'])
def api_select():
	query_parameters = request.args
	title = query_parameters.get('title')
	query = "SELECT * FROM bikes WHERE"
	to_filter = []

	if title:
		query += ' title=? AND'
		to_filter.append(title)
	

	query = query[:-4] + ';'

	conn = sqlite3.connect('bikes1.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()

	results = cur.execute(query, to_filter).fetchall()

	return jsonify(results)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/bikes/purchase', methods=['GET'])
def api_purchase():
	query_parameters = request.args
	title = query_parameters.get('title')
	query = "SELECT * FROM bikes WHERE"
	to_filter = []

	if title:
		query += ' title=? AND'
		to_filter.append(title)
	

	query = query[:-4] + ';'

	conn = sqlite3.connect('bikes1.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute('''UPDATE bikes SET inventory_count = inventory_count -1 where title = ? ''', (title,) )

	results = cur.execute(query, to_filter).fetchall()

	return jsonify(results)

app.run()