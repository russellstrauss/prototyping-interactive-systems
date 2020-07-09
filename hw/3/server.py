#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™

import os
import sqlite3
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_folder='public', template_folder='views')
app.secret = os.environ.get('SECRET')

DEMOINFO = ("George","Burdell",94,"M")
DBNAME = 'database.db'

def bootstrap_db():

	if os.path.exists(DBNAME):
		os.remove(DBNAME)

	conn = sqlite3.connect(DBNAME)
	c = conn.cursor()
	c.execute('CREATE TABLE dreams(firstname text,lastname text, age int, gender text)')
	c.execute('INSERT INTO  dreams(firstname,lastname,age,gender) VALUES (?,?,?,?)', DEMOINFO)
	c.execute('SELECT * FROM dreams')
	print("first dream in db: " + str(c.fetchone()))
	conn.commit()
	conn.close()

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
			print('storing')
			store_dream(data)
				
	return jsonify(get_dreams())

if __name__ == '__main__':
	bootstrap_db()
	app.run()