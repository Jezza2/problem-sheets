import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

T_0 = 90	# K
p_c0 = 1.13e4	# Pa
L = 3.57e5	# J/kg
M_c = 0.016	# kg/mol
M_a = 0.028	# kg/mol
p_a = 1e5	# Pa
R_a = 296.9	# J kg/K
R_c = 519.7 # J kg/K
c_p = 1039	# J/kg/K

T = np.linspace(80, 100, 20)
dry = np.full_like(T, R_a/c_p)

p_c = p_c0 * np.exp((L/R_c)*(1/T_0-1/T))
q = M_c*p_c / (M_a*p_a + M_c*p_c)

grad = (R_a/c_p)*(1 + L*q / (R_a * T))/(1 + L*L*q / (c_p * R_c * T**2))

plt.figure(1)

line_dry, = plt.plot(T, dry, label='dry adiabat')
line_grad, = plt.plot(T, grad, label='dilute moist adiabat')
plt.legend()
plt.xlabel('$T/K$')
plt.ylabel('$\mathrm{d}\ln T/\mathrm{d}\ln p$')
plt.title("\\textbf{Dry and dilute moist adiabats for methane in Titan's atmosphere}")
plt.show()
