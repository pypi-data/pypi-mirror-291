#  Copyright (C) 2021 Vremsoft LLC and/or its subsidiary(-ies).
#  All rights reserved.
#  Contact: Laura Chapman  (edc@vremsoft.com)
#  Commercial Usage
#  Licensees holding valid Vremsoft LLC licenses may use this file in
#  accordance with the License Agreement provided with the
#  Software or, alternatively, in accordance with the terms contained in
#  a written agreement between you and Vremsoft. LLC
#

import pyqtgraph as pg
import numpy as np
import re


try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen


class stdcomplot(QWidget):
    """

    """

    chart = None
    item = None
    #color = 200, 200, 200
    color = QColor(255, 0, 0)
    XName = 'Offsets'
    XUnits = 'Zone'

    YName = 'Drift'
    YUnits = 'DBX'

    parameters = {}

    WidgetParent = None
    graphWidget  = None

    def graph(self, points, x = None, colour = None, clear = None  ):
        """
        :param points:
        :param key:
        :return:
        """
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        if clear == None :
            clear = True

        Max = None
        Min = None
        X = []
        Y = []
        for i in range(0, len(points)):

            if Max is None or points[i] > Max:
                Max = points[i]
            if Min is None or points[i] < Min:
                Min = points[i]

            Y.append(float(points[i]))
            if x is None :
                X.append(float(i + 1))

        if x != None :
            X = x

        if Max is not None and Min is not None:

            if self.graphWidget is not None and clear == True:
                 self.graphWidget.clear()

            p1 = self.graphWidget.plot()

            if colour == None :
                p1.setPen(pg.mkPen(self.color))
            else:
                p1.setPen(pg.mkPen(colour))

            p1.setData(X, Y)

    def __init__(self, parant,  prams = {}  ):

        self.parameters= prams
        super().__init__(parant)

        self.color =  self.parameters.get("color", self.color)
        self.XName =  self.parameters.get("xname", self.XName)
        self.XUnits = self.parameters.get("xunits", self.XUnits)
        self.YName  = self.parameters.get("yname", self.YName)
        self.YUnits = self.parameters.get("yunits", self.YUnits)
        self.WidgetParent = parant

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        if self.graphWidget is None:
            self.graphWidget = pg.PlotWidget(self.WidgetParent)
            self.WidgetParent.setWidget(self.graphWidget)
            self.graphWidget.setLabel('bottom', self.XName, self.XUnits)
            self.graphWidget.setLabel('left', self.YName, self.YUnits)
            self.graphWidget.show()
            self.WidgetParent.show()


    def DrawControl(self, vals, x : None  ):
        """
        :param mainproject:
        :param item:
        :param command:
        :return:
        """
        if isinstance(vals, np.ndarray):
            if self.graphWidget != None :
                self.graphWidget.clear()

            if vals.ndim == 1 :
                r = vals.tolist()
                self.chart = self.graph(r, x,None, False)
            else:

                inc = 0
                for row in vals :
                    r = row.tolist()
                    color = (200 - inc), inc, inc
                    self.chart = self.graph(r, x, color, False)
                    inc = inc + 20


        else:
            self.chart = self.graph(vals, x)

        return None


