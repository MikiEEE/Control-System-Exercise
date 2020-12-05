import os
import sys
import pandas
import time


#Function Imports
from Interview.data_util.Numbers import round_decimals_up
from Interview.algorithms import find_threshold_recursive, find_minimum_capacity_iterative
from Interview.data_util.FileIO import parse_csv, groom_data, \
								write_rows, write_to_text_file

#Class Imports 
from Interview.models.Battery import Battery
from Interview.Errors import Max_Discharge, Over_Charge





#Groom the data.
filename = 'load_data.csv'
data = parse_csv(filename)



#Create Data Frame Categories.
timestamps, consumption = groom_data(data)
data = {'Date':timestamps, 'Usage':consumption}
df = pandas.DataFrame(data)



#Change dates to indexable date time.
df['Date'] = pandas.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')



#Initiate Date Iteration Variables.
startDate = df.Date.iloc[1]
endDate = df.Date.iloc[-1]

capacity_by_month = list()
threshold_by_month = list()



#Monthly Operations.
print('Beginning Monthly Operations...\n')
starttime = time.time()
currentDate = startDate
while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
	data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

	write_str = '{}-{}'.format(currentDate.year,currentDate.month)

	threshold = find_threshold_recursive(data,100,.001)
	threshold = round_decimals_up(threshold,3)

	result = [write_str,threshold]

	threshold_by_month.append(result)

	capacity_needed = find_minimum_capacity_iterative(data,20,.001,10)
	capacity_needed = round_decimals_up(capacity_needed,3)

	result = [write_str,capacity_needed]

	capacity_by_month.append(result)

	Letter = currentDate.strftime("%B")[0]
	print(Letter,end='')
	sys.stdout.flush()

	currentDate = (currentDate + pandas.offsets.MonthBegin()).date()


timer = time.time() - starttime
timer = round(timer,1)
print('\n\nFinished Monthly Operations...{} seconds'.format(timer))


print('\n')


#Total Data Operations.
starttime = time.time()

print('Beginning Full Data Set Analysis...')
data = df.Usage

capacity = find_minimum_capacity_iterative(data,50,.001,10)
capacity = round_decimals_up(capacity,3)
capacity = str(capacity)

timer = time.time() - starttime
timer = round(timer,1)
print('Finished Full Data Set Analysis...{} seconds'.format(timer))


print('\n')


print('Writing to files...')
#Output Minimum Threshold Values to CSV.
path = os.path.join('Output','minimum_threshold.csv')
data = threshold_by_month
write_rows(path,data)



#Output Minimum Capacity Values to CSV.
path = os.path.join('Output','minimum_capacity.csv')
data = capacity_by_month
write_rows(path,data)



#Output Minimum Capacity Value for enter dataset
#	to text. 
path = os.path.join('Output','50kwh_threshold_battery_size.txt')
data = [capacity]
write_to_text_file(path,data)
print('Files Written')

 