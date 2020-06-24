import participant
import datetime
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
	print("\nReady to capture data for participant id " + participant_id + ". Please type the test sentence as quickly as you can and press Enter to submit. Your test sentence is:\n\n" + test_sentence + "\n")
	input("Press Enter to begin.")
	start_time = datetime.datetime.now()
	test_result = str(input())
	end_time = datetime.datetime.now()
	time_elapsed = end_time - start_time
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
			print("Test complete. Results: \n")
			pprint(result)