import matplotlib.pyplot as plt
import numpy as np

def E(q, r0, x, y):
    den = np.hypot(x-r0[0], y-r0[1])**3
    return q * (x - r0[0]) / den, q * (y - r0[1]) / den

nx, ny = 128, 128
x= np.linspace(-1, 5, nx)
y= np.linspace(-3, 3, ny)
X,Y = np.meshgrid(x,y)
q1 = (-4, (0,0))
q2 = (1, (2, 0))
charges = [q1, q2]
Ex, Ey = np.zeros((ny,nx)), np.zeros((ny,nx))

for charge in charges:
    ex, ey = E(*charge, x=X, y=Y)
    Ex += ex
    Ey += ey

color = 2*np.log(np.hypot(Ex,Ey))

fig = plt.figure(figsize = (8,8))
plt.grid(True)
plt.pcolormesh(x,y,color,cmap=plt.cm.inferno, alpha=0.5)
plt.streamplot(x,y,Ex,Ey,density=[1.2,2], arrowstyle='->', color=color, linewidth=1.5, arrowsize=1.5) #cmap=plt.cm.inferno, 
plt.show()
