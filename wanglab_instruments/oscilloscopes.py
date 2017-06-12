import numpy as np

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
