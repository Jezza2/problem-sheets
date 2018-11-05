import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

A = np.array([24.99735,
			  55.18696,
			 -33.69137,
			  7.948387,
			 -0.136638])
A = A / 0.044

R = 189.0

def shomate(t):
	return A[0]+A[1]*t+A[2]*t**2+A[3]*t**3+A[4]/(t**2)

hcap = np.vectorize(shomate)

data = np.loadtxt('PV_large_probe.txt', 
					skiprows=30, usecols=[2, 3])
data = np.transpose(data)
temperature, pressure = data[1], data[0]

T_0 = temperature[0]
p_0 = pressure[0]

T_dry_const = T_0 * (pressure/p_0)**(0.1718)

p = np.logspace(np.log10(pressure[-1]), np.log10(pressure[0]), 1000)
T = np.empty_like(p)
T[-1] = T_0
for i in range(T.shape[0]-2, -1, -1):
	dT = (R * T[i+1] / shomate(T[i+1]/1000)) * (np.log(p[i])-np.log(p[i+1]))
	T[i] = T[i+1] + dT

plt.plot(temperature, pressure, label='Pioneer Venus Large probe, 1978')
plt.plot(T_dry_const, pressure, label='dry adiabat, constant $c_p$')
plt.plot(T, p, label='dry adiabat, variable $c_p$')
plt.gca().invert_yaxis()
plt.yscale('log')
plt.xlabel('$T$/K')
plt.ylabel('$p$/Pa')
plt.title('\\textbf{Two models for the temperature profile on Venus}')
plt.legend()

plt.show()
