
import time

from Errors import Max_Discharge
from models.Battery import Battery

from data_util.File_Parse import parse_csv, groom_data 

from algorithms import find_threshold_recursive,find_threshold_iterative, \
	find_minimum_capacity_recursive, find_minimum_capacity_iterative








filename = 'january.csv'

data = parse_csv(filename)
timestamps, consumption = groom_data(data)


print('\n\n\nTHRESHOLD CALCULATIONS')

start = time.time()
threshold = find_threshold_recursive(consumption,50,.001)
print('V2:\n',threshold,'\n', time.time() - start,'seconds')



start = time.time()
threshold = find_threshold_iterative(consumption,50,.001)
print('V3:\n',threshold,'\n', time.time() - start,'seconds')



print('\n\n\nBattery (kwh) Calculations')
# start = time.time()
# kwh_needed = find_kwh_needed(consumption,20,1)
# print('V1:\n',kwh_needed,'\n', time.time() - start,'seconds')

start = time.time()
kwh_needed = find_minimum_capacity_recursive(consumption,50,.01,10)
print('V2:\n',kwh_needed,'\n', time.time() - start, 'seconds')

start = time.time()
kwh_needed = find_minimum_capacity_iterative(consumption,50,.01,10)
print('V3:\n',kwh_needed,'\n', time.time() - start, 'seconds')






