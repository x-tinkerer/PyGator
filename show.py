import time
import matplotlib.pyplot as plt
from matplotlib import animation

class Calc(object):
    def __init__(self):
        pass

class CpufreqCalc(Calc):
    def __init__(self, num):
        self.cpuNum = num
        self.freqinfo = [{} for x in range(num)]

        self.cpufreq = [[] for i in range(num)]
        self.timeline = [[] for i in range(num)]
        self.count = [0 for x in range(num)]

        self.lastkey = [-1 for x in range(num)]
        self.lastts = [-1 for x in range(num)]

    def update_freq_list(self, cpu, ts, value):
        self.cpufreq[cpu].append(value)
        self.timeline[cpu].append(ts)

        self.count[cpu] += 1

    def update_freq_bit(self, cpu, ts, value):
        if not self.freqinfo[cpu].has_key(value):
            self.freqinfo[cpu][value] = 0

        old_total = self.freqinfo[cpu].get(self.lastkey[cpu])
        if self.lastkey[cpu] != -1:
            delta_time = ts - self.lastts[cpu]
            self.freqinfo[cpu][self.lastkey[cpu]] = old_total + delta_time

        self.lastkey[cpu] = value
        self.lastts[cpu] = ts

class GpufreqCalc(Calc):
    def __init__(self):
        self.gpuinfo = {}

        self.gpufreq = []
        self.timeline = []
        self.count = 0

        self.lastkey = -1
        self.lastts = -1

    def update_freq_list(self, ts, value):
        self.gpufreq.append(value)
        self.timeline.append(ts)
        self.count += 1

    def update_freq_bit(self, ts, value):
        if self.gpuinfo.has_key(value):
            old_total = self.gpuinfo.get(value)
            delta_time = ts - self.lastts
            self.freqinfo[value] = old_total + delta_time
        else:
            self.freqinfo[value] = 0

        self.lastkey = value
        self.lastts = ts

class FpsCalc(Calc):
    def __init__(self):
        pass


fig = plt.figure()
ax0 = fig.add_subplot(10, 1, 1, xlim=(0, 20000), ylim=(0, 2100))

def init():
    pass
def animate(cpu):
    pass
def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=30, interval=10)
    plt.show()

if __name__ == "__main__":
    load_show()