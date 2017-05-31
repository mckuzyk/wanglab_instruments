class SR844(object):
    def __init__(self,inst):
        self.inst = inst

    def read_ref_freq(self):
        return float(self.inst.query('FRAQ?'))

    ref_freq = property(read_ref_freq)

    def read_ch1(self):
        return float(self.inst.query('OUTR? 1'))

    ch1 = property(read_ch1)

    def read_ch2(self):
        return float(self.inst.query('OUTR? 2'))

    ch2 = property(read_ch2)

    def read_xy(self):
        vals = self.inst.query('SNAP? 1,2')
        x=float(vals.split(',')[0])
        y=float(vals.split(',')[1])
        return x,y

    xy = property(read_ch2)

    def get_phase(self):
        return float(self.inst.query('PHAS?'))

    def set_phase(self,phase):
        self.inst.write('PHAS {}'.format(phase))

    phase = property(get_phase,set_phase)

    def auto_phase(self):
        self.inst.write('APHS')

    zero_phase = property(auto_phase)
