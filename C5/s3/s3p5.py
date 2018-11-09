import numpy as np
print("numpy imported")
import matplotlib.pyplot as plt
print("pyplot imported")

# Optical depth is defined as increasing upwards
# tau = 0 at ground, tau = tau_cloud at level of cloud.
tau_cloud = 1.0
T_cloud = 255.0   # Blackbody temperature of Earth = temp of cloud
# Ground temperature is a function of tau_cloud and T_cloud
T_ground = ((tau_cloud + 4.0) / 2.0)**0.25 * T_cloud

num_points = 500
tau = np.linspace(0.0, tau_cloud, num_points)

T = np.zeros(num_points)
T[0] = T_ground
T[-1] = T_cloud

T[1:-1] = (0.5 * (tau_cloud - tau[1:-1] + 3.0))**0.25 * T_cloud

print("Plotting...")
plt.plot(T, tau)
plt.show()
