import random
import datetime

def generate_participant(snum, tnum):
	#get timestamp
	#generate random number between 1 and 1000
	currenttime = datetime.datetime.now()
	formattime = currenttime.strftime("%Y-%m-%d %H:%M:%S")
	# result = "RANDOMID,SESSIONNUM,TRIALNUM,TIMESTAMP"
	result = str(random.randint(1, 1000)) + ',' + snum + ',' + tnum + ',' + formattime
	return result