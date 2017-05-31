import numpy as np

class Tek7104(object):
    def __init__(self,inst):
        self.inst = inst

    def fetch_spectrum(self,trace,offset=False):
        self.inst.write('*CLS')
        self.inst.write('DAT:ENCDG ASCII')
        self.inst.write('DAT:SOU CH{}'.format(trace))
        self.inst.write('DAT:STOP 250000')
        self.inst.write('WAVF?')
        #WAVF? returns the results of CURV? and WFMO?.  WFMO? has the 
        #relevant list parameters:
        #[6]: POINTS, [8]: XUNIT, [9]:XUNIT/PT,[10]: XZERO,[12]:YUNIT,
        #[13]:YMULT,[14]:YOFFSET
        #[17] is the result of the CURV? command, which is the raw data from 
        #the scope with encoding DAT:ENCDG
        result=self.inst.read().split(';')
        x=[(float(i)+float(result[10]))*float(result[9]) for i in range(int(result[6]))]
        y=[(float(val)-float(result[14]))*float(result[13]) for val in result[17].split(',')]
        if offset:
            y=[float(val)*float(result[13]) for val in result[17].split(',')]
        return np.array(x),result[8].strip('"'),np.array(y),result[12].strip('"') #x,xunit,y,yunit

class Tek3034(object):
    def __init__(self,inst):
        self.inst = inst

    def fetch_spectrum(self, trace, offset=False):
        self.inst.write('*CLS')
        self.inst.write('DAT:ENCDG ASCII')
        self.inst.write('DAT:SOU CH{}'.format(trace))
        self.inst.write('DAT:SART 1')
        self.inst.write('DAT:STOP 10000')
        raw=np.array(self.inst.query_ascii_values('CURV?'))
        ymult=float(self.inst.ask('WFMP:YMULT?'))
        yoff=float(self.inst.ask('WFMP:YOFF?'))
        yzero=float(self.inst.ask('WFMP:YZERO?'))
        if offset is True:
            y=(raw)*ymult + yzero
        else:
            y=(raw-yoff)*ymult + yzero
        xinc=float(self.inst.ask('WFMP:XINC?'))
        xzero=float(self.inst.ask('WFMP:XZERO?'))
        pts=int(self.inst.ask('WFMP:NR_PT?'))
        x=np.linspace(xzero,xzero+pts*xinc,pts)
        return x,y
