import csv 
import os

from dateutil.parser import parse

from Interview.Errors import Input_Format


def parse_csv(full_path:str):
	'''
	@function parse_csv() - Parses the csv file and 
			returns a list of rows.
		*Raises IOError if file does not exist.
	@param full_path - str - Full path of the file to be opened.
	@return list(str) - List of lines read.
	'''

	if not os.path.isfile(full_path):
		Error_Msg = 'File {} is not found.'.format(full_path)
		raise IOError(Error_Msg)

	file_type = full_path.split('.')[-1]
	if file_type != 'csv':
		Error_Msg = 'Invalid file type. CSV required.'
		raise IOError(Error_Msg)

	result = list()
	with open(full_path) as file:
		csv_reader = csv.reader(file, delimiter=',')
		for row in csv_reader:
			result.append(row)
	return result


def validate_date(date:str):
	'''
	@function validate_date - Makes sure the string passed in 
			can be parsed into a datetime format.
	@param date - str - String to be validated. 
	@return - bool - True if the date can be parsed and False
		if the date cannot be parsed.
	'''
	try: 
	    parse(date)
	except ValueError:
		return False
	return True


def validate_usage(usage:str):
	'''
	@function validate_usage - Makes sure that the string passed in 
			can be converted into a float. 
	@param usage - str - String to be validated.
	@return - bool - True if the string can be converted to a float 
			and False if the string cannot be converted to a float.
	'''
	try:
		float(usage)
	except ValueError:
		return False
	return True



def groom_data(csv_obj:iter):
	'''
	@function groom_data() - Niche function that makes the data 
			into a format that is easier to analyze.
	@param csv_obj - csv.writer - csv writer object.
	@return list(str),list(float) - Two lists one containing the timestamps
			and one containing the usage data.
	'''

	timestamps = list()
	consumption = list()

	for row in csv_obj[1:]:

		if len(row) != 2:
			Error_Msg = 'Input file is not in correct format.'
			raise Input_Format(Error_Msg)
		
		if not validate_date(row[0]):
			Error_Msg = 'Time Stamp is not in correct format.'
			raise ValueError(Error_Msg)

		if not validate_usage(row[1]):
			Error_Msg = 'Usage data is not being interpreted as a number.'
			raise ValueError(Error_Msg)

		timestamps.append(row[0])
		consumption.append(row[1])

	consumption = [float(num) for num in consumption]
	return timestamps, consumption


def write_rows(full_path:str,data:list,fields:list=None):
	'''
	@function write_rows() - Writes data and/or fields to a csv 
			file.
	@param full_path - str -  Full path of the file to be opened.
	@param data - list(str) - List of strings to be written to.
			*Format = [col1,col2,col3,...coln]
	@param fields - list(str) - List of field names.
			*Format = [field1,field2,field3,...fieldn]
	@return - void
	'''

	with open(full_path,'w',newline='') as csvfile:
		writer = csv.writer(csvfile)

		if fields:
			writer.writerow(fields)
		
		writer.writerows(data)
	return


def write_to_text_file(full_path:str,data:list):
	'''
	@function write_to_text_file() - Writes text to a a file.
	@param full_path - str - Full path of the file to be opened.
	@param data - list(str) - List of strings to be written to.
	@return - void
	'''
	
	with open(full_path,'w') as file:
		file.writelines(data)
	return



