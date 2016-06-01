from __future__ import division
import xlsxwriter
import os

class Xls(object):
    cpunum = 0

    cpuinfo = None
    gpuinfo = None
    fpsinfo = None
    cputemp = None
    boardtemp = None

    sugg_cpufreq = []
    sugg_cpufreq_ll = 0
    sugg_cpufreq_l = 0
    sugg_cpufreq_b = 0
    sugg_cpunum_ll = 0
    sugg_cpunum_l = 0
    sugg_cpunum_b = 0
    sugg_gpufreq = 0

    def __init__(self, dir, excle_name, device):
        """
        """
        self.dev = device
        self.cpunum = self.dev.cpu_num
        excle_path = os.path.join(dir, excle_name)
        self.workbook = xlsxwriter.Workbook(excle_path)
        self.showsheet = self.workbook.add_worksheet()
        self.cpusheet = self.workbook.add_worksheet()
        self.gpusheet = self.workbook.add_worksheet()
        self.fpssheet = self.workbook.add_worksheet()
        self.tempsheet = self.workbook.add_worksheet()

        bold = self.workbook.add_format({'bold': True})

        cheadings = []
        for cpu in range(self.cpunum):
            cheadings.extend(['CPU' + str(cpu), 'Times'])

        self.cpusheet.write_row('A1', cheadings, bold)

        gheadings = ['GPUFreq', 'Times']
        self.gpusheet.write_row('A1', gheadings, bold)

        fheadings = ['FPS', 'Counts']
        self.fpssheet.write_row('A1', fheadings, bold)

        fheadings = ['Min Temp', 'Max Temp', 'Avg Temp']
        self.tempsheet.write_row('A1', fheadings, bold)

    def writeCpuinfo(self, cpuinfo):

        self.cpuinfo = cpuinfo

        for cpu in range(self.cpunum):
            row = 1
            col = cpu * 2
            curr_sorted = sorted(cpuinfo[cpu].items(), key=lambda d: d[0])
            for item in curr_sorted:
                self.cpusheet.write(row, col, item[0])
                self.cpusheet.write(row, col + 1, item[1])
                row += 1

            chart = self.workbook.add_chart({'type': 'pie'})

            # Configure the series. Note the use of the list syntax to define ranges:
            chart.add_series({
                'name': 'CPU Frequency',
                'categories': ['Sheet2', 1, col, row, col],
                'values': ['Sheet2', 1, col + 1, row, col + 1],
            })

            # Add a title.
            title = 'CPU' + str(cpu)
            chart.set_title({'name': title})

            # Set an Excel chart style. Colors with white outline and shadow.
            chart.set_style(10)

            # Insert the chart into the worksheet (with an offset).
            chart.set_size({'width': 250, 'height': 200})
            if cpu > 4:
                self.showsheet.insert_chart('C2', chart, {'x_offset': 270 * (cpu - 5), 'y_offset': 250})
            else:
                self.showsheet.insert_chart('C2', chart, {'x_offset': 270 * cpu, 'y_offset': 10})

    def writeGpuinfo(self, gpuinfo):

        self.gpuinfo = gpuinfo

        row = 1
        curr_sorted = sorted(gpuinfo.items(), key=lambda d: d[0])
        for item in curr_sorted:
            self.gpusheet.write(row, 0, item[0])
            self.gpusheet.write(row, 1, item[1])
            row += 1

        chart = self.workbook.add_chart({'type': 'pie'})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart.add_series({
            'name': 'GPU Frequency',
            'categories': ['Sheet3', 1, 0, row, 0],
            'values': ['Sheet3', 1, 1, row, 1],
        })

        # Add a title.
        chart.set_title({'name': 'GPU Frequency'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        chart.set_size({'width': 300, 'height': 250})
        self.showsheet.insert_chart('C2', chart, {'x_offset': 100, 'y_offset': 500})

    def writeFpsinfo(self, fpsinfo):

        self.fpsinfo = fpsinfo

        row = 1
        curr_sorted = sorted(fpsinfo.items(), key=lambda d: d[0])
        for item in curr_sorted:
            self.fpssheet.write(row, 0, item[0])
            self.fpssheet.write(row, 1, item[1])
            row += 1

        chart = self.workbook.add_chart({'type': 'pie'})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart.add_series({
            'name': 'FPS Info',
            'categories': ['Sheet4', 1, 0, row, 0],
            'values': ['Sheet4', 1, 1, row, 1],
        })

        # Add a title.
        chart.set_title({'name': 'FPS Info'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        chart.set_size({'width': 300, 'height': 250})
        self.showsheet.insert_chart('C2', chart, {'x_offset': 500, 'y_offset': 500})

    def writeTempinfo(self, cputemp, boardtemp):

        self.cputemp = cputemp
        self.boardtemp = boardtemp

        # CPU Temperature
        self.tempsheet.write(1, 0, cputemp[0])
        self.tempsheet.write(1, 1, cputemp[1])
        self.tempsheet.write(1, 2, cputemp[2])

        # Board Temperature
        self.tempsheet.write(2, 0, boardtemp[0])
        self.tempsheet.write(2, 1, boardtemp[1])
        self.tempsheet.write(2, 2, boardtemp[2])


        chart = self.workbook.add_chart({'type': 'bar'})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart.add_series({
            'name': 'CPU',
            'categories': ['Sheet5', 1, 0, 1, 2],
            'values': ['Sheet5', 1, 0, 1, 2],
        })

        chart.add_series({
            'name': 'Board',
            'categories': ['Sheet5', 1, 0, 1, 2],
            'values': ['Sheet5', 2, 0, 2, 2],
        })

        # Add a title.
        chart.set_title({'name': 'Temperature'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        chart.set_size({'width': 300, 'height': 250})
        self.showsheet.insert_chart('C2', chart, {'x_offset': 900, 'y_offset': 500})

    def finish(self):
        self.workbook.close()

    def calc_reggestion_cpu(self):

        sugg = []

        if self.dev.cluster_0 > 0:
            self.sugg_cpufreq_ll = 0
            for cpu in range(self.dev.cluster_0):
                if self.sugg_cpufreq_ll < self.sugg_cpufreq[cpu]:
                    self.sugg_cpufreq_ll = self.sugg_cpufreq[cpu]

                if self.sugg_cpufreq[cpu] > 0:
                    self.sugg_cpunum_ll += 1

            sugg.append(self.sugg_cpufreq_ll)
            sugg.append(self.sugg_cpunum_ll)

        if self.dev.cluster_1 > 0:
            self.sugg_cpufreq_l = 0
            for cpu in range(self.dev.cluster_0, self.dev.cluster_0 + self.dev.cluster_1):
                if self.sugg_cpufreq_l < self.sugg_cpufreq[cpu]:
                    self.sugg_cpufreq_l = self.sugg_cpufreq[cpu]

                if self.sugg_cpufreq[cpu] > 0:
                    self.sugg_cpunum_l += 1

            sugg.append(self.sugg_cpufreq_l)
            sugg.append(self.sugg_cpunum_l)

        if self.dev.cluster_2 > 0:
            self.sugg_cpufreq_b = 0
            for cpu in range(self.dev.cluster_0 + self.dev.cluster_1, self.dev.cluster_0 + self.dev.cluster_1 + self.dev.cluster_2):
                if self.sugg_cpufreq_b < self.sugg_cpufreq[cpu]:
                    self.sugg_cpufreq_b = self.sugg_cpufreq[cpu]

                if self.sugg_cpufreq[cpu] > 0:
                    self.sugg_cpunum_b += 1

            sugg.append(self.sugg_cpufreq_b)
            sugg.append(self.sugg_cpunum_b)

        sugg.append(self.sugg_gpufreq)

        return sugg

    def write_suggestion_info(self):

        total_time = 0
        curr_sorted = sorted(self.cpuinfo[0].items(), key=lambda d: d[0])
        for item in curr_sorted:
            ts = item[1]
            total_time += ts

        for cpu in range(self.cpunum):
            percent = 0
            curr_sorted = sorted(self.cpuinfo[cpu].items(), key=lambda d: d[0])
            for item in curr_sorted:
                ts = item[1]
                percent += ts / total_time

                if percent > 0.5:
                    self.sugg_cpufreq.append(item[0])
                    self.showsheet.write(0, cpu, item[0])
                    break

        percent = 0
        curr_sorted = sorted(self.gpuinfo.items(), key=lambda d: d[0])
        for item in curr_sorted:
            ts = item[1]
            percent += ts / total_time

            if percent > 0.5:
                self.sugg_gpufreq = item[0]
                self.showsheet.write(0, cpu + 1, item[0])
                break
