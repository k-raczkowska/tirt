# coding=utf-8


class abcd():
    def __init__(s, mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, G, if_cool, if_heat, i):
        s.mk = mk
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

    def suma(s, a, i):
        return a * i

    def f(s, y, if_cool, if_heat):
        Y =  s.q_wall(y) + s.q_int() # + s.q_win() + s.q_int()
        if if_cool:
            Y += s.q_cool(y)
            if s.Tk < s.Tp - Y:
                Y = s.Tk - s.Tp
        if if_heat:
            Y = s.q_heat()
            if s.Tp + Y >= 90:
                Y = 90 - s.Tp
        s.result = Y
        return Y

    def q_cool(self, y):  # klimatyzacja
        res = self.mk * (self.Tk - y) / (self.V * self.d)
        return self.mk * (self.Tk - y) / (self.V * self.d)

    def q_heat(self):  # grzejnik
        return (self.Qg - 1500) * 3600 / (self.V * self.d * 1000)

    def q_int(self):  # osoby w pomieszczeniu
        return self.Np / (self.V * self.d * self.c)

    def q_wall(s, y):  # cieplo przeplywajace przez sciany
        s1 = s.suma(s.Ai / s.hi, s.i)
        s2 = s.suma(s.Al / s.hl, 4 - s.i)
        res = s.k * (s.To - y) / (s.V * s.d * s.c) * (s.suma(s.Ai / s.hi, s.i) + s.suma(s.Al / s.hl, 4 - s.i))
        return s.k * (s.To - y) / (s.V * s.d * s.c) * (s.suma(s.Ai / s.hi, s.i) + s.suma(s.Al / s.hl, 4 - s.i))

    def q_win(self):  # okna
        return self.suma(self.G * self.Ai * self.I, 2) / (self.V * self.d * self.c)

    # rungego kutty 4 rzędu
    def solve(s, if_cool, if_heat):  # początkowe wartości x i y
        h = 0.01

        k1 = h * s.f(s.Tp, if_cool, if_heat)
        x = s.Tp + 1 / 2 * k1 * h
        k2 = h * s.f(s.Tp + 1 / 2 * k1 * h, if_cool, if_heat)
        k3 = h * s.f(s.Tp + 1 / 2 * k2 * h, if_cool, if_heat)
        k4 = h * s.f(s.Tp + k3 * h, if_cool, if_heat)
        dy = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        s.Tp += dy
        return s.Tp
