import sys
import csv 
import numpy as np
import math
import time

sys.path.append('..')
from models.Battery import Battery


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

def calculate_new_step(current_step):
	power = math.log10(current_step)
	power -= 1
	return 10**power


def find_threshold(data,step,kwh_storage):
	#Solve for the threshold iteratively
	#need to make the upper and minimum adjustable.
	answer = -1
	ceiling = np.amax(data)
	for threshold in np.arange(0,ceiling,step):
		usage = list()
		battery = Battery(kwh_storage,kwh_storage, threshold)
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


def find_threshold_2(data,step,kwh_storage,tolerance=1,floor=None,ceiling=None):
	#Solve for the threshold iteratively
	#need to make the upper and minimum adjustable.
	if not floor:
		floor = 0
	if not ceiling:
		ceiling = np.amax(data)

	answer = -1
	for threshold in np.arange(floor,ceiling,step):
		usage = list()
		battery = Battery(kwh_storage,kwh_storage,threshold)
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
			break
	if step != tolerance:
		new_step = calculate_new_step(step)
		new_floor = threshold - step
		return find_threshold_2(data,new_step,kwh_storage,tolerance,new_floor,ceiling)
	else:
		return answer


def find_threshold_3(data,kwh_storage,tolerance=1,floor=None,ceiling=None):
	if not floor:
		floor = 0
	if not ceiling:
		ceiling = np.amax(data)
	step = int(math.log10(ceiling))
	step = 10**(step)
	answer = -1
	while step >= tolerance: # x log(ceiling) - log(tolerance)
		for threshold in np.arange(floor,ceiling,step): #x 10
			usage = int()
			battery = Battery(kwh_storage,kwh_storage,threshold)
			for kwh_usage in data: #x n
				try:
					charge = battery.charge(kwh_usage)
					discharge = battery.discharge(kwh_usage)
					usage += 1
				except Max_Discharge as e:
					break
			if usage == len(data):
				answer = threshold
				break
		if answer != -1:
			floor = answer - step
		step = calculate_new_step(step)	
	return answer


def potential_modifier(potential_charge,usage):
	if potential_charge - usage >= 0:
		return 0, potential_charge
	else:
		return usage - potential_charge, 0


def find_threshold_4(data,kwh_storage,tolerance=1,floor=None,ceiling=None):
	if not floor:
		floor = 0
	if not ceiling:
		ceiling = np.amax(data)
	step = int(math.log10(ceiling))
	step = 10**step
	answer = -1
	threshold = 0.0
	potential_charge = 0.0
	battery = Battery(kwh_storage,kwh_storage,threshold)
	# while battery.threshold <= ceiling:
	usage = 1
	for kwh_usage in data:
		try:
			battery.charge(kwh_usage)
			modified_usage, potential_charge = potential_modifier(potential_charge, kwh_usage)
			battery.discharge(modified_usage)
		except Max_Discharge as e:
			print('adding:',step,usage)
			battery.threshold += step
			potential_charge += step * usage
		usage += 1

			
	# if step >= tolerance:
	# 	answer = battery.threshold
		# if answer != -1:
		# 	floor = answer - step
		# step = calculate_new_step(step)	
	return battery.threshold

def find_kwh_needed(data,threshold,step):
	if threshold > 0:
		kwh_storage = 0
		answer = find_threshold(data,step,kwh_storage)
		while answer == -1 or answer > threshold:
			kwh_storage += 1
			answer = find_threshold(data,step,kwh_storage)
		return kwh_storage
	return -1



def find_kwh_needed_2(data,threshold,t_step,k_step,value=0):
	if threshold > 0:
		kwh_storage = value
		answer = find_threshold_2(data,t_step,kwh_storage)
		while answer == -1 or answer > threshold:
			kwh_storage += k_step
			answer = find_threshold_2(data,t_step,kwh_storage)
		if k_step == 1:
			return kwh_storage
		else:
			new_k_step = calculate_new_step(k_step)
			return find_kwh_needed_2(data,threshold,t_step,new_k_step,kwh_storage - k_step)


def find_kwh_needed_3(data,threshold,tolerance=1):
	if threshold < 0: 
		return -1
	answer = -1
	kwh_storage = 0
	step = int(math.log10(sum(data)))
	step = 10**(step + 1)
	cont = True 
	while cont:#X log(sum) - log(tolerance)
		answer = find_threshold_3(data,kwh_storage,tolerance) 
		while answer == -1 or answer > threshold: #X10
			kwh_storage += step
			answer = find_threshold_3(data,kwh_storage,tolerance) #klog(n)
		if step > tolerance:
			kwh_storage = kwh_storage - step
			step = calculate_new_step(step)
		else:
			cont = False
	return kwh_storage



filename = 'january.csv'

data = parse_csv(filename)
timestamps, consumption = groomdata(data)

step = int(math.log10(sum(consumption)))
step = 10**(step + 1)

print('\n\n\nTHRESHOLD CALCULATIONS')
start = time.time()
# threshold = find_threshold(consumption,.1,100)
# print('V1:\n',threshold,'\n', time.time() - start,'seconds')

start = time.time()
threshold = find_threshold_2(consumption,step,1000,.1)
print('V2:\n',threshold,'\n', time.time() - start,'seconds')



start = time.time()
threshold = find_threshold_3(consumption,100,.1)
print('V3:\n',threshold,'\n', time.time() - start,'seconds')


# start = time.time()
# threshold = find_threshold_4(consumption,1000,.1)
# print('V4:\n',threshold,'\n', time.time() - start,'seconds')
# print('\n\n\nBattery (kwh) Calculations')
# start = time.time()
# kwh_needed = find_kwh_needed(consumption,20,1)
# print('V1:\n',kwh_needed,'\n', time.time() - start,'seconds')

# start = time.time()
# kwh_needed = find_kwh_needed_2(consumption,20,1,step)
# print('V2:\n',kwh_needed,'\n', time.time() - start, 'seconds')

start = time.time()
kwh_needed = find_kwh_needed_3(consumption,20)
print('V3:\n',kwh_needed,'\n', time.time() - start, 'seconds')






