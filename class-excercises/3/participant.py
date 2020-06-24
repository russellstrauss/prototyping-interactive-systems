import random
from datetime import datetime

def generate_participant(snum, tnum):
	formattime = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
	result = str(random.randint(1, 99999)) + ',' + snum + ',' + tnum + ',' + formattime
	return result