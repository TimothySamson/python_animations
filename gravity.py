import numpy as np
import itertools
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-25, 25), ylim=(-25, 25))

dt = 1.0 / 30
G = 10
lw = 1

class Particle:
    def __init__(self, position, velocity, mass, c="b", rad=1):
        self.position = position
        self.velocity = velocity
        self.acceleration = (0, 0)
        self.mass = mass
        self.circle = plt.Circle((-1000, 1000), rad, fc=c)
        self.track, = ax.plot([], [], c, lw=lw)

        self.record = ([], [])

        ax.add_patch(self.circle)

    def set_position(self, position):
        x, y = position
        self.position = position

        self.record[0].append(x)
        self.record[1].append(y)

        self.track.set_data(self.record)
        self.circle.center = self.position

    # based on current acceleration, change position
    def update(self):
        x_accel, y_accel = self.acceleration
        # update velocity
        x_dv, y_dv = (x_accel*dt, y_accel*dt)
        x_vel_old, y_vel_old = self.velocity
        x_vel, y_vel = (x_vel_old + x_dv, y_vel_old + y_dv)
        self.velocity = (x_vel, y_vel)

        #update position
        x_dp, y_dp = (x_vel*dt, y_vel*dt)
        x_pos_old, y_pos_old = self.position
        x_pos, y_pos = (x_pos_old + x_dp, y_pos_old + y_dp)

        self.set_position((x_pos, y_pos))


class Particle_System:
    def __init__(self, particle_array):
        self.particle_array = particle_array

    def distance(self, part1, part2):
        x1, y1 = part1.position
        x2, y2 = part2.position

        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # returns vector going from part1 to part2
    def rel(self, part1, part2):
        x1, y1 = part1.position
        x2, y2 = part2.position

        return (x2 - x1, y2 - y1)

    # Acceleration of particle 1 due to particle 2
    def accel(self, part1, part2):
        distance = self.distance(part1, part2)

        # vector going from part1 to part2
        xrel, yrel = self.rel(part1, part2)
        temp = G / (distance**3)

        accx1, accy1 = temp * xrel * part2.mass, temp * yrel * part2.mass

        return (accx1, accy1)

    # Update position for every particle
    def update(self):
        # reset acceleration to zero
        for part in self.particle_array:
            part.acceleration = (0, 0)

        # acceleration pairs
        for (part1, part2) in itertools.product(self.particle_array, repeat=2):
            if part1 == part2:
                continue
            accel_x, accel_y = self.accel(part1, part2)
            accel_x0, accel_y0 = part1.acceleration

            part1.acceleration = (accel_x + accel_x0,
                                  accel_y + accel_y0)

        for part in self.particle_array:
            part.update()

    def get_objects(self):
        objs = [part.circle for part in self.particle_array]
        objs.extend([part.track for part in self.particle_array])
        return tuple(objs)



def particle_circle(num, radius, velocity):
    angle = 2*np.pi / num
    particles = []
    colors = ['r', 'g', 'b', 'y'] * 10
    for i in range(0, num):
        theta = angle * i
        x, y = radius * np.cos(theta), radius * np.sin(theta)
        theta = theta + np.pi/2
        xvel, yvel = velocity * np.cos(theta), velocity * np.sin(theta)

        particles.append(Particle((x, y), (xvel, yvel), 100, c=colors[i]))

    return particles


particles = Particle_System(particle_circle(9, 20, 9))

def init():
    return particles.get_objects()

def animate(i):
    particles.update()
    return particles.get_objects()



anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)
plt.show()
