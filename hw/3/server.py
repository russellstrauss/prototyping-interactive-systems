import os
import sqlite3
from flask import Flask, request, render_template, jsonify
import webbrowser

app = Flask(__name__, static_folder='public', template_folder='views') # Support for gomix's 'front-end' and 'back-end' UI.
app.secret = os.environ.get('SECRET') # Set the app secret key from the secret environment variables.
DREAMS = ['Python. Python, everywhere.'] # Dream database. Store dreams in memory for now. 
DBNAME = 'database.db'

# TODO don't call this every start-up (see below where called in if...__MAIN__)
# probably a way with flask to have an initial database.db instead
def bootstrap_db():

	if os.path.exists(DBNAME):
		os.remove(DBNAME)
	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	c.execute('CREATE TABLE dreams (dream text)')
	c.execute('INSERT INTO dreams VALUES (?)', DREAMS)
	# c.execute('SELECT * FROM dreams')
	# print("first dream in db: " + str(c.fetchone()))
	conn.commit()
	conn.close()

def store_dream(dream):
	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	dream_dat = [dream,]
	print("dream data to insert: " + str(dream_dat))
	c.execute("INSERT INTO dreams VALUES (?)", dream_dat)
	conn.commit()
	conn.close()
	
def get_dreams():
	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	c.execute('SELECT * FROM dreams')
	ret = c.fetchall()
	conn.commit()
	conn.close()  
	return ret

@app.after_request
def apply_kr_hello(response):
	"""Adds some headers to all responses."""

	# Made by Kenneth Reitz. 
	if 'MADE_BY' in os.environ:
			response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
	
	# Powered by Flask. 
	response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
	return response

@app.route('/')
def homepage():
	"""Displays the homepage."""
	return render_template('index.html')
		
@app.route('/dreams', methods=['GET', 'POST'])
def dreams():
	"""Simple API endpoint for dreams. 
	In memory, ephemeral, like real dreams.
	"""

	# Add a dream to the in-memory database, if given. 
	if request.method == 'POST':
		data = None
		if request.is_json:
			data = request.get_json()
			print('JSON!')
			print(data)
		else:
			# Note: request args is bad form for POSTs
			# However, we're preserving this approach so that the HTML client
			# can still work
			data = request.args
			print('NOT JSON!')
			print(data)
			
		if 'dream' in data:
			new_dream = data['dream']
			# DREAMS.append(new_dream)
			store_dream(new_dream)
						
	# Return the list of remembered dreams. 
	#return jsonify(DREAMS)
	return jsonify(get_dreams())

webbrowser.open('http://127.0.0.1:5000', new=2)

if __name__ == '__main__':
	bootstrap_db()
	app.run()
