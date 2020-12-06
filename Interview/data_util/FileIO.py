import csv 


def parse_csv(full_path:str):
	'''
	@function parse_csv() - Parses the csv file and 
			returns a list of rows.
	@param full_path - str - Full path of the file to be opened.
	@return list(str) - List of lines read.
	'''

    result = list()
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            result.append(row)
    return result


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
	count = 0
	for row in csv_obj:
	    if count != 0:
	        timestamps.append(row[0])
	        consumption.append(row[1])
	    count +=1
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



