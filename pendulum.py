import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-5, 5), ylim=(-5, 4))
ax.grid()

dt = 1.0 / 30
g = 7.0
L = 2.5
ang_disp = np.pi/16

class Pendulum:
    def __init__(self, center):
        global ang_disp
        self.center = center
        self.ang_disp = ang_disp
        self.ang_vel = 0

    def update_approx(self):
        global dt
        ang_accel = -(g / L)* (self.ang_disp)

        self.ang_vel = self.ang_vel + dt * ang_accel
        self.ang_disp = self.ang_disp + dt * self.ang_vel

    def update(self):
        global dt
        ang_accel = -(g / L) * np.sin(self.ang_disp)

        self.ang_vel = self.ang_vel + dt * ang_accel
        self.ang_disp = self.ang_disp + dt * self.ang_vel

    def show(self):
        print self.ang_disp, self.ang_vel

    def pos(self):
        x0, y0 = self.center
        x = np.cumsum([x0, np.cos(self.ang_vel - np.pi / 2) * L])
        y = np.cumsum([y0, np.sin(self.ang_vel - np.pi / 2) * L])
        
        return (x, y)


pend = Pendulum((0, 0))
pend_approx = Pendulum((0, 0))

pendulum, = ax.plot([], [], 'go-')
pendulum_approx, = ax.plot([], [], 'ro-')

def init():
    return pendulum,pendulum_approx,

def animate(i):
    x, y = pend.pos()
    x_approx, y_approx = pend_approx.pos()

    pend.update()
    pend_approx.update_approx()

    pendulum.set_data(x, y)
    pendulum_approx.set_data(x_approx, y_approx)
    return pendulum,pendulum_approx,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
