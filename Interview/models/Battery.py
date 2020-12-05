
from ..Errors import Max_Discharge, Over_Charge

class Battery():

    def __init__(self,kwh_store,max):
        '''
        @param kwh_store - float - The amount of charge the 
                battery currently carries. 
        @param max - float - The max amount of capacity the 
                battery can carry.
        '''

        if kwh_store > max:
            raise Over_Charge()

        self.kwh_store = kwh_store
        self.max = max


    def discharge(self, total_usage, threshold):
        '''
        @function discharge() - Subtracts the amount of usage over threshold
                from the charge of the battery. If more KWH is needed than
                the battery currently carries then a Max_Discharge error is 
                raised.
        @param total_usage - float - The amount of power usage in KWH.
        @param threshold - float - The threshold that determines when the
                battery should 'kick in' and discharge to supplement the 
                usage.
        @return - float - The amount of drain the battery has incurred. 
        '''

        if total_usage > threshold:
            drain = total_usage - threshold

            if self.kwh_store - drain >= 0:
                self.kwh_store -= drain
                return drain
            else:
                raise Max_Discharge()
        return 0


    def charge(self, total_usage, threshold):
        '''
        @function charge() - Adds them amount of usage under the threshold 
                to the charge of the battery. If the battery is already
                charged to full capacity, no charge is taken. 
        @param total_usage - float - The amount of power usage in KWH.
        @param threshold - float - The threshold that determines when the
                battery should 'kick in' and charge to supplement the 
                usage.
        @return - float - The amount of additional usage the battery used 
                to replenish it's KWH stores.
        '''

        if total_usage < threshold:
            charge = threshold - total_usage
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


    def refresh(self):
        '''
        @function refresh() - Resets the battery's charge store
            the max value. Essentially charging the battery to 
            100%. 
        @return - void.
        '''

        self.kwh_store = self.max
        return

