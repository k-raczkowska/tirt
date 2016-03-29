# coding=utf-8
from PyQt4 import QtCore, QtGui
from equations import abcd
from newWindow import newWind


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Window(QtGui.QWidget):
    vbox1 = QtGui.QVBoxLayout()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        grid.addWidget(self.createPushButtonGroup(), 1, 1)
        grid.addWidget(self.createSciany(), 2, 0)
        grid.addWidget(self.createOkna(), 2, 1)
        grid.addWidget(self.solve(),3,1)

        self.setLayout(grid)

        self.setWindowTitle("Modelowanie temperatury pomieszczenia")
        self.resize(700, 520)

    def createFirstExclusiveGroup(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Temperatury"))

        l1 = QtGui.QLabel(_fromUtf8("Temperatura początkowa pomieszczenia"))
        self.temp_pom = QtGui.QDoubleSpinBox()
        self.temp_pom.setValue(25)
        l2 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz budynku"))
        self.temp_out = QtGui.QDoubleSpinBox()
        self.temp_out.setValue(15)
        self.temp_out.setRange(-50,50)
        l3 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz pomieszczenia"))
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
        groupBox = QtGui.QGroupBox("Klimatyzacja")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        l1 = QtGui.QLabel("Temperatura powietrza klimatyzacji")
        self.temp_pow = QtGui.QDoubleSpinBox()
        self.temp_pow.setValue(10)
        l2 = QtGui.QLabel(_fromUtf8("Przepływ powietrza"))
        self.przeplyw = QtGui.QDoubleSpinBox()
        self.przeplyw.setValue(5.0)
        #TODO jaka jednostka?


        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.temp_pow)
        vbox.addWidget(l2)
        vbox.addWidget(self.przeplyw)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createNonExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("Grzejnik")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        l1 = QtGui.QLabel(_fromUtf8("Wydajność cieplna grzejnika"))
        self.wydajnosc = QtGui.QDoubleSpinBox()
        self.wydajnosc.setValue(5.0)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.wydajnosc)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QtGui.QGroupBox("Charakterystyka pomieszczenia")

        l1 = QtGui.QLabel(_fromUtf8("Wysokość"))
        self.wys = QtGui.QDoubleSpinBox()
        self.wys.setValue(4) #jesli metry
        l2 = QtGui.QLabel(_fromUtf8("Szerokość"))
        self.szer = QtGui.QDoubleSpinBox()
        self.szer.setValue(5)
        l3 = QtGui.QLabel(_fromUtf8("Długość"))
        self.dlug = QtGui.QDoubleSpinBox()
        self.dlug.setValue(5)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.wys)
        vbox.addWidget(l2)
        vbox.addWidget(self.szer)
        vbox.addWidget(l3)
        vbox.addWidget(self.dlug)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createSciany(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Ściany"))

        l1 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        self.zew = QtGui.QSpinBox()
        self.zew.setValue(4)
        l2 = QtGui.QLabel(_fromUtf8("Grubość ścian zewnętrznych"))
        self.gr_zew = QtGui.QDoubleSpinBox()
        self.gr_zew.setValue(4.0)
        #TODO jaka jednostka
        l3 = QtGui.QLabel(_fromUtf8("Grubość ścian wewnętrznych"))
        self.gr_wew = QtGui.QDoubleSpinBox()
        self.gr_wew.setValue(5.0)
        #TODO jaka jednostka
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(self.zew)
        vbox.addWidget(l2)
        vbox.addWidget(self.gr_zew)
        vbox.addWidget(l3)
        vbox.addWidget(self.gr_wew)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createOkna(self):

        scrollArea= QtGui.QScrollArea()
        groupBox = QtGui.QGroupBox("Okna")
        scrollArea.setWidget(groupBox)
        scrollArea.setWidgetResizable(True)

        self.dodaj_o()
        dodaj_okno = QtGui.QPushButton("Dodaj okno")

        self.vbox1.addWidget(dodaj_okno)

        dodaj_okno.clicked.connect(self.dodaj_o)
        groupBox.setLayout(self.vbox1)
        return scrollArea

    def createLista(self):
        lista = QtGui.QComboBox()
        lista.addItem(_fromUtf8("Północ"))
        lista.addItem(_fromUtf8("Północny wschód"))
        lista.addItem(_fromUtf8("Wschód"))
        lista.addItem(_fromUtf8("Południowy wschód"))
        lista.addItem(_fromUtf8("Południe"))
        lista.addItem(_fromUtf8("Południowy zachód"))
        lista.addItem(_fromUtf8("Zachód"))
        lista.addItem(_fromUtf8("Połnocny zachód"))
        return lista

    def dodaj_o(self):
        hbox=QtGui.QHBoxLayout()
        l1=QtGui.QLabel("Położenie:")
        l2=QtGui.QLabel("Szerokość:")
        l3=QtGui.QLabel("Wysokość:")
        szer=QtGui.QDoubleSpinBox()
        wys=QtGui.QDoubleSpinBox()

        hbox.addWidget(l1)
        hbox.addWidget(self.createLista())
        hbox.addWidget(l2)
        hbox.addWidget(szer)
        hbox.addWidget(l3)
        hbox.addWidget(wys)

        groupBox2=QtGui.QGroupBox()
        groupBox2.setLayout(hbox)
        self.vbox1.addWidget(groupBox2)
        return hbox

    def solve(self):
        buttonSolve=QtGui.QPushButton("Rozwiąż równanie")
        buttonSolve.clicked.connect(self.solveEquation)
        return buttonSolve

    def solveEquation(self):
        mk=self.przeplyw.value()
        Tk=self.temp_pow.value()
        Tp=self.temp_pom.value()
        V=self.wys.value()*self.szer.value()*self.dlug.value()
        d=1.29 #kg/m^3
        c=1013 #hPa
        Qg=self.wydajnosc.value()
        Np=5  #osób w pokoju
        k=0.5 #W/m*stopień celsjusza
        hi=self.gr_zew.value()
        hl=self.gr_wew.value()
        To=self.temp_in.value()
        Ai=0 #TODO dodac parametry
        Al=0 #TODO dodac
        Tow=self.temp_out.value()
        R=0.96 #W/m*st celsjusza
        G=0 #TODO dodac
        print(V)
        solver=abcd(mk,Tk,Tp,V,d,c,Qg,Np,k,hi,hl,To,Ai,Al,Tow,R,G)

        u=newWind(solver)
        u.setupUi()
        u.show()
        u.exec_()








if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())