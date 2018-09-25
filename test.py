import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-25, 25), ylim=(-25, 25))

plot, = ax.plot(0,0  , 'bo')

def init():
    return plot,

def animate(i):
    x = 12.5*np.cos(np.radians(i))
    y = 12.5*np.sin(np.radians(i))
    plot.set_data(x, y)

    return plot,



anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
