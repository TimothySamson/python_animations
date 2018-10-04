import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, 50), ylim=(0, 50))
# ax.grid()

class Bezier:
    def __init__(self, points):
        self.points = points
        self.time = 0
        self.plot, = ax.plot([], [], "-o", color=tuple(np.random.rand(1, 3)[0]), lw=1)
        self.plot.set_data(points[:, 0], points[:, 1])

        if len(points) > 1:
            self.sub_bezier = Bezier(self.get_coord())

        if len(points) == 1:
            self.data = ([], [])
            self.track, = ax.plot([], [], "g", lw=2)

    # Based on the current time, where should the points of the n-1
    # bezier be?
    def get_coord(self):
        coords = []
        points = self.points
        time = self.time
        for p1, p2 in zip(points, points[1:]):
            coords.append(p1 + time*(p2 - p1))

        return np.array(coords)

    # update subbeziers time and points
    def update(self, time):
        self.time = time
        self.sub_bezier.points = self.get_coord()

        if len(self.points) > 2:
            self.sub_bezier.update(time)

    # Set the data to the plots and get plot objects
    def get_plot(self):
        points = self.points
        self.plot.set_data(points[:, 0], points[:, 1])

        if len(self.points) == 1:
            # print self.points
            self.data[0].append(self.points[0][0])
            self.data[1].append(self.points[0][1])
            self.track.set_data(*self.data)
            return [self.plot, self.track]

        return [self.plot] + self.sub_bezier.get_plot()

    def get_points(self):
        return self.points


# bez = Bezier(np.array([(0, 0), (-10, 10), (13, 4), (2, 23)]))
bez = Bezier(50 * np.random.rand(4, 2))

def init():
    return bez.get_plot()

def animate(i):
    bez.update(abs(np.sin(np.radians(i))))
    return bez.get_plot()

anim = animation.FuncAnimation(fig, animate,
                               init_func=init, 
                               frames=720, 
                               interval=30,
                               blit=True)


plt.show()
