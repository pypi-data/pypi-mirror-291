import  sys, os

import numpy as np
from PyQt5.QtWidgets import QApplication

import stdcomQt
from stdcomQt.stdcomutilitywidgets import StecIPconfigDialog, StecPostgresConfigWidget

import argparse

try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from stdcomQt.stdcomQtPjanice import *
from stdcomQt.stdcomvsettings import *

from PyQt5.QtWidgets import QDialog, QApplication, QTabWidget, QTableWidgetItem, QCheckBox, QMainWindow, QListWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent, QObject, QTimer, QFileInfo
from PyQt5.Qt import pyqtSlot, pyqtSignal
from stdcomQt import *
from stdcomQt.stdcomutilitywidgets import StecSqlConfigWidget
from stdcomQt.stdcomvsettings import *
from stdcomQt.utilitys.sqlplayback import *
from stdcomQt.utilitys.pjaniceExt import pjanice

try :
    from stdcomQt.stdcomQtconv import stdcomQtConv as conv
except :
    from stdcomQtconv import stdcomQtConv as conv



try:

    from stdcomQt import Subscriber
except:

    from stdcomQt.stdcomQt import Subscriber

class StdcomSqlPlayback(QMainWindow):

    database  : StecSqlConfigWidget  = None
    postgres = None
    allie = None
    actuator = None
    target  = None
    subPartner: Subscriber = None
    subTarget: Subscriber = None
    pj = None

    st = np.nan
    std   =  np.nan
    pnow = None
    playBackIndex = int(0)

    timer = None


    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_SqlPlayBack()
        self.ui.setupUi(self)
        self.show()


        self.database = StecSqlConfigWidget("Stec.Playback", self.SqlOkCallBack, self.SqlCancelCallBack)
        self.ui.action_Sql.triggered.connect(self.ShowSqlDbs)
        self.database.hide()
        self.ui.listWidgetTarget.itemClicked.connect(self.OnTarget)
        self.ui.listWidgetPartner.itemClicked.connect(self.OnPartner)
        self.ui.pushButtonConnectDB.clicked.connect(self.OnConnectToDB)
        self.ui.pushButtonSaveToCSV.clicked.connect(self.OnSaveToCSVs)
        self.ui.pushButtonStopPlay.clicked.connect(self.OnStopplayback)

        self.pj = pjanice()
        self.pj.setWindowTitle("PJanice")


        self.ui.pushButtonFetchFromDB.clicked.connect(self.OnGather)
        self.ui.pushButtonPlayToMultiverse.clicked.connect(self.OnPlayback)
        self.ui.pushButtonFetchFromCSV.clicked.connect(self.OnFetchCSV)

        self.cBridge = self.pj.cBridge
        self.ui.action_Multiverse.triggered.connect(self.OnPJanice)
        self.ui.action_Exit.triggered.connect(self.OnExit)

        self.timer = QTimer(self)
        pb = int(self.ui.spinBoxPlayBackSpeed.value())
        self.timer.setInterval(pb)
        self.timer.timeout.connect(self.timeOut)

        self.ui.spinBoxPlayBackSpeed.valueChanged.connect(self.OnPlaybackSpeed)


    def SqlOkCallBack(self, a,b,c,d,e,f):
        self.database.hide()
        self.OnConnectToDB()

    def SqlCancelCallBack(self):
        self.database.hide()
    @pyqtSlot()
    def ShowSqlDbs(self):
        self.database.show()

    @pyqtSlot(int)
    def OnPlaybackSpeed(self, pb):
        self.timer.setInterval(pb)

    @pyqtSlot(QListWidgetItem)
    def OnTarget(self, item):
        text = item.text()
        self.target = text


        csv = text.replace("/", "_") + ".csv"
        self.ui.lineEditTargetCsv.setText(csv)
        self.ui.lineEditTargetTag.setText(text)
        self.BuildTargetTags()

        table = self.allie.get(text)
        r = self.postgres.GetLastDataRecordsFromTrendTable(table)
        self.ui.listWidgetLastValues.clear()
        if r is not None:
            today = r._timeOf
            before = today.addDays(-1)

            self.ui.dateTimeEditStart.setDateTime(before)
            self.ui.dateTimeEditEnd.setDateTime(today)
            cv = conv()
            data = list(r._data)
            data = cv.toStr(data)


            self.ui.listWidgetLastValues.insertItems(0,data)
            self.ui.lineEditNbrLast.setText("Len :" + str(len(data)))


    @pyqtSlot(QListWidgetItem)
    def OnPartner(self, item):
        text = item.text()
        self.actuator = text
        csv = text.replace("/", "_") + ".csv"
        self.ui.lineEditPartnerCsv.setText(csv)
        self.ui.lineEditPartnerTag.setText(text)
        self.BuildPartnerTags()

    @pyqtSlot()
    def OnConnectToDB(self):
        if self.postgres != None:
            del self.postgres
        self.postgres = self.database.GetDatabase()
        self.ui.listWidgetPartner.clear()
        self.ui.listWidgetTarget.clear()

        self.allie = self.postgres.getAllTracking()
        self.ui.listWidgetTarget.insertItems(0, self.allie.keys())
        self.ui.listWidgetPartner.insertItems(0, self.allie.keys())
        self.ui.lineEditTargetTag.clear()
        self.ui.lineEditTargetCsv.clear()
        self.ui.lineEditPartnerTag.clear()
        self.ui.lineEditPartnerCsv.clear()
        self.target = None
        self.actuator = None

    def closeEvent(self, event: QEvent = None):

        if self.cBridge != None:
            self.cBridge.quit()
            self.cBridge = None

        if self.pj != None:
            self.pj.deleteLater()
            self.pj = None

        event.accept()

    @pyqtSlot()
    def BuildTargetTags(self):
        target = self.ui.lineEditTargetTag.text()
        if target is None or len(target) == 0:
            msgBox = QMessageBox()
            msgBox.setText("Must Have a Target Tag Name for Multiverse ")
            msgBox.exec();
            return

        if self.subTarget != None:
            if self.subTarget.name != target:
                self.subTarget.deleteLater()
                self.subTarget = Subscriber(target, self.cBridge)
                self.subTarget = None

        if self.subTarget == None:
            self.subTarget = Subscriber(target, self.cBridge)
            self.cBridge.setOwner(self.subTarget, True)
            self.subTarget.UpdateDesc("Target Playback")

    @pyqtSlot()
    def BuildPartnerTags(self):

        partner = self.ui.lineEditPartnerTag.text()
        if partner is None or len(partner) == 0:
            msgBox = QMessageBox()
            msgBox.setText("Must Have a Partner Tag Name for Multiverse ")
            msgBox.exec();
            return

        if self.subPartner != None:
            if self.subPartner.name != partner:
                self.subPartner.deleteLater()
                self.subPartner = Subscriber(partner, self.cBridge)
                self.subPartner = None

        if self.subPartner == None:
            self.subPartner = Subscriber(partner, self.cBridge)
            self.cBridge.setOwner(self.subPartner, True)
            self.subPartner.UpdateDesc("Partner Playback")

    @pyqtSlot()
    def OnGather(self):

        st = None
        std = None

        if self.allie != None and self.target != None and self.actuator != None:
            table = self.allie.get(self.target, None)
            tableActuator = self.allie.get(self.actuator, None)

            if table != None and tableActuator != None:

                print("Found " + table + " " + tableActuator)

                today = self.ui.dateTimeEditEnd.dateTime()
                before = self.ui.dateTimeEditStart.dateTime()

                try:

                    r = self.postgres.GetAllDataRecordsFromTrendTable(table, before, today)

                except:
                    self.ui.lineEditStatusMessages.setText("Error " + self.target)
                    msgBox = QMessageBox()
                    msgBox.setText("Error Gathering " + self.target)
                    msgBox.exec();
                    return st, std

                length = len(r)
                StartFound = None
                NextFound = None
                self.ui.progressBar.setRange(0, length)
                self.ui.lineEditStatusMessages.setText("Found " + str(len) + " Records")

                for j in range(0, length):
                    self.ui.progressBar.setValue(j)
                    rec = r[j]


                    if StartFound == None :
                        StartFound = rec._timeOf
                        continue

                    NextFound  = StartFound
                    StartFound = rec._timeOf

                    dtime = StartFound.secsTo(rec._timeOf)

                    try:
                        rA = self.postgres.GetAllDataRecordsFromTrendTable(tableActuator,NextFound, StartFound)

                    except:
                        self.ui.lineEditStatusMessages.setText("Error " + self.actuator)

                        msgBox = QMessageBox()
                        msgBox.setText("Error Gathering " + self.actuator)
                        msgBox.exec();
                        return st, std

                    if rA is not None:
                        if len(rA):
                            # sum = postgres.ComputeAverage(rA)
                            recA = rA[0]

                            te = str(recA._timeOf.toString("yyyy MM dd hh:mm:ss"))

                            dataLen = len(recA._data)
                            if dataLen > 0:
                                data = np.array(recA._data)

                                matrix = [self.actuator, te, dtime]
                                matrix = np.hstack([matrix, data])
                                if st is None:
                                    st = matrix
                                else:
                                    st = np.vstack([st, matrix])

                                data = np.array(rec._data)
                                matrix = [self.target, te, dtime]
                                matrix = np.hstack([matrix, data])

                                if std is None:
                                    std = matrix
                                else:
                                    std = np.vstack([std, matrix])



            self.st = np.array(st)
            self.std = np.array(std)

            self.ui.lineEditStatusMessages.setText("Operation Complete")
            self.ui.progressBar.setValue(0)



    @pyqtSlot()
    def OnExit(self):
        if self.cBridge != None:
            self.cBridge.quit()
            self.cBridge = None

        if self.pj != None :
            self.pj.deleteLater()
            self.pj = None

        self.deleteLater()


    @pyqtSlot()
    def OnSaveToCSVs(self):

        st = self.st
        std = self.std

        messages = ""

        try:
            if (st is not None  ):
                csv = self.ui.lineEditPartnerCsv.text()
                df = pd.DataFrame(st)
                df.to_csv(csv, index=False)
                messages = messages + " Targeted Save to " + csv
        except :
            messages = ("Error Creating: ", self.ui.lineEditTargetCsv.text() )
            print(messages)

        try :
            if (std is not  None ):
                csv = self.ui.lineEditTargetCsv.text()
                df = pd.DataFrame(std)
                df.to_csv(csv, index=False)
                messages = messages + " Partner Saved to CSV " + csv
        except :
            messages = ("Error Creating: ", self.ui.lineEditPartnerCsv.text())
            print(messages)

        self.ui.lineEditStatusMessages.setText(messages)

    @pyqtSlot()
    def OnPJanice(self):
        if self.pj is None :
            self.pj = pjanice()
            self.pj.show()
        else:
            self.pj.show()

        self.cBridge = self.pj.cBridge

    @pyqtSlot()
    def OnPlayback(self):
        try :
            self.pnow = None
            self.playBackIndex = 0
            self.BuildPartnerTags()
            self.BuildTargetTags()
            self.timer.start()
            self.ui.lineEditStatusMessages.setText("Playback begins")
        except:
            self.ui.lineEditStatusMessages.setText("Playback FAILED")

    @pyqtSlot()
    def OnStopplayback(self):
        self.playBackIndex = 0
        self.timer.stop()


    @pyqtSlot()
    def OnFetchCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filter = "csv(*.csv)"

        fileName, _ = QFileDialog.getOpenFileName(self, "Target CSV", "",
                                                  filter, options=options)

        if fileName:
            print(fileName)
            fn = QFileInfo(fileName)
            self.ui.lineEditTargetCsv.setText(fn.fileName())
            df1 = pd.read_csv(fileName)
            start_dates = df1['QDateTime']

            std = df1.to_numpy()
            tag = std[0, 0]
            self.std = std

            self.ui.lineEditTargetTag.setText(str(tag))

            print(tag)

            fileName, _ = QFileDialog.getOpenFileName(self, "Partner CSV", "",
                                                      filter, options=options)


            if fileName:
                print(fileName)
                fn = QFileInfo(fileName)
                self.ui.lineEditPartnerCsv.setText(fn.fileName())

                df2 = pd.read_csv(fileName)

                start_date = start_dates[0]
                len = start_dates.size
                end_date = start_dates[len -1]

                mask = (df2['QDateTime'] > start_date) & (df2['QDateTime'] <= end_date)
                df2 = df2.loc[mask]

                st = df2.to_numpy()
                tag2 = st[0, 0]
                self.st = st
                self.ui.lineEditPartnerTag.setText(str(tag2))



    @pyqtSlot()
    def timeOut(self):

        try :
            if np.isnan(self.std) == True or np.isnan(self.st) == True :
                self.ui.lineEditStatusMessages.setText("Nothing Gathered from csv files or database")
                self.timer.stop()
                self.playBackIndex = 0
                self.pnow = None
                return
        except :
            print("Will Continue Play")

        if self.subTarget != None and self.subPartner != None :
            r1, c1 = np.shape(self.st)
            r2, c2 = np.shape(self.std)
            r = max(r1, r2)
            self.ui.progressBar.setRange(0, r)
        else:
            self.timer.stop()
            self.playBackIndex = 0

            return

        if self.playBackIndex >= r :
            self.timer.stop()
            self.playBackIndex = 0
            return

        try :
            scan = self.playBackIndex

            actuatorProfile = self.st[scan, 3:]
            actuatorProfile = actuatorProfile.astype(float)

            if np.all(actuatorProfile == 0.0) :
                self.playBackIndex = self.playBackIndex + 1
                return


            scannerProfile = self.std[scan, 3:]
            scannerProfile = scannerProfile.astype(float)


            scannerProfile = list(scannerProfile)
            actuatorProfile = list(actuatorProfile)

            self.ui.progressBar.setValue(scan)
            self.subTarget.UpdateData(scannerProfile, 0)
            self.subPartner.UpdateData(actuatorProfile, 0)
            self.playBackIndex = self.playBackIndex + 1
        except:
            self.timer.stop()
            self.playBackIndex = 0
            return





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
    w = StdcomSqlPlayback()
    w.show()

    sys.exit(app.exec_())