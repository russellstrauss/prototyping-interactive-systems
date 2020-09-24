import participant
import studydata
from datetime import datetime
from pprint import pprint

running = True
result = {}
participant_session = []
print("Welcome to the typing studying. Prepare to be analyzed.")
test_sentence = str(input("[For Experimenter] Enter a test sentence: "))
session_number = str(input("[For Experimenter] Enter session num: "))
trial_number = str(input("[For Experimenter] Enter trial num: "))
participant_id = participant.generate_participant(session_number, trial_number)

while running:
	print("\nReady to capture data for participant id " + participant_id + ". Please type the test sentence as quickly as you can and submit. Your test sentence is:\n\n" + test_sentence + "\n")
	input("Press Enter to begin.")
	start_time = datetime.now()
	test_result = str(input())
	end_time = datetime.now()
	time_elapsed = end_time - start_time
	start_time = str(datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f'))
	end_time = str(datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f'))
	print("You typed: " + test_result)
	print("Time elapsed: ", time_elapsed)
	trial = (start_time, end_time, test_result)
	participant_session.append(trial)
	result.update({participant_id: participant_session})
	answer = str(input("Continue testing this participant? Enter y or n. ")).lower()
	if answer == "n":
		answer = str(input("Continue testing with a new participant? Enter y or n. ")).lower()
		participant_session = []
		participant_id = participant.generate_participant(session_number, trial_number)
		if answer == "n":
			running = False
			filename = str(input("Test complete. Enter a filename for your result database. "))
			studydata.save_json(result, filename + '.json')
			print("Results saved to " + filename + '.json')
			studydata.write_config(filename + "_config.csv", session_number, trial_number, start_time, test_sentence)
			print("Configuration saved to " + filename + "_config.csv")