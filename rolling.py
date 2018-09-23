import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-10, 10), ylim=(-10, 10))
# ax.grid()

angular_vel = 0.5
dtheta = angular_vel / 30.0
RAD_1 = 4.0
RAD_2 = 2.0
CENTER = (0, 0)
circ2 = 2 * np.pi * RAD_2

class Circles:
    def __init__(self):
        self.theta1 = 0
        self.theta2 = 0
        self.center = CENTER

    def update(self):
        theta1 = self.theta1
        new_theta1 = theta1 + dtheta
        self.theta1 = new_theta1

        arc1 = RAD_1 * theta1
        theta2 = (arc1 / circ2) * 2 * np.pi + theta1
        self.theta2 = theta2

    def circle2_center(self):
        theta1 = self.theta1
        #center of circle1
        x0, y0 = CENTER

        x = x0 + (RAD_1 + RAD_2)*np.cos(theta1)
        y = y0 + (RAD_1 + RAD_2)*np.sin(theta1)

        return (x, y)

    def track(self):
        # center of circle2
        x0, y0 = self.circle2_center()
        theta2 = self.theta2

        x = x0 - RAD_2 * np.cos(theta2)
        y = y0 - RAD_2 * np.sin(theta2)

        return (x, y)

circle_obj = Circles()

x0, y0 = CENTER
circle1 = plt.Circle(CENTER, RAD_1, fc='y')
circle2 = plt.Circle((x0 + RAD_1 + RAD_2, y0), RAD_2, fc='b')
mark = plt.Circle((0, 0), 0.2, fc='g')
track, = ax.plot([], [], 'g')
trackx, tracky = [], []

def init():
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(mark)
    return circle1, circle2,track,mark,

def animate(i):
    global circle_obj
    circle_obj.update()
    circle2.center = circle_obj.circle2_center()

    x, y = circle_obj.track()
    trackx.append(x)
    tracky.append(y)
    track.set_data(trackx, tracky)
    mark.center = (x, y)

    return circle1, circle2,mark,track,


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
