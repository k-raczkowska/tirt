from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class newWind(QtGui.QDialog):
    x=0
    y=0
    def __init__(self, solver,parent=None):
        super(newWind, self).__init__(parent)
        self.solver=solver

    def setupUi(self):
        grid = QtGui.QGridLayout()
        self.text=QtGui.QTextBrowser()
        grid.addWidget(self.text, 0, 0)
        self.btn=QtGui.QPushButton("Stop")
        grid.addWidget(self.btn,1,0)

        self.timer=QTimer(self)
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.doSolving)
        self.connect(self.btn,QtCore.SIGNAL("clicked()"),self.stop)
        # self.btn.clicked.connect(self.solveEquation)
        self.start()

        print("hi")
        self.setLayout(grid)
        self.setWindowTitle("Temperatura")
        self.resize(600, 600)

    def doSolving(self):
        self.solver.solve(self.x,self.y)
        self.text.append("\n"+str(self.solver.Tp))

    def stop(self):
        self.timer.stop()

    def start(self): #chcialem tez zrobic wznawianie ale za duzo kombinacji
        self.timer.start()


