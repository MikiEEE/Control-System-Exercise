import math


def round_decimals_up(number:float, decimals:int=2):
    '''
    @function - Rounds the number up to the nearest 
            decimal place of precision if the there is 
            any value past that decimal place. 
            *Always rounds up. 
    @number - float - Number to be rounded.
    @decimals - int - Number of decimal places to be retained in
            the final answer.
    @return - float - Number rounded up to the nearest decimal place.
    '''

    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


def calculate_new_step(current_step:float):
    '''
    @function calculate_new_step - Finds the new step at a 
            decreased magnitude of 10.
    @return - int - New iteration step. 
    '''
    
    power = int(math.log10(current_step))
    power -= 1
    return 10**power