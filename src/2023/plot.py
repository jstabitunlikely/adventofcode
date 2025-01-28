import matplotlib.pyplot as plt
import numpy as np


def fun(x, y):
    return x**2 + y

x = y = np.linspace(0,100)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

X, Y = np.meshgrid(x, y)
zs = np.array(fun(np.ravel(X), np.ravel(Y)))
Z = zs.reshape(X.shape)
p = ax.plot_surface(X, Y, Z)
plt.show()
