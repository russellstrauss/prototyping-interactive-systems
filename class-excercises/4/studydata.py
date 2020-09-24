from datetime import datetime
import json
import csv
import os
	
def open_json(filename):
	try:
		with open(filename, 'r') as file_in:
			loaded_file = json.load(file_in)
			return loaded_file
	except FileNotFoundError:
		print("File" + filename + "not found.")
		
def open_csv(filename):
	try:
		with open(filename, 'r') as file_in:
			loaded_file = csv.reader(file_in, delimiter=',')
			return loaded_file
	except FileNotFoundError:
		print("File" + filename + "not found.")

def save_json(dictionary, filename):
	dictionary = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(filename, 'w') as file_out:
		file_out.write(dictionary)
		
def write_config(filename, snum, tnum, timestamp, teststring):
	
	with open(filename, mode='w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([snum, tnum, timestamp, teststring])

def json_file_to_dict(filename):
	with open(filename, 'r') as file_in:
		loaded_file = json.load(file_in)
	return loaded_file

def read_config(filename):
	config = open_csv(filename)
	return config