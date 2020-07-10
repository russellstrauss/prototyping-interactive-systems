import os
import csv
import json
import sqlite3
import requests
import webbrowser
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_folder='public', template_folder='views')
app.secret = os.environ.get('SECRET')
DBNAME = 'database.db'

def bootstrap_db():

	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	
	create_table_query = "CREATE TABLE dreams(firstname text,lastname text, age int, gender text)"
	table_exists_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='dreams'"
	print(table_exists_query)
	if not conn.execute(table_exists_query).fetchone():
		conn.execute(create_table_query)
	c.execute('SELECT * FROM dreams')
	print("first dream in db: " + str(c.fetchone()))

	conn.commit()
	conn.close()

# TODO I bet it is fine to leave sqlite connection persistent instead of opening/closing for each call
def store_dream(dream):
	
	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	dream_dat = [dream["firstname"],dream["lastname"],dream["age"],dream["gender"]]
	print("***********dream data to insert: ", dream_dat)
	c.execute("INSERT INTO dreams(firstname,lastname,age,gender) VALUES (?,?,?,?)", dream_dat)
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
			print('json store_dream')
			store_dream(data)
			print("jsonify")
			print(jsonify(get_dreams()).json)
		
	# dump csv file
	with open('output/dump.csv', mode='w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(['firstname', 'lastname', 'age', 'gender'])
		for row in jsonify(get_dreams()).json:
			csv_writer.writerow(row)		
	
	json_data_str = json.dumps(jsonify(get_dreams()).json, indent=4, sort_keys=True)
	with open("output/dump.txt", 'w') as f:
		f.write(json_data_str)
	
	return jsonify(get_dreams())

webbrowser.open('http://127.0.0.1:5000', new=2)

if __name__ == '__main__':
	bootstrap_db()
	app.run()