import numpy as np
class Hp8647(object):
    frequencies={'MHz':1000000.,'kHz':1000.,'Hz':1.}
    power_units=('dBm','mV')
    def __init__(self,inst):
        self.inst=inst
        self.freq_unit='MHz'
        self.pow_unit='dBm'
        self.max_pow=13

    def set_frequency(self,freq,unit=None):
        if unit is None:
            unit=self.freq_unit
        self.inst.write('FREQ:CW {} {}'.format(freq,unit))

    def get_frequency(self,unit=None):
        if unit is None:
            unit=self.freq_unit
        return float(self.inst.query('FREQ:CW?'))/self.frequencies[unit]

    frequency = property(get_frequency,set_frequency)

    def set_rf_on(self,on):
        self.inst.write('OUTP:STAT {}'.format(on))

    def get_rf_on(self):
        return float(self.inst.query('OUTP:STAT?'))

    rf_on = property(get_rf_on,set_rf_on)

    def set_power(self,power,unit=None):
        if unit is None:
            unit=self.pow_unit
        if power > self.max_pow:
            power = self.max_pow
            print('Warning: Power greater than max_pow.')  
            print('Power will be to {}{}'.format(self.max_pow,
                                                 self.pow_unit))
        self.inst.write('POW:AMPL {}{}'.format(power,unit))

    def get_power(self):
        return float(self.inst.query('POW:AMPL?'))

    pow = property(get_power,set_power) 


class Tek3102(object):
    frequencies={'MHz':1000000.,'kHz':1000.,'Hz':1.}
    voltages={'mV':.001,'V':1.}
    channels=(1,2)
    def __init__(self,inst):
        self.inst=inst
        self.freq_unit='MHz'
        self.volt_unit='V'
        self.channel=1

    def set_frequency(self,freq,unit=None,channel=None):
        if unit is None:
            unit=self.freq_unit
        if channel is None:
            channel=self.channel
        self.inst.write('SOUR{}:FREQ {}{}'.format(channel,freq,unit))

    def get_frequency(self,unit=None,channel=None):
        if unit is None:
            unit=self.freq_unit
        if channel is None:
            channel=self.channel
        return float(self.inst.query('SOUR{}:FREQ?'.format(channel)))/self.frequencies[unit]

    frequency=property(get_frequency,set_frequency)

    def get_volt_low(self,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:LOW?'))

    def set_volt_low(self,v,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        self.inst.write('SOUR{}:VOLT:LOW {}{}'.format(channel,v,unit))

    vmin=property(get_volt_low,set_volt_low)

    def get_volt_high(self,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:HIGH?'))

    def set_volt_high(self,v,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        self.inst.write('SOUR{}:VOLT:HIGH {}{}'.format(channel,v,unit))

    vmax=property(get_volt_high,set_volt_high)

    def get_volt_offset(self,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        return float(self.inst.query('SOUR{}:VOLT:OFFSET?'.format(channel)))

    def set_volt_offset(self,v,channel=None,unit=None):
        if channel is None:
            channel=self.channel
        if unit is None:
            unit=self.volt_unit
        self.inst.write('SOUR{}:VOLT:OFFSET {}{}'.format(channel,v,unit))

    voffset=property(get_volt_offset,set_volt_offset)

    def output(self,on,channel=None):
        if channel is None:
            channel=self.channel
        if on==1:
            self.inst.write('OUTPUT{} ON'.format(channel))
        elif on==0:
            self.inst.write('OUTPUT{} OFF'.format(channel))
        else:
            print('on=1 for on, on=0 for out')

    def get_waveform(self,channel=None):
        """Valid waveforms:
           SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe
        """
        if channel is None:
            channel=self.channel
        return self.inst.query('SOUR{}:FUNCTION?'.format(channel))

    def set_waveform(self,wave,channel=None):
        """Valid waveforms:
           SINusoid|SQUare|PULse|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|
           ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe
        """
        if channel is None:
            channel=self.channel
        self.inst.write('SOUR{}:FUNCTION {}'.format(channel,wave))

    waveform=property(get_waveform,set_waveform)

    def transfer_waveform(self,wvfrm,location=None,channel=None):
        # waveform must be integer values between 0 and 16382
        if location is None:
            location='USER1'
        if channel is None:
            channel=self.channel
        wv=np.array(wvfrm)
        points=len(wvfrm)
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
            channel=self.channel
        return self.inst.query('SOUR{}:BURST:STATE?'.format(channel))

    def set_burst(self,state,channel=None):
        #state = 1 for on, 0 for off, may use strings 'on/off' as well
        if channel is None:
            channel=self.channel
        self.inst.write('SOUR{}:BURST:STATE {}'.format(channel,state))

    burst=property(get_burst,set_burst)

    def get_burst_cycles(self,channel=None):
        """
        Returns 9.9E+37 if burst count is set to INFinity
        """
        if channel is None:
            channel=self.channel
        return self.inst.query('SOUR{}:BURST:NCYCLES?'.format(channel))

    def set_burst_cycles(self,cycles,channel=None):
        """
        cycles = <cycles>|INFinity|MIN|MAX}
        <cycles> ranges from 1 to 1,000,000
        """
        if channel is None:
            channel=self.channel
        self.inst.write('SOUR{}:BURST:NCYCLES {}'.format(channel,cycles))

    burst_cycles=property(get_burst_cycles,set_burst_cycles)

    def get_burst_mode(self,channel=None):
        if channel is None:
            channel=self.channel
        return self.inst.query('SOUR{}:BURST:MODE?'.format(channel))

    def set_burst_mode(self,mode,channel=None):
        """
        mode = {TRIGgered|GATed}
        """
        if channel is None:
            channel=self.channel
        self.inst.write('SOUR{}:BURST:MODE {}'.format(channel,mode))

    burst_mode=property(get_burst_mode,set_burst_mode)

    def get_trigger_source(self):
        return self.inst.query('TRIG:SOUR?')

    def set_trigger_source(self,source):
        """
        source = {EXTernal,TIMed}
        Note that TIMed is equivalent to 'internal' on the front panel
        """
        self.inst.write('TRIG:SOUR {}'.format(source))

    trigger_source=property(get_trigger_source,set_trigger_source)

