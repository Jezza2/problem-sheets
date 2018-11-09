# This script takes the absorption spectrum data for methane
# and computes the absorption spectrum by assuming each line
# has a Lorentzian shape.

# It then calculates the band averaged transmission function
# over the range of wavefunctions.


import numpy as np
print("numpy imported")
import matplotlib.pyplot as plt
print("pyplot imported")
import scipy.integrate as inte
print("integrate imported")
from multiprocessing import Pool
from multiprocessing import cpu_count
print("pool imported")

# --------- GLOBALS --------------

# Surface pressure
p_s = 1.0e5         # kg/m^2
# Surface gravity
g = 9.8             # m/s^2

# A function to return a lorentzian curve given
# the strength, width and centre of a line.
def lorentzian(S, d, nu_0, nu):
    x = (nu - nu_0)/d
    pre = S / (d * np.pi)
    return pre / (1.0 + x**2)
vlorentzian = np.vectorize(lorentzian)

# Helper function for parallelising the calculation of the
# absorption spectrum. Reducing parameter space to one dimension
# makes life much easier.
def calc_line_spectrum(i):
    return vlorentzian(strength[i], width[i], centre[i], wavenumber)

# Mass concentration of methane from parts per million
def q(ppmv):
    return ppmv * 1.0e-6 * 16.0 / 29.0

# Integrate exp(-tau) over wavenumber to get transmission function
def integrate_tau(ppm):
    tau = (q(ppm) * p_s / g) * abs_spectrum
    return inte.trapz(np.exp(-tau), wavenumber)


# ----------- MAIN -----------------------

# Read data in
DATA_FILE = "methane_lines"
centre, strength, width = np.loadtxt(DATA_FILE, unpack=True)

# Calculate line spectra over range of wavenumbers in file
wavenumber = np.linspace(np.min(centre), np.max(centre), 10000)
# Each line's spectrum is evaluated at each of the wavenumbers in the range.
line_spectrum = np.zeros((len(centre), len(wavenumber)))
# The overall spectrum is the sum of all the lines' spectra
abs_spectrum = np.zeros_like(wavenumber)

print("Calculating absorption spectrum...")

# Find absorption lineshapes in parallel - much faster on cluster.
p = Pool(cpu_count())
line_spectrum = p.map(calc_line_spectrum, range(0, len(centre)))
# Sum line spectra to get a total absorption spectrum
abs_spectrum = np.sum(line_spectrum, 0)

print("Calculating transmission functions...")

# Now use this absorption spectrum to calculate band averaged
# transmission functions

# Range of ppmv values to cover
ppmv_range = np.linspace(0, 100.0, 100)
# The transmission function for methane
transmission = np.zeros_like(ppmv_range)

p = Pool(cpu_count())
transmission = p.map(integrate_tau, ppmv_range)

print("Plotting...")
plt.plot(ppmv_range, transmission)
plt.show()
