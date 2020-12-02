import sys
sys.path.append('..')

from Errors import Max_Discharge

class Battery():

    def __init__(self,current_store,max_store,threshold):
        self.kwh_store = current_store
        self.max = max_store
        self.threshold = threshold


    def discharge(self, total_usage):
        if total_usage > self.threshold:
            drain = total_usage - self.threshold

            if self.kwh_store - drain >= 0:
                self.kwh_store -= drain
                return drain * -1
            else:
                raise Max_Discharge()
        return 0


    def charge(self, total_usage):
        if total_usage < self.threshold:
            charge = self.threshold - total_usage
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