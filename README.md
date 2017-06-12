# wanglab_instruments

This package provides a Python interface to lab equipment that is commonly
used in Hailin Wang's lab at University of Oregon in the Department of
Physics.  

### Recommended packages

* numpy
* pyVisa

### Usage

Each instrument is represented by a class, and each class is
instantiated with a communication object that can send and receive bits from
the instrument.  The most common way to set up communication is with a pyVisa
Resource object.  This is the only type of communication that this package has
been tested with, but it should work just as well with other types of
communication, for example pySerial.

The standard way to start a session is to:
1. Import wanglab_instruments and pyVisa.
2. Use the pyVisa resource manager to view available instruments.
3. Creat an instance of the desired instrument class with a pyVisa
    Resource object.

Example:
```python
>>> import wanglab_instruments as wl
>>> import visa
>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> rm = visa.ResourceManager()
>>> rm.list_resources()
('GPIB0::1::INSTR', 'GPIB0::13::INSTR')
# GPIB channel 1 is a Tek5103 spectrum analyzer
# GPIB channel 13 is a HP8467 signal generator
>>> rsa = wl.spectrum_analyzers.Tek5103(rm.open_resource('GPIB0::1::INSTR'))
>>> hp = wl.function_generators.Hp8467(rm.open_resource('GPIB0::13::INSTR'))
```

We now have an object called rsa (real-time spectrum analyzer) that
communicates with the Tek5103 and another object called hp that communicates
with the Hp8467 signal generator.  Each class has methods for controlling the
instruments in interesting ways.  Collecting a spectrum from trace 2 on the
spectrum analyzer can be accomplished with the code snippet

    >>> x, y = rsa.fetch_spectrum(2)

It should be noted that many methods return numpy arrays, and so it is
necessary to import numpy when using wanglab_instruments.

### Example

From the basic interfacing, one may now quickly create scripts to automate many
experiments.  The experiment, data collection, data analysis, and plotting
can all be done in a single pipeline in a Python environment.  

Suppose, for example, that our Hp8467 is connected through a bandpass filter
to the Tek5103 spectrum analyzer, and we want to measure the FWHM linewidth
and center frequency of the filter, which is known to have a Lorentzian
lineshape centered near 100MHz with a roughly 1 MHz linewidth.  The test could
be run as follows:

```python
>>> from scipy.optimize import curve_fit
>>> import matplotlib.pyplot as plt

# Define lorentzian function for fitting
>>> def lorentzian(x,x0,amp,width):
>>>    return 0.25*amp*width**2 / (x - x0)**2 + 0.25*width**2 # width is FWHM

# Collect data
>>> drive_frequency = np.linspace(90,110,50)
>>> response = np.zeros(len(drive_frequency))
>>>     for i in len(drive_frequency):
>>>     hp.frequency = drive_frequency[i]
>>>     x,y = rsa.read_spectrum(trace=1)
>>>     response[i] = np.max(y)

# Least squares fit
>>> popt, pcov = curve_fit(lorentzian, drive_frequency, response)
>>> FWHM = popt[-1]

>>> plt.plot(drive_frequency, response, '.')
>>> plt.plot(drive_frequency, lorentzian(drive_frequency, *popt))
```

This short script, from start to finish, collects 50 data points, performs
least squares fitting to the data, and plots the fit over the measured values.  
