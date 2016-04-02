from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class newWind(QtGui.QDialog):
    x = 0
    y = 0

    def __init__(self, solver, parent=None):
        super(newWind, self).__init__(parent)
        self.text = QtGui.QTextBrowser()
        self.btn = QtGui.QPushButton("Stop")
        self.timer = QTimer(self)
        self.solver = solver

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
        self.text.append("\n" + str(round(x + self.solver.result, 1)))
        self.solver.Tp = self.solver.result + x

    def stop(self):
        self.timer.stop()

    def start(self):  # chcialem tez zrobic wznawianie ale za duzo kombinacji
        self.timer.start(1000)
