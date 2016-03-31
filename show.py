import time
import matplotlib.pyplot as plt
from matplotlib import animation

global cpuNum
global count
global cpufreq
global linefreq
global timeline
global firsttime
global lasttime
firstts = 0
global lastts

def setupShow(num):
    global cpuNum
    global count
    global firsttime
    global count
    global cpufreq
    global timeline
    global fig
    global linefreq

    cpuNum = num
    firsttime = time.time() * 1000
    count = [0 for x in range(10)]
    linefreq = []
    firstts = 0
    cpufreq = [[] for i in range(num)]
    timeline = [[] for i in range(num)]

def update(cpu, ts, value):
    global firstts
    global firsttime
    global count
    global cfreq
    global timeline

    if firstts == 0:
        firstts = ts
        firsttime = time.time() * 1000
    cpufreq[cpu].append(value)
    timeline[cpu].append(ts)
    # self.lasttime = time.time() * 1000 # ms
    count[cpu] += 1

def startShow():
    setupShow(10)
    load_show()

def cut_show_point(start_t, end_t, pointx, pointy):
    tmpx = []
    tmpy = []
    xlen =len(pointx)
    if xlen >2 and pointx[xlen - 1] < 50 * 1000:
        return pointx, pointy
    elif xlen > 0 :
        for i in range(len(pointx)):
            if pointx[i] > start_t and pointx[i] < end_t:
                tmpx.append(pointx[i])
                tmpy.append(pointy[i])

        return tmpx, tmpy

def make_point(cpu):
    pointx = []
    pointy = []
    global lasttime
    global lastts
    global firstts
    global count
    global cpufreq
    global timeline
    global firsttime

    lasttime = time.time() * 1000  # ms
    lastts = lasttime - firsttime + firstts

    for i in range(count[cpu]):
        if count[cpu] > 0:
            if i == 0:
                pointx.append(timeline[cpu][0])
                pointy.append(0)

                pointx.append(timeline[cpu][0])
                pointy.append(cpufreq[cpu][0])
            elif i == count[cpu] - 1:
                pointx.append(timeline[cpu][i])
                pointy.append(cpufreq[cpu][i])

                pointx.append(lastts)
                pointy.append(cpufreq[cpu][i])
            else:
                pointx.append(timeline[cpu][i])
                pointy.append(cpufreq[cpu][i-1])

                pointx.append(timeline[cpu][i])
                pointy.append(cpufreq[cpu][i])

    return pointx, pointy

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1, xlim=(0, 50000), ylim=(0, 2500))
ax2 = fig.add_subplot(2, 1, 2, xlim=(0, 50000), ylim=(0, 2500))

load_sum_l, = ax1.plot([], [], lw=1)
load_sum_b, = ax2.plot([], [], lw=1)


def init():
    load_sum_l.set_data([], [])
    load_sum_b.set_data([], [])

    return load_sum_l, load_sum_b

def animate(cpu):
    load_sum_l.set_data([0, 3000, 3000, 15000], [500,500,800,800])
    load_sum_b.set_data([0, 3000, 3000, 15000], [500,500,800,800])
    return load_sum_l, load_sum_b

def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=30, interval=10)
    plt.show()


if __name__ == "__main__":
    load_show()