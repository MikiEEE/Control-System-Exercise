import nose
import sys

sys.path.append('../..')

from Interview.models.Battery import Battery
from Interview.Errors import Max_Discharge, Over_Charge


@nose.tools.raises(Over_Charge)
def test_init():
	#Initiate a battery object in the normal case.
	current_charge = 50
	max_charge = 100
	battery = Battery(current_charge,max_charge)

	#Make sure values are initialized properly.
	assert battery.max  == 100
	assert battery.kwh_store == 50

	#Makes sure battery cannot be initialized with higher
	#charge than capacity.
	max_charge_lower = 0
	current_charge_higher = 100
	battery = Battery(current_charge_higher,max_charge_lower)


@nose.tools.raises(Max_Discharge)
def test_discharge_normal():
	charge = 100
	normal_discharge = 50
	over_discharge = 1000
	threshold = 25
	battery =  Battery(charge,charge)

	#Discharge called when over the threshold.
	discharge = battery.discharge(normal_discharge,threshold)
	assert discharge == 25 
	assert battery.kwh_store == 75

	#Discharge when under threshold.
	normal_discharge = 25
	discharge = battery.discharge(normal_discharge,threshold)
	assert discharge == 0 
	assert battery.kwh_store == 75

	#Test Max_Discharge Raise.
	battery.discharge(over_discharge,threshold)


def test_charge():
	current_charge = 0
	max_charge = 100
	threshold = 25
	usage = 15

	#Initiate a discharged Battery object.
	battery = Battery(current_charge,max_charge)

	#Assert the battery is discharged.
	assert battery.kwh_store == 0

	#Charge the battery in incements of 10.
	for use in range(10):
		assert battery.charge(usage,threshold) == 10

	#Make sure the battery is not charging over max capacity.
	assert battery.charge(usage,threshold) == 0
	assert battery.kwh_store == battery.max

	





