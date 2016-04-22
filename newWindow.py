from sterowanie import sterowanie
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class newWind(QtGui.QDialog):
    x = 0
    y = 0
    sterowanie=False
    def __init__(self, solver, parent=None):
        super(newWind, self).__init__()
        self.parent=parent
        self.text = QtGui.QTextBrowser()
        self.btn = QtGui.QPushButton("Stop")
        self.timer = QTimer(self)
        self.solver = solver
        self.time=(datetime.datetime.now().hour)
        self.connect(self,QtCore.SIGNAL("rejected()"),self.stop)

    def setupUi(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.text, 0, 0)
        grid.addWidget(self.btn, 1, 0)

        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.doSolving)
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.stop)
        # self.btn.clicked.connect(self.solveEquation)
        self.start()

        self.setLayout(grid)
        self.setWindowTitle("Temperatura")
        self.resize(600, 600)

    def doSolving(self):
        x = self.solver.solve(self.solver.if_cool, self.solver.if_heat)
        self.text.append("\nGodzina " +str(self.time)+":  "+ str(round(self.solver.Tp, 3)))

        #self.solver.Tp = self.solver.result
        if (self.sterowanie==True):
            temperatura=self.sprawdzKtoraTemperaturaObecnie()
            self.text.append("teraz temperatura: "+str(temperatura))
            self.classSterowanie.podejmijDecyzje(self.solver.Tp,temperatura)
        self.time=(self.time+1)%24

    def stop(self):
        self.timer.stop()

    def start(self):  # chcialem tez zrobic wznawianie ale za duzo kombinacji
        self.timer.start(1000)

    def setTempWymagana(self, temperatura):
        self.temperaturaWymagana=temperatura
        self.sterowanie=True
        self.classSterowanie=sterowanie(self.solver,self.parent)

    def sprawdzKtoraTemperaturaObecnie (self):

        czasOd=self.parent.czas_dzien_od.value()
        czasDo=self.parent.czas_dzien_do.value()

        if (czasOd<czasDo): # typu dzien jest od godz 5 do 17
            if (self.time>=czasOd and self.time<=czasDo):
                temp=self.parent.temperatura_dzienna.value()
            else:
                temp=self.parent.temperatura_nocna.value()

        else: # a tutaj np od godziny 5 do 1 w nocy
            if (self.time>=czasDo and self.time<=czasOd):
                temp=self.parent.temperatura_nocna.value()
            else:
                temp=self.parent.temperatura_dzienna.value()

        return temp

