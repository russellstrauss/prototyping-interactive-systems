import sys
import math

class Stats(object):
	def __init__(self, numbers=[]):
		self.numbers = numbers
	
	def addNum(self, n):
		self.numbers.append(n)
		
	def range(self):
		minValue = sys.float_info.max
		maxValue = -sys.float_info.max
		
		for element in self.numbers:
			if (element < minValue):
				minValue = element
			if (element > maxValue):
				maxValue = element
		
		if (len(self.numbers) < 1):
			return (0,0)
		else:
			return (minValue, maxValue)
			
	def mean(self):
		result = 0.0
		for element in self.numbers:
			result += element
		if (len(self.numbers) < 1):
			return 0
		else:
			return (result / len(self.numbers))

	def median(self):
		if (len(self.numbers) < 1):
			return 0
		elif (len(self.numbers) % 2 == 0):
			lower_bound_middle_index = int(len(self.numbers) / 2) - 1
			return (self.numbers[lower_bound_middle_index] + self.numbers[lower_bound_middle_index + 1]) / 2
		else:
			middle_index = math.floor(len(self.numbers) / 2)
			return self.numbers[middle_index]
			
	def reset(self):
		self.numbers = []
		
	def mode(self):
		if (self.numbers == []):
			return []
		else:
			self.numbers.sort()
			temporaryList = []
			i = 0
			while i < len(self.numbers) : 
				temporaryList.append(self.numbers.count(self.numbers[i])) 
				i += 1
				
			d1 = dict(zip(self.numbers, temporaryList))
			d2 = {k for (k,v) in d1.items() if v == max(temporaryList) } 
			return d2
			
			

hr = "========================================"

myStats = Stats()
myStats.addNum(5)
myStats.addNum(50)
myStats.addNum(5)
myStats.addNum(60)
myStats.addNum(61)

print("\nContent:", myStats.numbers)
print(hr)
print("Range:", myStats.range())
print("Mean:", myStats.mean())
print("Median:", myStats.median())
print("Mode:", myStats.mode())
print(hr)
print("\n\n...list reset...\n\n")
myStats.reset()
print("\nContent:", myStats.numbers)
print(hr)
print("Range:", myStats.range())
print("Mean:", myStats.mean())
print("Median:", myStats.median())
print("Mode:", myStats.mode())