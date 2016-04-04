# coding=utf-8
from PyQt4 import QtCore, QtGui
from equations import abcd
from newWindow import newWind
from windows import okno

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Window(QtGui.QWidget):
    vbox1 = QtGui.QVBoxLayout()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.zew = QtGui.QSpinBox()
        self.klimatyzacja = QtGui.QGroupBox("Klimatyzacja")
        self.grzejnik = QtGui.QGroupBox("Grzejnik")
        self.czy_grzejnik = self.grzejnik.isChecked()
        self.lista_wys_okien = []
        grid = QtGui.QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createSecondExclusiveGroup(), 2, 1)
        grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        grid.addWidget(self.createPushButtonGroup(), 1, 0)
        grid.addWidget(self.createSciany(), 2, 0)
        grid.addWidget(self.createOkna(), 1, 1)
        grid.addWidget(self.create_persons(), 3, 0)
        grid.addWidget(self.solve(), 3, 1)

        self.setLayout(grid)

        self.setWindowTitle("Modelowanie temperatury pomieszczenia")
        self.resize(950, 620)

    def createFirstExclusiveGroup(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Temperatury"))

        l1 = QtGui.QLabel(_fromUtf8("Temperatura początkowa pomieszczenia (°C)"))
        self.temp_pom = QtGui.QDoubleSpinBox()
        self.temp_pom.setValue(25)
        l2 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz budynku (°C)"))
        self.temp_out = QtGui.QDoubleSpinBox()
        self.temp_out.setValue(15)
        self.temp_out.setRange(-50, 50)
        l3 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz pomieszczenia (°C)"))
        self.temp_in = QtGui.QDoubleSpinBox()
        self.temp_in.setValue(20)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.temp_pom)
        vbox.addWidget(l2)
        vbox.addWidget(self.temp_out)
        vbox.addWidget(l3)
        vbox.addWidget(self.temp_in)
        vbox.addStretch(1)

        groupBox.setLayout(vbox)

        return groupBox

    def createSecondExclusiveGroup(self):
        self.klimatyzacja.setCheckable(True)
        self.klimatyzacja.setChecked(False)

        l1 = QtGui.QLabel(_fromUtf8("Temperatura powietrza klimatyzacji (°C)"))
        self.temp_pow = QtGui.QDoubleSpinBox()
        self.temp_pow.setValue(20)
        self.temp_pow.setRange(0, 30)
        l2 = QtGui.QLabel(_fromUtf8("Przepływ powietrza (m3/h)"))
        self.przeplyw = QtGui.QDoubleSpinBox()
        self.przeplyw.setValue(300.0)
        self.przeplyw.setRange(100, 1000)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.temp_pow)
        vbox.addWidget(l2)
        vbox.addWidget(self.przeplyw)
        vbox.addStretch(1)
        self.klimatyzacja.setLayout(vbox)

        return self.klimatyzacja

    def createNonExclusiveGroup(self):
        self.grzejnik.setCheckable(True)
        self.grzejnik.setChecked(False)

        l1 = QtGui.QLabel(_fromUtf8("Wydajność cieplna grzejnika"))
        self.wydajnosc = QtGui.QDoubleSpinBox()
        self.wydajnosc.setValue(1000.0)
        self.wydajnosc.setRange(200, 2000)

        # l2 = QtGui.QLabel(_fromUtf8("Maksymalna temperatura"))
        # self.max_temp = QtGui.QDoubleSpinBox()
        # self.max_temp.setValue(20)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.wydajnosc)
        # vbox.addWidget(l2)
        # vbox.addWidget(self.max_temp)
        vbox.addStretch(1)
        self.grzejnik.setLayout(vbox)

        return self.grzejnik

    def createPushButtonGroup(self):
        groupBox = QtGui.QGroupBox("Charakterystyka pomieszczenia")

        l1 = QtGui.QLabel(_fromUtf8("Wysokość"))
        self.wys = QtGui.QDoubleSpinBox()
        self.wys.setValue(3)  # jesli metry
        l2 = QtGui.QLabel(_fromUtf8("Szerokość"))
        self.szer = QtGui.QDoubleSpinBox()
        self.szer.setValue(5)
        l4 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        self.sciany_zew_szer = QtGui.QDoubleSpinBox()
        self.sciany_zew_szer.setRange(0, 2)
        self.sciany_zew_szer.setValue(0)
        l3 = QtGui.QLabel(_fromUtf8("Długość"))
        self.dlug = QtGui.QDoubleSpinBox()
        self.dlug.setValue(5)
        l5 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        self.sciany_zew_dlug = QtGui.QDoubleSpinBox()
        self.sciany_zew_dlug.setRange(0, 2)
        self.sciany_zew_dlug.setValue(0)


        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.wys)
        vbox.addWidget(l2)
        vbox.addWidget(self.szer)
        vbox.addWidget(l4)
        vbox.addWidget(self.sciany_zew_szer)
        vbox.addWidget(l3)
        vbox.addWidget(self.dlug)
        vbox.addWidget(l5)
        vbox.addWidget(self.sciany_zew_dlug)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createSciany(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Ściany"))

        # l1 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        # self.zew.setValue(1)
        l2 = QtGui.QLabel(_fromUtf8("Grubość ścian zewnętrznych"))
        self.gr_zew = QtGui.QDoubleSpinBox()
        self.gr_zew.setValue(0.4)
        self.gr_zew.setRange(0.1, 2)
        # TODO jaka jednostka
        l3 = QtGui.QLabel(_fromUtf8("Grubość ścian wewnętrznych"))
        self.gr_wew = QtGui.QDoubleSpinBox()
        self.gr_wew.setValue(0.15)
        self.gr_wew.setRange(0.1, 2)
        # TODO jaka jednostka
        vbox = QtGui.QVBoxLayout()
        # vbox.addWidget(l1)
        # vbox.addWidget(self.zew)
        vbox.addWidget(l2)
        vbox.addWidget(self.gr_zew)
        vbox.addWidget(l3)
        vbox.addWidget(self.gr_wew)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createOkna(self):
        scrollArea = QtGui.QScrollArea()
        groupBox = QtGui.QGroupBox("Okna")
        scrollArea.setWidget(groupBox)
        scrollArea.setWidgetResizable(True)

        # self.dodaj_o()
        dodaj_okno = QtGui.QPushButton("Dodaj okno")

        self.vbox1.addWidget(dodaj_okno)

        dodaj_okno.clicked.connect(self.dodaj_o)
        groupBox.setLayout(self.vbox1)
        return scrollArea

    def createLista(self):
        lista = QtGui.QComboBox()
        lista.addItem(_fromUtf8("N"))
        lista.addItem(_fromUtf8("N-E"))
        lista.addItem(_fromUtf8("E"))
        lista.addItem(_fromUtf8("S-E"))
        lista.addItem(_fromUtf8("S"))
        lista.addItem(_fromUtf8("S-W"))
        lista.addItem(_fromUtf8("W"))
        lista.addItem(_fromUtf8("N-W"))
        return lista

    def dodaj_o(self):
        hbox = QtGui.QHBoxLayout()
        l1 = QtGui.QLabel(_fromUtf8("Natężenie promieniowania słonecznego:"))
        l2 = QtGui.QLabel(_fromUtf8("Szerokość:"))
        l3 = QtGui.QLabel(_fromUtf8("Wysokość:"))
        nat = QtGui.QDoubleSpinBox()
        nat.setRange(0, 2000)
        nat.setValue(500)
        szer = QtGui.QDoubleSpinBox()
        wys = QtGui.QDoubleSpinBox()

        hbox.addWidget(l1)
        # lista = self.createLista()
        # hbox.addWidget(lista)
        hbox.addWidget(nat)
        hbox.addWidget(l2)
        hbox.addWidget(szer)
        hbox.addWidget(l3)
        hbox.addWidget(wys)
        o = okno(wys, szer, nat)
        self.lista_wys_okien.append(o)
        print(self.lista_wys_okien.__len__())

        groupBox2 = QtGui.QGroupBox()
        groupBox2.setLayout(hbox)
        self.vbox1.addWidget(groupBox2)
        return hbox

    def create_persons(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Osoby"))

        l = QtGui.QLabel(_fromUtf8("Liczba osób"))
        self.liczba_osob = QtGui.QSpinBox()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l)
        vbox.addWidget(self.liczba_osob)
        groupBox.setLayout(vbox)
        self.vbox1.addWidget(groupBox)

        return groupBox

    def solve(self):
        buttonSolve = QtGui.QPushButton(_fromUtf8("Rozwiąż równanie"))
        buttonSolve.clicked.connect(self.solveEquation)
        return buttonSolve

    def solveEquation(self):
        # mk = self.przeplyw.value() / 3600  # podawany w m3/h, przeliczenie na sekundy
        mk = self.przeplyw.value() / 3600
        Tk = self.temp_pow.value()
        Tp = self.temp_pom.value()
        V = self.wys.value() * self.szer.value() * self.dlug.value()
        d = 1.29  # kg/m^3
        c = 1000000
        Qg = self.wydajnosc.value()
        Np = self.liczba_osob.value()  # osób w pokoju
        k = 0.5  # W/m*stopień celsjusza
        hi = self.gr_zew.value()
        hl = self.gr_wew.value()
        To = self.temp_in.value()
        Ai = self.sciany_zew_dlug.value() * self.dlug.value() * self.wys.value() + self.sciany_zew_szer.value() * self.szer.value() * self.wys.value()
        Al = (2 - self.sciany_zew_dlug.value()) * self.dlug.value() * self.wys.value() + (2 - self.sciany_zew_szer.value()) * self.szer.value() * self.wys.value()
        Tow = self.temp_out.value()
        R = 0.96  # W/m*st celsjusza
        G = 0  # TODO dodac
        i = self.zew.value()
        okna = self.lista_wys_okien
        print(V)
        solver = abcd(mk, Tk, Tp, V, d, c, Qg, Np, k, hi, hl, To, Ai, Al, Tow, R, G, self.klimatyzacja.isChecked(), self.grzejnik.isChecked(), i, okna)
        print(solver.f(Tp, self.klimatyzacja.isChecked(), self.grzejnik.isChecked()))
        print (solver.oknna)

        u = newWind(solver)
        u.setupUi()
        u.show()
        u.exec_()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
