# coding=utf-8
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class abcd():
    def __init__(s, mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, G, if_cool, if_heat, i, okna, TG):
        s.counter = 0
        s.mk = mk
        s.oknna = okna
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
        s.G = G
        s.I = 5  # todo dodac do gui
        s.if_cool = if_cool
        s.if_heat = if_heat
        s.i = i
        s.result = s.f(s.Tp, if_cool, if_heat)
        s.TG = TG

    def suma(s, a, i):
        return a * i

    def f(s, y, if_cool, if_heat):
        Y = 0
        if if_heat:
            h = s.q_heat()
            Y += 0.4 * s.q_heat()
            if s.Tp + Y >= 0.4 * 80:
                Y = 0.4 * 80 - s.Tp
            if s.Tp >= 0.4 * 80:
                Y = 0
        if if_cool:
            c = s.q_cool(y)
            Y += s.q_cool(y)
            if s.Tk > s.Tp - Y:
                Y = s.Tk - s.Tp
            if s.Tk * 1.1 >= s.Tp:
                Y = 0
            # if s.Tk * 1.1 <= s.Tp - Y:
            #     Y = 0
        if if_cool and s.Tk * 1.1 >= s.Tp:
            Y = 0
        else:
            Y += s.q_wall(y) + s.q_int() + s.q_win(s.oknna)
        s.result = Y + s.Tp
        return Y

    def q_cool(self, y):  # klimatyzacja
        res = self.mk * (self.Tk - y) / (self.V * self.d)
        return self.mk * (self.Tk - y) / (self.V * self.d)

    def q_heat(self):  # grzejnik
        return 0.4 * self.Qg * 3600 / (self.V * self.d * 1000)

    def q_int(self):  # osoby w pomieszczeniu
        return self.Np / (self.V * self.d * self.c)

    def q_wall(s, y):  # cieplo przeplywajace przez sciany
        s1 = s.suma(s.Ai / s.hi, s.i)
        s2 = s.suma(s.Al / s.hl, 4 - s.i)
        res = s.k * (s.To - y) / (s.V * s.d * s.c) * (s.suma(s.Ai / s.hi, s.i) + s.suma(s.Al / s.hl, 4 - s.i))
        res2 = s.k / (s.V * s.d * s.c) * (s.suma(s.Ai * (s.Tow - s.Tp) / s.hi, s.i) + s.suma(s.Al * (s.To - s.Tp) / s.hl, 4 - s.i))
        return res2

    def q_win(s, x):  # okna
        licznik_ulamka = 0
        for okno in s.oknna:
            licznik_ulamka += 0.5 * okno.wysokosc.value() * okno.szerokosc.value() * okno.strona.value()
            wsp = okno.strona.value()
            print okno.strona.value()
            print okno.wysokosc.value()
            print okno.szerokosc.value()
            s.G = 0.5
            s.Ai = okno.wysokosc.value() * okno.szerokosc.value()
        return licznik_ulamka / (s.V * s.d * s.c)

    # rungego kutty 4 rzędu
    def solve(s, if_cool, if_heat):  # początkowe wartości x i y
        h = 0.01

        k1 = h * s.f(s.Tp, if_cool, if_heat)
        x = s.Tp + 1 / 2 * k1 * h
        k2 = h * s.f(s.Tp + 1 / 2 * k1 * h, if_cool, if_heat)
        k3 = h * s.f(s.Tp + 1 / 2 * k2 * h, if_cool, if_heat)
        k4 = h * s.f(s.Tp + k3 * h, if_cool, if_heat)
        dy = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        # s.Tp += dy
        res = s.Tp + dy
        s.counter += 1
        return res
