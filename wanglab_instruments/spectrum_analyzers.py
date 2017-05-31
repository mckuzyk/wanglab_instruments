import numpy as np
from scipy.special import iv
import math
class Tek5103(object):
    """
    Class for the Textronix 5103B real-time spectrum analyzer.  To creat an
    instance of the class, one must pass an instrument object.  This is most
    often done with pyvisa.  For example:

    import visa
    import spectrum_analyzers
    rm=visa.ResourceManager()
    rsa=spectrum_analzyers.tex5103(rm.open_resource(address))

    In this example, address is the appropriate string to pass to pyvisa in an
    open_resource() call, and rsa is now an instance of the class tex5103.  In
    the Wang lab, the tex5103 is connected via GPIB and set to address 1.  The
    string address is then 'GPIB0::1::INSTR'.  See the pyvisa documentation
    for detals.

    The tex5103 class initializes the default frequency and time units to
    megahertz and microseconds respectively.  These units are stored as
    strings in the variables self.freq_unit and self.time_unit.  The
    case-sensitive unit options are:

    self.freq_unit=('Hz','kHz','MHz','GHz')
    self.time_unit=('s','ms','us','ns')

    Calls to properties, e.g. self.center_frequency, always use the current
    values of self.freq_unit and self.time_unit.  If you wish to keep the
    default parameters, but wish to get or set a property in another unit
    choice, that can be done by calling the corresponding function.  

    self.center_freq=50 #Sets center frequency to 50 MHz (assuming
                        #self.freq_unit='MHz')
    self.set_center_freq(1,'GHz') #Sets center frequency to 1 GHz without
                                  #changing the default frequency unit.
    self.freq_unit='GHz'    #Sets default frequency unit to GHz
    self.center_freq=1      #Sets center frequency to 1 GHz.
    """ 

    frequencies={'Hz':1.,'kHz':1000.,'MHz':1000000.,'GHz':1000000000.}
    times={'s':1.,'ms':.001,'us':.000001,'ns':.000000001}
    def __init__(self,inst):
        self.inst=inst
        self.freq_unit='MHz'
        self.time_unit='us'

#############################Data Transfer################################

    def fetch_spectrum_trace(self,trace):
        """
        Takes the spectrum data currently stored in the RSA.  To acquire a
        single fresh run, use read_spectrum(trace)
        Returns frequency,power in units unit,dB 

        """
        return self.inst.query_binary_values('FETCH:SPECTRUM:TRACE{}?'.format(trace))

    def fetch_spectrum(self,trace,unit=None):
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
        y=self.read_spectrum_trace(trace)
        x=np.linspace(self.get_start_freq(unit),self.get_stop_freq(unit),len(y))
        return x,np.array(y)

#############################Frequency Commands################################

    def set_center_freq(self,freq,unit=None):
        '''Input freq, unit='Hz','kHz','MHz','GHz' '''
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:CENT {}{}'.format(freq,unit))
    def get_center_freq(self,unit=None):
        '''Returns frequency in units freq_unit=Hz,kHz,MHz,GHz.'''
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:CENT?'))/self.frequencies[unit]
    center_freq = property(get_center_freq, set_center_freq)

    def set_freq_span(self,freq,unit=None):
        '''Input freq, unit='Hz','kHz','MHz','GHz' '''
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:SPAN {}{}'.format(freq,unit))
    def get_freq_span(self,unit=None):
        '''Returns frequency in Hz'''
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:SPAN?'))/self.frequencies[unit]
    freq_span=property(get_freq_span,set_freq_span)

    def set_start_freq(self,freq,unit=None):
        '''Input freq, unit='Hz','kHz','MHz','GHz' '''
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:STARt {}{}'.format(freq,unit))
    def get_start_freq(self,unit=None):
        '''Returns frequency in Hz'''
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:STARt?'))/self.frequencies[unit]
    start_freq=property(get_start_freq,set_start_freq)

    def set_stop_freq(self,freq,unit=None):
        '''Input freq, unit='Hz','kHz','MHz','GHz' '''
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:FREQ:STOP {}{}'.format(freq,unit))
    def get_stop_freq(self,unit=None):
        '''Returns frequency in Hz'''
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:FREQ:STOP?'))/self.frequencies[unit]
    stop_freq=property(get_stop_freq,set_stop_freq)

#############################Detection Window################################

    def set_gate_length(self,length,unit=None,auto=False):
        '''
        Sets spectrum measure duration.  
        set_spectrum_length(length, unit='s','ms','us','ns',auto=False)
        setting auto=1 will cause the analyzer to auto set the duration. 
        '''
        if auto:
            self.inst.write('SENS:SPEC:LENG:AUTO')
        else:
            if unit is None:
                unit=self.time_unit
            self.inst.write('SENS:SPEC:LENG {}{}'.format(length,unit))
    def get_gate_length(self,unit=None):
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:LENG?'))/self.times[unit:]
    def get_gate_length_actual(self,unit=None):
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:LENG:ACT?'))/self.times[unit]
    gate_length=property(get_gate_length_actual,set_gate_length)

    def set_gate_start(self,time,unit=None,auto=False):
        '''
        Sets spectrum offset time. set_spectrum_start(length,unit='s','ms'
        ,'us','ns', auto=False)
        auto=1 the analyzer will auto set the start time.
        '''
        if auto:
            self.inst.write('SENS:SPEC:STAR:AUTO')
        else:
            if unit is None:
                unit=self.time_unit
            self.inst.write('SENS:SPEC:STAR {}{}'.format(time,unit))
    def get_gate_start(self,unit=None):
        '''Returns the spectrum offset time.'''
        if unit is None:
            unit=self.time_unit
        return float(self.inst.query('SENS:SPEC:STAR?'))/self.times[unit]
    gate_start=property(get_gate_start,set_gate_start)

#############################Trace Options################################

    def show_trace(self,trace):
        self.inst.write('TRAC{}:SPEC ON'.format(trace))
    def trace_off(self,trace):
        self.inst.write('TRAC{}:SPEC OFF'.format(trace))

    def set_averaging(self,trace,avg,count=True):
        '''
        count=1 causes a single acquisition of the analyzer to avg over the
        number of spectra specified by avg.  If count=0, a single acquisition
        will only collect a single run, and averaging will only work with the
        analyzer in continuous acquisition mode.
        '''
        self.inst.write('TRAC{}:SPEC:FUNC AVER'.format(trace))
        self.inst.write('TRAC{}:SPEC:AVER:COUN {}'.format(trace,avg))
        if count:
            self.inst.write('TRAC{}:SPEC:COUNT:ENAB 1'.format(trace))
        else:
            self.inst.write('TRAC{}:SPEC:COUNT:ENAB 0'.format(trace))
    def get_averaging(self,trace):
        return float(self.inst.query('TRAC{}:SPEC:AVER:COUN?'.format(trace)))
    def reset_averaging(self,trace):
        self.inst.write('TRAC{}:SPEC:AVER:RES'.format(trace))

#############################Acquisition################################

    def acquisition_mode(self,mode):
        if mode==0 or mode=='single':
            self.inst.write('INIT:CONT OFF')
        elif mode==1 or mode=='cont' or mode=='continuous':
            self.inst.write('INIT:CONT ON')
        else: print('Invalid input.  Input 0 or \'single\' for single, 1 or \
            \'cont\' or \'continuous\' for continuous')

    def acquire(self):
        self.inst.write('INIT')


    def restart_acquire(self):
        self.inst.write('SENSE:SPECTRUM:CLEAR:RESULTS')

    def set_acq_time(self,time):
        self.inst.write('SENSE:ACQUISITION:SECONDS {}'.format(time))

    def get_acq_time(self):
        return float(self.inst.query('SENSE:ACQUISITION:SECONDS?'))

    acq_time = property(get_acq_time, set_acq_time)

    def set_acq_samples(self,samples):
        self.inst.write('SENSE:ACQUISITION:SAMPLES {}'.format(samples))

    def get_acq_samples(self):
        return float(self.inst.query('SENSE:ACQUISITION:SAMPLES?'))

    acq_samples = property(get_acq_samples, set_acq_samples)

#############################GPIB################################

    def set_gpib(self,address):
        self.inst.write('SYST:COMM:GPIB:SELF:ADDR {}'.format(address))

    def get_gpib(self):
        return float(self.inst.query('SYST:COMM:GPIB:SELF:ADDR?'))

    gpib = property(get_gpib,set_gpib)

#############################RBW################################

    def set_rbw(self,rbw,unit=None):
        if unit is None:
            unit=self.freq_unit
        self.inst.write('SENS:SPEC:BAND:RES {}{}'.format(rbw,unit))

    def get_rbw(self,unit=None):
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('SENS:SPEC:BAND:RES:ACT?'))/self.frequencies[unit]

    rbw = property(get_rbw,set_rbw)

    def set_rbw_auto(self,auto):
        self.inst.write('SENS:SPEC:BAND:RES:AUTO {}'.format(auto))

    def get_rbw_auto(self):
        return int(self.inst.query('SENS:SPEC:BAND:AUTO?'))

    rbw_auto = property(get_rbw_auto,set_rbw_auto)


class Tek5103Functions(Tek5103):
    def __init__(self,inst):
        self.inst=inst
        self.freq_unit='MHz'
        self.time_unit='us'

    def stitch_scans(self,start_freq,stop_freq,trace=None,scan_width=None):
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
        self.center_freq+=step_size
        print('Center: {}{}'.format(self.center_freq,self.freq_unit))

    def enbw(self):
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
