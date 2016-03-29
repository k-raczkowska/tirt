# coding=utf-8
class abcd():
    def __init__(s, mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, G):
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

    def suma(s, a):
        return a

    def f(s, x, y):
        Y = s.q_cool() + s.q_heat() + s.q_int() + s.q_wall() + s.q_win()
        return Y

    def q_cool(self):  # klimatyzacja
        return self.mk * (self.Tk - self.Tp) / (self.V * self.d)

    def q_heat(self):  # grzejnik
        return self.Qg / (self.V * self.d)

    def q_int(self):  # osoby w pomieszczeniu
        return self.Np / (self.V * self.d * self.c)

    def q_wall(s): # cieplo przeplywajace przez sciany
        return s.k * (s.To - s.Tp) / (s.V * s.d * s.c) * (s.suma(s.Ai / s.hi) + s.suma(s.Al / s.hl))

    def q_win(self):
        return self.suma(self.G * self.Ai * self.I) / (self.V * self.d * self.c)

    # rungego kutty 4 rzędu
    def solve(s, x, y):  # początkowe wartości x i y
        h = 0.01

        k1 = h * s.f(x, y)
        k2 = h * s.f(x + h / 2, y + 1 / 2 * k1 * h)
        k3 = h * s.f(x + h / 2, y + 1 / 2 * k2 * h)
        k4 = h * s.f(x + h, y + k3 * h)
        dy = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        s.Tp = s.Tp + dy
