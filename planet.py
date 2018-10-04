import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

EARTH_CENTER = (15.0, 0)
G = 30.0
SUN_MASS = 140.0
SUN_CENTER = (0, 0)
dt = 1.0 / 120
INITIAL_VEL = 30

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-25, 25), ylim=(-25, 25))
ax.grid()

sun = plt.Circle(SUN_CENTER, 3, fc='y')
earth = plt.Circle(EARTH_CENTER, 1, fc='b')
track, = ax.plot([], [], 'g' , lw=2)

# Given dt, update pos will update the position.
class Planet:
    def __init__(self):
        global EARTH_CENTER
        self.pos = EARTH_CENTER
        self.vel = (0, INITIAL_VEL)

    def distance(self, x, y):
        return np.sqrt(x**2 + y**2)

    # Returns acceleration given the from self.pos
    def accel(self):
        global SUN_CENTER
        x_earth, y_earth = self.pos
        x_sun, y_sun = SUN_CENTER

        x_rel, y_rel = (x_earth - x_sun, y_earth - y_sun)

        sol_dist = self.distance(x_rel, y_rel)

        accel_x = -G * SUN_MASS * x_rel / (sol_dist**2)
        accel_y = -G * SUN_MASS * y_rel / (sol_dist**2)

        return (accel_x, accel_y)

    def update_pos(self):
        global dt
        x_accel, y_accel = self.accel()

        # update velocity
        x_dv, y_dv = (x_accel*dt, y_accel*dt)
        x_vel_old, y_vel_old = self.vel
        x_vel, y_vel = (x_vel_old + x_dv, y_vel_old + y_dv)
        self.vel = (x_vel, y_vel)

        #update position
        x_dp, y_dp = (x_vel*dt, y_vel*dt)
        x_pos_old, y_pos_old = self.pos
        x_pos, y_pos = (x_pos_old + x_dp, y_pos_old + y_dp)
        self.pos = (x_pos, y_pos)

        return self.pos

earth_planet = Planet()


def init():
    ax.add_patch(sun)
    ax.add_patch(earth)
    return sun,earth,track

xdata, ydata = [], []

def animate(i):
    global earth_planet
    global earth

    x, y = earth_planet.update_pos()
    earth.center = (x, y)

    xdata.append(x)
    ydata.append(y)
    track.set_data(xdata, ydata)

    # ax.plot(x, y, 'go-', markersize = 1)

    return sun,earth,track, 

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
