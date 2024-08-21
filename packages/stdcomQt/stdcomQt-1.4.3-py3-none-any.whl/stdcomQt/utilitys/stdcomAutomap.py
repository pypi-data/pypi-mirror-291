import  sys, os

import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QApplication

import stdcomQt

from scipy.interpolate import BSpline, make_interp_spline, UnivariateSpline, CubicSpline


try :
    from stdcomQt.stdcomQtconv import stdcomQtConv as conv
    from stdcomQt.utilitys.stdcomplot import stdcomplot as plot
    from stdcomQt.stdcomQtC20 import CDCorrelations as Ccore

except :
    from stdcomQtconv import stdcomQtConv as conv
    from stdcomplot import stdcomplot as plot
    from stdcomQtC20 import CDCorrelations as Ccore




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
from stdcomQt.stdcomutilitywidgets import StecSqlConfigWidget
from stdcomQt.stdcomvsettings import *
from stdcomQt.utilitys.stdautomap import *
from stdcomQt.utilitys.pjaniceExt import pjanice



class MappingThread(QThread):
    sigOffsets = pyqtSignal(list)

    actshapes = None
    databoxshapes = None
    actshapesList = []
    databoxshapesList = []

    parameters = None

    firstGood = 15
    lastGood = 187

    mapA = None
    tauScans = 1
    typec = "spearman"

    offset = 100
    zoneWidth = 10

    correlation_limit = .52

    stage1window = 2
    waitToGo = 50
    timesGone = 0
    usedelta = 1
    centerDataBoxes : list = None

    CDstats = None


    def __init__(self, parameters, Parent=None):

        if Parent is not None:
            super().__init__(Parent)
        else:
            super().__init__()

        self.CDstats = CDCorrelations(parameters)


        self.SetMap(parameters)
        self.start()

    @pyqtSlot(dict)
    def SetMap(self, parameters):

        if type(parameters) != dict:
            raise Exception('exceptions  Parameters are needed" ')
            return

        self.parameters = parameters

        self.mapA = MapToZonesFromCenter(self.parameters)
        self.offset = self.mapA.Offset()

        # For new mapping
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            self.centerAct = self.mapA.CenterActuator()
            self.centerDbx = self.mapA.CenterDbx()
            self.centerDataBoxes = [self.centerDbx] * self.mapA.d_count

        self.d_count = self.mapA.DCount()
        self.zoneWidth = self.mapA.MinDWidth()
        self.initialShrinkage = [float(1.0)] * self.d_count
        self.correlation_limit = self.parameters.get("correlation_limit", self.correlation_limit)
        self.tauScans = self.parameters.get("tauscans", self.tauScans)
        self.typec = self.parameters.get("typec", self.typec)
        self.usedelta = self.parameters.get("usedelta", self.usedelta)
        self.firstGood = self.parameters.get('firstgood', self.firstGood)
        self.lastGood = self.parameters.get('lastgood', self.lastGood)

        self.stage1window = self.parameters.get("stage1window", self.stage1window)
        self.waitToGo = self.parameters.get("waittogo", self.waitToGo)

        if self.typec == "kendall" or self.typec == "pearson" or self.typec == "spearman":
            print("Will Do Using:", self.typec)
        else:
            raise Exception('exceptions  typec == "kendall"  or typec == "pearson" or typec == "spearman" ')
            return


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


    """
    df_1 = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]],columns=['A','B','C'])
    df_2 = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]],columns=['D','E','F'])
   

  
        pd.concat([df_1, df_2], axis=1, keys=['df_1', 'df_2']).corr().loc['df_2', 'df_1']


    """

    def Remap(self, databoxes, RowsD, offset_or_centerdbx):
        return self.CDstats.Remap(self.mapA, databoxes, RowsD, offset_or_centerdbx)


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

    def ComputerVariance(self, act : np.array ):
        var = act.var(axis=0)
        return var

    def ComputerStd(self, act: np.array):
        std = act.std(axis=0)
        return std

    def CreateCorrelationRange(self, MINTarget, rangeWindow=None):

        if rangeWindow is None:
            rangeWindow = self.stage1window

        minr = MINTarget - rangeWindow
        if minr < 0:
            minr = 0
        maxr = MINTarget + rangeWindow
        if maxr > self.d_count:
            maxr = self.d_count

        return minr, maxr

    def StageOneCorrTable(self, databoxes, actuators, offset_or_centerdbx, RowsD, finds):

        # map the number captured
        remap = self.Remap(databoxes, RowsD, float(offset_or_centerdbx))
        cTable = self.CDstats.MapTableCorrelation(actuators,remap)

        a = []
        for each in finds :
            cor = cTable.loc['E'+str(each)]['A'+str(each)]
            if np.isnan(cor) == False :
                a.append(each)

        return a

    def StageOneAa(self, databoxes, actuators, target, offset_or_centerdbx, RowsD):

        target = int(target)
        if target == 0:
            return 0
        elif target >= self.d_count:
            return 0

        RowsP, ColsP = actuators.shape
        RowsD, ColsD = databoxes.shape
        mrow  = min(RowsP,RowsD)

        nameDBX = "Target"

        minr, maxr = self.CreateCorrelationRange(target, self.stage1window)

        minoff = offset_or_centerdbx - ((target - minr) * self.zoneWidth)
        maxoff = offset_or_centerdbx + ((maxr - target) * self.zoneWidth)

        zwh = self.zoneWidth / 2
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            zone_width_in_dbx = ColsD / self.d_count
            minoff = offset_or_centerdbx - ((target - minr) * zone_width_in_dbx)
            maxoff = offset_or_centerdbx + ((maxr - target) * zone_width_in_dbx)
            zwh = int(zone_width_in_dbx / 2)
        span = int((maxoff - minoff) / zwh) + 1

        names = [nameDBX]
        rows = actuators[:mrow,target]
        init = True

        of = minoff

        for o in range(0, span):
            remap = self.Remap(databoxes, RowsD, float(of))
            dbx_eng = remap[:mrow, target]

            rows = np.vstack([rows, dbx_eng])
            init = False
            names.append(str(of))
            of = of + zwh

        cols = rows.transpose()
        df = pd.DataFrame(cols, columns=names)
        m = df.corr(self.typec)
        v = m.iloc[0]
        del v[nameDBX]
        maxz = v.max()
        maxl = v.idxmax()

        offset_or_centerdbx = float(maxl)

        return offset_or_centerdbx

    def StageThreeAa(self, databoxes, actuators, target, offset_or_centerdbx, RowsD):

        target = int(target)
        if target == 0:
            return 0
        elif target >= self.d_count:
            return 0

        zwh = self.zoneWidth / 2
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            row, col = databoxes.shape
            zwh = int(col / self.d_count / 2)

        lo = int(offset_or_centerdbx - zwh)
        hi = int(offset_or_centerdbx + zwh)
        act_pvs = actuators[:, target]
        nameDBX = "Target"

        names = [nameDBX]
        rows = np.array(act_pvs)
        df = pd.DataFrame()

        remap = self.Remap(databoxes, RowsD, float(offset_or_centerdbx))
        dbx = remap[:, target]

        RowsP = len( list(act_pvs))
        RowsD = len(list(dbx))
        mrow = min(RowsP, RowsD)

        df[nameDBX] = act_pvs[:mrow]
        df["PV"] = dbx[:mrow]

        m = df.corr(self.typec)
        beginCorr = m[nameDBX]["PV"]
        beginOffset = offset_or_centerdbx

        middle = int(offset_or_centerdbx) + 1
        step = 1
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            step = 0.1

        for o in np.arange(middle, hi, step):
        #for o in range(middle, hi):
            remap = self.Remap(databoxes, RowsD, float(o))
            dbx = remap[:, target]
            df["PV"] = dbx
            m = df.corr(self.typec)
            corr = m[nameDBX]["PV"]

            if corr > beginCorr:
                beginCorr = corr
                beginOffset = o
            else:
                break

        middle = int(offset_or_centerdbx) - 1
        step = -1
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            step = -0.1
        for o in np.arange(middle, lo, step):
        #for o in range(middle, lo, -1):
            remap = self.Remap(databoxes, RowsD, float(o))
            dbx = remap[:, target]
            df["PV"] = dbx
            m = df.corr(self.typec)
            corr = m[nameDBX]["PV"]

            if corr > beginCorr:
                beginCorr = corr
                beginOffset = o
            else:
                break

        print("StageThreeAa in / out", ":", target, ":", offset_or_centerdbx, ":", beginOffset)
        return beginOffset



    def MappAll(self, steps=1):


        databoxes, actuators = self.GetTauAdj()

        RowsD, ColsD = databoxes.shape
        RowsP, ColsP = actuators.shape


        # always going to need deltas to see if actuator has moved for corrleation
        if self.usedelta:
            actuators = self.DeltaP(actuators)
            actuatorsD = actuators
            RowsP, ColsP = actuators.shape

            databoxes = self.DeltaP(databoxes)
            RowsD, ColsD = databoxes.shape


        else:
            actuatorsD = self.DeltaP(actuators)

        # determine any movment
        # this could me modified to np.count_nonzero() if we need to have a percentage that moves later
        # but for now we use any movment as movment
        OkToDo = []
        for i in range(0, ColsP):
            cols = actuatorsD[:, i]
            if not np.any(cols) == False:
                OkToDo.append(i)


        ctr = None

        finds = self.CDstats.FindMovements(actuatorsD, self.firstGood, self.lastGood, 20)

        if len(finds)  ==  0 :
            if len(OkToDo) > 6:
                ctr = OkToDo[int(len(OkToDo) / 2)]
            else:
                return
        else:
            ctr =  finds[0]

        y = []
        x = []

        mustbePositive = True
        if self.offset < 0.0:
            mustbePositive = False

        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            for i in finds:
                o = self.centerDbx
                if np.isnan(o) == False:
                    no = self.StageThreeAa(databoxes, actuators, i, o, RowsD)
                    x.append(i)
                    y.append(no)
        else:
            for i in finds :
                o = self.StageOneAa(databoxes, actuators, i, self.offset, RowsD)
                if np.isnan(o) == False :
                    no = self.StageThreeAa(databoxes, actuators, i, o, RowsD)
                    if no >= 0  and mustbePositive == True :
                        x.append(i)
                        y.append(no)
                    elif no <= 0 and mustbePositive == False :
                        x.append(i)
                        y.append(no)



        if len(x) > 2:
            offsets = self.centerDataBoxes
            for i in range(0, len(x)) :
                index = x[i]
                value = y[i]
                offsets[index] = value
                self.centerDataBoxes = offsets

            self.sigOffsets.emit(list(offsets))


    @pyqtSlot(list, list)
    def UpdateProfiles(self, actuators: list, profile: list):

        if actuators is None or profile is None:
            return

        self.actshapesList.append(actuators)
        self.databoxshapesList.append(profile)

        nbrRows = len(self.actshapesList)
        if nbrRows > self.waitToGo:
            self.databoxshapes = np.array(self.databoxshapesList)
            self.actshapes = np.array(self.actshapesList)
            self.MappAll()
            self.databoxshapesList.clear()
            self.actshapesList.clear()



class StdcomAutomap(QMainWindow):
    sigNewUpdates = pyqtSignal(list, list)
    newParmeters = pyqtSignal(dict)
    proxLock = QMutex()

    pj = None
    cBridge = None

    lastOffsets = None

    typec = str("spearman")
    stage1window = int(5)
    tauscans = int(1)
    correlation_limit = .52

    useDelta = "false"

    actuatorCount = 96
    actuatorZoneWidth = 50

    sheetWidth = 4800
    offset = 100
    offsets = {}
    trendOffsets = np.nan
    # For new mapping
    centerAct = 48
    centerDbx = 96

    firstGood = 15
    lastGood = 187
    dbxcount = 500
    trendZone = 46

    scansb4calculations = int(50)
    offsetsToFilter = 50
    bsplineFilter  = .5
    bspline  : np.array = np.nan
    splits = 5
    CDstats = None

    reverseProfile = "false"

    partner = "ActuatorZones"
    target = "ScannerBWProfile"

    targetSub  : Subscriber = None
    partnerSub : Subscriber = None
    targetOffsets : Subscriber = None
    targetAutomappedSub: Subscriber = None


    parmeters : {} = None
    worker: MappingThread = None

    timeofDbx            = None
    actuatorPartnerArray = None
    databoxTargetArray = None

    mappedSubs = {}

    """
    offsetplt : plot = None
    dbsplt : plot = None
    actplt : plot = None
    """


    offsetsRoll : np.array = np.nan
    dbxRoll  : np.array = np.nan
    actRoll: np.array = np.nan

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

        z = []
        for i in  range(self.actuatorCount) :
            z.append(i)

        self.offsets = {self.offset:z}
        self.lastOffsets = [self.offset] * self.actuatorCount


        #self.mapA = MapToZones(self.parmeters)
        self.mapA = MapToZonesFromCenter(self.parmeters)
        if type(self.mapA).__name__ == 'MapToZonesFromCenter':
            self.offsets = {self.centerDbx: z}
            self.lastOffsets = [self.centerDbx] * self.actuatorCount

        self.worker = MappingThread(self.parmeters)
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

        self.offsetsRoll = self.AddV(self.offsetsRoll, offsets, self.offsetsToFilter )

        try:
            RowsD, ColsD = self.offsetsRoll.shape
            trend = int(self.ui.spinBoxTrend.value())
            t = self.offsetsRoll[:, trend]

            if RowsD > 1 :
                self.trendingOffset = list(t)
                x = list(np.arange(0, len(self.trendingOffset) * self.scansb4calculations, self.scansb4calculations ))
                self.offsetplt.DrawControl(self.trendingOffset, x)


                meanO = list(self.offsetsRoll.mean(axis=0))
                x2 = list( range(0, ColsD))
                self.offsetpltArray.DrawControl(meanO, x2)


                o3 = np.array(meanO, dtype = float)
                o3a = np.array_split(o3,self.splits)

                mGroups = None

                for row in o3a:
                    m = np.mean(row.astype(float))
                    repeat = len(list(row))
                    repeats = [m] * repeat
                    if mGroups == None :
                        mGroups = repeats
                    else:
                        mGroups = mGroups + repeats



                spl = UnivariateSpline(x2, mGroups)
                spl.set_smoothing_factor(self.bsplineFilter)
                bspline = spl(x2)
                self.offsetpltArrayGroup.DrawControl(bspline, x2)

                self.targetOffsets.UpdateData(bspline, 0)
                self.bspline = bspline
                #   self.AddV(self.bspline, bspline, self.offsetsToFilter)

        except:
            print("Shapes Not Ready Yest")
            return


    @pyqtSlot()
    def CreateParameters( self) :

        usedelta = 0
        if self.useDelta == "true":
            usedelta = 1


        self.parmeters = {'start_s': 1,
                     'end_s': self.dbxcount,
                     'left_s': 1,
                     'right_s': self.dbxcount,
                     'offset': self.offset,
                     'total_s_width': self.sheetWidth,
                     'd_count': self.actuatorCount,
                     'min_d_width': self.actuatorZoneWidth,
                     'shrinkage': [1.0] * self.actuatorCount,
                     'zerocheck': 1,
                     'typec': self.typec,
                     'stage1window': self.stage1window,
                     'tauscans': self.tauscans,
                     'correlation_limit': self.correlation_limit,
                     'usedelta':  usedelta,
                     'firstgood' : self.firstGood,
                     'lastgood' : self.lastGood,
                     # For new mapping
                     'center_actuator' : self.centerAct,
                     'center_dbx' : self.centerDbx,
                     'waittogo' : self.scansb4calculations
                     }

        self.newParmeters.emit(self.parmeters)
        self.CDstats = CDCorrelations(self.parmeters)


    @pyqtSlot()
    def LoadConfig(self):
        settings = VSettings("Stec.Automap")

        self.typec = str(settings.value("typec", self.typec))
        self.ui.lineEditTypec.setText(self.typec)

        self.bsplineFilter = float( settings.value("bsplinefilter", self.bsplineFilter ))
        self.ui.doubleSpinBoxSplineFilter.setValue(self.bsplineFilter)

        self.splits = int( settings.value("widthsplits", self.splits))
        self.ui.spinBoxGroups.setValue(self.splits)


        self.scansb4calculations = int(settings.value("scansb4offsetcalc",self.scansb4calculations))
        self.ui.spinBoxSampleLength.setValue(self.scansb4calculations)

        self.offsetsToFilter = int(settings.value("offsettofilter",  self.offsetsToFilter))
        self.ui.spinBoxHistoryOffset.setValue(self.offsetsToFilter)


        self.stage1window = int(settings.value("stage1window", self.stage1window))
        self.ui.spinBoxstage1window.setValue(self.stage1window)

        self.tauscans =  int(settings.value("tauscans", self.tauscans))
        self.ui.spinBoxtauscans.setValue(self.tauscans)

        self.correlation_limit = float(settings.value("correlation_limit", self.correlation_limit))
        self.ui.doubleSpinBoxcorrelationlimit.setValue(self.correlation_limit)

        self.useDelta = settings.value("usedelta", self.useDelta)

        if self.useDelta == "true" :
            self.ui.checkBoxusedelta.setChecked(True)
        else:
            self.ui.checkBoxusedelta.setChecked(False)
        #............................

        self.actuatorCount = int( settings.value("actuatorcount", self.actuatorCount))
        self.ui.spinBoxActCount.setValue(self.actuatorCount)
        self.ui.spinBoxTrend.setRange(1, self.actuatorCount)

        self.actuatorZoneWidth = int(settings.value("actuatorzonewidth", self.actuatorZoneWidth ))
        self.ui.spinBoxZnWidth.setValue(self.actuatorZoneWidth)

        self.sheetWidth = int( settings.value("sheetwidth", self.sheetWidth))
        self.ui.spinBoxShtWidth.setValue(self.sheetWidth)

        self.offset = int( settings.value("offset", self.offset))
        self.ui.spinBoxOffset.setValue(self.offset)

        self.centerAct = int( settings.value("centeractuator", self.centerAct))
        self.ui.spinBoxCenterAct.setValue(self.centerAct)

        self.centerDbx = float(settings.value("centerdatabox", self.centerDbx))
        self.ui.spinBoxCenterDbx.setValue(self.centerDbx)

        self.firstGood = int( settings.value( "firstgood", self.firstGood ))
        self.ui.spinBoxFirstGoodDBX.setValue(self.firstGood)

        self.lastGood = int(settings.value("lastgood", self.lastGood))
        self.ui.spinBoxLastGoodDBX.setValue(self.lastGood)

        self.reverseProfile = str(settings.value("reverseprofile", self.reverseProfile))

        if self.reverseProfile == "true" :
            self.ui.checkBoxRev.setChecked(True)
        else:
            self.ui.checkBoxRev.setChecked(False)

        self.partner = str(settings.value("partner", self.partner))
        self.ui.lineEditPartner.setText(self.partner)

        self.target = str(settings.value("target", self.target))
        self.ui.lineEditTarget.setText(self.target)

        self.dbxcount = int(settings.value("dbxcount", self.dbxcount))
        self.ui.spinBoxDbxCount.setValue(self.dbxcount)

        self.trendZone = int(settings.value("trendzone", self.trendZone))
        self.ui.spinBoxTrend.setValue(self.trendZone)

        self.CreateParameters()

        self.BuildTags()

    @pyqtSlot()
    def SaveConfig(self):

        settings = VSettings("Stec.Automap")

        self.typec = str(self.ui.lineEditTypec.text())
        settings.setValue("typec", self.typec)

        self.stage1window = int(  self.ui.spinBoxstage1window.value())
        settings.setValue("stage1window", self.stage1window)

        self.tauscans = int(self.ui.spinBoxtauscans.value())
        settings.setValue("tauscans", self.tauscans)

        self.correlation_limit = float(self.ui.doubleSpinBoxcorrelationlimit.value())
        settings.setValue("correlation_limit", self.correlation_limit)

        # ............................

        self.actuatorCount = int(self.ui.spinBoxActCount.value())
        settings.setValue("actuatorcount",  self.actuatorCount)

        self.actuatorZoneWidth = int(self.ui.spinBoxZnWidth.value())
        settings.setValue("actuatorzonewidth", self.actuatorZoneWidth)

        self.sheetWidth = int(self.ui.spinBoxShtWidth.value())
        settings.setValue("sheetwidth", self.sheetWidth)

        self.offset = int(self.ui.spinBoxOffset.value() )
        settings.setValue("offset", self.offset)

        self.centerAct = int(self.ui.spinBoxCenterAct.value())
        settings.setValue("centeractuator", self.centerAct)


        self.centerDbx = float(  self.ui.spinBoxCenterDbx.value())
        settings.setValue("centerdatabox", self.centerDbx)

        self.firstGood = int(self.ui.spinBoxFirstGoodDBX.value())
        settings.setValue("firstgood", self.firstGood)

        self.lastGood = int(self.ui.spinBoxLastGoodDBX.value())
        settings.setValue("lastgood", self.lastGood)

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

        self.dbxcount = int(self.ui.spinBoxDbxCount.value())
        settings.setValue("dbxcount", self.dbxcount)

        self.trendZone = int(self.ui.spinBoxTrend.value())
        settings.setValue("trendzone", self.trendZone)


        #...................................
        self.bsplineFilter = self.ui.doubleSpinBoxSplineFilter.value()
        settings.setValue( "bsplinefilter", self.bsplineFilter )

        self.scansb4calculations = self.ui.spinBoxSampleLength.value()
        settings.setValue("scansb4offsetcalc",  self.scansb4calculations)

        self.offsetsToFilter = self.ui.spinBoxHistoryOffset.value()
        settings.setValue("offsettofilter", self.offsetsToFilter)

        self.splits = self.ui.spinBoxGroups.value()
        settings.setValue("widthsplits", self.splits)

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


    def isLoaded(self, roll ):
        try:
            if np.isnan(roll):
                return True
            else:
                return False

        except:
            return False

        return False
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




                #Profile = self.CDstats.profileFilterFirstLastNonZero(self.databoxTargetArray)
                Profile = self.mapA.profileAvgIgnoreZero(self.databoxTargetArray)


                spProfile = self.CDstats.Spline(Profile, self.splits, self.bsplineFilter)
                x2 = list(range(0, len(self.databoxTargetArray)))

                self.scannerProfile.DrawControl(Profile,x2)
                self.scannerProfileSpline.DrawControl(spProfile,x2)

                mappedProfile = self.doAiMapped(Profile)
                if mappedProfile != None:
                    print("Mapped Profile: ", mappedProfile)
                    x2 = list(range(0, len(mappedProfile)))
                    self.splSplineProfile.DrawControl(mappedProfile, x2)
                    self.targetAutomappedSub.UpdateData(mappedProfile, 0)

                    spProfile = self.CDstats.Spline(mappedProfile, self.splits, self.bsplineFilter)

                    self.mappedProfileSpline.DrawControl(  spProfile ,  x2 )


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
                    else:
                        x2 = list(range(0, len(self.actuatorPartnerArray)))
                        self.actuatorProfile.DrawControl(self.actuatorPartnerArray,x2)



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

                if self.targetOffsets != None :
                    self.targetOffsets.deleteLater()
                    self.targetOffsets = None



                offsetName = self.target + ".Offsets"
                self.targetOffsets = Subscriber(offsetName, self.cBridge, self.newData, self.newDesc)

                if self.targetAutomappedSub != None :
                    self.targetAutomappedSub.deleteLater()
                    self.targetAutomappedSub = None

                targetAutomappedName = self.target + ".AutoMapped"
                self.targetAutomappedSub = Subscriber(targetAutomappedName , self.cBridge, self.newData, self.newDesc)

    @pyqtSlot()
    def DeleteMaps(self):
        selected = self.ui.listWidgetmaps.selectedItems()

        if selected != None :
            for itm in selected :
                self.ui.listWidgetmaps.takeItem(self.ui.listWidgetmaps.row(itm))

        self.SaveConfig()

    @pyqtSlot()
    def BuildMapTo(self):

        keys = self.mappedSubs.keys()
        for key in keys :
            if key not in self.toMap :
                lst = self.mappedSubs.get(key)
                lst[0].deletelater
                lst[1].deletelater
                self.mappedSubs.update({key:None})

        for key in self.toMap :
            if key not in self.mappedSubs.keys() :
                sub1 = Subscriber(key, self.cBridge,self.newData)
                sub2 = Subscriber(key+".mapped",self.cBridge,self.newData)
                lst = [ sub1,sub2]
                self.mappedSubs.update( {key:lst})

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and source is self.ui.listWidgetmaps):
            menu = QtWidgets.QMenu()
            menu.addAction('Delete')
            menu.triggered.connect(self.DeleteMaps)

            if menu.exec_(event.globalPos()):
                return True

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