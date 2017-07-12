import numpy as np
from scipy.optimize import curve_fit
import datetime

###################### Timestamp ###############################

def timestamp():
    return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')

###################### linear<-->log ###############################

def unlog(y):
    return 10**(y/10)

def log(y):
    return 10*np.log10(y)

###################### Functional Forms ###############################

def h(t):
    """
    Heaviside function: 
        1 if t > 0
        0 if t < 0
        0.5 if t = 0

    Args:
        t : float, array
    """
    return 0.5*(np.sign(t) + 1)

def exp_decay(x,x0=0,y0=0,amp=1,gamma=1):
    """
    exp_decay(x,x0=0,y0=0,gamma=1):
    """
    return y0 + amp*h(x-x0)*np.exp(-(x-x0)*gamma)

def lorentzian(x,x0=0,y0=0,amp=1,fwhm=1):
    """
    lorentzian(x,x0=0,y0=0,amp=1,fwhm=1)

    Args:
        x : float, array  
            x values to evaluate function
        x0 : float, optional
            x-axis location of peak.  Default value is 0.
        y0 : float, optional  
            y-axis offset.  Default value is 0.
        amp : float, optional
            amplitude of the peak (max - min).  Default value is 1.
        fwhm : float, optional
            Full width at half max of the peak.  Defaul value is 1.

    Returns:
        float, array : lorentzian function evaluated at x values
    """
    return y0 + 0.25*amp*fwhm**2/((x-x0)**2 + 0.25*fwhm**2)

def lorentzian_triplet(x,x0=0,y0=0,amp=1,fwhm=.2,
                        xl=-1,ampl=1,fwhml=.2,
                        xr=1,ampr=1,fwhmr=.2):
    return lorentzian(x,xl,y0,ampl,fwhml) + \
           lorentzian(x,x0,0,amp,fwhm) + \
           lorentzian(x,xr,0,ampr,fwhmr) 

def line(x,m=1,b=0):
    """
    line(x, m, b)

    Equation for a line with slope m and y-intercept b

    Args:
        x : float, array
            x-axis values 
        m : float
            Slope of line.  Default value is 1.
        b : float
            y-intercept.  Default value is 0

    Returns:
        float, array : linear function evaluated at x values
    """
    return m*x + b

###################### Fitting ###############################

def fit_lorentzian(x_data, y_data, x0=None, y0=None, amp=None, fwhm=None):
    if x0 is None:
        x0 = x_data[np.argmax(y_data)]
    if y0 is None:
        y0 = np.amin(y_data)
    if amp is None:
        amp = np.amax(y_data) - np.amin(y_data)
    if fwhm is None:
        fwhm = 0.2*np.abs((x_data[-1] - x_data[0]))
    popt, pcov = curve_fit(lorentzian, x_data, y_data, [x0,y0,amp,fwhm])
    return popt, pcov

def fit_lorentzian_triplet():
    pass

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = np.linspace(-2,2,500)
    vals = (0,1,1,.1,-1,.5,.02,1.1,.5,.05)
    y1 = lorentzian_triplet(x,*vals)
    popt, pcov = fit_lorentzian(x,y1,y0=1)
    print(popt)
    plt.plot(x,y1)
    plt.plot(x,lorentzian(x,*popt),linewidth=2)
    plt.show()
