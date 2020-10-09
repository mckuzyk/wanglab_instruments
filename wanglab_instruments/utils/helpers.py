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

def optical_doublet(d,k0,kex,gamma):
    '''
    optical_dobulet(d, d0, k0, kex, gamma)

    Optical transmission lineshape when CW and CCW modes couple.
    gamma is the frequency splitting of the two modes.
    '''
    k = k0 + kex
    den = 0.5*k - 1.j*d + 0.25*gamma**2/(0.5*k - 1.j*d)
    return np.abs(1 - kex/den)**2

def optical_doublet_fit(d,d0,off,amp,k0,kex,gamma):
    return off + amp*optical_doublet(d-d0,k0,kex,gamma)

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

def K():
    '''
    K()

    Transduction coefficient that realates power spectral density for direct
    detection through a cavity to the spectral density of the phase noise
    generating the signal.

    In other words, S_{PP}(\omega) = K(\omega) \cdot S_{\phi\phi}(\omega).
    '''
    pass

###################### Fitting ###############################

def fit_lorentzian(x_data, y_data, x0=None, y0=None, amp=None, fwhm=None,
        bounds=(-np.inf, np.inf)):
    if x0 is None:
        x0 = x_data[np.argmax(y_data)]
    if y0 is None:
        y0 = np.amin(y_data)
    if amp is None:
        amp = np.amax(y_data) - np.amin(y_data)
    if fwhm is None:
        fwhm = 0.2*np.abs((x_data[-1] - x_data[0]))
    popt, pcov = curve_fit(lorentzian, x_data, y_data, p0=[x0,y0,amp,fwhm],
        bounds=bounds)
    return popt, pcov

def print_lorentzian_fit(popt, units=('','','','')):
    fit_params = ('x0', 'y0', 'amplitude', 'fwhm')
    s = ''
    for i in range(len(popt)):
        s += '{}: {} {}\n'.format(fit_params[i], popt[i], units[i])
    print(s)
    return s

def fit_lorentzian_triplet(x_data, y_data, x0=None, y0=None, amp=None,
    fwhm=None, xl=None, ampl=None, fwhml=None,
    xr=None, ampr=None,fwhmr=None, inverted=False):
    # If all paramaters are None, assume a large center peak with small,
    # resolved sidebands
    if not any([x0,y0,amp,fwhm,xl,ampl,fwhml,xr,ampr,fwhmr]) and not inverted:
        x0 = x_data[y_data==np.max(y_data)][0]
        y0 = np.min(y_data)
        amp = np.max(y_data) - np.min(y_data)
        half_max = y_data > y0 + 0.5*amp
        fwhm = x_data[half_max][-1] - x_data[half_max][0]
        left_filt = x_data < x0 - 3.0*fwhm
        right_filt = x_data > x0 + 3.0*fwhm
        x_datal = x_data[left_filt]
        x_datar = x_data[right_filt]
        y_datal = y_data[left_filt]
        y_datar = y_data[right_filt]
        xl = x_datal[y_datal==np.max(y_datal)][0]
        xr = x_datar[y_datar==np.max(y_datar)][0]
        ampl = np.max(y_datal) - np.min(y_datal)
        ampr = np.max(y_datar) - np.min(y_datar)
        popt, pcov = curve_fit(lorentzian_triplet,x_data,y_data,
            [x0,y0,amp,fwhm,xl,ampl,fwhm,xr,ampr,fwhm])
        return popt, pcov

    elif not any([x0,y0,amp,fwhm,xl,ampl,fwhml,xr,ampr,fwhmr]) and inverted:
        x0 = x_data[y_data==np.min(y_data)][0]
        y0 = np.max(y_data)
        amp = np.max(y_data) - np.min(y_data)
        half_max = y_data < y0 - 0.5*amp
        fwhm = x_data[half_max][-1] - x_data[half_max][0]
        left_filt = x_data < x0 - 2*fwhm
        right_filt = x_data > x0 + 2*fwhm
        x_datal = x_data[left_filt]
        x_datar = x_data[right_filt]
        y_datal = y_data[left_filt]
        y_datar = y_data[right_filt]
        xl = x_datal[y_datal==np.min(y_datal)][0]
        xr = x_datar[y_datar==np.min(y_datar)][0]
        ampl = np.max(y_datal) - np.min(y_datal)
        ampr = np.max(y_datar) - np.min(y_datar)
        popt, pcov = curve_fit(lorentzian_triplet,x_data,y_data,
            [x0,y0,amp,fwhm,xl,ampl,fwhm,xr,ampr,fwhm])
        return popt, pcov

    else:
        if x0 is None:
            x0 = x_data[np.argmax(y_data)]
        if y0 is None:
            y0 = np.amin(y_data)
        if amp is None:
            amp = np.amax(y_data) - np.amin(y_data)
        if fwhm is None:
            fwhm = 0.05*np.abs((x_data[-1] - x_data[0]))
        if xl is None:
            xl = x0 - 0.25*np.abs(x_data[-1] - x_data[0])
        if ampl is None:
            ampl = .1*amp
        if fwhml is None:
            fwhml = fwhm
        if xr is None:
            xr = x0 - 0.25*np.abs(x_data[-1] - x_data[0])
        if ampr is None:
            ampr = .1*amp
        if fwhmr is None:
            fwhmr = fwhm
        popt, pcov = curve_fit(lorentzian_triplet,x_data,y_data,
            [x0,y0,amp,fwhm,xl,ampl,fwhml,xr,ampr,fwhmr])
        return popt, pcov

###################Optical Mode Analysis##########################

def calibrate_x(x,y,eom_frequency,invert=False):
    if invert:
        y = -y
    popt, pcov = fit_lorentzian_triplet(x,y)
    x0,xl,xr = popt[0],popt[4],popt[-3]
    xcal = (x - x0)/(xr - xl)*2*eom_frequency
    return xcal

def normalize_transmission_dip(x,y,baseline):
    popt, pcov = fit_lorentzian(x,-y)
    ymax = -1*popt[1]
    ymin = np.average(baseline)
    ynorm = -1*(y - ymax)/(ymax - ymin)
    return ynorm

def get_linewidth(x,y,eom_frequency,invert=True):
    xcal = calibrate_x(x,y,eom_frequency,invert)
    popt, pcov = fit_lorentzian(xcal,y,x0=0) # Central peak at x=0 
    return popt[-1]

    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = np.linspace(-2,2,500)
    vals = (0,1,1,.1,-.5,.1,.02,.5,.1,.05)
    y1 = lorentzian_triplet(x,*vals)
    popt, pcov = fit_lorentzian_triplet(x,y1)
    print(popt)
    plt.figure()
    plt.plot(x,y1)
    plt.plot(x,lorentzian_triplet(x,*popt),linewidth=1)
    plt.figure()
    plt.plot(x,optical_doublet(x,.1,.05,.2))
    y2 = lorentzian(x, vals[0], vals[1], vals[2], vals[3])
    popt2, pcov2 = fit_lorentzian(x, y2)
    print_lorentzian_fit(popt2, ('MHz', 'V', 'V', 'MHz'))
    plt.figure()
    plt.plot(x,y2)
    plt.plot(x,lorentzian(x, *popt2))

    plt.show()
    
