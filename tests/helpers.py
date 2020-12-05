import sys

sys.path.append('..')

from Errors import Max_Discharge
from models.Battery import Battery


def run_sim(data:iter, threshold:float, capacity:float):
	'''
	@function run_sim() - Runs the a scenario with a battery at 
			a set capacity and checks to see if iit goes over the
			threshold.
	@param data - list(float) - list of floats with the power usage 
			data in it.
	@param threshold - float - Threshold for battery to charge and 
			discharge from. 
	@param capacity - Capacity of battery under test in KWH. 
	@return - bool - 
			* True upon successful Battery threshold and capacity
				combination. 
			* False upon battery not beiing sufficient in capacity to 
				maintian the threshold. 
	'''

	battery = Battery(capacity,capacity)

	for usage in data:
		try:
			battery.charge(usage,threshold)
			battery.discharge(usage,threshold)
		except Max_Discharge as e:
			return False
	return True

	