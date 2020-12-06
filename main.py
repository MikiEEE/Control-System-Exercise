import os
import sys
import pandas
import time
import argparse


#Function Imports
from Interview.data_util.Numbers import round_decimals_up
from Interview.algorithms import find_threshold_recursive, find_minimum_capacity_iterative
from Interview.data_util.FileIO import parse_csv, groom_data, \
								write_rows, write_to_text_file

#Class Imports 
from Interview.models.Battery import Battery
from Interview.Errors import Max_Discharge, Over_Charge


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


#Parse Arguements.
parser = argparse.ArgumentParser(description='')
parser.add_argument('Path', type=str,
                       		help='Path of data file.')
parser.add_argument('-ob1','--objective1',type=str2bool, default=True,
							help='Determines if objective1 should be calaculated.')
parser.add_argument('-ob2','--objective2',type=str2bool, default=True,
							help='Determines if objective2 should be calaculated.')
parser.add_argument('-ob3','--objective3',type=str2bool, default=True,
							help='Determines if objective3 should be calaculated.')
args = parser.parse_args()


#Groom the data.
filename = args.Path

print('Validating data...')
#Make sure the file exists.
try:
	data = parse_csv(filename)

except  IOError as e:
	print(e)
	sys.exit(0)


#Make sure the file is in the correct format.
try:
	timestamps, consumption = groom_data(data)

except ValueError as e:
	print(e)
	sys.exit(0)
print('Data validated.\n')

#Create Data Frame Categories.
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
if args.objective1 or args.objective2:

	print('Beginning Monthly Operations...\n')
	starttime = time.time()
	currentDate = startDate
	while currentDate.strftime('%Y-%m') != endDate.strftime('%Y-%m'):
		data = df.loc[(df.Date.dt.month==currentDate.month) & (df.Date.dt.year==currentDate.year)].Usage

		write_str = '{}-{}'.format(currentDate.year,currentDate.month)

		if args.objective1:
			threshold = find_threshold_recursive(data,100,.001)
			threshold = round_decimals_up(threshold,3)

			result = [write_str,threshold]

			threshold_by_month.append(result)

		if args.objective2:
			capacity_needed = find_minimum_capacity_iterative(data,20,1,10)
			capacity_needed = round_decimals_up(capacity_needed,0)

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
if args.objective3:
	starttime = time.time()

	print('Beginning Full Data Set Analysis...')
	data = df.Usage

	capacity = find_minimum_capacity_iterative(data,50,1,10)
	capacity = round_decimals_up(capacity,0)
	capacity = str(capacity)

	timer = time.time() - starttime
	timer = round(timer,1)
	print('Finished Full Data Set Analysis...{} seconds'.format(timer))


	print('\n')


#Check to make sure the output directory exists.
try:
	if not os.path.isdir('Output'):
		Error_Msg = 'The "Output/" directory does not exist.'
		raise IOError(Error_Msg)
except IOError as e:
	print(e)
	sys.exit(0)



try:
	print('Writing to file(s)...')

	files_written = list()

	if args.objective1:
		#Output Minimum Threshold Values to CSV.
		path = os.path.join('Output','minimum_threshold.csv')
		data = threshold_by_month
		write_rows(path,data)
		files_written.append(path)


	if args.objective2:
		#Output Minimum Capacity Values to CSV.
		path = os.path.join('Output','minimum_capacity.csv')
		data = capacity_by_month
		write_rows(path,data)
		files_written.append(path)


	if args.objective3:
		#Output Minimum Capacity Value for enter dataset
		#	to text. 
		path = os.path.join('Output','50kwh_threshold_battery_size.txt')
		data = [capacity]
		write_to_text_file(path,data)
		files_written.append(path)
	
	files = ', '.join(files_written)
	print('File(s) Written: {}.'.format(files))

except Exception as e:
	Error_Msg = 'There was an error writting to one of the files'
	print(Error_Msg)
	sys.exit(0)


 
	 