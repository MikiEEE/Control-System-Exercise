import argparse



def str2bool(v):
	'''
	@function str2bool() - Translates common boolean intended strings to 
		respective boolean values.
	*NOTE  - Raises ArgumentTypeError if v param is not one of the
			common boolean intended strings.
	@param v - str - String to be converted into bool.
	@return bool - Boolean translation of the string.
	'''

	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')