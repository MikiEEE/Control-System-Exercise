import sys
import os
import nose
import math
import numpy
import pandas


sys.path.append('..')

from algorithms import find_threshold_recursive, find_threshold_iterative, \
						find_minimum_capacity_iterative, find_minimum_capacity_recursive

from data_util.Numbers import round_decimals_up
from data_util.FileIO import parse_csv, groom_data, \
								write_rows, write_to_text_file

from helpers import run_sim





def setUp():
	full_path = os.path.join('test_input','load_data.csv')
	data = parse_csv(full_path)
	timestamps, consumption = groom_data(data)
	data = {'Date':timestamps, 'Usage':consumption}
	df = pandas.DataFrame(data)
	df['Date'] = pandas.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
	data = df.loc[(df.Date.dt.month==1)].Usage
	return [float(usage) for usage in data]


def test_find_minimum_capacity_iterative():
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
	data = setUp()
	capacities = range(0,10**3,50)
	precision = .001

	for capacity in capacities:
		threshold = find_threshold_recursive(data,capacity,precision)
		threshold = round_decimals_up(threshold,3)
		assert run_sim(data,threshold,capacity)



def test_find_threshold_iterative():
	data = setUp()
	capacities = range(0,10**3,50)
	precision = .001

	for capacity in capacities:
		threshold = find_threshold_iterative(data,capacity,precision)
		threshold = round_decimals_up(threshold,3)
		print(capacity, threshold)
		assert run_sim(data,threshold,capacity)



