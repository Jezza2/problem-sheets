import numpy as np
print("numpy imported")
import matplotlib.pyplot as plt
print("pyplot imported")

DATA_FILE = "methane_lines"
centre, strength, width = np.loadtxt(DATA_FILE, unpack=True)

num_thin = 0
num_thick = 0

# Volume concentration of methane
ppmv = 10.0

# Mass concentration of methane
q = ppmv * 1e-6 * 16.0 / 29.0

p_s = 1e5
g = 9.8


# Absorption coefficient at centre of line is strength/width.
# Then optical thickness of atmosphere is given by:
tau = (q * p_s / g) * strength/width

for t in tau:
    if t <= 0.1: num_thin += 1
    if t >= 10: num_thick += 1


print(num_thin, num_thick)
