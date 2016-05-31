
class controlling():

    def __init__(self, solver, window):
        self.solver = solver
        self.window = window
        self.difference = 0.5  # that difference is small enough to take action
        self.temperaturesList = []

    def chooseAction(self, temporalTemp, desiredTemp):

        self.temperaturesList.append(temporalTemp)
        if temporalTemp < desiredTemp:
            if not self.solver.if_heat and not self.solver.if_cool:
                self.window.radiator.setChecked(True)
                self.window.update(self.window.radiator, True)
                self.solver.if_heat=True

            if self.solver.if_cool:
                self.window.airConditioner.setChecked(False)
                self.window.update(self.window.airConditioner, False)
                self.solver.if_cool=False

        if temporalTemp > desiredTemp:
            difference = desiredTemp - temporalTemp
            if not self.solver.if_cool:
                self.window.update(self.window.airConditioner, True)

            t=self.checkIfAirTemperatureNeedsChange(desiredTemp, temporalTemp, difference)
            if self.solver.Tk != t:
                self.window.update(self.window.airConditionerTemp,t)
                self.solver.Tk = t

            #last temperature is higher than desired and 2nd last is between desired and last one +0,5
            if len(self.temperaturesList) > 1 and self.temperaturesList[-1] > desiredTemp and \
                                    desiredTemp < self.temperaturesList[-2] < self.temperaturesList[-1] + self.difference:

                if not self.solver.if_cool:
                    self.window.update(self.window.airConditioner, True)

                if self.solver.if_heat:
                    self.window.update(self.window.radiator, False)

    def checkIfAirTemperatureNeedsChange(self, desiredTemp, temporalTemp, difference):

        heat = self.solver.mk * (desiredTemp - temporalTemp) / (self.solver.V * self.solver.d)
        if difference < heat:
            if desiredTemp != self.window.spBoxConditionerTempMin.value():
                return self.checkIfAirTemperatureNeedsChange(desiredTemp - 1, temporalTemp, difference)
            else:
                return desiredTemp
        else:
            return desiredTemp
