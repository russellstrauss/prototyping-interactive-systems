
print("\nEnter integers to calculate the average of all inputs, enter -1 to exit.\n")
running = True
result = []

while running:
	inputField = input("Listening for input... ")
	if inputField != "":
		answer = float(inputField)
		if answer == -1:
			running = False
		else:
			result.append(answer)
	
		total = 0	
		for item in result:
			total += item

		if len(result) > 0:
			average = total / len(result)
			print(result)
			if running:
				print("Total average:", average)
			else:
				print('\nexited\n')
				print("Final average:", average)