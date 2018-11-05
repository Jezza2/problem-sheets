import numpy as np
import matplotlib.pyplot as plt


plt.rc('text', usetex=True)
plt.rc('font', family='serif')

T_0 = 90	# K
p_c0 = 1.13e4	# Pa
L = 3.57e5	# J/kg
M_c = 0.016	# kg/mol
M_a = 0.028	# kg/mol
R_a = 296.9	# J kg/K
R_c = 519.7 # J kg/K
c_p = 1040	# J/kg/K

T_s = 90	# K
p_s = 2e5	# Pa


def q(temp, p_a):
	p_c = p_c0 * np.exp((L/R_c)*(1/T_0-1/temp))
	return M_c*p_c / (M_a*p_a + M_c*p_c)
	
def grad(temp, p_a):
	return temp * (R_a/c_p)*(1 + L*q(temp, p_a) / (R_a * temp)) \
			/ (1 + L*L*q(temp, p_a) / (c_p * R_c * temp**2))


p = np.logspace(1, np.log10(p_s), num=1000)
T_dry = T_s*np.power(p / p_s, R_a/c_p)
T_moist = np.empty_like(T_dry)
qq = np.empty_like(T_dry)

T_moist[-1] = T_s
qq[-1] = q(T_s, p_s)
for i in range(p.shape[0]-2, -1, -1):
	dT = grad(T_moist[i+1], p[i+1]) * (np.log(p[i]) - np.log(p[i+1]))
	T_moist[i] = T_moist[i+1] + dT
	qq[i] = q(T_moist[i], p[i])



fig1 = plt.figure(1)
plt.plot(T_dry, p, label='dry adiabat')
plt.yscale('log')
plt.ylabel('p/Pa')
plt.xlabel('T/K')
plt.gca().invert_yaxis()

plt.plot(T_moist, p, label='moist adiabat')
plt.legend()
plt.title("\\textbf{Dry and moist adiabats for Titan's atmosphere}")

fig2 = plt.figure(2)
plt.plot(qq, p)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('p/Pa')
plt.xlabel('q')
plt.gca().invert_yaxis()
plt.title("\\textbf{Specific humidity, q, on Titan}")

plt.show()
