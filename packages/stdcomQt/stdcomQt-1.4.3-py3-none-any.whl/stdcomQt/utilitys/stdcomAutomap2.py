import  sys, os

import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QApplication

import stdcomQt

from scipy.interpolate import BSpline, make_interp_spline, UnivariateSpline, CubicSpline


try :
    from stdcomQt.stdcomQtconv import stdcomQtConv as conv
    from stdcomQt.stdcomQtconv import stdcomQtMappingAlgorithm as mp
    from stdcomQt.utilitys.stdcomplot import stdcomplot as plot



except :
    from stdcomQtconv import stdcomQtConv as conv
    from stdcomQtconv import stdcomQtMappingAlgorithm as mp
    from stdcomplot import stdcomplot as plot





import argparse
import time


try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from stdcomQt.stdcomQtPjanice import *
from stdcomQt.stdcomvsettings import *

from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QTabWidget, QTableWidgetItem, QCheckBox, QMainWindow, QListWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent, QObject, QTimer, QFileInfo
from PyQt5.Qt import pyqtSlot, pyqtSignal
from stdcomQt import *

from stdcomQt.stdcomvsettings import *
from stdcomQt.utilitys.stdautomap2 import *
from stdcomQt.utilitys.pjaniceExt import pjanice



class MappingThread(QThread):
    sigOffsets = pyqtSignal(list)

    parameters = None
    numberzones = 96
    numberdataboxes = 500
    first = 10
    last  = 86

    mapA : mp = None
    tauScans = 3
    shift = 0.0

    waitToGo = 50
    timesGone = 0
    usedelta = 0

    algo = conv()

    databoxshapes = np.nan
    actshapes = np.nan

    databoxlist = []
    actlist = []

    def __init__(self,  Parent=None, **kwargs):

        if Parent is not None:
            super().__init__(Parent)
        else:
            super().__init__()

        self.SetMap(**kwargs)
        self.start()


    @pyqtSlot(dict)
    def SetMap(self, **kwargs ):

        if type(kwargs) != dict:
            raise Exception('exceptions  Parameters are needed" ')

        self.numberzones = kwargs.get("numberzones", self.numberzones)
        self.numberdataboxes = kwargs.get("numberdataboxes", self.numberdataboxes)
        self.tauScans = kwargs.get("tauscans", self.tauScans)
        self.usedelta = kwargs.get("usedelta", self.usedelta)
        self.first = kwargs.get('first', self.first)
        self.last =  kwargs.get('last', self.last)
        self.parameters = kwargs
        self.mapA = mp(**kwargs)

    def ActuatorMinusTau(self):
        return self.actshapes

    def DBXMinusTau(self):
        if self.databoxshapes is None:
            return None

        r, c = self.actshapes.shape
        if r >= self.tauScans:
            rawdbx = self.databoxshapes[self.tauScans - 1:, :]
            return rawdbx

        return None

    def GetTauAdj(self):

        try :
            rawdbx = np.array(self.databoxshapes[self.tauScans - 1:, :])
            rdbx, cdbx = rawdbx.shape

            rawactuator = np.array(self.actshapes)

            rawact, rawact = rawactuator.shape

            if rawact > rdbx & rdbx > 2 :
                rawactuator = np.delete(rawactuator,np.s_[rdbx::],axis=0)
            elif rdbx  > rawact & rdbx > 2 :
                rawdbx = np.delete(rawdbx, np.s_[rawact::], axis=0)

            return rawdbx, rawactuator


        except :
            print("Could Not GetTauAdj(self):")


        return np.nam, np.nan

    def DeltaP(self, aArray):
        RowsD, ColsD = aArray.shape
        ba = None
        for i in range(0, RowsD, 2):
            if i + 1 < RowsD:
                s1 = aArray[i][:]
                s2 = aArray[i + 1][:]
                sd = np.subtract(s1, s2)
                if ba is None:
                    ba = sd
                else:
                    ba = np.vstack([ba, sd])
        return ba






    def MappAll(self, steps=1):


        databoxes, actuators = self.GetTauAdj()

        self.shift = self.mapA.autoMap(self.databoxshapes, self.actshapes)

        self.sigOffsets.emit([self.shift] )


    @pyqtSlot(list, list)
    def UpdateProfiles(self, actuators: list, databoxes: list):

        if actuators is None or databoxes is None:
            return

        self.actlist.append(actuators)
        self.databoxlist.append(databoxes)

        rows = len(self.databoxlist)

        if rows >= self.waitToGo:
            self.databoxshapes = np.array(self.databoxlist, dtype=float)
            self.actshapes = np.array(self.actlist, dtype=float)
            self.MappAll()
            self.databoxlist.clear()
            self.actlist.clear()





class StdcomAutomap(QMainWindow):
    sigNewUpdates = pyqtSignal(list, list)
    newParmeters = pyqtSignal(dict)
    proxLock = QMutex()

    pj = None
    cBridge = None


    tauscans = int(3)
    useDelta = "false"
    numberzones = 96
    numberdataboxes = 500
    shift = 0
    first = 10
    last = 90
    filter  = .5
    groups = 10
    reverseProfile = "false"

    partner = "ActuatorZones"
    target =  "ScannerBWProfile"
    targetSub  : Subscriber = None
    partnerSub : Subscriber = None

    targetAutomappedSub: Subscriber = None
    parmeters : {}
    worker: MappingThread = None
    timeofDbx            = None

    actuatorPartnerArray = None
    databoxTargetArray = None


    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_StdcomAutomap()
        self.ui.setupUi(self)
        self.show()

        self.pj = pjanice()
        self.pj.setWindowTitle("PJanice")
        self.cBridge = self.pj.cBridge

        self.ui.action_Exit.triggered.connect(self.OnExit)
        self.ui.actionPJanice.triggered.connect(self.OnPJanice)
        self.ui.actionSave_Configuration.triggered.connect(self.SaveConfig)

        self.LoadConfig()
        self.mapA = mp(**self.parmeters)
        self.worker = MappingThread(**self.parmeters )
        self.newParmeters.connect( self.worker.SetMap)
        self.worker.sigOffsets.connect(self.newOffsets)
        self.sigNewUpdates.connect(self.worker.UpdateProfiles)

        self.offsetplt = plot(self.ui.scrollAreaOffset, {'xunits':"Number Samples ",
                                                         'xname' : "Per Offset Calculation",
                                                         'yunits' : "Zones",
                                                         'yname' :"Center Databox"})


        self.ui.pushButtonSaveTrend.clicked.connect( self.buildCsv)

        self.offsetpltArray = plot(self.ui.scrollAreaOffsetArray, {'xunits':"Sheet Zones",
                                                         'xname' : "Zone Number",
                                                         'yunits' : "Zone Fraction",
                                                         'yname' :"Center Databox"})


        self.offsetpltArrayGroup = plot(self.ui.scrollAreaOffsetArrayGroup, {'xunits':"Spline Sheet Zones",
                                                         'xname' : "Zone Number",
                                                         'yunits' : "Zone Fraction",
                                                         'yname' :"Center Databox"})

        self.splSplineProfile = plot(self.ui.scrollAreaSplineProfile, {'xunits': "AutoMapped Zones",
                                                                             'xname': "Zone Number",
                                                                             'yunits': "Eng Units",
                                                                             'yname': "gsm"})

        self.actuatorProfile = plot(self.ui.scrollAreaActualProfile, {'xunits': "Zones Position",
                                                                             'xname': "Zone Number",
                                                                             'yunits': "Openings",
                                                                             'yname': "open"})
        self.scannerProfile = plot(self.ui.scrollAreaScannerProfile , {'xunits': "Databox Position",
                                                                      'xname': "Databox Number",
                                                                      'yunits': "DWT",
                                                                      'yname': "gsm"})

        self.mappedProfileSpline = plot(self.ui.scrollAreaMappedProfileSpline, {'xunits': "Spline Position",
                                                                      'xname': "Zone Number",
                                                                      'yunits': "DWT",
                                                                      'yname': "gsm"})

        self.scannerProfileSpline = plot(self.ui.scrollAreaScannerProfileSpline, {'xunits': "Spline Databox Position",
                                                                      'xname': "Databox Number",
                                                                      'yunits': "DWT",
                                                                      'yname': "gsm"})


    @pyqtSlot(list)
    def newOffsets(self, offsets):


            return


    @pyqtSlot()
    def CreateParameters( self) :

        usedelta = 0
        if self.useDelta == "true":
            usedelta = 1

        self.parmeters = {'start_s': 1,
                     'numberzones': self.numberzones,
                     'numberdataboxes': self.numberdataboxes,

                     'tauscans': self.tauscans,
                     'usedelta':  usedelta,
                     'first' : self.first,
                     'last' : self.last,
                     'filter': self.filter,
                     }

        self.newParmeters.emit(self.parmeters)


    @pyqtSlot()
    def LoadConfig(self):
        settings = VSettings("Stec.Automap2")

        self.filter = float( settings.value("filter", self.filter ))
        self.ui.doubleSpinBoxSplineFilter.setValue(self.filter)

        self.groups  = int( settings.value("groups", self.groups))
        self.ui.spinBoxGroups.setValue(self.groups)

        self.tauscans =  int(settings.value("tauscans", self.tauscans))
        self.ui.spinBoxtauscans.setValue(self.tauscans)

        self.useDelta = settings.value("usedelta", self.useDelta)

        if self.useDelta == "true" :
            self.ui.checkBoxusedelta.setChecked(True)
        else:
            self.ui.checkBoxusedelta.setChecked(False)

        #............................

        self.numberzones = int( settings.value("numberzones", self.numberzones))
        self.ui.spinBoxActCount.setValue(self.numberzones)

        self.numberdataboxes = int(settings.value("numberdataboxes", self.numberdataboxes))
        self.ui.spinBoxDbxCount.setValue(self.numberdataboxes)

        self.first = int( settings.value( "first", self.first ))
        self.ui.spinBoxFirstGoodDBX.setValue(self.first)

        self.last = int(settings.value("last", self.last))
        self.ui.spinBoxLastGoodDBX.setValue(self.last)

        self.reverseProfile = str(settings.value("reverseprofile", self.reverseProfile))

        if self.reverseProfile == "true" :
            self.ui.checkBoxRev.setChecked(True)
        else:
            self.ui.checkBoxRev.setChecked(False)

        self.partner = str(settings.value("partner", self.partner))
        self.ui.lineEditPartner.setText(self.partner)

        self.target = str(settings.value("target", self.target))
        self.ui.lineEditTarget.setText(self.target)

        self.CreateParameters()
        self.BuildTags()

    @pyqtSlot()
    def SaveConfig(self):

        settings = VSettings("Stec.Automap2")

        self.tauscans = int(self.ui.spinBoxtauscans.value())
        settings.setValue("tauscans", self.tauscans)

        # ............................

        self.numberzones = int(self.ui.spinBoxActCount.value())
        settings.setValue("numberzones",  self.numberzones)

        self.numberdataboxes = int(self.ui.spinBoxDbxCount.value())
        settings.setValue("numberdataboxes", self.numberdataboxes)

        self.first = int(self.ui.spinBoxFirstGoodDBX.value())
        settings.setValue("first", self.first)

        self.last = int(self.ui.spinBoxLastGoodDBX.value())
        settings.setValue("last", self.last)

        if self.ui.checkBoxRev.isChecked():
            self.reverseProfile = "true"
        else:
            self.reverseProfile = "false"

        if self.ui.checkBoxusedelta.isChecked() :
            self.useDelta = "true"
        else:
            self.useDelta = "false"

        settings.setValue("usedelta", self.useDelta)
        settings.setValue("reverseprofile", self.reverseProfile)

        self.partner = self.ui.lineEditPartner.text()
        settings.setValue("partner", self.partner)

        self.target = self.ui.lineEditTarget.text()
        settings.setValue("target", self.target)

        #...................................
        self.filter = self.ui.doubleSpinBoxSplineFilter.value()
        settings.setValue( "bsplinefilter", self.filter )

        self.CreateParameters()
        self.BuildTags()

    def closeEvent(self, event: QEvent = None):

        if self.worker != None :
            self.worker.quit()
            self.worker.wait()

        if self.cBridge != None:
            self.cBridge.quit()
            self.cBridge = None

        if self.pj != None:
            self.pj.deleteLater()
            self.pj = None

        event.accept()

    @pyqtSlot()
    def OnExit(self):
        if self.cBridge != None:
            self.cBridge.quit()
            self.cBridge = None

        if self.pj != None:
            self.pj.deleteLater()
            self.pj = None

        self.deleteLater()

    @pyqtSlot()
    def OnPJanice(self):
        if self.pj is None:
            self.pj = pjanice()
            self.pj.show()
        else:
            self.pj.show()

        self.cBridge = self.pj.cBridge

    def newDesc(self, name, desc):
        print(name, desc)

    def doAiMapped(self, Profile):

        mapped = []

        if self.isLoaded(self.bspline) == True:
            return None


        all = self.bspline[0:-1]

        try :
            for i in range(0, len(all)) :
                offset = all[i]
                partialProfile = self.mapA.Control(Profile, offset)
                mapped.append(partialProfile[i])

            return mapped

        except :
            return None


    def AddV(self, roll, values : [], limit : int):

        offsetsRol = np.nan

        if self.isLoaded(roll) == True :
            return np.array(values)

        offsetsRoll = np.vstack([roll, values])

        try:
            RowsD, ColsD = self.offsetsRoll.shape
        except:
            RowsD = 1
            ColsD = len(values)

        if RowsD > limit:

            return offsetsRoll[: limit+1]

        return  offsetsRoll


    def newData(self, name, data):

        if len(data) :

            cv = conv()

            if name == self.targetSub.name :
                self.timeofDbx = time.time()
                self.databoxTargetArray = list(cv.toFloat(data))
                if cv.AllThis(self.databoxTargetArray, 0.0) :
                    self.databoxTargetArray = None
                    return


            elif name == self.partnerSub.name :
                if self.timeofDbx == None :
                    self.actuatorPartnerArray = None
                    return # time 0, forget

                now = time.time()
                seconds = abs(now - self.timeofDbx) # must be withing 3 seconds of each other
                if seconds < 3 :
                    self.actuatorPartnerArray =  list(cv.toFloat(data))
                    if cv.AllThis(self.actuatorPartnerArray,0.0  ) :
                        self.actuatorPartnerArray = None
                        return



            if self.actuatorPartnerArray != None and self.databoxTargetArray != None :
                a = self.actuatorPartnerArray.copy()
                b = self.databoxTargetArray.copy()
                self.sigNewUpdates.emit(a, b)

                self.actuatorPartnerArray = None
                self.databoxTargetArray = None


    @pyqtSlot()
    def BuildTags(self):
        if self.target != None and self.partner !=  None:
            if len(self.target) > 0 and len(self.partner) > 0 :
                print("Will Subscribe  Build Target : Partner ", self.target, " : ", self.partner)

                if self.targetSub != None :
                    if self.target != self.targetSub.name :
                        self.targetSub.deleteLater()
                        self.targetSub : Subscriber = None


                if self.partnerSub != None:
                    if self.partner != self.partnerSub.name:
                        self.partnerSub.deleteLater()
                        self.partnerSub: Subscriber = None


                if self.targetSub == None :
                    self.targetSub =  Subscriber(self.target, self.cBridge, self.newData, self.newDesc )


                if self.partnerSub == None :
                    self.partnerSub = Subscriber(self.partner, self.cBridge,self.newData, self.newDesc )

                if self.targetAutomappedSub != None :
                    self.targetAutomappedSub.deleteLater()
                    self.targetAutomappedSub = None

                targetAutomappedName = self.target + ".AutoMapped"
                self.targetAutomappedSub = Subscriber(targetAutomappedName , self.cBridge, self.newData, self.newDesc)

    def eventFilter(self, source, event):
        if (event.type() != QtCore.QEvent.ContextMenu ) :
            return super(StdcomAutomap, self).eventFilter(source, event)

    def buildCsv(self):

        if self.isLoaded(self.bspline) == False:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                      "All Files (*);;Text Files (*.csv)", options=options)
            if fileName :
                try :
                    df = pd.DataFrame(self.bspline)
                    df.to_csv(fileName)
                except :

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Cannot Save BSpline")
                    msg.setInformativeText('Might Wait for more updates')
                    msg.setWindowTitle("Error")
                    msg.exec_()



if __name__ == "__main__":

    my_parser = argparse.ArgumentParser(description="Version :" + stdcomQt.stdcomQtVersion + " Stec SqlPlayback Python Version")
    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.
    sys.path.append(parent)
    app = QApplication(sys.argv)
    w = StdcomAutomap()
    w.show()

    sys.exit(app.exec_())