#!/usr/bin/env python3

'''
Arrival.py v1.0

Application is used to determine optimal departure times.

'''


import re
import datetime
from time import sleep
from urllib.request import urlopen

print("\nRUNNING: test.py\n\n")

def main():
		
	#Program parameters		
	day = 'Tuesday'
	arrival_time = time = '17:00'
	g=[]
	count = 0

	try:		
		#Open the file with desired route		
		file1 = open('3023+freethy+pl_to_uvic.csv', 'r')
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

			if temp_minute == 0:
				temp_minute = 60
				temp_hour = temp_hour - 1

			temp_minute = temp_minute - 5
			count = count + 5

			time = str(temp_hour) + ':' + str(temp_minute)

			if check <= count:
				print(time)
				print(check)
				return


	except:
		print("Somthing went wrong")

main()

