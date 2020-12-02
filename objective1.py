
import time
import pandas as pd

from Errors import Max_Discharge
from models.Battery import Battery

from data_util.File_Parse import parse_csv, groom_data 

from algorithms import find_threshold_recursive,find_threshold_iterative, \
	find_minimum_capacity_recursive, find_minimum_capacity_iterative








filename = 'load_data.csv'

data = parse_csv(filename)
timestamps, consumption = groom_data(data)

data = {'Date':timestamps, 'Usage':consumption}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')

startDate = df.Date.iloc[1]
endDate = df.Date.iloc[-1]

currentDate = startDate
while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

	start = time.time()
	threshold = round(find_threshold_recursive(data,100,.001),3)
	print(currentDate.strftime('%Y-%m'), threshold, time.time() - start,'seconds')
	
	currentDate = (currentDate + pd.offsets.MonthBegin()).date()

print('\n\n\n\n\n')

currentDate = startDate
while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

	start = time.time()
	kwh_needed = round(find_minimum_capacity_iterative(data,20,.001,10),3)
	print(currentDate.strftime('%Y-%m'),kwh_needed, time.time() - start)

	currentDate = (currentDate + pd.offsets.MonthBegin()).date()


#Need to string battery results together

print('\n\n\n\n\n')

data = df.Usage

start = time.time()
kwh_needed = round(find_minimum_capacity_recursive(data,50,.001,10),3)
print(currentDate.strftime('%Y-%m'),kwh_needed, time.time() - start)


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






