import numpy as np
class Hp8647(object):
    """Initialize Hp8467 class object

    Args:
        inst (object): Object for communication with an HP8647 
            signal generator.  Typically a pyVisa Resource.
        freq_unit (str, optional): Default frequency unit.  May be 
            MHz, kHz, or Hz.  Defaults to MHz.
        pow_unit (str, optional): Default power unit.  May be dBm or
            mV.  Defaults to dBm.
        max_power (float): Maximum power the generator can be set to.
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
        self._freq_unit = freq_unit
        self._pow_unit = pow_unit
        self.max_power = max_power

    def get_freq_unit(self):
        return self._freq_unit

    def set_freq_unit(self,freq):
        if freq in self.frequencies.keys():
            return freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = MHz|kHz|Hz')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_freq_unit, set_freq_unit)

    def get_pow_unit(self):
        return self._pow_unit

    def set_pow_unit(self,power):
        if power in self.power_units.keys():
            return power
        else:
            if type(power) == str:
                raise ValueError('pow_unit = dBm|mV')
            else:
                raise TypeError('pow_unit must be str')

    pow_unit = property(get_pow_unit, set_pow_unit)

    def __repr__(self):
        return 'Hp8647({!r}, {!r}, {!r}, max_power={!r})'.format(
        self.inst, self.freq_unit, self.pow_unit, self.max_power)

    def set_frequency(self,freq,unit=None):
        """Set frequency.

        Args:
            freq (float): Frequency
            unit (str, optional): Frequency unit.  Can be MHz, kHz, or Hz.  
            If None, unit is set by self.freq_unit.
        """
        if unit is None:
            unit = self.freq_unit
        self.inst.write('FREQ:CW {} {}'.format(freq,unit))

    def get_frequency(self,unit=None):
        """Get current frequency.

        Args:
            unit (str, optional): Frequency unit used to report the 
            frequency.  If none, unit is set by self.freq_unit.
        Returns:
            Float: Frequency setting on instrument.
        """
        if unit is None:
            unit = self.freq_unit
        return float(self.inst.query('FREQ:CW?'))/self.frequencies[unit]

    frequency = property(get_frequency,set_frequency)

    def set_rf_on(self,on):
        self.inst.write('OUTP:STAT {}'.format(on))

    def get_rf_on(self):
        return float(self.inst.query('OUTP:STAT?'))

    rf_on = property(get_rf_on,set_rf_on)

    def set_power(self,power,unit=None):
        if unit is None:
            unit = self.pow_unit
        if power > self.max_power:
            power = self.max_power
            print('Warning: Power greater than max_pow.')  
            print('Power will be to {}{}'.format(self.max_power,
                                                 self.pow_unit))
        self.inst.write('POW:AMPL {}{}'.format(power,unit))

    def get_power(self):
        return float(self.inst.query('POW:AMPL?'))

    power = property(get_power,set_power) 


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
    """

    frequencies = {'MHz':1000000.,'kHz':1000.,'Hz':1.}
    voltages = {'mV':.001,'V':1.}
    channels = (1,2)

    def __init__(self,inst, freq_unit='MHz', volt_unit='V', channel=1):
        self.inst = inst
        self._freq_unit = freq_unit
        self._volt_unit = volt_unit
        self._channel = channel

    def get_freq_unit(self):
        return self._freq_unit

    def set_freq_unit(self,freq):
        if freq in self.frequencies.keys():
            return freq
        else:
            if type(freq) == str:
                raise ValueError('freq_unit = MHz|kHz|Hz')
            else:
                raise TypeError('freq_unit must be str')

    freq_unit = property(get_volt_unit, set_volt_unit)

    def get_volt_unit(self):
        return self._volt_unit

    def set_volt_unit(self,volt):
        if volt in self.voltages.keys():
            return volt
        else:
            if type(volt) == str:
                raise ValueError('volt_unit = V|mV')
            else:
                raise TypeError('volt_unit must be str')

    volt_unit = property(get_volt_unit, set_volt_unit)

    def get_channel(self):
        return self._channel

    def set_channel(self,channel):
        if channel in self.channels.keys():
            return channel
        else:
            if type(channel) == int:
                raise ValueError('channel = 1|2')
            else:
                raise TypeError('channel must be int')

    channel = property(get_channel, set_channel)

    def __repr__(self):
        return '{!r}, {!r}, {!r}, channel={!r}'.format(
        self.inst, self.freq_unit, self.volt_unit, self.channel)

    def set_frequency(self,freq,unit=None,channel=None):
        if unit is None:
            unit = self.freq_unit
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:FREQ {}{}'.format(channel,freq,unit))

    def get_frequency(self,unit=None,channel=None):
        if unit is None:
            unit = self.freq_unit
        if channel is None:
            channel = self.channel
        return float(self.inst.query('SOUR{}:FREQ?'.format(channel)))/self.frequencies[unit]

    frequency = property(get_frequency,set_frequency)

    def get_volt_low(self,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:LOW?'))

    def set_volt_low(self,v,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:LOW {}{}'.format(channel,v,unit))

    vmin = property(get_volt_low,set_volt_low)

    def get_volt_high(self,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:HIGH?'))

    def set_volt_high(self,v,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:HIGH {}{}'.format(channel,v,unit))

    vmax = property(get_volt_high,set_volt_high)

    def get_volt_offset(self,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:OFFSET?'.format(channel)))

    def set_volt_offset(self,v,channel=None,unit=None):
        if channel is None:
            channel = self.channel
        if unit is None:
            unit = self.volt_unit
        self.inst.write('SOUR{}:VOLT:OFFSET {}{}'.format(channel,v,unit))

    voffset = property(get_volt_offset,set_volt_offset)

    def output(self,on,channel=None):
        if channel is None:
            channel = self.channel
        if on == 1:
            self.inst.write('OUTPUT{} ON'.format(channel))
        elif on == 0:
            self.inst.write('OUTPUT{} OFF'.format(channel))
        else:
            print('on = 1 for on, on = 0 for out')

    def get_waveform(self,channel=None):
        """Valid waveforms:
           SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe
        """
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:FUNCTION?'.format(channel))

    def set_waveform(self,wave,channel=None):
        """Valid waveforms:
           SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:FUNCTION {}'.format(channel,wave))

    waveform = property(get_waveform,set_waveform)

    def transfer_waveform(self,wvfrm,location=None,channel=None):
        # waveform must be integer values between 0 and 16382
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
        #returns 1 for on, 0 for off
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:BURST:STATE?'.format(channel))

    def set_burst(self,state,channel=None):
        #state = 1 for on, 0 for off, may use strings 'on/off' as well
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:STATE {}'.format(channel,state))

    burst = property(get_burst,set_burst)

    def get_burst_cycles(self,channel=None):
        """
        Returns 9.9E+37 if burst count is set to INFinity
        """
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:BURST:NCYCLES?'.format(channel))

    def set_burst_cycles(self,cycles,channel=None):
        """
        cycles = <cycles>|INFinity|MIN|MAX}
        <cycles> ranges from 1 to 1,000,000
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:NCYCLES {}'.format(channel,cycles))

    burst_cycles = property(get_burst_cycles,set_burst_cycles)

    def get_burst_mode(self,channel=None):
        if channel is None:
            channel = self.channel
        return self.inst.query('SOUR{}:BURST:MODE?'.format(channel))

    def set_burst_mode(self,mode,channel=None):
        """
        mode = {TRIGgered|GATed}
        """
        if channel is None:
            channel = self.channel
        self.inst.write('SOUR{}:BURST:MODE {}'.format(channel,mode))

    burst_mode = property(get_burst_mode,set_burst_mode)

    def get_trigger_source(self):
        return self.inst.query('TRIG:SOUR?')

    def set_trigger_source(self,source):
        """
        source = {EXTernal,TIMed}
        Note that TIMed is equivalent to 'internal' on the front panel
        """
        self.inst.write('TRIG:SOUR {}'.format(source))

    trigger_source = property(get_trigger_source,set_trigger_source)

