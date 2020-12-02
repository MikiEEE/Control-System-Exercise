def calculate_new_k_step(k_step):
	power = math.log10(k_step)
	power -= 1
	return 10**power

def find_kwh_needed_2(data,threshold,t_step,k_step):
	if threshold > 0:
		kwh_storage = 0
		answer = find_threshold(data,t_step,kwh_storage)
		while answer == -1 or answer > threshold:
			kwh_storage += k_step
			answer = find_threshold(data,t_step,kwh_storage)
		if k_step < 1:
			return kwh_storage
		else:
			new_k_step = calculate_new_k_step(k_step)
			return find_kwh_needed(data,threshold,t_step,new_k_step)
	return -1

def find_kwh_needed_1(data,threshold,step,tolerance=1):
	if threshold > 0:
		kwh_storage = 0
		answer = find_threshold(data,step,kwh_storage)
		while answer == -1 or answer > threshold:
			kwh_storage += 1
			answer = find_threshold(data,step,kwh_storage)
		return kwh_storage
	return -1

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

def find_threshold_3(data,kwh_storage,tolerance=1,floor=None,ceiling=None):
	if not floor:
		floor = 0
	if not ceiling:
		ceiling = np.amax(data)
	step = int(math.log10(sum(data)))
	step = 10**(step + 1)
	answer = -1
	while step >= tolerance:
		for threshold in np.arange(floor,ceiling,step):
			usage = int()
			battery = Battery(kwh_storage,kwh_storage,threshold)
			for kwh_usage in data:
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

def find_threshold_4(data,kwh_storage,tolerance=1,floor=None,ceiling=None):
	if not floor:
		floor = 0
	if not ceiling:
		ceiling = np.amax(data)
	step = int(math.log10(ceiling))
	step = 10**(step + 1)
	answer = -1
	while step >= tolerance:
		for threshold in np.arange(floor,ceiling,step):
			usage = int()
			battery = Battery(kwh_storage,kwh_storage,threshold)
			for kwh_usage in data:
				try:
					charge = battery.charge(kwh_usage)
					discharge = battery.discharge(kwh_usage)
					usage += 1
				except Max_Discharge as e:

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
	usage = int()
	for kwh_usage in data:
		try:
			battery.charge(kwh_usage)
			modified_usage, potential_charge = potential_modifier(potential_charge, kwh_usage)
			battery.discharge(modified_usage)
			usage += 1
		except Max_Discharge as e:
			print('adding:',step,usage)
			battery.threshold += step
			potential_charge += step * usage
			
	if step >= tolerance:
		answer = battery.threshold
		# if answer != -1:
		# 	floor = answer - step
		# step = calculate_new_step(step)	
	return battery.threshold
