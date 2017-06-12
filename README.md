This package provides a Python interface to lab equipment that is commonly
used in Hailin Wang's lab at University of Oregon in the Department of
Physics.  Each instrument is represented by a class, and each class is
instantiated with a communication object that can send and receive bits from
the instrument.  The most common way to set up communication is with pyVisa
Resource object.  This is the only type of communication that this package has
been tested with, but it should work just as well with other types of
communication, for example pySerial.


