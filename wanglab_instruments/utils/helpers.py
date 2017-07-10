import numpy as np
import datetime

def timestamp():
    return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')

def unlog(y):
    return 10**(y/10)

def log(y):
    return 10*np.log10(y)

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

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    x = np.linspace(-2,2,100)
    vals = (1,1,.5,2)
    y1 = lorentzian(x,*vals)
    popt,pcov = curve_fit(lorentzian,x,y1)
    print(popt)
    plt.plot(x,y1,'.')
    plt.plot(x,2-y1)
    plt.plot(x,lorentzian(x,*popt),linewidth=2,alpha=0.8)
    plt.plot(x,line(x))
    plt.plot(x,exp_decay(x))
    plt.show()
