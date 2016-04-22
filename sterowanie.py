from PyQt4 import QtCore
from math import ceil

class sterowanie():


    def __init__(self, solver,window):
        self.solver=solver
        self.window=window
        self.roznica=0.5 #stopnie celsjusza - taka roznica powoduje klimatyzacje
        self.temperatury=[]
        self.temperaturyCh=[] #temperatury powodujace chlodzenie, czyli za wysokie
        self.temperaturyGrz=[] # -..- grzanie, czyli za niskie


    def podejmijDecyzje(self,tempAktualna,tempZadana):
        self.temperatury.append(tempAktualna)
        print(self.temperatury)
        if (tempAktualna<tempZadana):
            if (self.solver.if_heat==False):
                self.window.grzejnik.setChecked(True)
                self.window.update(self.window.grzejnik,True)

            if (self.solver.if_cool==True):
                self.window.klimatyzacja.setChecked(False)
                self.window.update(self.window.klimatyzacja,False)

            # poziom=ceil((tempZadana-self.window.temperaturaMin.value())/self.window.roznice.value())+1 #bo poziom 1=temp min grzejnika
            # if (poziom>self.window.poziomy.value()):
            #     poziom=self.window.poziomy.value()

            # if (int(self.window.poziomGrzania.currentText())!=poziom):
            #     id=self.window.poziomGrzania.findText(str(poziom),QtCore.Qt.MatchFixedString)
            #     self.window.poziomGrzania.setCurrentIndex(id)
            #     self.window.update(self.window.poziomGrzania,poziom)

                #self.window.changedPoziom(poziom)

            #print("heating")
        if (tempAktualna>tempZadana):
            #sprawdzamy 2 ostatnie temperatury; jesli obie są ponad zadaną i 2 od końca jest mniejsza od ostatniej o "różnicę"
            #to chłodzimy
            if (len(self.temperatury)>1 and self.temperatury[-1]>tempZadana and self.temperatury[-2]>tempZadana and
                        self.temperatury[-2]<self.temperatury[-1]+self.roznica):
                self.temperaturyCh.append(tempAktualna)
            # w liscie element -2 oznacza 2 drugi od końca
            #sprawdzamy czy 2 ostatnie temperatury różnią się o więcej niż różnicę, jeśli nie to włączamy klimatyzację
                if (len(self.temperaturyCh)>1 and self.temperaturyCh[-2]<self.temperaturyCh[-1]+self.roznica):
                    self.window.update(self.window.temp_pow, self.window.temp_pow.value()-1)
                if (self.solver.if_cool==False):
                    self.window.update(self.window.klimatyzacja,True)
                    #self.window.klimatyzacja.setChecked(True)
                if (self.solver.if_heat==True):
                    self.window.update(self.window.grzejnik,False)
                    #self.window.grzejnik.setChecked(False)
            print("cooling")