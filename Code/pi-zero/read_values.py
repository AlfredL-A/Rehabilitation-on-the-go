#!/usr/bin/env python3
from os.path import *
import sys
from data_frame import *

def run():
	curr_path = dirname(abspath(__file__)) 
	
	alt_file = None
	if len(sys.argv) > 1:
		alt_file = sys.argv[1]
		
	n_sensors = 4

	df = MeasurmentData(curr_path, n_sensors, alt_file)
	df.read_data()
	
	
	print(df.sensors[0].acc)
run()

