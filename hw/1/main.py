import sys
import csv
import json
import datetime
from calc_string_dist import calc_string_dist
running = True
hr = "---------------------------------"

def load_csv(filepath):
	with open(filepath) as fp:
		reader = csv.reader(fp, delimiter=",", quotechar='"')
		data = [row for row in reader]
	return data
	
def load_json(filename):
	try:
		with open(filename, "r") as file_in:
			loaded_file = json.load(file_in)
			return loaded_file
	except FileNotFoundError:
		print("File" + filename + "not found.")

#load_file = str(input("Enter the file name (without extension) for the data: "))
load_file = "studydata2"
config = load_csv(load_file + "_config.csv")[0]
study_data = load_json(load_file + "_data.json")
test_string = config[3]

global_stats = []
def calc_global_stats():
	total_typing_session_count = 0
	average_time = datetime.timedelta(0)
	average_accuracy = 0.0
	average_time_delta = datetime.timedelta(0)
	average_accuracy_delta = 0.0
	slowest_time = datetime.timedelta(0)
	fastest_time = datetime.timedelta(hours=9999)
	least_accurate = 0.0
	most_accurate = sys.float_info.max
	worst_time_delta = datetime.timedelta(0)
	best_time_delta = datetime.timedelta(hours=9999)
	worst_accuracy_delta = 0.0
	best_accuracy_delta = sys.float_info.max
	
	for participant_id in study_data:
		
		participant_sessions = study_data[participant_id]
		participant_typing_session_count = 0
		
		time_delta = datetime.timedelta(0)
		accuracy_delta = 0.0
		
		for typing_session in participant_sessions:
			
			error = calc_string_dist(typing_session[2], test_string)
			start_time = datetime.datetime.strptime(typing_session[0], "%Y-%m-%d %H:%M:%S.%f")
			end_time = datetime.datetime.strptime(typing_session[1], "%Y-%m-%d %H:%M:%S.%f")
			time_elapsed = end_time - start_time
			average_time += time_elapsed
			average_accuracy += error
			
			if (participant_typing_session_count == 0):
				first_time_elapsed = time_elapsed
				first_accuracy = error
				
			if (participant_typing_session_count == len(participant_sessions) - 1):
				last_time_elapsed = time_elapsed
				last_accuracy = error
				
				accuracy_delta = last_accuracy - first_accuracy
				time_delta = last_time_elapsed - first_time_elapsed
				
				if (time_delta > worst_time_delta):
					worst_time_delta = time_delta
				if (time_delta < best_time_delta):
					best_time_delta = time_delta
				if (accuracy_delta > worst_accuracy_delta):
					worst_accuracy_delta = accuracy_delta
				if (accuracy_delta < best_accuracy_delta):
					best_accuracy_delta = accuracy_delta

				average_accuracy_delta += accuracy_delta
				average_time_delta += time_delta
			
			if (time_elapsed > slowest_time):
				slowest_time = time_elapsed
			if (time_elapsed < fastest_time):
				fastest_time = time_elapsed
			if (error < most_accurate):
				most_accurate = error
			if (error > least_accurate):
				least_accurate = error
			
			participant_typing_session_count += 1
			total_typing_session_count += 1
			
	average_time /= total_typing_session_count
	average_accuracy /= total_typing_session_count
	average_accuracy_delta /= total_typing_session_count
	average_time_delta /= total_typing_session_count

	global_stats.append({"Session": config[0]})
	global_stats.append({"Trial": config[1]})
	global_stats.append({"Timestamp": config[2]})
	global_stats.append({"Test String": test_string})
	global_stats.append({"Num Participants": len(study_data)})
	global_stats.append({"Total Typing Sessions": total_typing_session_count})
	global_stats.append({"Average Time": average_time})
	global_stats.append({"Average Accuracy": average_accuracy})
	global_stats.append({"Average Time Delta": average_time_delta})
	global_stats.append({"Average Accuracy Delta": average_accuracy_delta})
	global_stats.append({"Slowest Time": slowest_time})
	global_stats.append({"Fastest Time": fastest_time})
	global_stats.append({"Least Accurate": least_accurate})
	global_stats.append({"Most Accurate": most_accurate})
	global_stats.append({"Worst Time Delta": worst_time_delta})
	global_stats.append({"Best Time Delta": best_time_delta})
	global_stats.append({"Worst Accuracy Delta": worst_accuracy_delta})
	global_stats.append({"Best Accuracy Delta": best_accuracy_delta})

while running:
	
	query = str(input("Select an Option: (G)lobal stats, (Q)uery a participant, (R)emove participant, (E)xport data, (P)rint participant IDs, e(X)it. "))
	query = query.lower()
	
	if (query == "p"):
		print(hr)
		for row in study_data:
			print(row)
		print(hr)
		
	elif (query == "x"):
		running = False
	
	elif (query == "g"):
		global_stats = []
		calc_global_stats()
		print(hr)
		for row in global_stats:
			for column in row:
				print(str(column).ljust(25) + ": " + str(row[column]))
		print(hr)
		
	elif (query == "q"):
		participant_id = str(input("Please enter participant ID. "))
		try:
			participant_session = study_data[participant_id]
		except KeyError:
			print("No participant with that ID found.")
		
		if (participant_session):
			participant_stats = []
			participant_typing_session_count = 0
			average_time = datetime.timedelta(0)
			average_accuracy = 0.0
			slowest_time = datetime.timedelta(0)
			fastest_time = datetime.timedelta(hours=9999)
			least_accurate = 0.0
			most_accurate = sys.float_info.max
			
			for typing_session in participant_session:
				
				error = calc_string_dist(typing_session[2], test_string)
				start_time = datetime.datetime.strptime(typing_session[0], "%Y-%m-%d %H:%M:%S.%f")
				end_time = datetime.datetime.strptime(typing_session[1], "%Y-%m-%d %H:%M:%S.%f")
				time_elapsed = end_time - start_time
				average_time += time_elapsed
				average_accuracy += error
				
				if (participant_typing_session_count == 0):
					first_time_elapsed = time_elapsed
					first_accuracy = error
					
				if (participant_typing_session_count == len(participant_session) - 1):
					last_time_elapsed = time_elapsed
					last_accuracy = error
					
					accuracy_delta = last_accuracy - first_accuracy
					time_delta = last_time_elapsed - first_time_elapsed

					average_time_delta += time_delta
				
				if (time_elapsed > slowest_time):
					slowest_time = time_elapsed
				if (time_elapsed < fastest_time):
					fastest_time = time_elapsed
				if (error < most_accurate):
					most_accurate = error
				if (error > least_accurate):
					least_accurate = error
				
				participant_typing_session_count += 1
				
			average_time /= participant_typing_session_count
			average_accuracy /= participant_typing_session_count
			
			participant_stats.append({"Participant Record": participant_id})
			participant_stats.append({"Num Typing Sessions": participant_typing_session_count})
			participant_stats.append({"Average time": average_time})
			participant_stats.append({"Max time": slowest_time})
			participant_stats.append({"Min time": fastest_time})
			participant_stats.append({"Average accuracy": average_accuracy})
			participant_stats.append({"Least accurate": least_accurate})
			participant_stats.append({"Most accurate": most_accurate})
			participant_stats.append({"Time delta": time_delta})
			participant_stats.append({"Accuracy delta": accuracy_delta})
			
			print(hr)
			for row in participant_stats:
				for column in row:
					print(str(column).ljust(25) + ": " + str(row[column]))
			print(hr)
		
	elif (query == "p"):
		for participant_id in study_data:
			print(participant_id)
			
	elif (query == "r"):
		participant_id = str(input("Please enter participant ID. "))
		
		try:
			study_data.pop(participant_id, None)
		except KeyError:
			print("No participant with that ID found.")
	
	elif (query == "e"):
		filename = str(input("Please enter a filename without extension. "))
		
		header = []
		for row in global_stats:
			for key in row:
				header.append(key)
		
		with open(filename + ".csv", mode="w") as file_out:
			writer = csv.writer(file_out, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
			
			writer.writerow(header)
			
			values = []
			for row in global_stats:
				for column in row:
					if (str(row[column]) != ""):
						values.append(str(row[column]))
			writer.writerow(values)