import argparse
import random

import numpy as np
import time
from six.moves import range


"""
    This is where Stec misc control objects are kept
"""

class ExpFilter :
    """
    Exponetial filter
    """
    FI = 1.0
    FV = None
    reset = True

    def __init__(self, FI : float = .20):
        """
        .01 to 1 where 1 in no filter
        default is .2
        """
        self.FV = 0.0
        self.reset = True
        self.FI = FI

    def Reset(self):
        """
        clean out history
        """
        self.reset = True

    def XtoC(self, X : float):
        """
        in with value return filtered value
        """
        if self.reset is True :
            self.FV = X
            self.reset = False

        else:
            fi = (1 - self.FI)
            self.FV = np.add(np.multiply(self.FV, fi), np.multiply(X,self.FI))

        return self.FV

    def Control(self, X : float):
        """
        Conforms to control method
        """
        return self.XtoC(X)

    def SetFI(self, FI : float = 1):
        """
        sets to new FI
        """
        self.FI = FI

    def Reset(self):
        """
        clean out history
        """
        self.FV = None
        self.reset = True





    def Control(self, X : np.array):
        """
        Conforms to control method
        """
        return self.XtoC(X)

    def SetFI(self, FI: float = 1):
        """
        sets to new FI
        """
        self.FI = FI


class RollingAverageFilter :
    """
    rolling average filter
    """
    nbrSamples=5
    Samples=[]

    def __init__(self, nbrSamples : int = 5):
        """
        number of samples to use for filter
        default is 5
        """
        self.nbrSamples = nbrSamples

    def Reset(self):
        """
        clears history
        """
        self.Samples.clear()

    def XtoC(self, X: float):
        self.Samples.insert(0,X)

        if len(self.Samples > self.nbrSamples) :
            self.Samples.pop(len(self.Samples)  -1 )

        FV = sum(self.Samples) / len(self.Samples)

        return FV

    def Control(self, X:float ):
        """
        Conforms to control method
        """
        return self.XtoC(X)



class Dahlin :
    """
    simple Dahlin controller, if you don't like the PID controller
    """
    G = 1.0
    TC = 30
    LAMBDA = 1
    Em1 = 0.0
    now = time.time()
    then = now
    reset = True
    T = 0.0

    def __init__(self, TC: float = 15.0, LAMBDA : float = .1, GAIN : float = 1):
        """
        :param: TC
        :param: Lambda
        :param: Gain
        First order Dahlin Control
        """
        self.G = GAIN
        self.TC = TC
        self.LAMBDA = LAMBDA
        self.Em1 = 0.0
        self.now = time.time()
        self.then = self.now
        self.reset = True

    def Reset(self):
        """
        clears history
        """
        self.Em1 = 0.0
        self.reset = True


    def Control(self, X : float ):
        """
        :param: error for controller

        in with error from 0, where 0 is the target,
        return controller output
        """

        self.now = time.time()

        if self.reset is True :
            self.then = self.now
            self.reset = False

        seconds = self.now - self.then

        if seconds == 0:
            T = float(.0001)
        else:
            T = float(seconds)

        self.then = self.now

        L = 1 - np.exp(-T / self.TC)
        Q = 1 - np.exp(-self.LAMBDA * T)
        K = Q / (L * self.G)
        En = X
        X = K * ( En - (1-L) * self.Em1)
        self.Em1 = En
        return X

    def ControlWithSpPv(self, spt: float, pv: float):
        """
        :param: spt
        :param: pv

        Does Control with setpoint and process value, rather than delta..

        """
        delta = spt - pv
        return self.Control(delta)

    def Time(self):
        return self.now

    def GetError(self, sp: float, pv: float):
        """
        :param : sp or setpoint
        :param : pv or value
        returns the sp - pv
        """
        e_n = sp - pv
        return e_n





class PID(object):
    """
    Simple PID control.
    """

    def __init__(self, p=0, i=0, d=0, **kwargs):

        self._get_time = kwargs.pop('get_time', None) or time.time

        # initialze gains
        self.Kp = p
        self.Ki = i
        self.Kd = d

        # The value the controller is trying to get the system to achieve.
        self._target = 0

        # initialize delta t variables
        self._prev_tm = self._get_time()

        self._prev_feedback = 0

        self._error = None

    def Reset(self):
        # initialize delta t variables
        self._prev_tm = self._get_time()
        self._prev_feedback = 0
        self._error = None

    @property
    def error(self):
        return self._error

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, v):
        self._target = float(v)

    def __call__(self, feedback, curr_tm=None):
        """ Performs a PID computation and returns a control value.

            This is based on the elapsed time (dt) and the current value of the process variable
            (i.e. the thing we're measuring and trying to change).

        """

        # Calculate error.
        error = self._error = self._target - feedback

        # Calculate time differential.
        if curr_tm is None:
            curr_tm = self._get_time()
        dt = curr_tm - self._prev_tm

        # Initialize output variable.
        alpha = 0

        # Add proportional component.
        alpha -= self.Kp * error

        # Add integral component.
        alpha -= self.Ki * (error * dt)

        # Add differential component (avoiding divide-by-zero).
        if dt > 0:
            alpha -= self.Kd * ((feedback - self._prev_feedback) / float(dt))

        # Maintain memory for next loop.
        self._prev_tm = curr_tm
        self._prev_feedback = feedback
        return alpha


class PIDClassic :
    """
    Classic PID, uses pv and sp
    """
    Kc = 6.0
    tauI = 75.0  # sec
    tauD = 0.0  # sec

    ierr = 0.0
    pv_last = 0.0
    op0 = 0.0

    lastTime=None


    def __init__(self, Kc : float = 2, tauI : float  = 10, tauD : float = 0):
        self.Kc = Kc
        self.tauI = tauI
        self.tauD = tauD

        self.KP = Kc
        self.KI = Kc / tauI
        self.KD = Kc * tauD
        self.ierr = 0.0
        self.pv_last = 0.0

    def Reset(self):
        """
        resets the control
        """
        self.ierr = 0.0
        self.pv_last = 0.0
        self.lastTime = None

    def Control(self, sp : float = 0, pv : float = 0 ):

        op0 = 0.0

        # calculate the error
        error = sp - pv

        tm = time.time()
        if self.lastTime is None :
            self.lastTime = tm

        dt = tm - self.lastTime
        self.lastTime = tm

        # calculate the integral error
        self.ierr = self.ierr + self.KI * error * dt

        # calculate the measurement derivative
        if dt >= 1e-8:
            dpv = (pv - self.pv_last) / dt
        else:
            dpv = 0.0;

        # calculate the PID output
        P = self.KP * error
        I = self.ierr
        D = -self.KD * dpv
        op = op0 + P + I + D

        self.pv_last = pv

        # implement anti-reset windup
        I = I - self.KI * error * dt

        # return the controller output and PID terms
        return [op, P, I, D]




class ComputerSL:

    """
    computers the slope and intercept for interpolation of history array
    """
    def __init__(self, X1,X2, Y1,Y2):
        self.s = (Y2 - Y1) / (X2 - X1)
        self.i =  Y1 - (self.s * X1)

    def Y(self, X):
        c = (X * self.s) + self.i
        return c

    def X(self, Y):
        c = None
        if self.s != 0.0 :
            c = (Y -self.i) / self.s

        return c


class HistoryQue :

    """
    This is not a history array, but rather a history queue.. it returns sum of everything > than tau, and deletes portion after the sum
    This can be used to create a model
    """
    history = []
    speed = 1000.0
    tau = 45.0


    def __init__(self, tau: float = 45, speed : float = 1000):
        """
        :param: tau the tau of the history queue to retain
        """
        self.history = []
        self.tau = tau

    def Control(self, v : float = 0):
        """
        :param:  value, returns the sum of all inputs above tau, then removes all values above tau
        """
        tm = time.time()
        pair = (tm, v)
        self.history.insert(0, pair)

        marker = None
        for i in range(0, len(self.history ) ) :
            tm1, v1 = self.history[i]
            df1 = tm - tm1
            if df1 > self.tau:
                marker = i
                break
        sum = 0.0
        if marker is not None :
            for i in range(marker, len(self.history)) :
                tm1, v1 = self.history[i]
                sum = sum + v1
            de = len(self.history) - marker
            self.history = self.history[:-de]

        return sum

    def setNewTau(self, tau):
        self.tau = tau

class HistoryQueRate :

    """
    This is not a history array, but rather a history queue.. it returns sum of everything > than tau, and deletes portion after the sum
    This can be used to create a model
    """
    history = []

    tau = 45.0
    r = None


    def __init__(self, tau: float = 45):
        """
        :param: tau the tau of the history queue to retain
        """
        self.history = []
        self.tau = tau
        r = None

    def Control(self, v : float = 0,  r : float = 5):
        """
        :param:  value, returns the sum of all inputs above tau, then removes all values above tau
        """
        if self.r is None :
            self.r = 0.0

        else:
            self.r = self.r + r

        tm = self.r

        pair = (tm, v)
        self.history.insert(0, pair)

        marker = None
        for i in range(0, len(self.history ) ) :
            tm1, v1 = self.history[i]
            df1 = tm - tm1
            if df1 > self.tau:
                marker = i
                break
        sum = 0.0
        if marker is not None :
            for i in range(marker, len(self.history)) :
                tm1, v1 = self.history[i]
                sum = sum + v1
            de = len(self.history) - marker
            self.history = self.history[:-de]

        return sum

    def setNewTau(self, tau):
        self.tau = tau




class HistoryDelay :
    """
    This is a history array, it will work with either number storage IE steps, or if tau is not None, then it will work off of Tau
    It is meant as to not store more than necessary if tau is given.. if steps are used, then storage will be in steps and the use must ensure
    then number of steps is suffecient to store what is needed.
    No Block rate is needed, this works of actual seconds.
    """
    history = []
    historyLimit = 40
    tau = None
    interval = None
    interpolate = True

    def __init__(self, steps : int = 40, tau : float = None, interpolate = True):
        """
        :param: steps or number to save if tau is not entered
        :param: tau, this overides steps, and it seconds are entered, this will be the optimimized of history array
        :param: interpolate, if set to true, this allows an abstract to be created if the requested is segmented ... this most like should be set to Fase for F25
        """
        self.historyLimit = 40
        self.history = []
        self.tau = tau
        self.interpolate = interpolate


    def Insert(self, v):
        tm = time.time()
        pair = (tm,v)
        self.history.insert(0,pair)
        if self.tau is None :
            if len(self.history) > self.historyLimit :
                self.history.pop(len(self.history) -1 )
        else:
            for i1 in  range(0, len(self.history)) :
                tm1, v1 = self.history[i1]
                df1 = tm - tm1
                if df1 > self.tau :
                    i2 = i1 + 1
                    if i2 < len(self.history) :
                        del self.history[len(self.history) - i2 : ]
                    return



    def ComputeSumToPosition(self, seconds,  multi : float = 1):
        sum = 0.0
        tm = time.time()
        for i in range(0, len(self.history)) :

            t, v = self.history[i]
            df = tm - t

            if df <= seconds :
                sum = sum + (v * multi)

            else:
                if i >= 1 and self.interpolate == True:

                    t1, v1 = self.history[i - 1]

                    df2 = df
                    df1 = tm - t1

                    nv  = ComputerSL(df1,df2,v,v1)
                    computedV = nv.Y(seconds)
                    sum = sum + ( computedV * multi)

                return sum

        return sum

    def ComputeListToPosition(self, seconds, Q : float =  1):
        tm = time.time()
        sum = 0.0

        lastT = 0.0
        N = 0

        for i in range(0, len(self.history)):

            t, v = self.history[i]
            df = tm - t

            N = i
            if df <= seconds:
                lastT = v * Q
                sum = sum + lastT


            else:
                if i >= 1 and self.interpolate == True:
                    t1, v1 = self.history[i - 1]

                    df2 = df
                    df1 = tm - t1
                    nv = ComputerSL(df1, df2, v, v1)
                    computedV = nv.Y(seconds)
                    lastT =  ( computedV * Q)

                return sum, lastT, i

        return sum, lastT, N



class HistoryDelayQueRate :
    """
    This is a history array, it will work with either number storage IE steps, or if tau is not None, then it will work off of Tau
    It is meant as to not store more than necessary if tau is given.. if steps are used, then storage will be in steps and the use must ensure
    then number of steps is suffecient to store what is needed.
    No Block rate is needed, this works of actual seconds.
    """

    history = []
    historyLimit = 40
    tau = None
    interval = 5
    interpolate = True
    tm = None

    def __init__(self, rate: int = 5, tau: float = None, interpolate=True):
        """
        :param: steps or number to save if tau is not entered
        :param: tau, this overides steps, and it seconds are entered, this will be the optimimized of history array
        :param: interpolate, if set to true, this allows an abstract to be created if the requested is segmented ... this most like should be set to Fase for F25
        """

        self.history = []
        self.tau = tau
        self.interpolate = interpolate
        self.interval = rate
        self.tm = None

    def Insert(self, v):

        if self.tm is None:
            tm = time.time()
            self.tm = tm
        else:
            tm = self.tm + self.interval
        pair = (tm, v)
        self.history.insert(0, pair)
        self.tm = tm

        if self.tau is None:
            if len(self.history) > self.historyLimit:
                self.history.pop(len(self.history) - 1)
        else:
            for i1 in range(0, len(self.history)):
                tm1, v1 = self.history[i1]
                df1 = tm - tm1
                if df1 > self.tau:
                    i2 = i1 + 1
                    if i2 < len(self.history):
                        del self.history[len(self.history) - i2:]
                    return

    def ComputeSumToPosition(self, seconds, multi: float = 1):
        sum = 0.0
        tm = time.time()
        for i in range(0, len(self.history)):

            t, v = self.history[i]
            df = tm - t

            if df <= seconds:
                sum = sum + (v * multi)

            else:
                if i >= 1 and self.interpolate == True:
                    t1, v1 = self.history[i - 1]

                    df2 = df
                    df1 = tm - t1

                    nv = ComputerSL(df1, df2, v, v1)
                    computedV = nv.Y(seconds)
                    sum = sum + (computedV * multi)

                return sum

        return sum

    def ComputeListToPosition(self, seconds, Q: float = 1):
        tm = time.time()
        sum = 0.0

        lastT = 0.0
        N = 0

        for i in range(0, len(self.history)):

            t, v = self.history[i]
            df = tm - t

            N = i
            if df <= seconds:
                lastT = v * Q
                sum = sum + lastT


            else:
                if i >= 1 and self.interpolate == True:
                    t1, v1 = self.history[i - 1]

                    df2 = df
                    df1 = tm - t1
                    nv = ComputerSL(df1, df2, v, v1)
                    computedV = nv.Y(seconds)
                    lastT = (computedV * Q)

                return sum, lastT, i

        return sum, lastT, N


import operator
class F25(HistoryDelay) :
    """
    F25 Lambda tuned Algorith
    """

    G = None
    TC = None
    LAMBDA = None
    TAU = None
    TC = None

    e_m_1 = 0.0
    y_m_1 = 0.0
    lastTime = None

    def __init__(self, G : float,  LAMBDA : float, TC : float, TAU : float,  steps: int = 40, interpolate = False ):
        """
        :param : G gain ...
        :param: LAMBDA
        :param: TC Time Constant
        :param: TAU
        :param: steps   is really not used, it is for history storage, but this algorithm uses tau and tc to efficently project storage
        """
        super().__init__(steps, (TC + TAU), interpolate)
        self.G = G
        self.TC = TC
        self.LAMBDA = LAMBDA
        self.TAU = TAU
        self.e_m_1 = 0.0
        self.y_m_1 = 0.0
        self.lastTime = None

    def Control(self, deletaError : float):
        """
        :param: Value or error for the controller 0 is always the target so the value is delta to 0, it is the error
        :param: setpoint  if set to None, then value parameter is used
        :param:  processvalue if set to None, then value parameter is used
        returns control move
        """

        if self.lastTime is None :
            self.lastTime = time.time()

        nowTime = time.time()

        dfTime = nowTime - self.lastTime
        self.lastTime = nowTime
        if dfTime == 0:
            T = float(.0001)
        else:
            T = float(dfTime)

        M = self.TAU / T

        Q = 1 - np.exp(-self.LAMBDA * T)
        L = 1 - np.exp(-T / self.TC)
        K = Q / (L * self.G)

        APrime = -(1 - L)
        SMY, YNEM1, N  = self.ComputeListToPosition( self.TAU, -Q)
        Y = YNEM1 * (-M*Q) + SMY + K * ( deletaError  + APrime * self.e_m_1)
        self.e_m_1 = deletaError
        self.Insert(Y)
        return Y

    def ControlWithSpPv(self, spt : float, pv : float):
        """
        :param: spt
        :param: pv

        Does Control with setpoint and process value, rather than delta..

        """
        delta = spt - pv
        return self.Control(delta)

    def GetError(self, sp: float, pv: float):
        """
        :param : sp or setpoint
        :param : pv or value
        returns the sp - pv
        """
        e_n = sp - pv
        return e_n

    def Reset(self):
        """
        reset, normally just make a new controller, but if you want you can reset
        """
        self.lastTime = None
        self.e_m_1 = 0.0
        self.y_m_1 = 0.0

    def SetGain(self, gain: float):
        self.G = gain

    def SetLambda(self, lamb: float):
        self.LAMBDA = lamb

    def SetTc(self, tc: float):
        self.TC = tc
        self.tau = tc + self.TAU

    def SetTau(self, tau: float):
        self.TAU = tau
        self.tau = self.TC + tau


class F25QueRate(HistoryDelayQueRate ) :
    """
    F25 Lambda tuned Algorith
    """

    G = None
    TC = None
    LAMBDA = None
    TAU = None
    TC = None

    e_m_1 = 0.0
    y_m_1 = 0.0
    lastTime = None
    rate = 5

    def __init__(self, G : float,  LAMBDA : float, TC : float, TAU : float,  rate: int = 5, interpolate = False ):
        """
        :param : G gain ...
        :param: LAMBDA
        :param: TC Time Constant
        :param: TAU
        :param: steps   is really not used, it is for history storage, but this algorithm uses tau and tc to efficently project storage
        """
        super().__init__(rate, (TC + TAU), interpolate)
        self.G = G
        self.TC = TC
        self.LAMBDA = LAMBDA
        self.TAU = TAU
        self.e_m_1 = 0.0
        self.y_m_1 = 0.0
        self.lastTime = None
        self.rate = rate

    def Control(self, deletaError : float):
        """
        :param: Value or error for the controller 0 is always the target so the value is delta to 0, it is the error
        :param: setpoint  if set to None, then value parameter is used
        :param:  processvalue if set to None, then value parameter is used
        returns control move
        """

        if self.lastTime is None :
            self.lastTime = time.time()
            nowTime = self.lastTime
        else:
            nowTime = self.lastTime + self.rate

        dfTime = nowTime - self.lastTime
        self.lastTime = nowTime

        if dfTime == 0:
            T = float(.0001)
        else:
            T = float(dfTime)

        M = self.TAU / T

        Q = 1 - np.exp(-self.LAMBDA * T)
        L = 1 - np.exp(-T / self.TC)
        K = Q / (L * self.G)

        APrime = -(1 - L)
        SMY, YNEM1, N  = self.ComputeListToPosition( self.TAU, -Q)
        Y = YNEM1 * (-M*Q) + SMY + K * ( deletaError  + APrime * self.e_m_1)
        self.e_m_1 = deletaError
        self.Insert(Y)
        return Y

    def ControlWithSpPv(self, spt : float, pv : float):
        """
        :param: spt
        :param: pv

        Does Control with setpoint and process value, rather than delta..

        """
        delta = spt - pv
        return self.Control(delta)

    def GetError(self, sp: float, pv: float):
        """
        :param : sp or setpoint
        :param : pv or value
        returns the sp - pv
        """
        e_n = sp - pv
        return e_n

    def Reset(self):
        """
        reset, normally just make a new controller, but if you want you can reset
        """
        self.lastTime = None
        self.e_m_1 = 0.0
        self.y_m_1 = 0.0


class F21 :
    """
    Simple PI controller that works off error, that implies block rate as a constant and is not needed
    """
    e_n_1 = 0.0
    K = 0
    A1 = 0
    max = None
    min = None
    deadZone = None

    def __init__(self, K : float = 1,
                 tauI : float = 0,
                 min : float = None,
                 max : float = None,
                 deadZone : float = None) :
        """
        :param K:     gain term, the P term
        :param tauI:  I term
        :param min:    min clamp of controller output
        "param max:    max output of controller

        """
        self.e_n_1 = 0.0
        self.K = K
        self.A1 = tauI
        self.min = min
        self.max = max
        self.deadZone = deadZone

    def Control(self, e_n : float = 0):
        """
        :param : error this is the sp - pv
        return the controller output
        """

        if self.deadZone is not None:
            if abs(e_n) < self.deadZone:
                error = 0

        copt = (self.K * (e_n + (self.A1 * self.e_n_1) ))
        self.en_1 = e_n


        if self.max is not None :
            if copt > self.max :
                copt = self.max
        if self.min is not None :
            if copt < self.min :
                copt = self.min

        return copt

    def ControlWithSpPv(self, spt: float, pv: float):
        """
        :param: spt
        :param: pv
        Does Control with setpoint and process value, rather than delta..
        """
        e_n = spt - pv
        if self.deadZone is not None :
            if abs(e_n) < self.deadZone:
                e_n = 0

        return self.Control(e_n)


    def GetError(self, sp : float, pv : float ):
        """
        :param : sp or setpoint
        :param : pv or value
        :returns: the sp - pv with deadZone is set not to None
        """
        e_n = spt - pv
        if self.deadZone is not None:
            if abs(e_n) < self.deadZone:
                e_n = 0
        return e_n

    def Reset(self):
        """
        resets the controller
        """
        self.en_1 = float(0.0)



try:
    from stdcomQtargs import stdcomQtargs as arguments
except :
    from stdcomQt.stdcomQtargs import stdcomQtargs as arguments

class MapToZones() :
    """
    args = edge_allow_0=True   allows 0's at the edges
           middle_allow_0=False allows 0's in the middle
           start_s=1   starting slice number or databox number
           end_s=20    ending slice number of databox number
           left_s=1    if rev with right_s then porfile is to be reversed
           right_s=20
           offset=0.0    offset in units of total_s_width actuator to headbox
           total_s_width=100   total slice width or headbox width
           min_d_width=6    units of total_s_width, the min actuator wisth
           d_count=10       number of actuators

           maps profile from scanner to actuator zones

    """

    edge_allow_0 = True
    middle_allow_0 = False
    start_s = int(1)
    end_s =  int(20)
    left_s = int(1)
    right_s = int(20)
    offset = float(0)
    total_s_width = float(100)
    min_d_width = float(6)
    d_count = int(10)
    shrinkage = [1.0] * d_count
    zerocheck = 1
    THRESHOLD = float(.0000001)
    MAXVAL = float(1.0E38)

    def __init__(self, args):
        if type(args).__name__ == "dict":

            self.edge_allow_0 = args.get('edge_allow_0', self.edge_allow_0)
            self.middle_allow_0 = args.get('middle_allow_0', self.middle_allow_0)
            self.start_s = args.get('start_s', self.start_s)
            self.end_s = args.get('end_s', self.end_s)
            self.left_s = args.get('left_s', self.left_s)
            self.right_s = args.get('right_s', self.right_s)
            self.offset = args.get('offset', self.offset)
            self.total_s_width = args.get('total_s_width', self.total_s_width)
            self.min_d_width = args.get('min_d_width', self.min_d_width)
            self.d_count = int(args.get('d_count', self.d_count))
            self.shrinkage = args.get('shrinkage', self.shrinkage)
            self.zeroCheck = args.get('zerocheck',  self.zerocheck )
        else:
            print("No Parameter Passed")
    def setOffset(self, offset : float ):
        self.offset = offset

    def Offset(self):
        return self.offset

    def setTotalWidth(self, total_width : float):
        self.total_s_width = total_width

    def TotalWidth(self):
        return self.total_s_width

    def DCount(self):
        return self.d_count

    def MinDWidth(self):
        return self.min_d_width

    def setShrinkage(self, shrinkage, zoneIndex : int = None  ):
        """
        No can use list or one by one
        """
        if type(shrinkage) == list :
            self.shrinkage = shrinkage

        elif zoneIndex == None :
            zoneIndex = 0

            if zoneIndex >= 0 & zoneIndex < len(self.shrinkage) :
                self.shrinkage[zoneIndex] = shrinkage

    def Shrinkage(self, zoneIndex : int = None):

        if zoneIndex == None :
            return self.shrinkage

        elif zoneIndex >= 0 & zoneIndex < len(self.shrinkage):
            return self.shrinkage[zoneIndex]
        return None

    def CheckBound(self, left, right, start, end, invert):
        if invert == 1:
            left += self.THRESHOLD
            right -= self.THRESHOLD
        else:
            left -= self.THRESHOLD
            right += self.THRESHOLD
        if left <= start:  # out on start side
            if right >= (end + 1):  # & on end side */
                return 5
            elif right <= start:
                return 3  # completely out on start side */
            else:
                return 1  # partially out on start side */
        elif left >= (end + 1):  # out on end side */
            if right <= start:  # & on start side */
                return 5
            elif right >= (end + 1):
                return 4  # completely out on end side */
            else:
                return 2  # partially out on end side */
        else:
            if right <= start:
                return 1  # partially out on start side */
            elif right >= (end + 1):
                return 2  # partially out on end side */
            else:
                return 0  # in bounds */

    def ZeroCheck(self, src):
        data = []
        for x in range(0, len(src)):
            if (src[x] < 0.0):
                src[x] = 0.0
        return src


    def Control(self, source, offsetOptional : float = None, Shrinkage = None ):
        """
        Enter with profile, return with profile mapped to zone
        """

        if source is None :
            return None

        src =  source.copy()

        if Shrinkage == None :
            shrinkage = self.shrinkage
        else:
            if type(Shrinkage) == list :
                shrinkage = Shrinkage
            else :
                shrinkage = [float(Shrinkage)] * self.d_count

        self.inv = 1


        if offsetOptional is None :
            offset = self.offset
        else:
            offset = offsetOptional

        self.num_s = abs(self.end_s - self.start_s) + 1

        if (self.left_s > self.right_s):
            self.inv = -1

        interm = abs(self.right_s - self.left_s)
        interm += 1
        self.s_width = self.total_s_width / interm
        self.step = self.inv * self.min_d_width / self.s_width
        self.right_edge = self.left_s + self.inv * (offset / self.s_width)
        if self.inv == -1:
            self.right_edge += 1.

        dest = [0.0] * self.d_count

        right = left = 0
        if self.zerocheck == 1 :
            src = self.ZeroCheck(src)
        s = 0
        lcstart_s = self.start_s

        s -= lcstart_s

        lcend_s = self.end_s

        right_edge = self.right_edge
        left_edge = right_edge

        for x in range(0, self.d_count):
            left_edge = right_edge  # next d in s space * /
            if len(self.shrinkage) >= self.d_count:
                right_edge += self.step * self.shrinkage[x]
            else:
                right_edge += self.step

            bounds = self.CheckBound(left_edge, right_edge, lcstart_s, lcend_s, self.inv)

            if bounds == 0:  # completely in bounds
                left = left_edge
                right = right_edge

            elif bounds == 1:  # partially out on start side
                if self.inv == 1:
                    left = lcstart_s
                    right = right_edge
                else:
                    left = left_edge
                    right = lcstart_s

            elif bounds == 2:  # partially out on end side
                if self.inv == 1:
                    left = left_edge
                    right = lcend_s + 1
                else:
                    left = lcend_s + 1
                    right = right_edge

            elif bounds == 3:  # completely out on start side
                left = lcstart_s
                right = lcstart_s + 1

            elif bounds == 4:  # completely out on end side
                left = lcend_s
                right = lcend_s + 1

            elif bounds == 5:  # completely out of bounds
                left = lcstart_s
                right = lcend_s + 1

            if left > right:  # inverted so right edge is less than left
                temp = left  # swap to do summation * /
                left = right
                right = temp

            if bounds == 3 or bounds == 4:
                dest[int(x)] = 0.

            else:
                j = int(left)
                k = int(right)
                min = self.MAXVAL
                max = 0.0
                sum = 0.0
                divisor = abs(right - left)

                value = src[int(j + s)]  # sum or max / min an edge * /
                sum += (j + 1 - left) * value
                # .....................................................................

                if (j == k):  # d lies completely within a single s * /
                    divisor = (k + 1) - left
                else:
                    if (k + s) >= len(src):
                        value = 0.0
                    else:
                        value = src[int(k + s)]

                    sum += (right - k) * value

                    m = j + 1

                    for m in range(j + 1, k):
                        if (m >= len(src)):
                            divisor -= 1.

                        else:
                            sum += src[int(m)]

                if divisor > self.THRESHOLD:  # check valid divisor * /
                    dest[int(x)] = sum / divisor  # * new  average in d * /
                else:
                    dest[int(x)] = dest[int(x - 1)]  # use the adjacent value

        return dest



if __name__ == '__main__':


    """
    test on PIDClassic
    """
    sleepTime = 5.0


    #error = 40
    #f21 = F21(-.2,50)
    #for i in range(0,50) :
        #e = f21.Control(error)
        #error = error + e
        #print(e, ":", error)
        #time.sleep(sleepTime)



    databoxes = [ 1,2,3,4,5,6,7,8,9,10]
    parameters= [ "start_s=1", "end_s=10", "left_s=1", "right_s=10", "offset=3", "total_s_width=120", "min_d_width=2", "d_count=40"  ]

    mapclass = MapToZones(parameters)

    key = mapclass.Control(databoxes)
    print(key)
    #for i, item in enumerate(key, start=1):
        #print(i, item)

    # TODO: 'min_d_width' set to 12 or larger, or 'offset' larger than 9, will get error
    argsDict = {'start_s': 1, 'end_s': 10, 'left_s': 1, 'right_s': 10, 'offset': 8, 'total_s_width': 120, 'min_d_width': 11, 'd_count': 8}
    argsDict['shrinkage'] = [1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5]
    mapclass_2 = MapToZones(argsDict)
    key = mapclass_2.Control(databoxes)
    print(key)

    NPTS = 100
    parmeters = {'start_s': 1,
                 'end_s': NPTS,
                 'left_s': 1,
                 'right_s': NPTS,
                 'offset': 50,
                 'total_s_width': NPTS * 10,
                 'd_count': NPTS,
                 'min_d_width': 1,
                 'shrinkage': [1.0] * NPTS,
                 'zerocheck': 1
                 }
    mp = MapToZones(parmeters)

    zones = [1.0] * NPTS


    print('Mr Wang plase Look Zones Before :', zones)
    zones = mp.Control(zones)
    print('Mr Wang this should be 0,s to start Zones After: ', zones)

    """
    f25 = F25( -1, .018, 1, 40, 40)
    spt = 0
    value = 40
    hl = [0] * 9
    T1 = []
    Q1 = []
    t = []
    Tsp1 = []

    for i in range(0,50):
        v = f25.ControlWithSpPv(0,value)
        hl.insert(0,v)
        hl.pop(len(hl) - 1)
        value = value + hl[len(hl) - 1]
        print(i, ":" ,v,":", value)
        time.sleep(sleepTime)
        t.append(i * sleepTime)
        T1.append(value)
        Q1.append(v)
        Tsp1.append(float(0) )

    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.DataFrame()
    df['Q1'] = Q1[:i]
    df['Q1'].fillna(0, inplace=True)
    df['T1'] = T1[:i]
    df['Tsp'] = Tsp1[:i]
    df.to_csv('F25Trainig.csv', index=False)


    n = 50
    tm = np.linspace(0, n - 1, n)
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot([0, tm[-1] / 60.0], [50, 50], 'k-', label=r'$T_1$ SP')
    plt.plot(t, T1, 'r.', label=r'$T_1$ PV')
    plt.ylabel(r'Eng Value ($^oC$)')
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.grid()
    plt.plot(t, Q1, 'b-', label=r'$Q_1$')
    plt.ylabel(r'Actuator (%)');
    plt.xlabel('Time (Seconds)')
    plt.legend()
    plt.show()
    """




