

class Max_Discharge(Exception):
	'''
	Raised in the event a battery is being asked to 
	discharge more than it currently is able to.
	'''
	pass


class Over_Charge(Exception):
	'''
	Raised when the battery is carrying more charge
	than it's capacity.
	'''
	pass