import numpy as np
from collections import deque
from scipy.integrate import odeint
from matplotlib import pyplot as plt
from matplotlib import animation

M1=1
L1=1
M2=1
L2=2
G=9.8
ORIGIN=np.array([0,0])
dt = 1/30

class DoublePendulum:
    def __init__(self, init_state):# theta1, omega1, theta2, omega2
        self.state = init_state*np.pi / 180
    
    def position(self):
        theta1 = self.state[0]
        theta2 = self.state[2]

        return np.cumsum([
                [ORIGIN[0], L1*np.sin(theta1), L2*np.sin(theta2)],
                [ORIGIN[1],  -L1*np.cos(theta1),  -L2*np.cos(theta2)]],
                axis=1)
        

    # Returns [omega1, alpha1, omega2, alpha2]
    def dstate(self, state, t):
        deriv = np.zeros(4)
            
        theta1 = state[0]
        omega1 = state[1]
        theta2 = state[2]
        omega2 = state[3]

        deriv[0] = omega1
        deriv[2] = omega2

        dtheta = theta1 - theta2

        left = np.array([
            [(M1 + M2)*L1, M2*L2*np.cos(dtheta)],
            [M2*L1*np.cos(dtheta), M2*L2]
            ])

        right = np.array([
                (-M2*L2*(omega2**2)*np.sin(dtheta) -
                G*(M1 + M2)*np.sin(theta1)),
                (M2*L1*(omega1**2)*np.sin(dtheta) -
                    M2*G*np.sin(theta2))
            ])
        
        temp = np.linalg.solve(left, right)


        deriv[1] = temp[0]
        deriv[3] = temp[1]

        return deriv

    def step(self):
        self.state = odeint(self.dstate, 
                self.state, [0, dt])[1]


########
# TEST #
########

pend = DoublePendulum(np.array([45, 0, -180, 0]))
print(pend.state)
print(pend.position())
print(pend.dstate(pend.state, 0))



fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-5, 5), ylim=(-5, 4))
ax.grid()

lines, = ax.plot([], [], 'bo-')
track1, = ax.plot([], [], 'r')
track2, = ax.plot([], [], 'g')

length = 100
data1 = []
data1.append(deque([], maxlen=length))
data1.append(deque([], maxlen=length))
data2 = []
data2.append(deque([], maxlen=length))
data2.append(deque([], maxlen=length))

def init():
    return lines,track1,track2,

def animate(i):
    x, y = pend.position()
    
    data1[0].append(x[1])
    data1[1].append(y[1])
    data2[0].append(x[2])
    data2[1].append(y[2])

    track1.set_data(data1)
    track2.set_data(data2)


    lines.set_data(x, y)
    pend.step()

    return lines,track1,track2


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
