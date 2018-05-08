#!/usr/bin/env python3

'''
data_correction.py v1.0

Application is used to fix duplicates in TrafficApp.py files

'''


import re

print("\nRUNNING: data_correction.py\n\n")

def main(filename):
		
	weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	print("Attempting to fix previous data file...")


	for day in weekday:
		
		time = "00:00"
		print(day)

		while time != "24:00":

			with open(filename, 'r') as file1:
				file_info = file1.read()
				file1.close()

			sub_expression = re.compile(day+','+time+','+'(\d*)'+','+'(\d*)'+','+'(\d*.?\d*)'+','+'(\d*)'+','+'(\d*)')
			u = re.findall(sub_expression, file_info)
			
			try:
				writes = int(u[1][0]) + int(u[0][0])
				total = int(u[1][1]) + int(u[0][1])
				average = total / writes

				with open("1" + filename, 'a') as file1:
					file1.write(day+','+time+','+str(writes)+','+str(total)+','+str(average)+','+u[0][3]+','+u[0][4]+'\n')
					file1.close()

			except:
				try:
					with open("1" + filename, 'a') as file1:
						file1.write(day+','+time+','+u[0][0]+','+u[0][1]+','+u[0][2]+','+u[0][3]+','+u[0][4]+'\n')
						file1.close()
				except:
					None

			#Rolls time forward 5 minutes
			m = re.findall('(\d*)'+':'+'(\d*)', time)

			minute = int(m[0][1])+5
			hour = int(m[0][0])

			if minute >= 60:
				hour = hour+1
				minute = '00'

			if minute == 5:
				minute = '05'

			if hour < 10:
				time = '0' + str(hour) + ':' + str(minute)
			else:
				time = str(hour) + ':' + str(minute)


	print("...Fix has been successfully applied to {}.\n".format(filename))


main('3023+freethy+pl_to_uvic.csv')
main("uvic_to_3023+freethy+pl.csv")

