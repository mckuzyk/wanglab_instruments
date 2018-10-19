import numpy as np
from PyDAQmx import uInt32, int32, int16, byref
import PyDAQmx as daq
import time
import os
def make_counter(countchan, trig=None):
    """
    Configure the given counter to count, maybe with a pause trigger.
    """
    ctr = daq.Task()
    ctr.CreateCICountEdgesChan(countchan, "",
                               daq.DAQmx_Val_Rising,
                               0,  # initial count
                               daq.DAQmx_Val_CountUp)

    if trig is not None:
        # configure pause trigger
        ctr.SetPauseTrigType(daq.DAQmx_Val_DigLvl)
        ctr.SetDigLvlPauseTrigSrc(trig)
        ctr.SetDigLvlPauseTrigWhen(daq.DAQmx_Val_Low)

    return ctr

def make_pulse(duration, pulsechan):
    """
    Configure the counter `pulsechan` to output
    a pulse of the given `duration` (in seconds).
    """
    pulse = daq.Task()
    pulse.CreateCOPulseChanTime(
        pulsechan, "",            # physical channel, name to assign
        daq.DAQmx_Val_Seconds,   # units:seconds
        daq.DAQmx_Val_Low,       # idle state: low
        0.00, .0001, duration,   # initial delay, low time, high time
    )
    return pulse

def configure_counter(duration=.1,
                      pulsechan="Dev1/ctr1",
                      countchan="Dev1/ctr0"):
    """
    Configure the card to count edges on `countchan`, for the specified
    `duration` of time (seconds). This is a hardware-timed thing,
    using the paired counter `pulsechan` to gate the detection
    """

    # configure pulse (for hardware timing)
    pulse = make_pulse(duration, pulsechan)

    # if these are paired counters, we can use the internal output
    # of the pulsing channel to trigger the counting channel
    trigchan = "/%sInternalOutput" % pulsechan.replace('ctr', 'Ctr')

    # configure counter
    ctr = make_counter(countchan, trig=trigchan)

    return pulse, ctr

def start_count(pulse, ctr):
    """ start counting events. """
    # start counter
    ctr.StartTask()
    # fire pulse
    pulse.StartTask()
    return

def finish_count(pulse, ctr):
    """ finish counting events and return the result. """
    # initialize memory for readout
    count = uInt32()
    # wait for pulse to be done
    pulse.WaitUntilTaskDone(10.)
    # timeout, ref to output value, reserved
    ctr.ReadCounterScalarU32(10., byref(count), None)
    pulse.StopTask()
    ctr.StopTask()
    return count.value

def do_count(pulse, ctr):
    """
    simple counting in a synchronous mode
    """
    start_count(pulse, ctr)
    return finish_count(pulse, ctr)

pulse, ctr = configure_counter()
while True:
    print('counts/sec: {0:07d}\r'.format(10*do_count(pulse, ctr)), end='\r')
