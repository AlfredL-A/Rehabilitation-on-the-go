#!/usr/bin/env python3
from os import listdir
import pandas as pd
from os.path import *

class MeasurmentData:
	def __init__(self, code_path, n_sensors, file_name = None):
		self.data = None
		self.n_sensors = n_sensors
		self.potentiometer = None
		self.sensors = []
		self.default_file = 'sensor_output'
		self.curr_path = code_path + '/'
		self.file_name = file_name
		self.file_path = None
		self.check_file_path(file_name)
		print('Chosen file: ' + self.file_name + '\nLocated at: ' + self.file_path)
	
	def change_file(self):
		file_name = input('Please enter a valid filename: ')
		self.check_file_path(file_name)
		
	# Verify that the choosen file is valid
	def check_file_path(self, file_name = None):
	
		if file_name != None: self.file_name = file_name
		else: self.file_name = self.default_file
		if self.file_name == self.default_file:
			self.file_path = self.curr_path + self.default_file
		else:
			self.file_path = self.curr_path + 'data/' + self.file_name
			
		if not isfile(self.file_path):
			text = input('The path:' + self.file_path +'\nDoes not lead to a valid file, please enter a valid filename or type show: ')
			if text.lower() == 'show':
				onlyfiles = [f for f in listdir(self.curr_path + 'data') if isfile(join(self.curr_path + 'data/', f))]
				print('Valid datafiles:')
				print(onlyfiles)
				text = input('Please enter a valid filename: ')
				
			self.file_name = text
			self.check_file_path(self.file_name)
	
	# Reads the data and assigns them to the 4 sensors
	def read_data(self):
		data = pd.read_csv(self.file_path, sep='|', comment='#', header=None)
		data = data.rename(columns={0:'sensor',1:'Ax',2:'Ay',3:'Az',4:'Gx',5:'Gy',6:'Gz',7:'Time'})
		
		for i in range(self.n_sensors):
			sensor = self.SensorData(i, data.loc[data['sensor'] == i+1])
			self.sensors.append(sensor)
		self.potentiometer = self.Potentiometer(data.loc[data['sensor'] == 5])
			
		
	
	class SensorData:
		def __init__(self, number, df):
			self.name = number
			self.r1 = 10
			self.r2 = 15
			self.dataframe = df 
			self.time = df[['Time']]
			self.acc = df[['Ax','Ay','Az']]
			self.gyro = df[['Gx','Gy','Gz']]
	
	class Potentiometer:
		def __init__(self, df):
			self.zero_value = None # Maybe implement?
			self.datafram = df 
			self.time = df[['Ay']]
			self.values = df[['Ax']]
		
		
	
