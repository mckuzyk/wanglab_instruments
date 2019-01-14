import numpy as np

class LecroyWaverunner(object):
    def __init__(self, inst):
        self.inst = inst
        self.inst.write('comm_format def9,word,bin')
        self.preamble = 21 # bytes in waveform preamble

    def __repr__(self):
        return 'LecroyWaverunner({!r})'.format(self.inst)

    def catBytes(self, byteSequence):
        numBytes = len(byteSequence)
        maxVal = 2**(8*numBytes-1) - 1
        unsignedInt = 0
        byteVals = [int(i) for i in byteSequence]
        index = 0
        for i in byteVals[::-1]:
            unsignedInt += i*256**index
            index += 1
        return unsignedInt
    
    def getFloat(self, waveform, startByte):    
        b0 = format(int(waveform[startByte]), '#010b')[2::]
        b1 = format(int(waveform[startByte + 1]), '#010b')[2::]
        b2 = format(int(waveform[startByte + 2]), '#010b')[2::]
        b3 = format(int(waveform[startByte + 3]), '#010b')[2::]
        s = int(b0[0], 2)
        e = int(b0[1::] + b1[0], 2)
        f = int(b1[1::] + b2 + b3, 2)

        frac = 1 + f*10**(-1*len(str(f)))
        exp = 2**(e-127)

        return (-1)**s * exp * frac

    def catBytesSigned(self, byteSequence):
        numBytes = len(byteSequence)
        maxVal = 2**(8*numBytes-1) - 1
        unsignedVal = 0
        signedVal = 0
        byteVals = [int(i) for i in byteSequence]
        index = 0
        for i in byteVals[::-1]:
            unsignedVal += i*256**index
            index += 1
        if unsignedVal > maxVal:
            signedVal = unsignedVal - 2**(8*numBytes)
        else:
            signedVal = unsignedVal
        return signedVal

    def getDatArrayLength(self, waveform, byteLocation=60+self.preamble):
        return self.catBytesSigned(waveform[byteLocation:byteLocation+4])

    def getNumDataPoints(self, waveform, byteLocation=116+self.preamble):
        return self.catBytesSigned(waveform[byteLocation:byteLocation+4])

    def getLenDescriptor(self, waveform, byteLocation=36+self.preamble):
        return self.catBytesSigned(waveform[byteLocation:byteLocation+4])

    def getVerticalGain(self, waveform, byteLocation=156+self.preamble):
        return self.getFloat(waveform, byteLocation)

    def getVerticalOffset(self, waveform, byteLocation=160+self.preamble):
        return self.getFloat(waveform, byteLocation)

    def getHorizontalInterval(self, waveform, byteLocation=176+self.preamble):
        return self.getFloat(waveform, byteLocation)

    def get_waveform(self, channel):
        waveform = self.inst.query('c{}:waveform?'.format(channel))
        return waveform

    def format_waveform(self, waveform):
        LenDesc = self.getLenDescriptor(waveform)
        NumDatPoints = self.getNumDataPoints(waveform)
        DatArrayLength = self.getDatArrayLength(waveform)
        dataBytes = int(DatArrayLength/NumDataPoints)
        wavArray = []
        for i in range(LenDesc+self.preamble, len(waveform), 2):
            wavArray.append(catBytesSigned(waveform[i:i+dataBytes]))
        vertGain = self.getVerticalGain(waveform)
        vertOff = self.getVerticalOffset(waveform)
        horInt = self.getHorizonatlInterval(waveform)

        t = np.linspace(0,len(wavArray)*horInt, len(wavArray))
        y = np.array(wavArray)*vertGain - vertOff

        return t, y

        

class Tek7104(object):
    """Initialize Tek7104 class object

    Args:
        inst (object) : Object for communication with a Tek7104 oscilloscope.
        Typically a pyVisa Resource.

    Examples:
        # Assuming Tek7104 on GPIB channel 2
        >>> from wanglab_instruments.oscilloscopes import Tek7104
        >>> import visa
        >>> rm = visa.ResourceManager()
        >>> rm.list_resources()
        ('GPIB0::2::INSTR')
        >>> scope = Tek7104(rm.open_resource('GPIB0::2::INSTR'))
        # retrieve waveform from scope channel 2
        >>> x, y = scope.fetch_spectrum(2)
    """
    def __init__(self,inst):
        self.inst = inst

    def __repr__(self):
        return 'Tek7104({!r})'.format(self.inst)

    def fetch_spectrum(self,trace,offset=False):
        """
        fetch_spectrum(self, trace, offset=False)

        Return the x and y axes data from a channel (trace).

        Args:
            trace (int) : channel to retrieve
            offset (bool) : if True, the y axis is offset from 0V according to
                the offset set on the scope for viewing multiple waveforms

        Returns:
            tuple : numpy array of time axis, numpy array of volt axis
        """
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
        return np.array(x),np.array(y) #x,y

class Tek3034(object):
    """Initialize Tek3034 class object

    Args:
        inst (object) : Object for communication with a Tek7104 oscilloscope.
        Typically a pyVisa Resource.

    Examples:
        # Assuming Tek3034 on GPIB channel 3
        >>> from wanglab_instruments.oscilloscopes import Tek3034
        >>> import visa
        >>> rm = visa.ResourceManager()
        >>> rm.list_resources()
        ('GPIB0::3::INSTR')
        >>> scope = Tek3034(rm.open_resource('GPIB0::2::INSTR'))
        # retrieve waveform from scope channel 2
        >>> x, y = scope.fetch_spectrum(2)
    """

    def __init__(self,inst):
        self.inst = inst

    def __repr__(self):
        return 'Tek3034({!r})'.format(self.inst)

    def fetch_spectrum(self, trace, offset=False):
        """
        fetch_spectrum(self, trace, offset=False)

        Return the x and y axes data from a channel (trace).

        Args:
            trace (int) : channel to retrieve
            offset (bool) : if True, the y axis is offset from 0V according to
                the offset set on the scope for viewing multiple waveforms

        Returns:
            tuple : numpy array of time axis, numpy array of volt axis
        """

        self.inst.write('*CLS')
        self.inst.write('DAT:ENCDG ASCII')
        self.inst.write('DAT:SOU CH{}'.format(trace))
        self.inst.write('DAT:SART 1')
        self.inst.write('DAT:STOP 10000')
        raw=np.array(self.inst.query_ascii_values('CURV?'))
        ymult=float(self.inst.query('WFMP:YMULT?'))
        yoff=float(self.inst.query('WFMP:YOFF?'))
        yzero=float(self.inst.query('WFMP:YZERO?'))
        if offset is True:
            y=(raw)*ymult + yzero
        else:
            y=(raw-yoff)*ymult + yzero
        xinc=float(self.inst.query('WFMP:XINC?'))
        xzero=float(self.inst.query('WFMP:XZERO?'))
        pts=int(self.inst.query('WFMP:NR_PT?'))
        x=np.linspace(xzero,xzero+pts*xinc,pts)
        return x,y
