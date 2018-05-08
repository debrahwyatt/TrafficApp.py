#!/usr/bin/env python3

'''
TrafficApp v1.1

Application stores route data into a file then sorts it for grafial representation.

'''

'''
Bugs and additions:

	csv files need headers
	rework function1
	Runtime error should not cancel forced interrupt
	sorting data could be ommitted by making space and writting into csv once.
	Wednesday at 11:30pm has a second entry and unusual data.
	Cannot append or write to file while it is open by explorer.
	most errors come from sorting csv file, more error log details needed.
	need more safety nets for backup while sorting.

'''

import re
import datetime
from time import sleep
from urllib.request import urlopen

print("\n\nRUNNING: TrafficApp.py\n")

def main():

	location1 = "3023 freethy pl"
	location2 = "uvic"

	while True:
		
		#waits 1 minute to run program
		waiting()

		try:
			function1(location1,location2)
			function1(location2,location1)


		except:
			print("Fatal runtime error.")
			errorlog('0', "Fatal runtime error.")
		

def curr_time():

	#Gives the time in hh:mm
	time = re.findall("^(\d\d:\d\d)", str(datetime.datetime.time(datetime.datetime.now())))
	return time[0]

def waiting():

	print("\nWaiting for: time = 0min (mod5)\n")
	sleep(60)

	try:	
		while True:

			#waits until time is a mod of 5min
			if int(re.sub("\d+:", '', curr_time()))%5 == 0:
				break
	
	except:
		print("Waiting function crash!")
		errorlog('1', "Waiting function crash!")

	return


def errorlog(filename, message):

	try:
		file = open("errorlog.csv", 'a')
		todays_date = str(datetime.date.today())
		time = curr_time()
		
		file.write(todays_date + ',' + time + ',' + filename + ': ' + message + '\n')
		file.close()
		
		print("...Errorlog updated.")

	except:
		print("...Could not update errorlog.")


#extracts the csv file data, sorts it, then rewrites the file
def sort_file(filename):

	print("Sorting csv file...")

	try:
		backup = open(filename, 'r')
		backup_data = backup.readlines()
		backup.close()

	except:
		print("could not create backup, file not sorted.")
		errorlog(filename, "Could not create backup.")
		main()

	weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	temp_data=[]

	try:
		for day in weekday:
			
			minx = 0

			#1440 minutes in a day 
			while minx != 1440:

				file = open(filename, 'r')

				for line in file.readlines():

					line_data = re.findall(day + ',(\d*):(\d*)', line)

					if line_data == []:
						continue

					if int(line_data[0][0])*60 + int(line_data[0][1]) == minx:
						temp_data.append(line)
				
				file.close()

				minx = minx + 5

		#writes the information in temp_data to the file
		file = open(filename, 'w')

		for x in temp_data:
			file.write(x)

		file.close()

		print("...csv file sorted.\n")

	except:

		errorlog(filename, "Could not sort csv file.")

		print("...Could not sort csv file, creating backup...\n")

		backup = open(filename, 'w')

		for line in backup_data:
			backup.write(line)

		backup.close()
		print("...Backup created.")

	return


def function1(l1,l2):

	print("\nGATHERING ROUTE DATA:\n{} to {}\n".format(l1, l2))

	try:
		l1 = l1.replace(' ', '+')
		l2 = l2.replace(' ', '+')
		filename = l1 + '_to_' + l2 + '.csv'

	except:
		print("filename error")
		errorlog('2', "filename error")
		return

	try:
		#loads webpage
		url = 'http://www.google.ca/maps/dir/' + l1 + '/' + l2
		page = urlopen(url)

	except:
		print("Could not find", url)
		errorlog(filename, "Could not find " + url)
		return

	try:
		#regular expression for extracting travel time
		site_info = re.findall("\[\[\d\d\d\d,\"(\d*)?\s*\w*\s*(\d*) min\"\]", str(page.read()))

		formatted_info=[]
		#Extracts all values and converts hours to minutes
		for x in site_info:
			if x[1] != '':
				formatted_info.append(int(x[0])*60+int(x[1]))
			else:
				formatted_info.append(int(x[0]))

		#fastest travel time
		formatted_info=list(sorted(formatted_info))

	except:
		print("Could not extract data from ", url)
		errorlog(filename, "Could not extract data from " + url)
		return


	try:
		travel_time = int(formatted_info[0])
	except:
		print("Could not decifer travel time.")
		errorlog(filename, "Could not decifer travel time.")
		return

	try:
		#extracts the day of the week
		day = str(datetime.date.today().strftime("%A"))
		time = curr_time()
		#prints data to screen
		print ("Day:", day)
		print ("Time:", time)
		print("Commute:",travel_time,"min\n")

	except:
		print("Could not aquire travel info.")
		errorlog(filename, "Could not aquire travel info.")
		return

	'''
	This next section should be broken and cleaned up for error log.
	Nested try statment may not be necessary.
	Maybe this section should be governed by an if statment.
	'''

	#reads data from csv
	try:

		print("Attempting to read previous data file...")
		with open(filename, 'r') as file1:

			file_info = file1.read()
			file1.close()

		sub_expression = re.compile(day+','+time+','+'(\d*)'+','+'(\d*)'+','+'(\d*.?\d*)'+','+'(\d*)'+','+'(\d*)')
		u = re.findall(sub_expression, file_info)
		
		#Algorithm to update data 
		low_travel_time = int(u[0][3])
		high_travel_time = int(u[0][4])

		if travel_time > high_travel_time:
			high_travel_time = travel_time

		if travel_time < low_travel_time:
			low_travel_time = travel_time

		total_travel_time = travel_time + int(u[0][1])
		writes = int(u[0][0]) + 1
		
		print("...File read successful.\n\nUpdating data...")

		avg_travel_time = total_travel_time/writes

		file_info = re.sub(sub_expression,\
		day+','+time+','+str(writes)+','+str(total_travel_time)+','+str(avg_travel_time)+','+str(low_travel_time)+','+str(high_travel_time),\
		file_info)


		with open(filename, 'w') as file1:
			file1.write(str(file_info))
			file1.close()

		print("...Update successful.\n")

	except:
		print("...No previous data found.\n\nAppending file...")

		try:
			with open(filename, 'a') as file1:
				file1.write(day+','+time+','+str(1)+','+str(travel_time)+','+str(travel_time)+','+str(travel_time)+','+str(travel_time)+'\n')
				file1.close()
				print("...File appended.\n")

		except:
			print("...Could not append file.\n")
			errorlog(filename, "Could not append file.")

			return

	sort_file(filename)	

	return

main()


