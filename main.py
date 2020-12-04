import time
import math
import os
import pandas as pd


#Function Imports
from data_util.FileIO import parse_csv, groom_data, write_rows
from data_util.Numbers import round_decimals_up
from algorithms import find_threshold_recursive, find_minimum_capacity_iterative

#Class Imports 
from models.Battery import Battery
from Errors import Max_Discharge




def test_threshold(data:iter, threshold:float, capacity:float):
	battery = Battery(capacity,capacity)

	for usage in data.Usage:
		try:
			battery.charge(usage,threshold)
			battery.discharge(usage,threshold)
		except Max_Discharge as e:
			return False
	return True


#Rounding issue, ceiling up done
#Tests
#data in csv




filename = 'load_data.csv'

data = parse_csv(filename)
timestamps, consumption = groom_data(data)

data = {'Date':timestamps, 'Usage':consumption}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')

startDate = df.Date.iloc[1]
endDate = df.Date.iloc[-1]
times = 0.0

capacity_by_month = list()
threshold_by_month = list()



currentDate = startDate
while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

	write_str = '{}-{}'.format(currentDate.year,currentDate.month)

	threshold = find_threshold_recursive(data,100,.0001)
	threshold = round_decimals_up(threshold,3)

	result = [write_str,threshold]

	threshold_by_month.append(result)

	capacity_needed = find_minimum_capacity_iterative(data,20,.0001,10)
	capacity_needed = round_decimals_up(capacity_needed,3)

	result = [write_str,capacity_needed]

	capacity_by_month.append(result)

	currentDate = (currentDate + pd.offsets.MonthBegin()).date()



path = os.path.join('Output','minimum_threshold.csv')
data = threshold_by_month
write_rows(path,data)

path = os.path.join('Output','minimum_capacity.csv')
data = capacity_by_month
write_rows(path,data)

# print(kwh_by_month)
# print(threshold_by_month)

# fails = list()
# currentDate = startDate
# for threshold in threshold_by_month:
# 	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)]
	
# 	if not test_threshold(data,threshold,100):
# 		fails.append((currentDate.month,currentDate.year))

# 	currentDate = (currentDate + pd.offsets.MonthBegin()).date()

# print(fails)
# print(times,'\n\n\n\n\n')
# count = 1
# currentDate = startDate
# times = 0.0
# while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
# 	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

# 	start = time.time()
# 	kwh_needed = find_minimum_capacity_iterative(data,20,.001,10)
# 	kwh_needed = round_decimals_up(kwh_needed,3)
# 	times  += time.time() - start
# 	print(count, currentDate.strftime('%Y-%m'),'{0:<10}'.format(kwh_needed), time.time() - start)

# 	currentDate = (currentDate + pd.offsets.MonthBegin()).date()
# 	count += 1


#Need to string battery results together

# print(times,'\n\n\n\n\n')

# data = df.Usage

# start = time.time()
# kwh_needed = find_minimum_capacity_recursive(data,50,.0001,10)
# print(kwh_needed)
# kwh_needed = round_decimals_up(kwh_needed,3)
# print(kwh_needed, time.time() - start)


# print('\n\n\nTHRESHOLD CALCULATIONS')

# start = time.time()
# threshold = find_threshold_recursive(consumption,50,.001)
# # threshold = round(threshold,3)
# print('V2:\n',threshold,'\n', time.time() - start,'seconds')



# start = time.time()
# threshold = find_threshold_iterative(consumption,50,.001)
# # threshold = round(threshold,3)
# print('V3:\n',threshold,'\n', time.time() - start,'seconds')



# print('\n\n\nBattery (kwh) Calculations')
# # start = time.time()
# # kwh_needed = find_kwh_needed(consumption,20,1)
# # print('V1:\n',kwh_needed,'\n', time.time() - start,'seconds')
# threshold = 30
# start = time.time()
# kwh_needed = find_minimum_capacity_recursive(consumption,threshold,.001,10)
# kwh_needed = round(kwh_needed,3)
# print('V2:\n',kwh_needed,'\n', time.time() - start, 'seconds')

# start = time.time()
# kwh_needed = find_minimum_capacity_iterative(consumption,threshold,.001,10)
# # kwh_needed = round(kwh_needed,3)
# print('V3:\n',kwh_needed,'\n', time.time() - start, 'seconds')






