import xlsxwriter


class Xls(object):
    cpunum = 0

    def __init__(self, excle_name, cpunum):
        """
        """
        self.cpunum = cpunum
        self.workbook = xlsxwriter.Workbook(excle_name)
        self.showsheet = self.workbook.add_worksheet()
        self.cpusheet = self.workbook.add_worksheet()
        self.gpusheet = self.workbook.add_worksheet()
        self.fpssheet = self.workbook.add_worksheet()

        bold = self.workbook.add_format({'bold': True})

        cheadings = []
        for cpu in range(cpunum):
            cheadings.extend(['CPU' + str(cpu), 'Times'])

        self.cpusheet.write_row('A1', cheadings, bold)

        gheadings = ['GPUFreq', 'Times']
        self.gpusheet.write_row('A1', gheadings, bold)

        fheadings = ['FPS', 'Counts']
        self.fpssheet.write_row('A1', fheadings, bold)

    def writeCpuinfo(self, cpuinfo):
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

    def finish(self):
        self.workbook.close()
