import numpy as np
from numpy import cos
from numpy import sin
import matplotlib.pyplot as plt
from matplotlib import animation

fig = plt.figure()

ax_lim = (-10, 10)

##########
# DOMAIN #
##########

        ###########################
        # CREATE YOUR DOMAIN HERE #
        ###########################

# zs = [2+2*complex(cos(x), sin(x)) for x in np.linspace(0, 2*np.pi, 100)]
zs = ([complex(2*x, 3) for x in np.linspace(-7, 7, 1000)])

        ###########################
        # END END END END END END #
        ###########################

axDom = fig.add_subplot(121, aspect='equal', autoscale_on=True,
                     xlim=ax_lim, ylim=ax_lim)

domain, = axDom.plot([], [])

def plotComplex(plot, nums):
    xs = nums.real
    ys = nums.imag
    plot.set_data(xs, ys)

zs = np.array(zs)
plotComplex(domain, zs)

#########
# RANGE #
#########

        ###########################
        # TRANSFORMATION ######
        ###########################

def transformation(nums):
    return 2**nums - 2**(-nums)

        ###########################
        # END END END END END END #
        ###########################

axRange = fig.add_subplot(122, aspect='equal', autoscale_on=True,
                     xlim=ax_lim, ylim=ax_lim)

output, = axRange.plot([], [])

fzs = transformation(zs)
plotComplex(output, fzs)

        #############
        # ANIMATION #
        #############



def init():
    return domain, output,

def animate(i):
    out = zs - complex(0, i * 10 / 360)
    plotComplex(domain, out)

    out = transformation(out)
    plotComplex(output, out)
    

    return domain, output,

anim = animation.FuncAnimation(fig, animate, frames=500, 
        interval=10, blit=False, init_func=init)

plt.show()

