import numpy as np
import itrm

# Constants
K = 2000
J = 6

# x axis
x = np.linspace(0, 1, K)

# y axis data
y = np.cos(2*np.pi*2*x)
Y = np.zeros((J, len(x)))
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

# plots
itrm.config(uni = True)
itrm.plot(x, y, "Single curve", lg="x")
itrm.plot(x, Y, "Multiple curves", rows=0.5)
itrm.config.uni = False
itrm.plot(x, y, "Single curve")
