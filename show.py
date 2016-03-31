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
ax0 = fig.add_subplot(10, 1, 1, xlim=(0, 50000), ylim=(0, 2500))
ax1 = fig.add_subplot(10, 1, 2, xlim=(0, 50000), ylim=(0, 2500))
ax2 = fig.add_subplot(10, 1, 3, xlim=(0, 50000), ylim=(0, 2500))
ax3 = fig.add_subplot(10, 1, 4, xlim=(0, 50000), ylim=(0, 2500))
ax4 = fig.add_subplot(10, 1, 5, xlim=(0, 50000), ylim=(0, 2500))
ax5 = fig.add_subplot(10, 1, 6, xlim=(0, 50000), ylim=(0, 2500))
ax6 = fig.add_subplot(10, 1, 7, xlim=(0, 50000), ylim=(0, 2500))
ax7 = fig.add_subplot(10, 1, 8, xlim=(0, 50000), ylim=(0, 2500))
ax8 = fig.add_subplot(10, 1, 9, xlim=(0, 50000), ylim=(0, 2500))
ax9 = fig.add_subplot(10, 1, 10, xlim=(0, 50000), ylim=(0, 2500))

freq0, = ax0.plot([], [], lw=1)
freq1, = ax1.plot([], [], lw=1)
freq2, = ax2.plot([], [], lw=1)
freq3, = ax3.plot([], [], lw=1)
freq4, = ax4.plot([], [], lw=1)
freq5, = ax5.plot([], [], lw=1)
freq6, = ax6.plot([], [], lw=1)
freq7, = ax7.plot([], [], lw=1)
freq8, = ax8.plot([], [], lw=1)
freq9, = ax9.plot([], [], lw=1)

def init():
    freq0.set_data([], [])
    freq1.set_data([], [])
    freq2.set_data([], [])
    freq3.set_data([], [])
    freq4.set_data([], [])
    freq5.set_data([], [])
    freq6.set_data([], [])
    freq7.set_data([], [])
    freq8.set_data([], [])
    freq9.set_data([], [])

    return freq0, freq1, freq3, freq4, freq5, freq6, freq7, freq8, freq9

def animate(cpu):
    freq0.set_data(make_point(0))
    freq1.set_data(make_point(1))
    freq2.set_data(make_point(2))
    freq3.set_data(make_point(3))
    freq4.set_data(make_point(4))
    freq5.set_data(make_point(5))
    freq6.set_data(make_point(6))
    freq7.set_data(make_point(7))
    freq8.set_data(make_point(8))
    freq9.set_data(make_point(9))

    return freq0, freq1, freq3, freq4, freq5, freq6, freq7, freq8, freq9

def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=30, interval=10)
    plt.show()


if __name__ == "__main__":
    load_show()