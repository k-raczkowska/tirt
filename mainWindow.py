# coding=utf-8
from PyQt4 import QtCore, QtGui
from equations import solver
from simulation import simulation
from windowsSize import windowSize

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Window(QtGui.QWidget):
    vbox = QtGui.QVBoxLayout()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self, parent=None):

        super(Window, self).__init__(parent)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.createGroupTemperatures(), 0, 0)
        grid.addWidget(self.createGroupAirConditioning(), 0, 1)
        grid.addWidget(self.createGroupRadiator(), 0, 2)
        grid.addWidget(self.createGroupRoom(), 1, 0)
        grid.addWidget(self.createGroupWindows(), 1, 1)
        grid.addWidget(self.createGroupTemperatureControl(), 1, 2)
        grid.addWidget(self.createGroupWalls(), 2, 0)
        grid.addWidget(self.createGroupPeople(), 2, 1)
        grid.addWidget(self.solve(), 2, 2)

        self.setLayout(grid)
        self.setWindowTitle("Modelowanie temperatury pomieszczenia")

    def createGroupTemperatures(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Temperatury"))

        lab1 = QtGui.QLabel(_fromUtf8("Temperatura początkowa pomieszczenia (°C)"))
        self.temp_room = QtGui.QDoubleSpinBox()
        self.temp_room.setValue(25)
        lab2 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz budynku (°C)"))
        self.temp_out = QtGui.QDoubleSpinBox()
        self.temp_out.setValue(15)
        self.temp_out.setRange(-50, 50)
        lab3 = QtGui.QLabel(_fromUtf8("Temperatura na zewnątrz pomieszczenia (°C)"))
        self.temp_adjacent = QtGui.QDoubleSpinBox()
        self.temp_adjacent.setValue(20)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lab1)
        vbox.addWidget(self.temp_room)
        vbox.addWidget(lab2)
        vbox.addWidget(self.temp_out)
        vbox.addWidget(lab3)
        vbox.addWidget(self.temp_adjacent)
        vbox.addStretch(1)

        groupBox.setLayout(vbox)
        return groupBox

    def createGroupAirConditioning(self):

        self.airConditioner = QtGui.QGroupBox("Klimatyzacja")
        self.airConditioner.setCheckable(True)
        self.airConditioner.setChecked(False)

        grid=QtGui.QGridLayout()
        labTempMin=QtGui.QLabel("Temperatura minimalna")
        labTempMax=QtGui.QLabel("Temperatura maksymalna")

        self.spBoxConditionerTempMin=QtGui.QDoubleSpinBox()
        self.spBoxConditionerTempMin.setValue(4)
        self.spBoxConditionerTempMin.valueChanged.connect(self.setMin)
        self.spBoxConditionerTempMax=QtGui.QDoubleSpinBox()
        self.spBoxConditionerTempMax.setValue(32)
        self.spBoxConditionerTempMax.valueChanged.connect(self.setMax)

        grid.addWidget(labTempMin,0,0)
        grid.addWidget(labTempMax,0,1)
        grid.addWidget(self.spBoxConditionerTempMin, 1, 0)
        grid.addWidget(self.spBoxConditionerTempMax, 1, 1)

        lab1 = QtGui.QLabel(_fromUtf8("Przepływ powietrza (m3/h)"))
        self.airConditionerFlowRate = QtGui.QDoubleSpinBox()
        self.airConditionerFlowRate.setRange(100, 3000)
        self.airConditionerFlowRate.setValue(1000.0)

        lab2 = QtGui.QLabel(_fromUtf8("Temperatura powietrza klimatyzacji (°C)"))
        self.airConditionerTemp = QtGui.QDoubleSpinBox()
        self.airConditionerTemp.setValue(20)
        self.airConditionerTemp.setRange(self.spBoxConditionerTempMin.value(), self.spBoxConditionerTempMax.value())

        vbox = QtGui.QVBoxLayout()
        vbox.addItem(grid)
        vbox.addWidget(lab2)
        vbox.addWidget(self.airConditionerFlowRate)
        vbox.addStretch(1)

        vbox.addWidget(lab1)
        vbox.addWidget(self.airConditionerTemp)

        self.airConditioner.setLayout(vbox)
        return self.airConditioner

    def setMin(self,value):
        self.airConditionerTemp.setMinimum(value)

    def setMax(self, value):
        self.airConditionerTemp.setMaximum(value)

    def createGroupRadiator(self):

        self.radiator = QtGui.QGroupBox("Grzejnik")
        self.radiator.setCheckable(True)
        self.radiator.setChecked(False)

        label = QtGui.QLabel(_fromUtf8("Wydajność cieplna grzejnika (W)"))
        self.radiatorEfficiency = QtGui.QDoubleSpinBox()
        self.radiatorEfficiency.setRange(0, 2000)
        self.radiatorEfficiency.setValue(2000.0)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.radiatorEfficiency)
        vbox.addStretch(1)

        self.radiator.setLayout(vbox)
        return self.radiator

    def createGroupRoom(self):
        groupBox = QtGui.QGroupBox("Charakterystyka pomieszczenia")

        lab1 = QtGui.QLabel(_fromUtf8("Wysokość"))
        self.roomHeight = QtGui.QDoubleSpinBox()
        self.roomHeight.setValue(3)
        lab2 = QtGui.QLabel(_fromUtf8("Szerokość"))
        self.roomWidth = QtGui.QDoubleSpinBox()
        self.roomWidth.setValue(5)
        lab3 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        self.exteriorWallsNumber = QtGui.QDoubleSpinBox()
        self.exteriorWallsNumber.setRange(0, 2)
        self.exteriorWallsNumber.setValue(0)
        lab4 = QtGui.QLabel(_fromUtf8("Długość"))
        self.roomDepth = QtGui.QDoubleSpinBox()
        self.roomDepth.setValue(5)
        lab5 = QtGui.QLabel(_fromUtf8("Liczba ścian zewnętrznych"))
        self.exteriorWallsNumberDepth = QtGui.QDoubleSpinBox()
        self.exteriorWallsNumberDepth.setRange(0, 2)
        self.exteriorWallsNumberDepth.setValue(0)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lab1)
        vbox.addWidget(self.roomHeight)
        vbox.addWidget(lab2)
        vbox.addWidget(self.roomWidth)
        vbox.addWidget(lab3)
        vbox.addWidget(self.exteriorWallsNumber)
        vbox.addWidget(lab4)
        vbox.addWidget(self.roomDepth)
        vbox.addWidget(lab5)
        vbox.addWidget(self.exteriorWallsNumberDepth)
        vbox.addStretch(1)

        groupBox.setLayout(vbox)
        return groupBox

    def createGroupWalls(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Ściany"))

        lab1 = QtGui.QLabel(_fromUtf8("Grubość ścian zewnętrznych"))
        self.externalWallThickness = QtGui.QDoubleSpinBox()
        self.externalWallThickness.setValue(0.4)
        self.externalWallThickness.setRange(0.1, 2)

        lab2 = QtGui.QLabel(_fromUtf8("Grubość ścian wewnętrznych"))
        self.internalWallThickness = QtGui.QDoubleSpinBox()
        self.internalWallThickness.setValue(0.15)
        self.internalWallThickness.setRange(0.1, 2)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lab1)
        vbox.addWidget(self.externalWallThickness)
        vbox.addWidget(lab2)
        vbox.addWidget(self.internalWallThickness)
        vbox.addStretch(1)

        groupBox.setLayout(vbox)
        return groupBox

    def createGroupWindows(self):
        self.windowsList = []
        scrollArea = QtGui.QScrollArea()
        groupBox = QtGui.QGroupBox("Okna")

        scrollArea.setWidget(groupBox)
        scrollArea.setWidgetResizable(True)

        buttonNewWindow = QtGui.QPushButton("Dodaj okno")

        box=QtGui.QHBoxLayout()
        box.addWidget(buttonNewWindow)
        box.addStretch(1)

        self.vbox.addLayout(box)
        self.vbox.addStretch(1)

        buttonNewWindow.clicked.connect(self.addRowWindow)
        groupBox.setLayout(self.vbox)
        return scrollArea


    def addRowWindow(self):

        grid = QtGui.QGridLayout()
        lab1 = QtGui.QLabel(_fromUtf8("Natężenie promieniowania słonecznego:"))
        lab2 = QtGui.QLabel(_fromUtf8("Szerokość:"))
        lab3 = QtGui.QLabel(_fromUtf8("Wysokość:"))
        solarRadiation = QtGui.QDoubleSpinBox()
        solarRadiation.setRange(0, 2000)
        solarRadiation.setValue(500)
        width = QtGui.QDoubleSpinBox()
        width.setValue(0.5)
        height = QtGui.QDoubleSpinBox()
        height.setValue(0.4)

        grid.addWidget(lab1,0,0)
        grid.addWidget(solarRadiation, 1, 0)
        grid.addWidget(lab2,0,1)
        grid.addWidget(width,1,1)
        grid.addWidget(lab3,0,2)
        grid.addWidget(height,1,2)
        window = windowSize(height, width, solarRadiation)
        self.windowsList.append(window)

        groupBox = QtGui.QGroupBox()
        groupBox.setLayout(grid)
        self.vbox.addWidget(groupBox)
        return grid

    def createGroupPeople(self):
        groupBox = QtGui.QGroupBox(_fromUtf8("Osoby"))

        label = QtGui.QLabel(_fromUtf8("Liczba osób"))
        self.peopleNumber = QtGui.QSpinBox()

        vbox = QtGui.QFormLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.peopleNumber)
        groupBox.setLayout(vbox)

        self.vbox.addWidget(groupBox)
        return groupBox

    def solve(self):

        buttonSolve = QtGui.QPushButton(_fromUtf8("Rozwiąż równanie"))
        buttonSolve.clicked.connect(self.solveEquation)

        return buttonSolve

    def createGroupTemperatureControl(self):

        #initiate elements

        self.temperatureControl =QtGui.QGroupBox(_fromUtf8("Sterowanie"))
        self.temperatureControl.setCheckable(True)
        self.temperatureControl.setChecked(False)

        lab1=QtGui.QLabel(_fromUtf8("Temperatura na dzień"))
        self.dailyTemperature = QtGui.QSpinBox()
        self.dailyTemperature.setValue(20)

        lab2=QtGui.QLabel(_fromUtf8("Temperatura na noc"))
        self.nightTemperature=QtGui.QSpinBox()
        self.nightTemperature.setValue(18)

        lab31=QtGui.QLabel(_fromUtf8("Od"))
        self.dayStartingHour=QtGui.QSpinBox()
        self.dayStartingHour.setValue(5)
        lab32=QtGui.QLabel(_fromUtf8("Do"))
        self.dayEndingHour=QtGui.QSpinBox()
        self.dayEndingHour.setValue(18)

        lab41=QtGui.QLabel(_fromUtf8("Od"))
        self.nightStartingHour=QtGui.QSpinBox()
        self.nightStartingHour.setValue(18)
        lab42=QtGui.QLabel(_fromUtf8("Do"))
        self.nightEndingHour=QtGui.QSpinBox()
        self.nightEndingHour.setValue(5)

        #add elements to layouts

        lay1=QtGui.QHBoxLayout()
        lay1=self.addToLayout(lay1,lab1)
        lay1=self.addToLayout(lay1,self.dailyTemperature)

        lay2=QtGui.QHBoxLayout()
        lay2=self.addToLayout(lay2,lab2)
        lay2=self.addToLayout(lay2,self.nightTemperature)

        lay3=QtGui.QHBoxLayout()
        lay3=self.addToLayout(lay3,lab31)
        lay3=self.addToLayout(lay3,self.dayStartingHour)
        lay3=self.addToLayout(lay3,lab32)
        lay3=self.addToLayout(lay3,self.dayEndingHour)

        lay4=QtGui.QHBoxLayout()
        lay4=self.addToLayout(lay4,lab41)
        lay4=self.addToLayout(lay4,self.nightStartingHour)
        lay4=self.addToLayout(lay4,lab42)
        lay4=self.addToLayout(lay4,self.nightEndingHour)

        #create a form layout containing newly created layouts

        finalLayout=QtGui.QFormLayout()
        finalLayout.addItem(lay1)
        finalLayout.addItem(lay3)
        finalLayout.addItem(lay2)
        finalLayout.addItem(lay4)

        self.dayStartingHour.valueChanged.connect(self.changedDayStartHour)
        self.dayEndingHour.valueChanged.connect(self.changedDayEndHour)

        self.temperatureControl.setLayout(finalLayout)
        return self.temperatureControl

    def addToLayout (self, layout, element):
        layout.addWidget(element)
        layout.addStretch(1)
        return layout

    def changedDayEndHour(self):
        self.nightStartingHour.setValue(self.dayEndingHour.value())

    def changedDayStartHour(self):
        self.nightEndingHour.setValue(self.dayStartingHour.value())

    def solveEquation(self):

        #constants
        d = 1.29  # kg/m^3
        c = 1000 # kJ/kg*K
        k = 0.5  # W/m*degrees Celsius
        R = 0.96  # W/m*degrees Celsius
        i = 2 # number of walls inside room in 1 direction; 2*i is total number of walls
        TG = 80 #constant connected to room equipment for an ordinary house

        mk = self.airConditionerFlowRate.value() / 60
        Tk = self.airConditionerTemp.value()
        Tin = self.temp_room.value()
        Tadj = self.temp_adjacent.value()
        Tout = self.temp_out.value()

        V = self.roomHeight.value() * self.roomWidth.value() * self.roomDepth.value()

        Qg = self.radiatorEfficiency.value()
        Np = self.peopleNumber.value()

        hi = self.externalWallThickness.value()
        hl = self.internalWallThickness.value()

        Ai = self.exteriorWallsNumberDepth.value() * self.roomDepth.value() * self.roomHeight.value() + self.exteriorWallsNumber.value() * self.roomWidth.value() * self.roomHeight.value()
        Al = (2 - self.exteriorWallsNumberDepth.value()) * self.roomDepth.value() * self.roomHeight.value() + (2 - self.exteriorWallsNumber.value()) * self.roomWidth.value() * self.roomHeight.value()

        windows = self.windowsList
        airCon=self.airConditioner.isChecked()
        radiator=self.radiator.isChecked()

        self.solver = solver(mk, Tk, Tin, V, d, c, Qg, Np, k, hi, hl, Tadj, Ai, Al, Tout, R, airCon,radiator,i,windows,TG)
        self.simulation = simulation(self.solver, self)

        if (self.temperatureControl.isChecked()):
            self.simulation.setDesiredTemperature(self.dailyTemperature.value())

        self.simulation.setupUi()
        self.simulation.show()
        self.simulation.exec_()

    def update(self,widgetChanged,value):

        if (widgetChanged==self.radiator):
            widgetChanged.setChecked(value)
            self.solver.if_heat=value

            if (value==True):
                state="wlaczony"
            else:
                state="wylaczony"

            self.simulation.text.append("Zmiana: Grzejnik został " + state)

        if (widgetChanged == self.airConditionerTemp):
            widgetChanged.setValue(value)
            self.solver.Tk=value
            self.simulation.text.append("Zmiana temperatury klimatyzacji na wartość: " + str(value))

        if (widgetChanged==self.airConditioner):
            widgetChanged.setChecked(value)
            self.solver.if_cool=value

            if (value==True):
                state="wlaczona"
            else:
                state="wylaczona"

            self.simulation.text.append("Zmiana: Klimatyzacja została " + state)



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    clock = Window()
    clock.show()
    clock.center()
    sys.exit(app.exec_())
