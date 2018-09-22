import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-2, 2), ylim=(-2, 1))
ax.grid()

dt = 1.0 / 30
g = 2.5
L = 1.0
ang_disp = np.pi/6

class Pendulum:
    def __init__(self):
        global ang_disp
        self.ang_disp = ang_disp
        self.ang_vel = 0

    def update_approx(self):
        global dt
        ang_accel = -(g / L)*(self.ang_disp)

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
        x = np.cos(self.ang_vel - np.pi / 2) * L
        y = np.sin(self.ang_vel - np.pi / 2) * L

        return ([0, x], [0, y])


pend = Pendulum()
pend_approx = Pendulum()

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
