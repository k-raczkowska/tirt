from PyQt4 import QtCore
from math import ceil


class sterowanie():
    def __init__(self, solver, window):
        self.solver = solver
        self.window = window
        self.roznica = 0.5  # stopnie celsjusza - taka roznica powoduje klimatyzacje
        self.temperatury = []
        self.temperaturyCh = []  # temperatury powodujace chlodzenie, czyli za wysokie
        self.temperaturyGrz = []  # -..- grzanie, czyli za niskie

    def podejmijDecyzje(self, temp_aktualna, temp_zadana):
        self.temperatury.append(temp_aktualna)
        print(self.temperatury)
        if temp_aktualna < temp_zadana:
            if not self.solver.if_heat:
                self.window.grzejnik.setChecked(True)
                self.window.update(self.window.grzejnik, True)

            if self.solver.if_cool:
                self.window.klimatyzacja.setChecked(False)
                self.window.update(self.window.klimatyzacja, False)

        if temp_aktualna > temp_zadana:
            roznica = temp_zadana - temp_aktualna
            self.window.update(self.window.klimatyzacja, True)
            x = self.window.temp_cool(temp_zadana, temp_aktualna, roznica)
            if len(self.temperatury) > 1 and self.temperatury[-1] > temp_zadana and temp_zadana < self.temperatury[-2] < \
                            self.temperatury[-1] + self.roznica:
                self.temperaturyCh.append(temp_aktualna)
                # if len(self.temperaturyCh) > 1 and self.temperaturyCh[-2] < self.temperaturyCh[-1] + self.roznica:
                #     self.window.update(self.window.temp_pow, self.window.temp_pow.value() - 1)
                if not self.solver.if_cool:
                    self.window.update(self.window.klimatyzacja, True)
                if self.solver.if_heat:
                    self.window.update(self.window.grzejnik, False)
            print("cooling", x)
