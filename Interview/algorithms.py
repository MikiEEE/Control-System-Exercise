import numpy as np
import math

from .data_util.Numbers import calculate_new_step

from .models.Battery import Battery
from .Errors import Max_Discharge



def find_threshold_bin(data,kwh_storage,floor=None,ceiling=None):
	if kwh_storage  < 0:
		return -1
	if kwh_storage == 0:
		return sum(data)

	if not ceiling:
		ceiling = np.amax(data)
	if not floor:
		floor = 0

	precision = 10
	mid = ((ceiling-floor) / 2) + floor

	answer = -1
	battery = Battery(kwh_storage,kwh_storage)
	for threshold in [mid,ceiling]:
		usage = int()
		battery.refresh()
		for kwh_usage in data:
			try:
				battery.charge(kwh_usage,threshold)
				battery.discharge(kwh_usage,threshold)
				usage += 1
			except Max_Discharge as e:
				break
		if usage == len(data):
			answer = threshold
			break

	if answer != -1:
		
		if answer == ceiling:
			floor = mid
		elif answer == mid:
			ceiling = mid

		if round(floor) != round(ceiling):
			return find_threshold_bin(data,kwh_storage,floor,ceiling)
		else:
			return answer
	return answer


def find_threshold_recursive(data,kwh_storage,precision=1,floor=None,ceiling=None,step=None):
	'''
	@function find_threshold_recursive() - Finds the power draw threshold a battery will 
			provide to a degree of precision. 
	@param data - list(float) - Power usage data in KWH.
	@param kwh_storage - float - Battery capcity in KWH. 
	@param precision - float - Default to 1. The Lowest magnitude of 10 in the result
			calculation.
	@param floor - float - Default to None. The lowest possible threshold used in a given 
			iteration of threshold approximation.
	@param ceiling - float - Default to None. The highest possible threshold used in a given 
			iteration of threshold approximation.
	@param step - float - The step size of each iteration.
	@return - float - The threshold of the battery.
	'''
	
	if kwh_storage  < 0:
		return -1
	if kwh_storage == 0:
		return sum(data)
	
	if not ceiling:
		ceiling = np.amax(data)
	if not floor:
		floor = 0
	if not step:
		step = 10 ** int(math.log10(ceiling))

	answer = -1
	battery = Battery(kwh_storage,kwh_storage)
	for threshold in np.arange(floor,ceiling,step):
		usage = int()
		battery.refresh()
		for kwh_usage in data:
			try:
				battery.charge(kwh_usage,threshold)
				battery.discharge(kwh_usage,threshold)
				usage += 1
			except Max_Discharge as e:
				break
		if usage == len(data):
			answer = threshold
			break
	if step > precision:
		floor = threshold - step
		step = calculate_new_step(step)
		return find_threshold_recursive(data,kwh_storage,precision,floor,ceiling,step)
	else:
		return answer


def find_threshold_iterative(data,kwh_storage,precision=1):
	'''
	@function find_threshold_recursive() - Finds the power draw threshold a battery will 
			provide to a degree of precision. 
	@param data - list(float) - Power usage data in KWH.
	@param precision - float - Default to 1. The Lowest magnitude of 10 in the result
			calculation.
	@param kwh_storage - float - Battery capcity in KWH. 
	@return - float - The threshold of the battery.
	'''

	if kwh_storage < 0:
		return -1
	if kwh_storage == 0:
		return sum(data)

	floor = 0
	ceiling = np.amax(data)
	step = 10 ** int(math.log10(ceiling))

	answer = -1
	battery = Battery(kwh_storage,kwh_storage)
	while step >= precision:
		for threshold in np.arange(floor,ceiling,step):
			usage = int()
			battery.refresh()
			for kwh_usage in data:
				try:
					battery.charge(kwh_usage,threshold)
					battery.discharge(kwh_usage,threshold)
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


def find_minimum_capacity_recursive(data,threshold,c_precision=1,t_precision=1,value=None,step=None):
	'''
	@function find_minimum_capacity_recursive() - Finds the minimum capacity of a battery 
			needed for the power usage to stay at or belwo a given threshold.
	@param data - list(float) - List of floats representing power usage in KWH. 
	@param threshold - float - The threshold a battery needs to provide.
	@param c_precsion - float - The precision of the battery capacity. Should be placed as
			a power of ten. ex: 10**-1 or .1 . 
	@param t_precision - float - The precision of the threshold. Should be placed as
			a power of ten. ex: 10**-1 or .1 . 
	@param value - Value passed from function call to function call in recursion, user should
			not need to use it. 
	@param step - float - Power of ten passed from funciton call to function call in recursion, 
		user should not need to use it.
	@return - float - Storage capacity needed in KWH.
	'''

	if threshold < 0:
		return -1

	if not value:
		value = 0
	if not step:
		step = 10 ** int(math.log10(sum(data)))

	kwh_storage = value

	answer = find_threshold_recursive(data,kwh_storage,t_precision)
	while answer == -1 or answer > threshold:
		kwh_storage += step
		answer = find_threshold_recursive(data,kwh_storage,t_precision)
	
	if step > c_precision:
		start = kwh_storage - step
		step = calculate_new_step(step)
		return find_minimum_capacity_recursive(data,threshold,c_precision,t_precision,start,step)
	else:
		return kwh_storage


def find_minimum_capacity_iterative(data,threshold,c_precision=1,t_precision=1):
	'''
	@function find_minimum_capacity_iterative() - Finds the minimum capacity of a battery 
			needed for the power usage to stay at or belwo a given threshold.
	@param data - list(float) - List of floats representing power usage in KWH. 
	@param threshold - float - The threshold a battery needs to provide.
	@param c_precsion - float - The precision of the battery capacity. Should be placed as
			a power of ten. ex: 10**-1 or .1 . 
	@param t_precision - float - The precision of the threshold. Should be placed as
			a power of ten. ex: 10**-1 or .1 . 
	@return - float - Storage capacity needed in KWH.
	'''

	if threshold < 0: 
		return -1
	
	step = 10**int(math.log10(sum(data)))
	kwh_storage = 0
	temp = -1

	cont = True
	while cont:
		
		temp = find_threshold_recursive(data,kwh_storage,t_precision) 
		while temp == -1 or temp > threshold: 
			kwh_storage += step
			temp = find_threshold_recursive(data,kwh_storage,t_precision)

		if step > c_precision:
			kwh_storage = kwh_storage - step
			step = calculate_new_step(step)
		else:
			cont = False

	return kwh_storage


