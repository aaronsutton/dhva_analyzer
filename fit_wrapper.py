# fit wrapper using least squares optimization routine, modified from 
# the scipy cookbook
#    Example usage:
#    pars = [fw.Parameter(1), fw.Parameter(1)]
#    data.y= data.y[data.x < 1]
#    data.x= data.x[data.x < 1]
#    f = lambda  x, pars: (pars[0]()/np.sqrt(x))*np.exp(-pars[1]()/x)
#    fw.fit(f, pars, [v.mean for v in data.y], data.x)
#    prefactor = pars[0].get()
#    gap = pars[1].get()

import numpy as np
from scipy import optimize

class Parameter:
    def __init__(self,value):
        self.value = value

    def set(self,value):
        self.value = value

    def get(self):
        return self.value
    
    def __call__(self):
        return self.value

def fit(function,parameters, y, x = None, err = 1., fit_range = None):
    
    def err_func(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return (y - function(x,parameters))/err
    
    if not fit_range == None :
        low_idx = np.nonzero(x >= fit_range[0])[0][0]
        high_idx = np.nonzero(x <= fit_range[1])[0][-1]
        y = y[low_idx:high_idx]

    if x == None : x = np.arange(y.shape[0])

    p = [param() for param in parameters]

    out = optimize.leastsq(err_func,p,full_output = 1)
        
    return out
