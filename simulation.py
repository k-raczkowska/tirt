
from controlling import controlling
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class simulation(QtGui.QDialog):

    temperatureControl=False

    def __init__(self, solver, parent=None):
        super(simulation, self).__init__()
        self.parent=parent
        self.text = QtGui.QTextBrowser()
        self.stopButton = QtGui.QPushButton("Stop")
        self.timer = QTimer(self)
        self.solver = solver
        self.time=(datetime.datetime.now().hour)
        self.connect(self,QtCore.SIGNAL("rejected()"),self.stop)

    def setupUi(self):

        grid = QtGui.QGridLayout()
        grid.addWidget(self.text, 0, 0)
        grid.addWidget(self.stopButton, 1, 0)

        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.doSolving)
        self.connect(self.stopButton, QtCore.SIGNAL("clicked()"), self.stop)
        self.start()

        self.setLayout(grid)
        self.setWindowTitle("Symulacja temperatury")
        self.resize(600, 600)

    def doSolving(self):

        self.solver.solve(self.solver.if_cool, self.solver.if_heat)
        self.text.append("--------------------------------------------------------------------------"
                         "\nGodzina " +str(self.time)+":  "+ str(round(self.solver.result, 2)))

        if (self.temperatureControl==True):
            desiredTemp=self.checkForDesiredTemp()
            self.text.append("Temeratura pożądana: "+str(desiredTemp)+"\n")
            self.tempControlling.chooseAction(self.solver.Tp, desiredTemp)

        self.time=(self.time+1)%24
        self.solver.Tp = self.solver.result

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start(1000)

    def setDesiredTemperature(self, temperature):

        self.desiredTemperature=temperature
        self.temperatureControl=True
        self.tempControlling=controlling(self.solver, self.parent)

    def checkForDesiredTemp (self):

        dayStart=self.parent.dayStartingHour.value()
        dayEnd=self.parent.dayEndingHour.value()

        if (dayStart<dayEnd):
            if (self.time>=dayStart and self.time<=dayEnd):
                temperature=self.parent.dailyTemperature.value()
            else:
                temperature=self.parent.nightTemperature.value()

        else:
            if (self.time>=dayEnd and self.time<=dayStart):
                temperature=self.parent.nightTemperature.value()
            else:
                temperature=self.parent.dailyTemperature.value()

        return temperature

