import csv 
import numpy as np

'''
Thought Process - 
	If I can get the total amount of energy used.

	Total Usage = 
'''
class Max_Discharge(Exception):
	pass




class Battery():

    def __init__(self,max_store,threshold):
        self.kwh_store = max_store
        self.max = max_store
        self.threshold = threshold

    def discharge(self, total_usage):
        if total_usage > self.threshold:
            drain = total_usage - self.threshold

            if self.kwh_store - drain >= 0:
                self.kwh_store -= drain
                return drain * -1
            else:
                # store = self.kwh_store
                # result = total_usage - self.kwh_store
                # self.kwh_store = 0
                raise Max_Discharge()
        return 0

    def charge(self, total_usage):
        if total_usage < self.threshold:
            charge = self.threshold - total_usage
            if self.kwh_store == self.max:
                return 0
            elif charge + self.kwh_store > self.max:
                result = self.max - self.kwh_store
                self.kwh_store = self.max
                return result
            else:
                self.kwh_store += charge
                return charge
        return 0



def parse_csv(filename):
    result = list()
    with open(filename) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            result.append(row)
    return result


def groomdata(csv_obj):
	timestamps = list()
	consumption = list()
	count = 0
	for row in data:
	    if count != 0:
	        timestamps.append(row[0])
	        consumption.append(row[1])
	    count +=1
	consumption = [float(num) for num in consumption]
	return timestamps, consumption


def find_threshold(data,step,kwh_storage):
	#Solve for the threshold iteratively
	#need to make the upper and minimum adjustable.
	answer = -1
	floor = np.amin(data)
	ceiling = np.amax(data)
	for threshold in np.arange(floor,ceiling,step):
		usage = list()
		battery = Battery(kwh_storage, threshold)
		for kwh_usage in data:
			try:
				charge = battery.charge(kwh_usage)
				discharge = battery.discharge(kwh_usage)
				total = kwh_usage + charge + discharge
				usage.append(total)
			except Max_Discharge as e:
				break
		if len(usage) == len(data):
			answer = threshold
			return answer
	return answer




filename = 'january.csv'

data = parse_csv(filename)
timestamps, consumption = groomdata(data)
threshold = find_threshold(consumption,.1,1000)


print(threshold)







