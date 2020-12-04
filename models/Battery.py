from Errors import Max_Discharge, Over_Charge

class Battery():

    def __init__(self,current_store,max_store):
        if current_store > max_store:
            raise Over_Charge()

        self.kwh_store = current_store
        self.max = max_store


    def discharge(self, total_usage, threshold):
        if total_usage > threshold:
            drain = total_usage - threshold

            if self.kwh_store - drain >= 0:
                self.kwh_store -= drain
                return drain
            else:
                raise Max_Discharge()
        return 0


    def charge(self, total_usage, threshold):
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
        self.kwh_store = self.max
        return