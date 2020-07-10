import requests
import json
import os
import csv

OUTPUT_ROOT_DIR_NAME = "output"

def check_make_output_root_dir():
	cwd = os.getcwd()
	output_path = os.path.join(cwd, OUTPUT_ROOT_DIR_NAME)
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	return output_path
	
def make_call(data):
	
	endpoint = "https://ninth-wool-string.glitch.me/"
	POST_request = requests.post(endpoint + "dreams", json=data).json() # sending post request and saving response as response object
	
	print('POST')
	print(POST_request)
	GET_request = requests.get(endpoint + "dreams").json()
	print('GET')
	print(GET_request)
	
	# dump txt file
	output_dir = check_make_output_root_dir()
	output_path = os.path.join(output_dir, 'dump.txt')
	
	# dump csv file
	with open(os.path.join(output_dir, 'dump.csv'), mode='w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(['firstname', 'lastname', 'age', 'gender'])
		for row in GET_request:
			csv_writer.writerow(row)
	
	json_data_str = json.dumps(GET_request, indent=4, sort_keys=True)
	print(json_data_str)
	with open(output_path, 'w') as f:
		f.write(json_data_str)