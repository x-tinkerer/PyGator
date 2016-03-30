import numpy as np
import matplotlib.pyplot as plt
import time

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
    count = 0

    cpufreq = None
    timeline = None
    firsttime = 0
    lasttime = 0
    firstts = 0
    lastts = 0

    def __init__(self, num):
        self.cpuNum = num
        self.count = 0
        self.firsttime = time.time() * 1000
        self.cpufreq = [[] for i in range(num)]
        self.timeline = [[] for i in range(num)]

    def update(self, cpu, ts, value):
        if self.firstts == 0:
            self.firstts = ts
            self.firsttime = time.time() * 1000
        self.cpufreq[cpu].append(value)
        self.timeline[cpu].append(ts)
        # self.lasttime = time.time() * 1000 # ms
        self.count += 1

    def display(self, sleep):
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

            time.sleep(sleep)


def demo():

    l = plt.axhline(y=.5, xmin=0.25, xmax=0.75)

    plt.axis([-1, 2, -1, 2])

    plt.show()

if __name__ == "__main__":
    demo()