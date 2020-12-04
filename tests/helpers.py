import sys

sys.path.append('..')

from Errors import Max_Discharge
from models.Battery import Battery


def run_sim(data:iter, threshold:float, capacity:float):
	battery = Battery(capacity,capacity)

	for usage in data:
		try:
			battery.charge(usage,threshold)
			battery.discharge(usage,threshold)
		except Max_Discharge as e:
			return False
	return True