import numpy as np
import matplotlib.pyplot as plt
import time
import threading
from matplotlib import animation

class Display(object):
    mActivy = False
    def update(self):
        pass

    def show(self):
        pass

    def setActivy(self, act):
        self.mActivy = act


cpuNum = 0
count = None
cpufreq = None
linefreq = None
timeline = None
firsttime = 0
lasttime = 0
firstts = 0
lastts = 0

def setup(num):
    global cpuNum
    global count
    global firsttime
    global count
    global cpufreq
    global timeline
    global fig

    cpuNum = num
    count = 0
    firsttime = time.time() * 1000
    count = [[0] for i in range(num)]
    cpufreq = [[] for i in range(num)]
    timeline = [[] for i in range(num)]
    linefreq = [] * 10
    fig = plt.figure()

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
    count[cpu][0] += 1

def start():
    # self.cpufreqth.setDaemon()
    # self.cpufreqth.start()
    setup(10)
    load_show()

"""
def display(self, interval):
    while self.mActivy == True:
        for cpu in range(self.cpuNum):
            lasttime = time.time() * 1000 # ms
            lastts = lasttime - firsttime + firstts
            if self.count > 0:
                for index in range(self.count):
                    if self.count == 1:
                        l = plt.axhline(y=self.cpufreq[cpu][index], xmin=0, xmax=self.lastts)
                    elif index == 0 :
                        l = plt.axhline(y=self.cpufreq[cpu][index], xmin=0, xmax=self.cpufreq[cpu][0])
                    elif index == self.count-1 and self.lastts - self.timeline[cpu][index] > 10: # >10ms
                        l = plt.axhline(y=self.cpufreq[cpu][index], xmin=self.timeline[cpu][index],
                                        xmax=self.lastts)
                    else:
                        l = plt.axhline(y=self.cpufreq[cpu][index], xmin=self.timeline[cpu][index],
                                        xmax=self.timeline[cpu][index + 1])
            if(self.lastts > 50 * 1000):
                plt.axis([0, 2500, lastts - 50 * 1000, lastts])
            else:
                plt.axis([0, 2500, 0, 50 * 1000])
            plt.show()

        time.sleep(interval)
"""

def init():
    num = cpuNum
    ax = []
    global linefreq
    for cpu in range(num):
        ax.append(fig.add_subplot(num, 1, 1, xlim=(0, 50000), ylim=(0, 2500)))
        linefreq[cpu], = ax[cpu].plot([], [], lw=1)
        linefreq[cpu].set_data([], [])

    return linefreq


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
    global count
    global cpufreq
    global timeline

    lasttime = time.time() * 1000  # ms
    lastts = lasttime - firsttime + firstts

    for i in range(count[cpu][0]):
        if count[cpu] > 0:
            if i == 0:
                pointx.append(timeline[cpu][0])
                pointy.append(0)

                pointx.append(timeline[cpu][0])
                pointy.append(cpufreq[cpu][0])
            elif i == count[cpu][0] - 1:
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

def animate():
    num = cpuNum

    global lasttime
    global lastts
    global count
    global cpufreq
    global timeline
    global linefreq
    cpointx = []
    cpointy = []
    x = range(50 * 1000)
    for cpu in range(num):
        time, freq = make_point(cpu)
        if len(time) > 0:
            cpointx, cpointy = cut_show_point(lastts - 50 * 1000, lastts, time, freq)
        linefreq[cpu].set_data(cpointx, cpointy)

    return linefreq

def load_show():
    am = animation.FuncAnimation(fig, animate(), init_func=init, frames=50, interval=1 / 100)
    plt.show()

def demo():
    l = plt.axhline(y=.5, xmin=0.25, xmax=0.75)
    plt.axis([-1, 2, -1, 2])
    plt.show()

if __name__ == "__main__":
    demo()