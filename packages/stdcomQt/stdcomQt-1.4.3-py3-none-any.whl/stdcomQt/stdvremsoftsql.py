#  Copyright (C) 2021 Vremsoft LLC and/or its subsidiary(-ies).
#  All rights reserved.
#  Contact: Laura Chapman  (edc@vremsoft.com)
#  Commercial Usage
#  Licensees holding valid Vremsoft LLC licenses may use this file in
#  accordance with the License Agreement provided with the
#  Software or, alternatively, in accordance with the terms contained in
#  a written agreement between you and Vremsoft. LLC
#

import math

from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import pandas as pd
import numpy as np
import argparse

class VremMYSqlRecord:
    def __init__(self, timeOf=QDateTime, d=None):
        self._timeOf = timeOf
        self._data = d


class Stats:
    def __init__(self, Val=None):
        if Val != None:
            self.N = Val.N
            self.Sum = Val.Sum
            self.SumSq = Val.SumSq
            self.Begin = Val.Begin
            self.Highest = Val.Highest
            self.Lowest = Val.Lowest
        else:
            self.N = 0
            self.Sum = 0.0
            self.SumSq = 0.0
            self.Begin = True
            self.Highest = 0
            self.Lowest = 0

    def Add(self, X, NoZ=True):
        if X != None:
            if X != 0 or (X == 0 and NoZ == False):
                self.N = self.N + X
                self.Sum = self.Sum + X
                self.SumSq = self.SumSq + (X * X)
                if self.Begin:
                    self.Begin = False
                    self.Highest = X
                    self.Lowest = X

                else:
                    if X > self.Highest:
                        self.Highest = X
                    if X < self.Lowest:
                        self.Lowest = X

    def GetMean(self):
        if self.N:
            return self.Sum / self.N
        return 0

    def GetStd(self):
        if self.N > 1:
            math.sqrt((self.SumSq - ((self.Sum * self.Sum) / self.N)) / (self.N - 1))
        return 0

    def GetLowest(self):
        return self.Lowest

    def GetHighest(self):
        return self.Highest

    def Reset(self):
        self.N = 0
        self.Sum = 0.0
        self.SumSq = 0.0
        self.Begin = True
        self.Highest = 0
        self.Lowest = 0


class CDStats:
    def __init__(self, ignorZ=True):
        self.IgnorZ = ignorZ
        self.stats = Stats

    def Reset(self):
        self.stats.Reset()

    def GetSigma(self):
        return self.stats.GetStd()

    def GetMean(self):
        return self.stats.GetMean()

    def GetHighest(self):
        return self.Highest_Value

    def GetWhereHigestHappened(self):
        return self.Highest_Position

    def GetLowest(self):
        return self.Lowest_Value

    def GetWhereLowestHappened(self):
        return self.Lowest_Position

    def Computer(self, records=[]):
        begin = True
        for i in range(0, len(records)):
            self.stats.Add(records[i], self.IgnorZ)


class DateTime:
    def __init__(self, dateTime=None):
        if dateTime == None:
            self.dateTime = QDateTime.currentDateTime()
        else:
            self.dateTime = QDateTime.fromString(dateTime, "yyyy MM dd hh:mm:ss")

    def SetDateTime(self, dateTime):
        self.dateTime = QDateTime.fromString(dateTime, "yyyy MM dd hh:mm:ss")

    def GetLocalDateTimeStr(self):
        return self.dateTime.toString("yyyy MM dd hh:mm:ss")

    def GetLocalDataTime(self):
        return self.dateTime


class StecPostgres():
    def __init__(self, user="vremsoft", database="vremsoft", hostname="localhost", port=5432, password="vrem2010!"):
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setDatabaseName(database)
        self.db.setHostName(hostname)
        self.db.setPort(int(port))
        self.db.setPassword(password)
        self.db.setUserName(user)
        self.db.setConnectOptions("connect_timeout=5")
        self.db.open()
        # In case driver not loaded, here gives hint
        print(self.db.lastError().text())
        self.database = database
        self.tableName = self.database + "_trendtable"
        self.sub_mode = QSqlTableModel()
        self.sub_mode.setTable(self.tableName)
        self.sub_mode.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.sub_mode.select()

    def ConvertToQVariantList(self, stream):
        var = QDataStream(stream, QIODevice.ReadWrite)
        var.setVersion(QDataStream.Qt_5_0)
        var.setByteOrder(QDataStream.LittleEndian)
        return var.readQVariantList()

    def getTableFromSub(self, sub):
        query = QSqlQuery(self.db)
        select = "SELECT  * FROM  " + self.database + "_trendtable where id_subscriber = " + sub + "';"
        if query.exec(select):
            if query.next():
                return query.value(1)
        return ""

    def getAllTracking(self):
        all = {}
        nrows = self.sub_mode.rowCount()
        for i in range(0, nrows):
            rc = self.sub_mode.record(i)
            subcount = rc.count()

            v1 = str(rc.value(0))
            v2 = str(rc.value(1))
            if v1 and v2:
                all.update({v1: v2})
        return all

    def GetLastDataRecordsFromTrendTable(self, table):

        t = table
        end = str(QDateTime.currentDateTimeUtc().toMSecsSinceEpoch() + 1)
        query = QSqlQuery(self.db)
        #      select = "SELECT * FROM " + t + " where id_datetime <= '" + end + "'"
        select = "SELECT * FROM " + t + " order by id_datetime desc limit 1"
        rec = VremMYSqlRecord

        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = UTC.toLocalTime()
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)

        return rec

    def GetLastDataRecordsFromTrendTableTo(self, table, toLocalTime):
        t = table
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())

        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime <= '" + end + "'"
        rec = VremMYSqlRecord

        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = QDateTime(UTC.toLocalTime())
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)

        return rec

    def GetLastDataRecordsFromTrendTableFromTo(self, table, fromLocalTime, toLocalTime):
        t = table
        begin = str(fromLocalTime.toUTC().toMSecsSinceEpoch())
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())
        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime  >='" + begin + "' and  id_datetime  <='" + end + "'"
        rec = VremMYSqlRecord
        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = QDateTime(UTC.toLocalTime())
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)

        return rec

    def GetAllDataRecordsFromTrendTable(self, table, fromLocalTime, toLocalTime):
        t = table
        begin = str(fromLocalTime.toUTC().toMSecsSinceEpoch())
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())
        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime  >= '" + begin + "' and " + " id_datetime  <='" + end + "'"

        lst = []
        if query.exec(select):
            while query.next():
                utime_t = query.value(0)
                UTC = QDateTime(QDateTime.currentDateTimeUtc())
                UTC.setMSecsSinceEpoch(utime_t)

                _timeOf = QDateTime(UTC.toLocalTime())
                _bs = query.value(1)
                _data = self.ConvertToQVariantList(_bs)
                lst.append(VremMYSqlRecord(_timeOf, _data))
        return lst

    def GetAllDataRecordsFromTrendTableAsMatrix(self, table, fromLocalTime, toLocalTime,
                                                format="yyyy.MM.dd hh:mm:ss AP"):
        t = table
        f = QDateTime.fromString(fromLocalTime, format)
        t = QDateTime.fromString(toLocalTime, format)

        r = self.GetAllDataRecordsFromTrendTable(self, table, f, t)

        lst = []
        for j in range(0, len(r)):
            row = []
            rec = r[j]
            te = str(rec._timeOf.toString())
            row.append(te)
            row = row + rec._data
            lst.append(row)

        return lst

    def ComputeAverage(self, r):

        length = len(r)

        if length == 1:
            rec = r[0]
            return np.array(rec._data)

        SumArray = None

        for j in range(0, length):
            rec = r[j]
            if len(rec._data) > 0:

                sd = np.array(rec._data)
                if SumArray is None:
                    SumArray = np.array(sd)
                else:

                    SumArray = np.vstack([SumArray, sd])

        if SumArray is None:
            return None

        result = np.mean(SumArray, axis=0)
        return result


class StecMySql():
    def __init__(self, user="vremsoft", database="vremsoft", hostname="localhost", port=3306, password="vrem2010!"):
        self.db = QSqlDatabase.addDatabase("QMYSQL")
        self.db.setDatabaseName(database)
        self.db.setHostName(hostname)
        self.db.setPort(int(port))
        self.db.setPassword(password)
        self.db.setUserName(user)
        self.db.setConnectOptions("MYSQL_OPT_CONNECT_TIMEOUT=5;MYSQL_OPT_RECONNECT=true")
        ok = self.db.open()
        if ok:
            print('Success')
        else:
            print(self.db.lastError().text())
        self.database = database
        listOfTables = self.db.tables()
        print(listOfTables)

        if "trendtable" in listOfTables :
            self.tableName = "trendtable"
            self.sub_mode = QSqlTableModel()
            self.sub_mode.setTable(self.tableName)
            self.sub_mode.setEditStrategy(QSqlTableModel.OnManualSubmit)
            self.sub_mode.select()

    def ConvertToQVariantList(self, stream):
        var = QDataStream(stream, QIODevice.ReadWrite)
        var.setVersion(QDataStream.Qt_5_0)
        var.setByteOrder(QDataStream.LittleEndian)
        return var.readQVariantList()

    def getTableFromSub(self, sub):
        query = QSqlQuery(self.db)
        select = "SELECT  * FROM  " + self.database + "_trendtable where id_subscriber = " + sub + "';"
        if query.exec(select):
            if query.next():
                return query.value(1)
        return ""

    def getAllTracking(self):
        all = {}
        nrows = self.sub_mode.rowCount()
        for i in range(0, nrows):
            rc = self.sub_mode.record(i)
            subcount = rc.count()

            v1 = str(rc.value(0))
            v2 = str(rc.value(1))
            if v1 and v2:
                all.update({v1: v2})
        return all

    def GetLastDataRecordsFromTrendTable(self, table):

        t = table
        end = str(QDateTime.currentDateTimeUtc().toMSecsSinceEpoch() + 1)
        query = QSqlQuery(self.db)
        #      select = "SELECT * FROM " + t + " where id_datetime <= '" + end + "'"

        select = "SELECT * FROM " + self.database + "." + t + " where id_datetime <= '" + end + "'"

        rec = VremMYSqlRecord

        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = UTC.toLocalTime()
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)
            return rec

        return None

    def GetLastDataRecordsFromTrendTableTo(self, table, toLocalTime):
        t = table
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())

        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime <= '" + end + "'"
        rec = VremMYSqlRecord

        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = QDateTime(UTC.toLocalTime())
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)

        return rec

    def GetLastDataRecordsFromTrendTableFromTo(self, table, fromLocalTime, toLocalTime):
        t = table
        begin = str(fromLocalTime.toUTC().toMSecsSinceEpoch())
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())
        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime  >='" + begin + "' and  id_datetime  <='" + end + "'"
        rec = VremMYSqlRecord
        if query.exec(select) and query.last():
            utime_t = query.value(0)
            UTC = QDateTime(QDateTime.currentDateTimeUtc())
            UTC.setMSecsSinceEpoch(utime_t)
            rec._timeOf = QDateTime(UTC.toLocalTime())
            bs = query.value(1)
            rec._data = self.ConvertToQVariantList(bs)

        return rec


    def GetAllDataRecordsFromTrendTable(self, table, fromLocalTime, toLocalTime):
        t = table
        begin = str(fromLocalTime.toUTC().toMSecsSinceEpoch())
        end = str(toLocalTime.toUTC().toMSecsSinceEpoch())
        query = QSqlQuery(self.db)
        select = "SELECT * FROM " + t + " where id_datetime  >= '" + begin + "' and " + " id_datetime  <='" + end + "'"

        lst = []
        if query.exec(select):
            while query.next():
                utime_t = query.value(0)
                UTC = QDateTime(QDateTime.currentDateTimeUtc())
                UTC.setMSecsSinceEpoch(utime_t)

                _timeOf = QDateTime(UTC.toLocalTime())
                _bs = query.value(1)
                _data = self.ConvertToQVariantList(_bs)
                lst.append(VremMYSqlRecord(_timeOf, _data))
            return lst

        return None

    def GetAllDataRecordsFromTrendTableAsMatrix(self, table, fromLocalTime, toLocalTime,
                                                format="yyyy.MM.dd hh:mm:ss AP"):
        t = table
        f = QDateTime.fromString(fromLocalTime, format)
        t = QDateTime.fromString(toLocalTime, format)

        r = self.GetAllDataRecordsFromTrendTable(self, table, f, t)

        lst = []
        for j in range(0, len(r)):
            row = []
            rec = r[j]
            te = str(rec._timeOf.toString())
            row.append(te)
            row = row + rec._data
            lst.append(row)

        return lst

    def ComputeAverage(self, r):

        length = len(r)

        if length == 1:
            rec = r[0]
            return np.array(rec._data)

        SumArray = None

        for j in range(0, length):
            rec = r[j]
            if len(rec._data) > 0:

                sd = np.array(rec._data)
                if SumArray is None:
                    SumArray = np.array(sd)
                else:

                    SumArray = np.vstack([SumArray, sd])

        if SumArray is None:
            return None

        result = np.mean(SumArray, axis=0)
        return result




if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Version 1.6.04 Stec Vremsoft SQL Utility")
    # Add the arguments

    parser.add_argument('-t', '--target', metavar='target', required=False, help="Enter Taget To Track")
    parser.add_argument('-a', '--actuator', metavar='actuator', required=False, help="Headbox Tag of actuators")
    parser.add_argument('-d', '--database', metavar='database', required=False, help="mysql or postgres, default postgres")

    parser.add_argument('-s', '--server', metavar='server', required=False, help="Host Name, default localhost")
    parser.add_argument('-l', '--length', metavar='length', required=False, help="length")
    parser.add_argument('-n', '--names',  action='store_true', help="names only")
    parser.add_argument('-b', '--days', metavar='days', required=False, help="Days back default -1")

    args = parser.parse_args()

    names = args.names
    type = args.database
    server = 'localhost'
    actuator = None



    s = args.server
    if s != None :
        server = s

    if type == None :
        type = "mysql"

    if type == "mysql" :
        postgres = StecMySql("vremsoft", "vremsoft", server)
        db = postgres.db
        allie = postgres.getAllTracking()
    else:
        postgres = StecPostgres("vremsoft", "vremsoft", server)
        db = postgres.db
        allie = postgres.getAllTracking()

    if names == True :
        for key in allie:
            t = key
            print(t)
        exit(0)

    target = args.target
    if target is None:
        print("Must have a target to track")
        exit(1)


    actuator = args.actuator

    days = args.days
    if days == None:
        days = -1
    else:
        days = int(days)

    length = args.length



    df = pd.DataFrame()
    st = None
    std = None

    table = allie.get(target, None)
    tableActuator = allie.get(actuator, None)

    if table != None and tableActuator != None:

        try:

            r = postgres.GetLastDataRecordsFromTrendTable(table)
            if r is not None :
                today =  r._timeOf
                before = today.addDays(days)
            else :
                print("Could not reach back: ", target)
                exit(1)


            r = postgres.GetAllDataRecordsFromTrendTable(table, before, today)

            if length is None:
                length = len(r)
            else:
                length = int(length)

            length = min(length, len(r))

            StartFound = None

            dataLen = 0

            for j in range(0, length):
                rec = r[j]
                if StartFound == None:
                    StartFound = rec._timeOf

                dtime = StartFound.secsTo(rec._timeOf)
                StartFound = rec._timeOf

                if dtime > 0 :
                    te = str(rec._timeOf.toString("yyyy MM dd hh:mm:ss"))
                    if j % 500 == 0 :
                        print(j, ": ", rec._data)

                    dataLen = len(rec._data)
                    if dataLen > 0:
                        data = np.array(rec._data)
                        matrix = [dtime, actuator, te]
                        matrix = np.hstack([matrix, data])

                        if st is None:
                            st = matrix
                        else:
                            st = np.vstack([st, matrix])

                    td = rec._timeOf
                    b4 = td.addSecs(-dtime)
                    rA = postgres.GetAllDataRecordsFromTrendTable(tableActuator, b4, td)
                    if rA is not None:
                        if len(rA):
                            sum = postgres.ComputeAverage(rA)
                            recA = rA[0]
                            te = str(recA._timeOf.toString("yyyy MM dd hh:mm:ss"))

                            dataLen = len(recA._data)
                            if dataLen > 0:
                                data = np.array(recA._data)
                                matrix = [dtime, actuator, te]
                                matrix = np.hstack([matrix, data])
                                if std is None:
                                    std = matrix
                                else:
                                    std = np.vstack([std, matrix])

        except:
            print("Error ", target)

    if (st is not None):
        headers = ["Target", "QDateTime", "Seconds"]

        for i in range(0, dataLen):
            headers.append("Zn" + str(i))
        csv = target.replace("/", "_") + ".csv"
        df = pd.DataFrame(st)
        df.to_csv(csv)

    if (std is not None):
        headers = ["Target", "QDateTime", "Seconds"]

        for i in range(0, dataLen):
            headers.append("Zn" + str(i))
        csv = actuator.replace("/", "_") + ".csv"
        df = pd.DataFrame(std)
        df.to_csv(csv)






