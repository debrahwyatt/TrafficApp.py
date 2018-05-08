#!/usr/bin/env python3

'''
Arrival.py v1.1

Application is used to determain optimal departure times.

Needs conversion from day to day.
Needs error messages when times arnt available.
Still needs estimate when times arn't available.
	

'''


import re

print("\nRUNNING: Arrival_v1.1.py\n\n")

def main():
		
	g=[]
	count = 0

	#Program parameters		
	while True:
		day = input("For what day of the week? ")
		weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

		if day in weekday:
			break
	
	#User input for arrival time
	arrival_time = time = input("\nWhat time? (use 24 hour format eg. 15:45) ")


	'''
	#Supposed to check valid input from user.

	while True:
		arrival_time = time = input("\nWhat time? (use 24 hour format eg. 15:45) ")
		user_test = re.findall('^(\d?\d:\d\d)$', time)
		print(user_test)

		if None in user_test:
			print('hah')
			break
	'''
	
	#user check for travel option
	while True:
		user = int(input("\nFrom home to work = 1\nFrom work to home = 2\n"))
		
		if user == 1:
			filename = '3023+freethy+pl_to_uvic.csv'
			break

		if user == 2:
			filename = 'uvic_to_3023+freethy+pl.csv'
			break



	try:		
		#Open the file with desired route		
		file1 = open(filename, 'r')
		file_info = file1.read()

		while True:

			#gets the arrival time minutes
			time_expression = re.compile('(\d*)' + ':' + '(\d*)')
			m1 = re.findall(time_expression, arrival_time)
			arrival_time_minutes = int(m1[0][1])

			#Expression used to extract travel time
			sub_expression = re.compile( day + ',' + '0?' +time + ',' + '(?:\d*)' + ',' + '(?:\d*)' + ',' + '(\d*)' )
			u = re.findall(sub_expression, file_info)

			#algorithm for departure time
			g.append(int(u[0]))
			check = sum(g)/len(g)

			#converts time from string to int
			m = re.findall(time_expression, time)
			temp_minute = int(m[0][1])
			temp_hour = int(m[0][0])

			#Rolls time over 
			if temp_minute == 0:
				temp_minute = 60
				temp_hour = temp_hour - 1

			#compensates int to string conversion
			temp_minute = temp_minute - 5
			if temp_minute == 5:
				temp_minute = '05'
			if temp_minute == 0:
				temp_minute = '00'

			#Progression counter
			count = count + 5

			#converts time back into string
			time = str(temp_hour) + ':' + str(temp_minute)

			#Determins departure time
			if check <= count:
				print("Time to get there: ", time)
				print("Travel time: ", check)
				return

	except:
		print("Somthing went wrong")

main()

