
import csv 


def parse_csv(filename):
    result = list()
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            result.append(row)
    return result


def groom_data(csv_obj):
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

	with open(full_path,'w',newline='') as csvfile:
		writer = csv.writer(csvfile)

		if fields:
			writer.writerow(fields)
		
		writer.writerows(data)
	return