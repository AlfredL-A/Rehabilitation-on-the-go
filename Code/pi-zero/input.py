#!/usr/bin/env python3
import datetime, time, select, sys


start_up_msg = '''***************************************************************************
--- Code by Alfred Lind-Anderton ---
Commands for program, type 'my_command' then press enter
'stop'			stops sensor readings
'start'			starts sensor readings
'restart' or 'new'	reruns the setup wiping the readings
'XX hz'			changes frequency, not accurate for high hz
'change'		saves and opens a new file in the data folder
'end'			stops the readings and quits the code
***************************************************************************'''

class UserInput:
	def __init__(self, outputFile, sensors, frequency):
		self.output_file = outputFile
		self.sensors = sensors
		self.freq = frequency
		self.read_sensors = True
		self.run_code = True
	
	def check(self):
		input = select.select([sys.stdin], [], [], 0)[0]
		if(input):
			self.read_input()
	
	def read_input(self):
		value = sys.stdin.readline().rstrip().lower()
		if(value == "stop" and self.read_sensors):
			print("Sensor readings have been stopped ")
			self.read_sensors = False
			self.pause()
		
		elif(value == 'start' and not self.read_sensors):
			print("Sensor readings have been started ")
			self.read_sensors = True
		
		elif(value == 'new' or value == 'restart'):
			print('Restarting the code and wiping old data')
			self.output_file.format()
			for s in self.sensors:
				s.calibrate_gyro()
			
		elif(value == 'end'):
			self.run_code = False
			self.output_file.file.close()
			
		elif(value.endswith('hz')):
			frequency = value.split()[0] if len(value.split()) == 2 else ''
			if(frequency != ''):
				print('Reading rate has been changed to {0} Hz'.format(float(frequency)))
				self.freq = float(frequency)
				
		elif(value == 'change'):
			file_name = input('The current file has been closed, the file will be placed in the datafolder.\nPlease enter the new filename: ')
			while len(file_name.split()) > 1:
				file_name = input('Too many inputs. Please enter the new filename: ')
			self.output_file.change_file_name(file_name)
			print(file_name, 'file created in data folder.')
			for s in self.sensors:
				s.calibrate_gyro()
	
	def pause(self):
		while(not self.read_sensors and self.run_code):
			self.check()
			time.sleep(0.1)	
			

class OutputFile:
	def __init__(self, file_name):
		self.name = file_name
		self.file = None
		self.format()
	
	def change_file_name(self, file_name):
		self.name = 'data/' + file_name
		self.format()
		
	
	def format(self):
		if self.file:
			self.file.close
		self.file = open('/home/pi/knee-extension/' + self.name, 'w')
		self.file.truncate(0)
		start_time_str = str(datetime.datetime.now())
		for c in ' :.':
			start_time_str = start_time_str.replace(c, '_')
		reading_topics = '# MPU6050 data recorded at: ' +  start_time_str + '\n' \
		+ '# Sensor | A_x | A_y | A_z | G_x | G_ y | G_z | Time\n'
		self.file.write(reading_topics)
		
	def write(self, data):
		self.file.write(data)
		
	
		
	
