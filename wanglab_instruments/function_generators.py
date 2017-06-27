import numpy as np
import datetime
def prop_doc(var):
    s1 = '{} = property(get_{}, set_{})\n\n'.format(var, var, var)
    s2 = 'See help on get_{} and set_{} functions for info.'.format(var, var)
    return s1 + s2

def timestamp():
    return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')

class RSsmc100(object):
    """ Initialize RSsmc100 class object.

    This class controls the Rohde and Schwarz smc100 signal generator.
    """

    frequencies = {'GHz':1000000000,'MHz':1000000.,'kHz':1000.,'Hz':1.}
    power_units = ('dBm','V','DBUV')
    phase_units = ('DEGR','RAD')

    def __init__(self,inst,pow_unit='dBm',freq_unit='MHz',phase_unit='RAD'):
        self.inst = inst
        self.pow_unit = pow_unit
        self.phase_unit = phase_unit
        self.freq_unit = freq_unit

    def __repr__(self):
        return 'RSsmc100({}, pow_unit = {}, freq_unit = {})'.format(
            str(self.inst).split()[-1],
            self.pow_unit,
            self.freq_unit)

    @property
    def pow_unit(self):
        """ pow_unit sets the power units.  Can be one of
        {dBm | V | DBUV }.
        """
        return self.inst.query('UNIT:POW?').strip()

    @pow_unit.setter
    def pow_unit(self, value):
        if value in self.power_units:
            self.inst.write('UNIT:POW {}'.format(value))
        else:
            if type(value) == str:
                raise ValueError('pow_unit = { dBm | V | DBUV }')
            else:
                raise TypeError('pow_unit must be str')
    @property
    def phase_unit(self):
        """ phase_unit sets the phase units.  Can be one of
        {RAD | DEGR }.
        """
        return self.inst.query('UNIT:ANGLE?').strip()

    @phase_unit.setter
    def phase_unit(self, value):
        if value in self.phase_units:
            self.inst.write('UNIT:ANGLE {}'.format(value))
        else:
            if type(value) == str:
                raise ValueError('phase_unit = { RAD | DEGR }')
            else:
                raise TypeError('phase_unit must be str')

    @property
    def freq_unit(self):
        """ freq_unit sets the frequency units.  Can be one of
        {GHz | MHz | kHz | Hz}.  
        
        Note that the smc100 works exclusively with Hz.  The freq_unit
        property looks up other units from a dictionary and does a
        conversion from Hz to the proper units.  This is opposed to the
        pow_unit and phase_unit, which are stored in the scm100.  In those
        cases, getting and setting actually make calls to the smc100.
        """
        return self._freq_unit

    @freq_unit.setter
    def freq_unit(self, value):
        if value in self.frequencies.keys():
            self._freq_unit = value
        else:
            if type(value) == str:
                raise ValueError('freq_unit = {}'.format(
                    self.frequencies.keys()))
            else:
                raise TypeError('freq_unit must be str')

    @property
    def power(self):
        return float(self.inst.query('POW?'))

    @power.setter
    def power(self, value):
        self.inst.write('POW {}'.format(value))

    @property
    def freq(self):
        return (float(self.inst.query('FREQ?'))
            /self.frequencies[self.freq_unit])

    @freq.setter
    def freq(self, value):
        self.inst.write('FREQ {} {}'.format(value,self.freq_unit))

    @property
    def phase(self):
        return float(self.inst.query('PHASE?'))

    @phase.setter
    def phase(self, value):
        self.inst.write('PHASE {}'.format(value))

    @property
    def zero_phase(self):
        self.inst.write('PHASE:REF')

    @property
    def rf_on(self):
        return int(self.inst.query('OUTP?'))

    @rf_on.setter
    def rf_on(self, value):
        if value == 0 or value == 1:
            self.inst.write('OUTP {}'.format(value))
        else:
            raise ValueError('rf_on takes 0 for off, 1 for on')

    def state(self, write_to=None, name=None):
        s = []
        s.append('{}\n'.format(timestamp()))
        if name is not None:
            s.append('nickname: {}\n'.format(name))
        s.append('{}'.format(self.inst.query('*IDN?')))
        s.append('Power: {} {}\n'.format(self.power,self.pow_unit))
        s.append('Frequency: {} {}\n'.format(self.freq,self.freq_unit))
        s.append('Phase: {} {}\n'.format(self.phase,self.phase_unit))
        if write_to is None:
            for line in s:
                print(line,end='')
        else:
            with open(write_to,'a') as f:
                for line in s:
                    f.write(line)

class Hp8647(object):
    """Initialize Hp8467 class object

    Args:
        inst (object) : Object for communication with an HP8647 
            signal generator.  Typically a pyVisa Resource.
        freq_unit (str, optional) : Default frequency unit.  May be 
            MHz, kHz, or Hz.  Defaults to MHz.
        pow_unit (str, optional) : Default power unit.  May be dBm or
            mV.  Defaults to dBm.
        max_power (float) : Maximum power the generator can be set to.
            Defaults to 13 dBm.

    Examples:
        # Hp8647 signal generator on GPIB channel 5.
        # Using pyVisa to create a Resource object.
        >>> from wanglab_instruments.function_generators import Hp8647
        >>> import visa
        >>> rm = visa.ResourceManager()
        >>> rm.list_resources()
        ('GPIB0::5::INSTR')
        >>> hp = Hp8647(rm.open_resource('GPIB0::5::INSTR'))
    """

    frequencies = {'MHz':1000000.,'kHz':1000.,'Hz':1.}
    power_units = ('dBm','mV')

    def __init__(self,inst,freq_unit='MHz', pow_unit='dBm', 
                    max_power=13):
        self.inst = inst
        self.freq_unit = freq_unit
        self.pow_unit = pow_unit
        self.max_power = max_power

    def get_freq_unit(self):
        """
        get_freq_unit(self):        

        get the value of freq_unit        

        Args:
            None
        
        Returns:
            self._freq_unit
        """
        return self._freq_unit

    def set_freq_unit(self,freq):
        """
        set_freq_unit(self,freq):        

        set the value of freq_unit        

        Args:
            freq (str) : { MHz | kHz | Hz }
        
        Returns:
            None
        """
        if freq in self.frequencies.keys():
            self._freq_unit = freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = { MHz | kHz | Hz }')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit, doc =
        prop_doc('freq_unit'))

    def get_pow_unit(self):
        """
        get_pow_unit(self):        

        get the value of pow_unit        

        Args:
            None
        
        Returns:
            self._pow_unit
        """
        return self._pow_unit

    def set_pow_unit(self,power):
        """
        set_pow_unit(self,power):        

        set the value of pow_unit        

        Args:
            power (str) : { dBm | mV }
        
        Returns:
            None
        """
        if power in self.power_units:
            self._pow_unit = power
        else:
            if type(power) == str:
                raise ValueError('pow_unit = dBm|mV')
            else:
                raise TypeError('pow_unit must be str')

    pow_unit = property(get_pow_unit, set_pow_unit, doc=prop_doc('pow_unit'))

    def __repr__(self):
        return 'Hp8647({!r}, {!r}, {!r}, max_power={!r})'.format(
        self.inst, self.freq_unit, self.pow_unit, self.max_power)

    def set_frequency(self,freq,unit=None):
        """
        set_frequency(self,freq,unit=None):        

        set the value of frequency        

        Args:
            freq (float) : Frequency
            unit (str, optional) : { MHz | kHz | Hz }
        
        Returns:
            None
        """
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:CW {} {}'.format(freq,unit))

    def get_frequency(self,unit=None):
        """
        get_frequency(self,unit=None):        

        get the value of frequency        

        Args:
            unit (str, optional) : { MHz | kHz | Hz }
        
        Returns:
            float: Value of frequency in specified unit
        """
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:CW?'))/self.frequencies[unit]

    frequency = property(get_frequency,set_frequency,
        doc=prop_doc('frequency'))

    def set_rf_on(self,on):
        """
        set_rf_on(self,on):        

        set the value of rf_on        

        Args:
            rf_on (bool) : True for on, False for off
        
        Returns:
            None
        """
        self.inst.write('OUTP:STAT {}'.format(on))

    def get_rf_on(self):
        """
        get_rf_on(self):        

        get the value of rf_on        

        Args:
            None
        
        Returns:
            1 for on, 0 for off
        """
        return float(self.inst.query('OUTP:STAT?'))

    rf_on = property(get_rf_on,set_rf_on, doc=prop_doc('rf_on'))

    def set_power(self,power,unit=None):
        """
        set_power(self,power,unit=None):        

        set the value of power        

        Args:
            power (float) : rf output power.  If power exceeds max_pow, pow is
                set to max_pow.
            unit (str, optional) : { dBm | mV }
        
        Returns:
            None
        """
        if unit is None:
            unit = self.pow_unit
        if power > self.max_power:
            power = self.max_power
            print('Warning: Power greater than max_pow.')  
            print('Power will be to {}{}'.format(self.max_power,
                                                 self.pow_unit))
        self.inst.write('POW:AMPL {}{}'.format(power,unit))

    def get_power(self):
        """
        get_power(self):        

        get the value of power        

        Args:
            None
        
        Returns:
            float: The current output power in specified units
        """
        return float(self.inst.query('POW:AMPL?'))

    power = property(get_power,set_power, doc=prop_doc('power')) 

    def state(self, write_to=None):
        s = []
        s.append('{}\n'.format(timestamp()))
        if name is not None:
            s.append('nickname: {}\n'.format(name))
        s.append('{}'.format(self.inst.query('*IDN?')))
        s.append('Power: {} {}\n'.format(self.power,self.pow_unit))
        s.append('Frequency: {} {}\n'.format(self.frequency,self.freq_unit))
        if write_to is None:
            for line in s:
                print(line,end='')
        else:
            with open(write_to,'a') as f:
                for line in s:
                    f.write(line)



class Tek3102(object):
    """Initialize Tek3102 class object

    Args:
        inst (object): Object for communication with an HP8647 
            signal generator.  Typically a pyVisa Resource.
        freq_unit (str, optional): Default frequency unit.  May be 
            MHz, kHz, or Hz.  Defaults to MHz.
        volt_unit (str, optional): Default voltage unit.  May be V or
            mV.  Defaults to V.
        channel (int, optional): Output channel to be controlled.  
            Default is channel 1.

    Examples:
        # Tek3102 funtion generator on GPIB channel 6.
        # Using pyVisa to create a Resource object.
        >>> from wanglab_instruments.function_generators import Tek3102
        >>> import visa
        >>> rm = visa.ResourceManager()
        >>> rm.list_resources()
        ('GPIB0::6::INSTR')
        >>> afg = Tek3102(rm.open_resource('GPIB0::6::INSTR'), channel=2)
        # Check which output channel we are controlling
        >>> afg.channel
        2
        # Check which waveform the function generator is outputting
        >>> afg.waveform
        'SIN'
        # Set waveform to DC
        >>> afg.waveform = 'DC'
        >>> afg.waveform
        'DC'
    """

    frequencies = {'MHz':1000000.,'kHz':1000.,'Hz':1.}
    voltages = {'mV':.001,'V':1.}
    channels = (1,2)

    def __init__(self,inst, freq_unit='MHz', volt_unit='V', channel=1):
        self.inst = inst
        self.freq_unit = freq_unit
        self.volt_unit = volt_unit
        self.channel = channel

    def get_freq_unit(self):
        """
        get_freq_unit(self):        

        get the value of freq_unit        

        Args:
            None
        
        Returns:
            self._freq_unit
        """
        return self._freq_unit

    def set_freq_unit(self,freq):
        """
        set_freq_unit(self,freq):        

        set the value of freq_unit        

        Args:
            freq (str) : { MHz | kHz | Hz } 
        
        Returns:
            None
        """
        if freq in self.frequencies.keys():
            self._freq_unit = freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = { MHz | kHz | Hz }')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit,
        doc=prop_doc('freq_unit'))

    def get_volt_unit(self):
        """
        get_volt_unit(self):        

        get the value of volt_unit        

        Args:
            None
        
        Returns:
            self._volt_unit
        """
        return self._volt_unit

    def set_volt_unit(self,volt):
        """
        set_volt_unit(self,volt):        

        set the value of volt_unit        

        Args:
            volt (str) : { V | mV }
        
        Returns:
            None
        """
        if volt in self.voltages.keys():
            self._volt_unit = volt
        else:
            if type(volt) == str:
                raise ValueError('volt_unit = { V | mV }')
            else:
                raise TypeError('volt_unit must be str')

    volt_unit = property(get_volt_unit, set_volt_unit,
        doc=prop_doc('volt_unit'))

    def get_channel(self):
        """
        get_channel(self):        

        get the value of channel        

        Args:
            None
        
        Returns:
            self._channel
        """
        return self._channel

    def set_channel(self,channel):
        """
        set_channel(self,channel):        

        set the value of channel        

        Args:
            channel (int) : { 1 | 2 } 
        
        Returns:
            None
        """
        if channel in self.channels:
            self._channel = channel
        else:
            if type(channel) == int:
                raise ValueError('channel = 1|2')
            else:
                raise TypeError('channel must be int')

    channel = property(get_channel, set_channel, doc=prop_doc('channel'))

    def __repr__(self):
        return 'Tek3102({!r}, {!r}, {!r}, channel={!r})'.format(
        self.inst, self.freq_unit, self.volt_unit, self.channel)

    def set_frequency(self,freq,unit=None,channel=None):
        """
        set_frequency(self,freq,unit=None,channel=None):        

        set the value of frequency        

        Args:
            freq (flot) : Frequency 
            unit (str, optional) : { MHz | kHz | Hz }
            channel (int, optional) : { 1 | 2 } 
        
        Returns:
            None
        """
        if unit is None:
            unit = self.freq_unit
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:FREQ {}{}'.format(channel,freq,unit))

    def get_frequency(self,unit=None,channel=None):
        """
        get_frequency(self,unit=None,channel=None):        

        get the value of frequency        

        Args:
            unit (str, optional) : { MHz | kHz | Hz }
            channel (, optional) : { 1 | 2 }
        
        Returns:
            output frequency on specified channel in specified units
        """
        if unit is None:
            unit = self.freq_unit
        if channel is None:
            channel = self.channel
        return float(self.inst.query('SOUR{}:FREQ?'.format(channel)))/self.frequencies[unit]

    frequency = property(get_frequency,set_frequency)

    def get_volt_low(self,channel=None,unit=None):
        """
        get_volt_low(self,channel=None,unit=None):        

        get the value of volt_low, setting the minimum voltage on the waveform        

        Args:
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            float: Minimum voltage on output waveform on specified channel
                with specified units.
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:LOW?'))

    def set_volt_low(self,v,channel=None,unit=None):
        """
        set_volt_low(self,v,channel=None,unit=None):        

        set the value of volt_low        

        Args:
            v (float) : low voltage for output waveform
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:LOW {}{}'.format(channel,v,unit))

    vmin = property(get_volt_low,set_volt_low)

    def get_volt_high(self,channel=None,unit=None):
        """
        get_volt_high(self,channel=None,unit=None):        

        get the value of volt_high, the max output voltage of the waveform     

        Args:
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            float: max output voltage of the waveform
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:HIGH?'))

    def set_volt_high(self,v,channel=None,unit=None):
        """
        set_volt_high(self,v,channel=None,unit=None):        

        set the value of volt_high, the max output voltage for the waveform        

        Args:
            v (float) : max output voltage
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:HIGH {}{}'.format(channel,v,unit))

    vmax = property(get_volt_high,set_volt_high)

    def get_volt_offset(self,channel=None,unit=None):
        """
        get_volt_offset(self,channel=None,unit=None):        

        get the value of volt_offset, the voltage offset for the waveform        

        Args:
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            float: waveform offset voltage
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:OFFSET?'.format(channel)))

    def set_volt_offset(self,v,channel=None,unit=None):
        """
        set_volt_offset(self,v,channel=None,unit=None):        

        set the value of volt_offset, the waveform offset voltage        

        Args:
            v (float) : waveform offset voltage
            channel (int, optional) : { 1 | 2 }
            unit (str, optional) : { V | mV }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:OFFSET {}{}'.format(channel,v,unit))

    voffset = property(get_volt_offset,set_volt_offset,
        doc=prop_doc('voffset'))

    def output(self,on,channel=None):
        """
        output(self, on, channel=None)

        Toggle the channel output on or off
        
        Args:
            on (int) : 1 for on, 0 for off
            channel(int, optional) : { 1 | 2 }
            
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        if on == 1:
            self.inst.write('OUTPUT{} ON'.format(channel))
        elif on == 0:
            self.inst.write('OUTPUT{} OFF'.format(channel))
        else:
            print('on = 1 for on, on = 0 for off')

    def get_waveform(self,channel=None):
        """
        get_waveform(self,channel=None):        

        get the value of waveform        
        valid waveforms:
           { SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe }

        Args:
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            str: output waveform on specified channel
        """
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:FUNCTION?'.format(channel))

    def set_waveform(self,wave,channel=None):
        """
        set_waveform(self,wave,channel=None):        

        set the value of waveform        
        valid waveforms:
           { SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe }

        Args:
            wave (str) : one of valid waveforms
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:FUNCTION {}'.format(channel,wave))

    waveform = property(get_waveform,set_waveform, doc=prop_doc('waveform'))

    def transfer_waveform(self,wvfrm,location=None,channel=None):
        """
        transfer_waveform(self,wvfrm,location=None,channel=None)

        Transfers user defined waveform to location, sets output channel to
        the waveform.  Waveform must be integer values between 0 and 16382.

        Args:
            wvfrm (list, tuple, or array of type int) : Waveform data to be transfered.
            location (str, optional) : location for transfer.  One of USER{1 |
                2 | 3 | 4}.  Default to USER1
            channel(int, optional) : { 1 | 2 }

        Returns:
            None
        """
        if location is None:
            location = 'USER1'
        if channel is None:
            channel = self.channel
        wv = np.array(wvfrm)
        points = len(wvfrm)
        self.inst.write('DATA:DEFINE EMEMORY,{}'.format(points))
        self.inst.write_binary_values('DATA:DATA EMEM,',wv,
        is_big_endian=True,datatype='h')
        print('Transfer complete')
        self.inst.write('TRAC:COPY {},EMEM'.format(location))
        print('Waveform copied to {}'.format(location))
        self.inst.write('SOURCE{}:FUNCTION {}'.format(channel,location))
        print('Function set to {}'.format(location))

    def get_burst(self,channel=None):
        """
        get_burst(self,channel=None):        

        get the value of burst.  1 if channel is set to burst mode, 0
        otherwise.        

        Args:
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            int: 1 if set to burst, 0 otherwise
        """
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:BURST:STATE?'.format(channel))

    def set_burst(self,state,channel=None):
        """
        set_burst(self,state,channel=None):        

        set the value of burst        

        Args:
            state (int) : 1 to turn burst mode on, 0 to turn off
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:STATE {}'.format(channel,state))

    burst = property(get_burst,set_burst,doc=prop_doc('burst'))

    def get_burst_cycles(self,channel=None):
        """
        get_burst_cycles(self,channel=None):        

        get the value of burst_cycles        

        Args:
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            float: number of burst cycles.  9.9E+37 if burst count is set to
            INFinity
        """
        if channel is None:
            channel = self.channel
        return float(self.inst.query('SOUR{}:BURST:NCYCLES?'.format(channel)))

    def set_burst_cycles(self,cycles,channel=None):
        """
        set_burst_cycles(self,cycles,channel=None):        

        set the value of burst_cycles        

        Args:
            cycles (int or str) : int between 1 and 1,000,000 | INFinity | MIN
                | MAX
            channel (, optional) : 
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:NCYCLES {}'.format(channel,cycles))

    burst_cycles = property(get_burst_cycles,set_burst_cycles,
        doc=prop_doc('burst_cycles'))

    def get_burst_mode(self,channel=None):
        """
        get_burst_mode(self,channel=None):        

        get the value of burst_mode        

        Args:
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            str : burst mode
        """
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:BURST:MODE?'.format(channel))

    def set_burst_mode(self,mode,channel=None):
        """
        set_burst_mode(self,mode,channel=None):        

        set the value of burst_mode        

        Args:
            mode (str) : { TRIGered | GATed }
            channel (int, optional) : { 1 | 2 }
        
        Returns:
            None
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:MODE {}'.format(channel,mode))

    burst_mode = property(get_burst_mode,set_burst_mode,
        doc=prop_doc('burst_mode'))

    def get_trigger_source(self):
        """
        get_trigger_source(self):        

        get the value of trigger_source        

        Args:
            None
        
        Returns:
            str : { EXTernal | TIMed }
        """
        return self.inst.query('TRIG:SOUR?')

    def set_trigger_source(self,source):
        """
        set_trigger_source(self,source):        

        set the value of trigger_source        
        Note that TIMed is equivalent to 'internal' on the front panel

        Args:
            source (str) : { EXTernal | TIMed } 
        
        Returns:
            None
        """
        self.inst.write('TRIG:SOUR {}'.format(source))

    trigger_source = property(get_trigger_source,set_trigger_source,
        doc=prop_doc('trigger_source'))

    def state(self, write_to=None, name=None):
        s = []
        s.append('nickname: {}\n'.format(timestamp()))
        if name is not None:
            s.append('{}\n'.format(name))
        s.append('{}'.format(self.inst.query('*IDN?')))
        s.append('Frequency: {} {}\n'.format(self.frequency,self.freq_unit))
        if write_to is None:
            for line in s:
                print(line,end='')
        else:
            with open(write_to,'a') as f:
                for line in s:
                    f.write(line)


