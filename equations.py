# coding=utf-8
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class abcd():
    def __init__(s, mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, G, if_cool, if_heat, i, okna,TG):
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
        s.if_cool = if_cool
        s.if_heat = if_heat
        s.i = i
        s.TG=TG
        print(str(TG)+" to jest TG")

        #s.result = s.f(s.Tp, if_cool, if_heat)
        #print("result start "+str(s.result))


    def suma(s, a, i):
        return a * i

    def f(s, y, if_cool, if_heat):

        Y = 0
        if if_cool:
            Y += s.q_cool(y)
            # if s.Tk > s.Tp - Y:
            #     Y = s.Tk - s.Tp
        if if_heat:
            Y += s.q_heat(y)
            # if s.Tp + Y >= 90:
            #     Y = 90 - s.Tp
        Y += s.q_wall(y) + s.q_int() + s.q_win(s.oknna)
        #s.result = Y + s.Tp
        #print("result "+str(s.result))

        return Y

    def q_cool(self, y):  # klimatyzacja
        res = self.mk*self.d * (self.Tk - y) / (self.V * self.d) #mk jest w m3/h a potrzebne są kg/h stąd mnożymy przez d
        print("cool"+str(self.mk * (self.Tk - y) / (self.V * self.d)))
        #print("from cool:"+str(self.mk * (self.Tk - y) / (self.V * self.d)))
        return self.mk * (self.Tk - y) / (self.V * self.d)


    def q_heat(self,y):  # grzejnik
        a=(self.Qg / (self.d*self.d*self.V * self.c))*3600
        return (self.Qg / (self.d*self.V * self.c))*3600

    def q_int(self):  # osoby w pomieszczeniu
        #print("from ppl "+str(self.Np / (self.V * self.d * self.c)))
        a=self.Np / (self.V * self.d * self.c)
        return self.Np / (self.V * self.d * self.c)

    def q_wall(s, y):  # cieplo przeplywajace przez sciany
        s1 = s.suma(s.Ai / s.hi, s.i)
        s2 = s.suma(s.Al / s.hl, 4 - s.i)
        res = s.k * (s.To - y) / (s.V * s.d * s.c) * (s.suma(s.Ai / s.hi, s.i) + s.suma(s.Al / s.hl, 4 - s.i))
        u=s.k/(s.V*s.d*s.c)
        i=s.suma(s.Al * (s.To - s.Tp) / s.hl, 4 - s.i)
        j=s.suma(s.Ai * (s.Tow - s.Tp) / s.hi, s.i)
        res2 = 3600*s.k / (s.V * s.d * s.c ) * (s.suma(s.Ai * (s.Tow - s.Tp) / s.hi, s.i) + s.suma(s.Al * (s.To - s.Tp) / s.hl, 4 - s.i))
        print("sciany "+str(res2))
        return res2

    def q_win(s, x):  # okna
        licznik_ulamka = 0
        for okno in s.oknna:
            licznik_ulamka += s.G * okno.wysokosc.value() * okno.szerokosc.value() * okno.strona.value()
            wsp = okno.strona.value()
            print (okno.strona.value())
            print (okno.wysokosc.value())
            print (okno.szerokosc.value())
            s.Ai = okno.wysokosc.value() * okno.szerokosc.value()
            print(licznik_ulamka )
            print(s.Ai)
            print("##")
        # print("sciany "+str(licznik_ulamka / (s.V * s.d * s.c/1000)))
        return licznik_ulamka / (s.V * s.d * s.c/1000)

    # rungego kutty 4 rzędu
    def solve(s, if_cool, if_heat):  # początkowe wartości x i y
        h = 0.01
        print("##"+str(if_heat))

        k1 = h * s.f(s.Tp, if_cool, if_heat)
        x = s.Tp + 1 / 2 * k1 * h
        k2 = h * s.f(s.Tp + 1 / 2 * k1 * h, if_cool, if_heat)
        k3 = h * s.f(s.Tp + 1 / 2 * k2 * h, if_cool, if_heat)
        k4 = h * s.f(s.Tp + k3 * h, if_cool, if_heat)
        dy = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        s.Tp += dy

        #print("przyrost "+str(dy))
        s.counter += 1
        return s.Tp






