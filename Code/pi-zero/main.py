#!/usr/bin/env python3
from sensors import *
from input import *


def init():
	print(start_up_msg)
	
	output_file = OutputFile('sensor_output')
	
	# Create the TCA9548A I2C multiplecer and test the connections
	i2c = I2C_Board()
	
	# Create the ADC object for the potentiometer
	adc = ADC(i2c.tca, output_file)
	
	# Choose number of IMU sensor to use
	
	# automate to find the number of channels with 0x68 and use that
	num_sensors = 4
	
	# Create the IMU sensor objects
	sensors = [ Sensor(n, i2c.tca, output_file) for n in range(num_sensors)]
	
	""" Has not be inplemented
	
	# Allow user to calibrate accelerometers
	response = input('Do you wish to calibrate the accelerometers?: ')
	if(response.lower().startswith('y')):
		[s.calibrate_acc() for s in sensors]
	"""
	
	# Calibrate the sensors
	print('Calibrating the sensors, please keep still')
	[s.calibrate_gyro() for s in sensors]
	
	adc.calibrate()
	
	print('Calibrating done!')
		
	# Initiate the UI object with the choosen frequency
	ui = UserInput(output_file, sensors, frequency = 100000)

	return output_file, sensors, adc, ui
	

def run():
	
	# Initialise the file to record to, the sensors and the UI
	output_file, sensors, adc, ui = init()
	
	# The number of readings before the measurments are written to the output file
	batch_size = 10
			
	i = 0
	data = ''
	
	input('Press enter to start: ')
	print ("Reading Data of Gyroscope and Accelerometer")
	
	# Run untill the user ends the program
	while(ui.run_code):
		# Check if values should be written to file
		if i == batch_size:
			output_file.write(data)
			i = 0
			data = ''
		# Record the sensor values
		for s in sensors: data += s.get_data()
		data += adc.get_data()
		i +=1
		# Allow the user to input commands
		ui.check()
		# Sleep to save power
		time.sleep(int(1/ui.freq))
		
	print("Quiting program")
	
run()

