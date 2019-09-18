from __future__ import print_function
import numpy as np
from scipy.special import iv
import math
import datetime
def prop_doc(var):
    s1 = '{} = property(get_{}, set_{})\n\n'.format(var, var, var)
    s2 = 'See help on get_{} and set_{} functions for info.'.format(var, var)
    return s1 + s2

def timestamp():
    return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')

class AgilentESA(object):

    frequencies={'Hz':1.,'kHz':1000.,'MHz':1000000.,'GHz':1000000000.}

    def __init__(self, inst, freq_unit = 'MHz'):
        self.inst = inst
        self.inst.write(':FORMat:TRACE:DATA ASCii')
        self._freq_unit = freq_unit

    def  __repr__(self):
        return 'KeysightPXA({!r})'.format(self.inst)

    def get_freq_unit(self):
        return self._freq_unit

    def set_freq_unit(self, freq):
        if freq in self.frequencies.keys():
            self._freq_unit = freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = { GHz | MHz | kHz | Hz }')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit)

    def set_center_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:CENTER {}{}'.format(freq,unit))

    def get_center_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:CENTER?'))/self.frequencies[unit]

    center_freq = property(get_center_freq, set_center_freq)

    def set_start_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:START {}{}'.format(freq,unit))

    def get_start_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:START?'))/self.frequencies[unit]

    start_freq = property(get_start_freq, set_start_freq)

    def set_stop_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:STOP {}{}'.format(freq,unit))

    def get_stop_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:STOP?'))/self.frequencies[unit]

    stop_freq  = property(get_stop_freq, set_stop_freq)

    def set_freq_span(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:SPAN {}{}'.format(freq,unit))

    def get_freq_span(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:SPAN?'))/self.frequencies[unit]

    freq_span  = property(get_freq_span, set_freq_span)

    def fetch_spectrum_trace(self, trace):
        y = self.inst.query_ascii_values(':TRACE? TRACE{}'.format(trace))
        return y

    def fetch_spectrum(self, trace):
        y = self.fetch_spectrum_trace(trace)
        x0 = self.start_freq
        xf = self.stop_freq
        x = np.linspace(x0, xf, len(y))
        return x, y


class KeysightPXA(object):

    frequencies={'Hz':1.,'kHz':1000.,'MHz':1000000.,'GHz':1000000000.}

    def __init__(self, inst, freq_unit = 'MHz'):
        self.inst = inst
        self.inst.write(':FORMat:TRACE:DATA ASCii')
        self._freq_unit = freq_unit

    def  __repr__(self):
        return 'KeysightPXA({!r})'.format(self.inst)

    def get_freq_unit(self):
        return self._freq_unit

    def set_freq_unit(self, freq):
        if freq in self.frequencies.keys():
            self._freq_unit = freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = { GHz | MHz | kHz | Hz }')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit)

    def set_center_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:CENTER {}{}'.format(freq,unit))

    def get_center_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:CENTER?'))/self.frequencies[unit]

    center_freq = property(get_center_freq, set_center_freq)

    def set_start_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:START {}{}'.format(freq,unit))

    def get_start_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:START?'))/self.frequencies[unit]

    start_freq = property(get_start_freq, set_start_freq)

    def set_stop_freq(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:STOP {}{}'.format(freq,unit))

    def get_stop_freq(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:STOP?'))/self.frequencies[unit]

    stop_freq  = property(get_stop_freq, set_stop_freq)

    def set_freq_span(self, freq, unit=None):
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:SPAN {}{}'.format(freq,unit))

    def get_freq_span(self, unit=None):
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:SPAN?'))/self.frequencies[unit]

    freq_span  = property(get_freq_span, set_freq_span)

    def fetch_spectrum_trace(self, trace):
        y = self.inst.query_ascii_values(':TRACE? TRACE{}'.format(trace))
        return y

    def fetch_spectrum(self, trace):
        y = self.fetch_spectrum_trace(trace)
        x0 = self.start_freq
        xf = self.stop_freq
        x = np.linspace(x0, xf, len(y))
        return x, y

class Tek5103(object):
    """
    Initialize Tek5103 class object

    Args:
        inst (object) : Object for communication with a Tek5103 spectrum
            analyzer.  Typically a pyVisa Resource.
        freq_unit (str, optional) : Default frequency unit.  May be 
            { MHz | kHz | Hz }.  Default is MHz.
        time_unit (str, optional) : Default time unit.  May be
            { s | ms | us | ns }.  Default is us.

    Examples:
        # Tek5103 spectrum analyzer on GPIB channel 1.
        >>> from wanglab_instruments.function_generators import Tek5103
        >>> import visa
        >>> rm = visa.ResourceManager()
        >>> rm.list_resources()
        ('GPIB0::1::INSTR')
        >>> rsa = Tek5103(rm.open_resource('GPIB0::1::INSTR'), time_unit='ns')
        >>> rsa.time_unit
        'ns'
        # Retrieve currently displayed waveform on channel 1
        >>> t, y = rsa.fetch_spectrum(1)
        """

    frequencies={'Hz':1.,'kHz':1000.,'MHz':1000000.,'GHz':1000000000.}
    times={'s':1.,'ms':.001,'us':.000001,'ns':.000000001}

    def __init__(self, inst, freq_unit = 'MHz', time_unit = 'us'):
        self.inst = inst
        self.freq_unit = freq_unit
        self.time_unit = time_unit

    def get_freq_unit(self):
        """
        get_freq_unit(self)

        get the value of freq_unit

        Args:
            None

        Returns:
            str : self._freq_unit
        """
        return self._freq_unit

    def set_freq_unit(self, freq):
        """
        set_freq_unit(self, freq)

        set the value of freq_unit

        Args:
            freq (str) : { GHz | MHz | kHz | Hz }

        Returns:
            None
        """
        if freq in self.frequencies.keys():
            self._freq_unit = freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = { GHz | MHz | kHz | Hz }')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit,
        doc=prop_doc('freq_unit'))

    def get_time_unit(self):
        """
        get_time_unit(self)

        get the value of time_unit

        Args:
            None

        Returns:
            str : self._time_unit
        """
        return self._time_unit

    def set_time_unit(self, time):
        """
        set_time_unit(self, time)

        set the value of time_unit

        Args:
            time (str) : { s | ms | us | ns }

        Returns:
            None
        """
        if time in self.times.keys():
            self._time_unit = time
        else:
            if type(time) == str:
                raise ValueError('time_unit = { s | ms | us | ns }')
            else:
                raise TypeError('time_unit must be str')

    time_unit = property(get_time_unit, set_time_unit,
        doc=prop_doc('time_unit'))

    def __repr__(self):
        return 'Tek5103({!r}, {!r}, {!r})'.format(self.inst, self.freq_unit,
        self.time_unit)


#############################Data Transfer################################

    def fetch_spectrum_trace(self,trace):
        """
        Takes the spectrum data currently stored in the RSA.  To acquire a
        single fresh run, use read_spectrum(trace)
        Returns frequency,power in units unit,dB 

        """
        return self.inst.query_binary_values('FETCH:SPECTRUM:TRACE{}?'.format(trace))

    def fetch_spectrum(self,trace,unit=None):
        """
        fetch_spectrum(self, trace, unit=None)

        fetch the current spectrum waveform from trace

        Args:
            trace (int) : { 1 | 2 | 3 | 4 } corresponding to trace to retrieve
            unit (str, optional): { GHz | MHz | kHz | Hz } unit for frequency axis

        Returns:
            x, y : numpy arrays corresponding to the x-axis and the spectrum
        """
        y=self.fetch_spectrum_trace(trace)
        x=np.linspace(self.get_start_freq(unit),self.get_stop_freq(unit),len(y))
        return x,np.array(y)

    def read_spectrum_trace(self,trace,unit=None):
        '''
        Take the spectrum data for the next acquisition from the
        analzyer.  To pull the current data, use fetch_spectrum(trace).
        
        Returns frequency,power in units unit,dB
        '''
        return self.inst.query_binary_values('READ:SPECTRUM:TRACE{}?'.format(trace))

    def read_spectrum(self,trace,unit=None):
        """
        read_spectrum(self, trace, unit=None)

        Acquires a new spectrum.
        This differs from fetch_spectrum in that it causes the analyzer to
        start a new acquisition, whereas fetch_spectrum retrieves whatever the
        current waveform being displayed is.

        Args:
            trace (int) : { 1 | 2 | 3 | 4 } corresponding to trace to retrieve
            unit (str, optional): { GHz | MHz | kHz | Hz } unit for frequency axis

        Returns:
            x, y : numpy arrays corresponding to the x-axis and the spectrum
        """

        y=self.read_spectrum_trace(trace)
        x=np.linspace(self.get_start_freq(unit),self.get_stop_freq(unit),len(y))
        return x,np.array(y)

#############################Frequency Commands################################

    def set_center_freq(self,freq,unit=None):
        """
        set_center_freq(self,freq,unit=None):        

        set the value of center_freq, the center analysis frequency        

        Args:
            freq (float) : center frequency 
            unit (str, optional) : { GHz | MHz | kHz | Hz } frequency unit
        
        Returns:
            None
        """
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:CENT {}{}'.format(freq,unit))

    def get_center_freq(self,unit=None):
        """
        get_center_freq(self,unit=None):        

        get the value of center_freq        

        Args:
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            float : Center analysis frequency in specified units
        """
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:CENT?'))/self.frequencies[unit]

    center_freq = property(get_center_freq, set_center_freq,
        doc=prop_doc('center_freq'))

    def set_freq_span(self,freq,unit=None):
        """
        set_freq_span(self,freq,unit=None):        

        set the value of freq_span, the frequency span for analysis.  If the
        span is greater than 25 MHz, the analyzer is swept instead of
        real-time.        

        Args:
            freq (float) : Frequency span
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            None
        """
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:SPAN {}{}'.format(freq,unit))

    def get_freq_span(self,unit=None):
        """
        get_freq_span(self,unit=None):        

        get the value of freq_span, the analysis frequency span  

        Args:
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            float : Analysis frequency span in specified units
        """
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:SPAN?'))/self.frequencies[unit]

    freq_span=property(get_freq_span,set_freq_span,doc=prop_doc('freq_span'))

    def set_start_freq(self,freq,unit=None):
        """
        set_start_freq(self,freq,unit=None):        

        set the value of start_freq, the starting analysis frequency        

        Args:
            freq (float) : Starting analysis frequency
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            None
        """
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:STARt {}{}'.format(freq,unit))

    def get_start_freq(self,unit=None):
        """
        get_start_freq(self,unit=None):        

        get the value of start_freq, the starting analysis frequency        

        Args:
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            float : starting analysis frequency
        """
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:STARt?'))/self.frequencies[unit]

    start_freq=property(get_start_freq,set_start_freq,doc=prop_doc('start_freq'))

    def set_stop_freq(self,freq,unit=None):
        """
        set_stop_freq(self,freq,unit=None):        

        set the value of stop_freq, the ending analysis frequency        

        Args:
            freq (float) : Ending analysis frequency
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            None
        """
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:STOP {}{}'.format(freq,unit))
    def get_stop_freq(self,unit=None):
        """
        get_stop_freq(self,unit=None):        

        get the value of stop_freq, the ending analysis frequency        

        Args:
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            float : Ending analysis frequency in specified units
        """
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:STOP?'))/self.frequencies[unit]
    stop_freq=property(get_stop_freq,set_stop_freq)

#############################Detection Window################################

    def set_gate_length(self,length,unit=None,auto=False):
        """
        set_gate_length(self,length,unit=None,auto=False):        

        set the value of gate_length, the time window for analysis        

        Args:
            length (float) : gate length
            unit (str, optional) : { s | ms | us | ns }
            auto (bool, optional) : True to let analyzer automatically set
                gate length
        
        Returns:
            None
        """
        if auto:
            self.inst.write('SENS:SPEC:LENG:AUTO')
        else:
            if unit is None:
                unit=self.time_unit
            self.inst.write('SENS:SPEC:LENG {}{}'.format(length,unit))

    def get_gate_length(self,unit=None):
        """
        get_gate_length(self,unit=None):        

        get the value of gate_length, the analysis time window        

        Args:
            unit (str, optional) : { s | ms | us | ns }
        
        Returns:
            float : analysis time window in specified units
        """
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:LENG?'))/self.times[unit:]

    def get_gate_length_actual(self,unit=None):
        """
        get_gate_length_actual(self,unit=None):        

        get the value of gate_length_actual, the actual analysis length, which
        may differ from the specified length

        Args:
            unit (str, optional) : { s | ms | us | ns }
        
        Returns:
            float : actual analysis time window in specified units
        """
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:LENG:ACT?'))/self.times[unit]

    gate_length=property(get_gate_length_actual,set_gate_length,doc=prop_doc('gate_length'))

    def set_gate_start(self,time,unit=None,auto=False):
        """
        set_gate_start(self,time,unit=None,auto=False):        

        set the value of gate_start, the analysis window offset        

        Args:
            time (float) : analysis offset time
            unit (str, optional) : { s | ms | us | ns }
            auto (bool, optional) : True to let analyzer automatically set the
                offset
        
        Returns:
            None
        """
        if auto:
            self.inst.write('SENS:SPEC:STAR:AUTO')
        else:
            if unit is None:
                unit=self.time_unit
            self.inst.write('SENS:SPEC:STAR {}{}'.format(time,unit))

    def get_gate_start(self,unit=None):
        """
        get_gate_start(self,unit=None):        

        get the value of gate_start, the analysis window offset        

        Args:
            unit (str, optional) : { s | ms | us | ns }
        
        Returns:
            float : analysis window offset time
        """
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:STAR?'))/self.times[unit]

    gate_start=property(get_gate_start,set_gate_start,doc=prop_doc('gate_start'))

#############################Trace Options################################

    def show_trace(self,trace):
        """
        show_trace(self, trace)

        Toggle trace on.

        Args:
            trace (int) : trace to toggle on

        Returns:
            None
        """
        self.inst.write('TRAC{}:SPEC ON'.format(trace))

    def trace_off(self,trace):
        """
        trace_off(self, trace)

        Toggle trace off.

        Args:
            trace (int) : trace to toggle off

        Returns:
            None
        """
        self.inst.write('TRAC{}:SPEC OFF'.format(trace))

    def set_averaging(self,trace,avg,count=True):
        """
        set_averaging(self,trace,avg,count=True):        

        set the number of averages
        count=1 causes a single acquisition of the analyzer to avg over the
        number of spectra specified by avg.  If count=0, a single acquisition
        will only collect a single run, and averaging will only work with the
        analyzer in continuous acquisition mode.

        Args:
            trace (int) : trace to set averaging for
            avg (int) : number of averages
            count (bool, optional) : True to enable count
        
        Returns:
            None
        """
        self.inst.write('TRAC{}:SPEC:FUNC AVER'.format(trace))
        self.inst.write('TRAC{}:SPEC:AVER:COUN {}'.format(trace,avg))
        if count:
            self.inst.write('TRAC{}:SPEC:COUNT:ENAB 1'.format(trace))
        else:
            self.inst.write('TRAC{}:SPEC:COUNT:ENAB 0'.format(trace))

    def get_averaging(self,trace):
        """
        get_averaging(self,trace):        

        get the value of averaging        

        Args:
            trace () : 
        
        Returns:
        """
        return float(self.inst.query('TRAC{}:SPEC:AVER:COUN?'.format(trace)))

    def reset_averaging(self,trace):
        """Reset the averaging on trace"""
        self.inst.write('TRAC{}:SPEC:AVER:RES'.format(trace))

#############################Acquisition################################

    def acquisition_mode(self,mode):
        """
        acquisition_mode(self, mode)

        specify the acquisition mode
        
        Args:
            mode (str or int) : 0 or 'single' for single acquisistion, 1 or
                'cont' or 'continuous' for continuous acquisition.

        Returns:
            None
        """
        if mode==0 or mode=='single':
            self.inst.write('INIT:CONT OFF')
        elif mode==1 or mode=='cont' or mode=='continuous':
            self.inst.write('INIT:CONT ON')
        else: print('Invalid input.  Input 0 or \'single\' for single, 1 or \
            \'cont\' or \'continuous\' for continuous')

    def acquire(self):
        """start acquisistion"""
        self.inst.write('INIT')


    def restart_acquire(self):
        """restart acquisition"""
        self.inst.write('SENSE:SPECTRUM:CLEAR:RESULTS')

    def set_acq_time(self,time):
        """
        set_acq_time(self,time):        

        set the value of acq_time, the time duration for acquisition        

        Args:
            time (float) : acquisition time duration 
        
        Returns:
            None
        """
        self.inst.write('SENSE:ACQUISITION:SECONDS {}'.format(time))

    def get_acq_time(self):
        """
        get_acq_time(self):        

        get the value of acq_time        

        Args:
            None
        
        Returns:
            float : acquisition time
        """
        return float(self.inst.query('SENSE:ACQUISITION:SECONDS?'))

    acq_time = property(get_acq_time, set_acq_time,doc=prop_doc('acq_time'))

    def set_acq_samples(self,samples):
        """
        set_acq_samples(self,samples):        

        set the value of acq_samples, the number of acquisition samples        

        Args:
            samples (int) : number of samples
        
        Returns:
            None
        """
        self.inst.write('SENSE:ACQUISITION:SAMPLES {}'.format(samples))

    def get_acq_samples(self):
        """
        get_acq_samples(self):        

        get the value of acq_samples, the number of acquisition samples        

        Args:
            None
        
        Returns:
            float : number of acquisition samples
        """
        return float(self.inst.query('SENSE:ACQUISITION:SAMPLES?'))

    acq_samples = property(get_acq_samples,
        set_acq_samples,doc=prop_doc('acq_samples'))

#############################GPIB################################

    def set_gpib(self,address):
        """
        set_gpib(self,address):        

        set the gpib address

        Args:
            address (int) : GPIB address
        
        Returns:
            None
        """
        self.inst.write('SYST:COMM:GPIB:SELF:ADDR {}'.format(address))

    def get_gpib(self):
        """
        get_gpib(self):        

        get the GPIB address

        Args:
            None
        
        Returns:
            float : GPIB address
        """
        return float(self.inst.query('SYST:COMM:GPIB:SELF:ADDR?'))

    gpib = property(get_gpib,set_gpib,doc=prop_doc('gpib'))

#############################RBW################################

    def set_rbw(self,rbw,unit=None):
        """
        set_rbw(self,rbw,unit=None):        

        set the value of rbw, the resolution bandwidth        

        Args:
            rbw (float) : resolution bandwidth
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            None
        """
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:BAND:RES {}{}'.format(rbw,unit))

    def get_rbw(self,unit=None):
        """
        get_rbw(self,unit=None):        

        get the value of rbw, the resolution bandwidth        

        Args:
            unit (str, optional) : { GHz | MHz | kHz | Hz }
        
        Returns:
            float : resolution bandwidth for the current acquisition
        """
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:BAND:RES:ACT?'))/self.frequencies[unit]

    rbw = property(get_rbw,set_rbw,doc=prop_doc('rbw'))

    def set_rbw_auto(self,auto):
        """
        set_rbw_auto(self,auto):        

        set analyzer to automatically choose the resolution bandwidth

        Args:
            auto (bool) : True for auto
        
        Returns:
            None
        """
        self.inst.write('SENS:SPEC:BAND:RES:AUTO {}'.format(auto))

    def get_rbw_auto(self):
        """
        get_rbw_auto(self):        

        get the value of rbw_auto, a bool specifying if the spectrum analyzer
        automatically sets the resolution bandwidth

        Args:
            None
        
        Returns:
            int : 1 for auto
        """
        return int(self.inst.query('SENS:SPEC:BAND:AUTO?'))

    rbw_auto = property(get_rbw_auto,set_rbw_auto,doc=prop_doc('rbw_auto'))

    def enbw(self):
        """
        enbw(self)

        Determine the effective noise bandwidth of the analyzer given its
        current state.

        Args:
            None

        Returns:
            float : effective noise bandwidth in Hz
        """
        pi = np.pi
        alpha = 16.7/pi
        N=self.acq_samples
        tau=self.acq_time
        fs=N/tau
        j=np.arange(N)
        def kaiser(j):
            z = 2.*j/N - 1.
            return iv(0,pi*alpha*np.sqrt(1-z**2))/iv(0,pi*alpha)
        def S1(x):
            sum = 0
            for i in x:
                sum = sum+i
            return sum

        def S2(x):
            sum = 0
            for i in x:
                sum = sum+i**2
            return sum
        x=kaiser(j)
        return fs*S2(x)/S1(x)**2

    def state(self, trace, write_to=None, name=None):
        s = []
        s.append('{}\n'.format(timestamp()))
        if name is not None:
            s.append('nickname: {}\n'.format(name))
        s.append('{}'.format(self.inst.query('*IDN?')))
        s.append('Center Frequency: {} {}\n'.format(self.center_freq, 
            self.freq_unit))
        s.append('Span: {} {}\n'.format(self.freq_span, self.freq_unit))
        s.append('RBW: {} {}\n'.format(self.rbw, self.freq_unit))
        s.append('Averaging: {}\n'.format(self.get_averaging(trace)))
        s.append('Acquisition Time: {} S\n'.format(self.acq_time))
        s.append('Acquisition Samples: {}\n'.format(self.acq_samples))
        s.append('ENBW: {} Hz\n'.format(self.enbw()))
        if write_to is None:
            for line in s:
                print(line,end='')
        else:
            with open(write_to,'a') as f:
                for line in s:
                    f.write(line)
        return ''.join(s)



class Tek5103Functions(Tek5103):
    def __init__(self,inst, freq_unit = 'MHz', time_unit = 'us'):
        self.inst=inst
        self.freq_unit=freq_unit
        self.time_unit=time_unit

    def stitch_scans(self,start_freq,stop_freq,trace=None,scan_width=None):
        """
        stitch_scans(self, start_freq, stop_freq, trace=None, scan_width=None)

        stitches together multiple scans, from start_freq to stop_freq,
        returning a single x and y axis for the spectrum over the full range. 
        This function allows one to use real-time analysis (25 MHz bandwidth
        max) over a larger frequency range than 25 MHz.

        Args:
            start_freq (float) : starting frequency for scan
            stop_freq (float) : ending frequency for scan
            trace (int, optional) : trace to use for scan
            scan_width(float, optional) : analysis frequency span to use for
                the individual scans.  Defaults to using the current frequency
                span.

        Returns:
            x, y : the frequency axis (x) and spectrum (y) as numpy arrays
                with floating point values.
        """
        if trace is None:
            trace=1
        if scan_width is None:
            scan_width=self.freq_span
        x=np.array([])
        y=np.array([])
        scans=math.ceil(float(stop_freq-start_freq)/float(scan_width))
        self.freq_span=scan_width
        self.center_freq=start_freq+0.5*scan_width
        print(self.start_freq)
        for i in range(int(scans)):
            print('scan {} of {}'.format(i,scans))
            a,b=self.read_spectrum(trace)
            x=np.append(x,a)
            y=np.append(y,b)
            self.center_freq+=scan_width
        return x,y

    def step(self,step_size):
        """Increment the center frequency"""
        self.center_freq+=step_size
        print('Center: {}{}'.format(self.center_freq,self.freq_unit))

    def enbw(self):
        """
        enbw(self)

        Determine the effective noise bandwidth of the analyzer given its
        current state.

        Args:
            None

        Returns:
            float : effective noise bandwidth in Hz
        """
        pi = np.pi
        alpha = 16.7/pi
        N=self.acq_samples
        tau=self.acq_time
        fs=N/tau
        j=np.arange(N)
        def kaiser(j):
            z = 2.*j/N - 1.
            return iv(0,pi*alpha*np.sqrt(1-z**2))/iv(0,pi*alpha)
        def S1(x):
            sum = 0
            for i in x:
                sum = sum+i
            return sum

        def S2(x):
            sum = 0
            for i in x:
                sum = sum+i**2
            return sum
        x=kaiser(j)
        return fs*S2(x)/S1(x)**2
