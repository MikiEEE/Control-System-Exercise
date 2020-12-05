import os
import nose
import math
import numpy
import pandas
import sys

sys.path.append('..')

from Interview.algorithms import find_threshold_recursive, find_threshold_iterative, \
						find_threshold_bin, find_minimum_capacity_iterative,\
						find_minimum_capacity_recursive

from Interview.data_util.Numbers import round_decimals_up
from Interview.data_util.FileIO import parse_csv, groom_data, \
								write_rows, write_to_text_file

from helpers import run_sim





def setUp():
	#Setup the data for the test. 
	full_path = os.path.join('test_input','load_data.csv')
	data = parse_csv(full_path)
	timestamps, consumption = groom_data(data)

	#Create the dataframe.
	data = {'Date':timestamps, 'Usage':consumption}
	df = pandas.DataFrame(data)
	df['Date'] = pandas.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')

	#Change Get Data from all of the Januarys.
	data = df.loc[(df.Date.dt.month==1)].Usage
	return [float(usage) for usage in data]


def test_find_minimum_threshold_bin():
	data = setUp()
	max_usage = max(data)
	min_usage = min(data)

	step = int(math.log10(max_usage))
	thresholds = numpy.arange(max_usage,min_usage,step)

	for threshold in thresholds:
		capacity = find_minimum_capacity_bin(data,threshold)
		capacity = round_decimals_up(capacity,3)
		assert run_sim(data,threshold,capacity)


def test_find_minimum_capacity_iterative():
	#Test find_minimum_capacity_recursive() with a 
	#variety of thresholds.

	data = setUp()
	max_usage = max(data)
	min_usage = min(data)
	step = int(math.log10(max_usage))

	thresholds = numpy.arange(max_usage,min_usage,step)

	for threshold in thresholds:
		capacity = find_minimum_capacity_iterative(data,threshold,.001,1)
		capacity = round_decimals_up(capacity,3)
		assert run_sim(data,threshold,capacity)


def test_find_minimum_capacity_recursive():
	#Test find_minimum_capacity_recursive() with a 
	#variety of thresholds.

	data = setUp()
	max_usage = max(data)
	min_usage = min(data)
	step = int(math.log10(max_usage))

	thresholds = numpy.arange(max_usage,min_usage,step)

	for threshold in thresholds:
		capacity = find_minimum_capacity_recursive(data,threshold,.001,1)
		capacity = round_decimals_up(capacity,3)
		assert run_sim(data,threshold,capacity)


def test_find_threshold_recursive():
	#Test the find_threshold_recursive() with 
	#multiple capacities. 

	data = setUp()
	capacities = range(-50,10**3,50)
	precision = .001

	for capacity in capacities:
		threshold = find_threshold_recursive(data,capacity,precision)
		threshold = round_decimals_up(threshold,3)

		if capacity < 0: 
			assert threshold == -1
			continue

		assert run_sim(data,threshold,capacity)



def test_find_threshold_iterative():
	#Test the find_threshold_iterative() with 
	#multiple capacities. 

	data = setUp()
	capacities = range(-50,10**3,50)
	precision = .001

	for capacity in capacities:
		threshold = find_threshold_iterative(data,capacity,precision)
		threshold = round_decimals_up(threshold,3)
		print(capacity, threshold)

		if capacity < 0: 
			assert threshold == -1
			continue
		
		assert run_sim(data,threshold,capacity)



