#!/usr/bin/env python3
import time, board
import numpy as np
import adafruit_mpu6050
import adafruit_tca9548a
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Sensor:
	def __init__(self, number, tca, output_file):
		self.num = number
		self.mpu = adafruit_mpu6050.MPU6050(tca[number])
		self.output_file = output_file
		self.offset = self.Offset()
		

	
	def calibrate_gyro(self):
		print ('Calibrating Gyroscope_{0}'.format(self.num+1))
		values = np.array([0] * 3)
		n = 50
		for i in range(n):
			values = np.add(values, np.array(self.mpu.gyro))
		gyro_offset = values/n
		self.offset.set(gyro_offset)
		print('Gyro offset: {0}'.format(gyro_offset))
		self.output_file.write('# Gyroscope {0} offset: Gx={1}, Gy={2}, Gz={3}\n'.format(self.num+1, gyro_offset[0], gyro_offset[1], gyro_offset[2]))
		
	"""
	# Has not bee inplemented, see:
	
	https://makersportal.com/blog/calibration-of-an-inertial-measurement-unit-imu-with-raspberry-pi-part-ii
	
	def calibrate_acc(self):
		print ('Calibrating Accelerometer_{0}'.format(self.num+1))
		values = np.array([0] * 3)
		n = 50
		for i in range(n):
			values = np.add(values, np.array(self.mpu.acceleration))
		gyro_offset = values/n
		self.offset.set(gyro_offset)
		print('Gyro offset: {0}'.format(gyro_offset))
		self.output_file.write('# Gyroscope {0} offset: Gx={1}, Gy={2}, Gz={3}\n'.format(self.num+1, gyro_offset[0], gyro_offset[1], gyro_offset[2]))
	"""
		
	def get_data(self):
		time_stamp = time.time()
		Ax, Ay, Az = self.mpu.acceleration
		# Gx, Gy, Gz = self.mpu.gyro
		Gx, Gy, Gz = 0, 0 ,0

		# Gx -= self.offset.x
		# Gy -= self.offset.y
		# Gz -= self.offset.z
		# print('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}\n'.format(self.num + 1,Ax,Ay,Az,Gx,Gy,Gz,time_stamp))
		return '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}\n'.format(self.num + 1,Ax,Ay,Az,Gx,Gy,Gz,time_stamp)

	class Offset:
		def __init__(self):
			self.x = 0
			self.y = 0
			self.z = 0
			
		def set(self, offset):
			[self.x, self.y, self.z] = offset
	
		def get(self):
			return self.x, self.y, self.z
			
class ADC:
	def __init__(self, tca, output_file):
		adc = ADS.ADS1115(tca[7])
		self.chan = AnalogIn(adc, ADS.P0)
		self.zero_value = None
		self.perpendicular = None
		self.value = None
		adc.gain = 2/3
		self.k_value = 0.00958*1.04
		self.m_value = -126

	def calibrate(self):
		input('Position the exoskeleton so that all sensors are along the same axis and press enter:')
		self.zero_value = self.chan.value*self.k_value + self.m_value
		print('The zero value for the potentiometer is set to {0}.'.format(self.zero_value))
		
		
	def get_data(self):
		time_stamp = time.time()
		self.value = self.chan.value*self.k_value + self.m_value
		#print('{0}|{1}|{2}\n'.format(5, self.value, time_stamp))
		return '{0}|{1}|{2}\n'.format(5, self.value, time_stamp)
		
class I2C_Board:
	def __init__(self):
		self.tca = adafruit_tca9548a.TCA9548A(board.I2C())
		self.check_i2c()
	
	def check_i2c(self):
		print('Reading the addresses on the I2C mutiplexer')
		for channel in range(8):
			if self.tca[channel].try_lock():
				print("Channel {}:".format(channel), end="")
				addresses = self.tca[channel].scan()
				print([hex(address) for address in addresses if address != 0x70])
				self.tca[channel].unlock()
		
