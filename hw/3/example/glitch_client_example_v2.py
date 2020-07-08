import requests
import json
import os

OUTPUT_ROOT_DIR_NAME = "output"

def check_make_output_root_dir():
    cwd = os.getcwd()
    output_path = os.path.join(cwd, OUTPUT_ROOT_DIR_NAME)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path

endpoint = "https://ninth-wool-string.glitch.me/"


data = { "firstname": "Billy Bob", "lastname": "Bobberson", "age":35, "gender": "M" } # data to be sent to api

post_res = requests.post(endpoint + "dreams", json=data).json() # sending post request and saving response as response object

print('POST')
print(post_res)
res = requests.get(endpoint + "dreams").json()
print('GET')
print(res)

json_data_str = json.dumps(res, indent=4, sort_keys=True)
print(json_data_str)

output_dir = check_make_output_root_dir()
output_path = os.path.join(output_dir, 'dump.txt')

with open(output_path, 'w') as f:
    f.write(json_data_str)
