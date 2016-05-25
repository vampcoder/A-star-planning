import matplotlib.pyplot as plt
import scipy as sp
from scipy.interpolate import interp1d
import numpy as np
x = []
y = []

with open('a.txt', 'r') as fp:
    for line in fp:
        a, b = line.split()
        x.append(int(a))
        y.append(int(b))

print x
print y
points = zip(x, y)

points = sorted(points, key=lambda point:points[0])

x, y = zip(*points)

print x
print y

length = 100
new_x = np.linspace(min(x), max(x), length)
new_y = interp1d(x, y, kind='cubic')(new_x)
print new_x
print new_y

plt.plot(x, y, 'o', new_x, new_y, '-')
plt.show()