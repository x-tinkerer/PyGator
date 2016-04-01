import time
import matplotlib.pyplot as plt
from matplotlib import animation

def setupShow(num):
    global cpuNum
    global cpuinfo
    global lastts
    global lastfreq

    cpuNum = num
    cpuinfo = [{} for x in range(10)]
    lastts = [0 for x in range(10)]
    lastfreq = [0 for x in range(10)]


def update(cpu, ts, value):
    tdict = {value:0}
    if cpuinfo.has_key(value):
        old_ts=cpuinfo.get(value)
        delta_time = ts - lastts[cpu]
        cpuinfo[value] = old_ts + delta_time

    else:
        cpuinfo.append(tdict)

    lastts[cpu] =ts
    lastfreq[cpu]= value

def startShow():
    setupShow(10)
    load_show()


fig = plt.figure()
ax0 = fig.add_subplot(10, 1, 1, xlim=(0, 20000), ylim=(0, 2100))


def init():


def animate(cpu):
    global firstts
    global lastts


def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=30, interval=10)
    plt.show()


if __name__ == "__main__":
    load_show()