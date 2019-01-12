import numpy as np
import matplotlib.pyplot as plt

kx = np.linspace(0, 1, 101)
k1 = np.squeeze(np.dstack((kx, kx)))

kx = np.ones(101)
ky = np.linspace(1, 0, 101)
k2 = np.squeeze(np.dstack((kx, ky)))

kx = np.linspace(1, 0, 101)
ky = np.zeros(101)
k3 = np.squeeze(np.dstack((kx, ky)))

k = np.concatenate((k1, k2, k3))

G = []
for i in range(-2, 5, 2):
    for j in range(-2, 5, 2):
        G.append([i, j])
G = np.array(G)

dmodk = np.zeros((len(G), len(k)))
energy = np.zeros((len(G), len(k)))
oldk = np.zeros(2)
cummodk = 0

for j in range(0, len(G)):
    for i in range(0, len(k)):
        energy[j][i] = (np.linalg.norm(k[i] - G[j]) ** 2 / 2) + j/50
        cummodk += np.linalg.norm(k[i] - oldk)
        dmodk[j][i] = cummodk
        oldk = k[i]
    plt.plot(dmodk[j], energy[j], color='black')
    cummodk = 0
    oldk = 0

plt.axvline(x=1.4142)
plt.axvline(x=2.4142)

plt.ylim((0, 10))
plt.xlim((0, 3.4142))

plt.xlabel("k")
plt.ylabel("Energy")
plt.show()
