import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

def calc_string_dist(str1, str2):

	x = np.zeros(len(str1))
	y = np.zeros(len(str2))
	
	#create array of ords for each char
	count = 0
	for char in str1:
		x[count] = ord(char)
		count = count + 1
	count = 0
	for char in str2:
		y[count] = ord(char)
		count = count + 1

	distance, path = fastdtw(x, y, dist=euclidean)
	
	# print(path)
	
	return distance
