def prop_doc(var):
    s1 = '{} = property(get_{}, set_{})\n\n'.format(var, var, var)
    s2 = 'See help on get_{} and set_{} functions for info.'.format(var, var)
    return s1 + s2
class SR844(object):
    def __init__(self,inst):
        self.inst = inst

    def read_ref_freq(self):
        """reads the reference frequency in Hz"""
        return float(self.inst.query('FRAQ?'))

    ref_freq = property(read_ref_freq,doc='reads reference frequency in Hz')

    def read_ch1(self):
        """reads channel 1 output"""
        return float(self.inst.query('OUTR? 1'))

    ch1 = property(read_ch1,doc='reads channel 1 output')

    def read_ch2(self):
        """reads channel 2 output"""
        return float(self.inst.query('OUTR? 2'))

    ch2 = property(read_ch2,'reads channel 2 output')

    def read_xy(self):
        """reads channel 1 and channel 2 outputs simultaneously

        Returns:
            tuple (float, float) : channel 1, channel 2
        """
        vals = self.inst.query('SNAP? 1,2')
        x = float(vals.split(',')[0])
        y = float(vals.split(',')[1])
        return x,y

    xy = property(read_ch2,doc='read channel 1 and channel 2')

    def get_phase(self):
        """
        get_phase(self):        

        get the value of the reference phase        

        Args:
            None
        
        Returns:
            float : phase in degrees
        """
        return float(self.inst.query('PHAS?'))

    def set_phase(self,phase):
        """
        set_phase(self,phase):        

        set the value of the reference phase        

        Args:
            phase (float) : reference phase in degrees
        
        Returns:
            None
        """
        self.inst.write('PHAS {}'.format(phase))

    phase = property(get_phase,set_phase,doc=prop_doc('phase'))

    def auto_phase(self):
        """Set instrument to autosynch reference phase"""
        self.inst.write('APHS')

    zero_phase = property(auto_phase,doc='autosynch reference phase')
