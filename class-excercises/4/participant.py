import random
import datetime

def generate_participant(snum, tnum):
	currenttime = datetime.datetime.now()
	formattime = currenttime.strftime("%Y-%m-%d%H:%M:%S")
	result = str(random.randint(1, 99999)) + ',' + snum + ',' + tnum + ',' + formattime
	return result