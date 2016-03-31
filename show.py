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

class CpufreqDisplay(Display):
    maxRecord = 10000
    cpuNum = 0
    count = None
    cpufreq = None
    timeline = None
    firsttime = 0
    lasttime = 0
    firstts = 0
    lastts = 0
    cpufreq = []
    fig = None

    def __init__(self, num):
        self.cpuNum = num
        self.count = 0
        self.firsttime = time.time() * 1000
        self.count = [[0] for i in range(num)]
        self.cpufreq = [[] for i in range(num)]
        self.timeline = [[] for i in range(num)]
        self.fig = plt.figure()

    def update(self, cpu, ts, value):
        if self.firstts == 0:
            self.firstts = ts
            self.firsttime = time.time() * 1000
        self.cpufreq[cpu].append(value)
        self.timeline[cpu].append(ts)
        # self.lasttime = time.time() * 1000 # ms
        self.count[cpu][0] += 1

    def start(self):
        # self.cpufreqth.setDaemon()
        # self.cpufreqth.start()
        self.load_show()

    def display(self, interval):
        while self.mActivy == True:
            for cpu in range(self.cpuNum):
                self.lasttime = time.time() * 1000 # ms
                self.lastts = self.lasttime - self.firsttime + self.firstts
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
                    plt.axis([0, 2500, self.lastts - 50 * 1000, self.lastts])
                else:
                    plt.axis([0, 2500, 0, 50 * 1000])
                plt.show()

            time.sleep(interval)

    def init(self):
        num = self.cpuNum
        ax = []
        for cpu in range(num):
            ax.append(self.fig.add_subplot(num, 1, 1, xlim=(0, 50000), ylim=(0, 2500)))
            self.cpufreq[cpu], = ax[cpu].plot([], [], lw=1)
            self.cpufreq[cpu].set_data([], [])

        return self.cpufreq


    def cut_show_point(self, start_t, end_t, pointx, pointy):
        tmpx = []
        tmpy = []

        if pointx[-1] < 50 * 1000:
            return pointx, pointy
        else:
            for i in range(len(pointx)):
                if pointx[i] > start_t and pointx[i] < end_t:
                    tmpx.append(pointx[i])
                    tmpy.append(pointy[i])

            return tmpx, tmpy

    def make_point(self,cpu):
        pointx = []
        pointy = []

        self.lasttime = time.time() * 1000  # ms
        self.lastts = self.lasttime - self.firsttime + self.firstts

        for i in range(self.count[cpu]):
            if self.count[cpu] > 0:
                if i == 0:
                    pointx.append(self.timeline[cpu][0])
                    pointy.append(0)

                    pointx.append(self.timeline[cpu][0])
                    pointy.append(self.cpufreq[cpu][0])
                elif i == self.count[cpu] - 1:
                    pointx.append(self.timeline[cpu][i])
                    pointy.append(self.cpufreq[cpu][i])

                    pointx.append(self.lastts)
                    pointy.append(self.cpufreq[cpu][i])
                else:
                    pointx.append(self.timeline[cpu][i])
                    pointy.append(self.cpufreq[cpu][i-1])

                    pointx.append(self.timeline[cpu][i])
                    pointy.append(self.cpufreq[cpu][i])

        return pointx, pointy

    def animate(self):
        num = self.cpuNum
        x = range(50 * 1000)
        for cpu in range(num):
            time, freq = self.make_point(cpu)

            pointx ,pointx = self.cut_show_point(self.lastts - 50 * 1000, self.lastts, time, freq)

            self.cpufreq[cpu].set_data(pointx, pointx)

        return self.cpufreq

    def load_show(self):
        am = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=50, interval=1 / 100)
        plt.show()

def demo():
    l = plt.axhline(y=.5, xmin=0.25, xmax=0.75)
    plt.axis([-1, 2, -1, 2])
    plt.show()

if __name__ == "__main__":
    demo()