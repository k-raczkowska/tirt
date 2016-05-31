# coding=utf-8
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class solver():
    def __init__(s, mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, isAirCon, isRadiator, i, windows, TG):

        s.mk = mk
        s.windows = windows
        s.Tk = Tk
        s.Tp = Tp
        s.V = V
        s.d = d
        s.c = c
        s.Qg = Qg
        s.Np = Np
        s.k = k
        s.hi = hi
        s.hl = hl
        s.To = To
        s.Ai = Ai
        s.Al = Al
        s.Tow = Tow
        s.R = R
        s.if_cool = isAirCon
        s.if_heat = isRadiator
        s.i = i
        s.TG = TG
        s.result = s.f(s.Tp, isAirCon, isRadiator)

    def multiply(s, a, i):
        return a * i

    def f(s, y, isAirCon, isRadiator):
        Y = 0
        if isRadiator:
            h = s.radiatorHeat()
            Y += s.k * s.radiatorHeat()
            if s.Tp + Y >= s.k * s.TG:
                Y = s.k * s.TG - s.Tp
            if s.Tp >= s.k * s.TG:
                Y = 0
        if isAirCon:
            c = s.airConHeat(y)
            Y += s.airConHeat(y)
            if s.Tk > s.Tp - Y:
                Y = s.Tk - s.Tp
            if s.Tk * s.d >= s.Tp:
                Y = 0
                
        if isAirCon and s.Tk * s.d >= s.Tp:
            Y = 0
        else:
            Y += s.wallsHeat(y) + s.peopleHeat() + s.windowsHeat(s.windows)
        s.result = Y + s.Tp
        return Y

    def airConHeat(self, y):
        return self.mk * (self.Tk - y) / (self.V * self.d)

    def radiatorHeat(self):  
        return self.k * self.Qg * 3600 / (self.V * self.d * 1000) # scaling into m^3/h

    def peopleHeat(self):
        return self.Np / (self.V * self.d * self.c)

    def wallsHeat(s, y):
        res2 = 100*s.k / (s.V * s.d * s.c) * (s.multiply(s.Ai * (s.Tow - s.Tp) / s.hi, s.i) + s.multiply(s.Al * (s.To - s.Tp)/ s.hl, 4 - s.i))
        return res2

    def windowsHeat(s, x):  
        numerator = 0
        for okno in s.windows:
            numerator += s.k * okno.height.value() * okno.width.value() * okno.radiation.value()
            s.Ai = okno.height.value() * okno.width.value()
        return numerator / (s.V * s.d * s.c)

    # 4-th order runge kutta method
    def solve(s, isAirCon, isRadiator):
        h = 0.01

        k1 = h * s.f(s.Tp, isAirCon, isRadiator)
        k2 = h * s.f(s.Tp + 1 / 2 * k1 * h, isAirCon, isRadiator)
        k3 = h * s.f(s.Tp + 1 / 2 * k2 * h, isAirCon, isRadiator)
        k4 = h * s.f(s.Tp + k3 * h, isAirCon, isRadiator)
        dy = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        res = s.Tp + dy
        return res
