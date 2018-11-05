import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

T_0 = 428
p_0 = 22.050

def func(x, a):
	return T_0 * (x / p_0)**a


data = np.genfromtxt('GalileoJupiter.txt', delimiter='\t', skip_header=1, 
					usecols=(0,1), unpack=True)

pressure = data[0,390:]
temperature = data[1,390:]

fit, pcov = curve_fit(func, pressure, temperature)

std = np.sqrt(pcov[0,0])
best_fit = func(pressure, fit[0])

plt.plot(best_fit, pressure, label='fit: R/c_p=%5.5f +- %5.5f' % (fit[0], std))
plt.plot(temperature, pressure, linestyle='none', marker='.', 
		label='data', markersize=1)
plt.yscale('log')
plt.gca().invert_yaxis()
plt.xlabel('T/K')
plt.ylabel('p/Pa')
plt.title('Temperature profile of Jupiter')
plt.legend()
plt.show()
