import numpy as np

class LecroyWaverunner(object):
    def __init__(self, inst):
        self.inst = inst
        self.inst.write('comm_format def9,word,bin')
        self.preamble = 21 # bytes in waveform preamble

    def __repr__(self):
        return 'LecroyWaverunner({!r})'.format(self.inst)

    def cat_bytes(self, byte_sequence):
        num_bytes = len(byte_sequence)
        max_val = 2**(8*num_bytes-1) - 1
        unsigned_int = 0
        byte_vals = [int(i) for i in byte_sequence]
        index = 0
        for i in byte_vals[::-1]:
            unsigned_int += i*256**index
            index += 1
        return unsigned_int
    
    def get_float(self, waveform, start_byte):    
        b0 = format(int(waveform[start_byte]), '#010b')[2::]
        b1 = format(int(waveform[start_byte + 1]), '#010b')[2::]
        b2 = format(int(waveform[start_byte + 2]), '#010b')[2::]
        b3 = format(int(waveform[start_byte + 3]), '#010b')[2::]
        s = int(b0[0], 2)
        e = int(b0[1::] + b1[0], 2)
        f = int(b1[1::] + b2 + b3, 2)

        frac = 1 + f*10**(-1*len(str(f)))
        exp = 2**(e-127)

        return (-1)**s * exp * frac

    def cat_bytes_signed(self, byte_sequence):
        num_bytes = len(byte_sequence)
        max_val = 2**(8*num_bytes-1) - 1
        unsigned_val = 0
        signed_val = 0
        byte_vals = [int(i) for i in byte_sequence]
        index = 0
        for i in byte_vals[::-1]:
            unsigned_val += i*256**index
            index += 1
        if unsigned_val > max_val:
            signed_val = unsigned_val - 2**(8*num_bytes)
        else:
            signed_val = unsigned_val
        return signed_val

    def get_dat_array_length(self, waveform, byte_location=60):
        byte_location += self.preamble
        return self.cat_bytes_signed(waveform[byte_location:byte_location+4])

    def get_num_data_points(self, waveform, byte_location=116):
        byte_location += self.preamble
        return self.cat_bytes_signed(waveform[byte_location:byte_location+4])

    def get_len_descriptor(self, waveform, byte_location=36):
        byte_location += self.preamble
        return self.cat_bytes_signed(waveform[byte_location:byte_location+4])

    def get_vertical_gain(self, waveform, byte_location=156):
        byte_location += self.preamble
        return self.get_float(waveform, byte_location)

    def get_vertical_offset(self, waveform, byte_location=160):
        byte_location += self.preamble
        return self.get_float(waveform, byte_location)

    def get_horizontal_interval(self, waveform, byte_location=176):
        byte_location += self.preamble
        return self.get_float(waveform, byte_location)

    def get_first_valid_point(self, waveform, byte_location=124):
        byte_location += self.preamble
        return self.cat_bytes_signed(waveform[byte_location:byte_location+4])

    def get_last_valid_point(self, waveform, byte_location=128):
        byte_location += self.preamble
        return self.cat_bytes_signed(waveform[byte_location:byte_location+4])

    def get_waveform(self, channel):
        waveform = self.inst.query('c{}:waveform?'.format(channel))
        return waveform

    def format_waveform(self, waveform):
        len_desc = self.get_len_descriptor(waveform)
        num_data_points = self.get_num_data_points(waveform)
        dat_array_length = self.get_dat_array_length(waveform)
        data_bytes = int(dat_array_length/num_data_points)
        wav_array = []
        for i in range(len_desc+self.preamble, len(waveform), 2):
            wav_array.append(self.cat_bytes_signed(waveform[i:i+data_bytes]))
        vert_gain = self.get_vertical_gain(waveform)
        vert_off = self.get_vertical_offset(waveform)
        hor_int = self.get_horizontal_interval(waveform)

        t = np.linspace(0,len(wavarray)*hor_int, len(wav_array))
        y = np.array(wav_array)*vert_gain - vert_off

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

class RigolDS2102(object):

    def __init__(self, inst):
        self.inst = inst

    def __repr__(self):
        return 'RigolDS2102({!r})'.format(self.inst)

    def fetch_spectrum(self, trace = 1):
        self.inst.write(':WAV:SOURce CHAN{}'.format(trace))
        self.inst.write(':WAV:FORMAT ASCII')
        x_inc = float(self.inst.query(':WAV:XINC?'))
        y = self.inst.query_ascii_values(':WAV:DATA?')
        x = np.linspace(0, x_inc*len(y), len(y))
        return x, np.array(y)
    

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
