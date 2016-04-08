import xlsxwriter


class Xls(object):
    cpunum = 0

    def __init__(self, excle_name, cpunum):
        """
        """
        self.cpunum = cpunum
        self.workbook = xlsxwriter.Workbook(excle_name)
        self.cpusheet = self.workbook.add_worksheet()
        self.gpusheet = self.workbook.add_worksheet()

        bold = self.workbook.add_format({'bold': True})

        cheadings = []
        for cpu in range(cpunum):
            cheadings.extend(['CPU'+ str(cpu), 'Times'])

        self.cpusheet.write_row('A1', cheadings, bold)

        gheadings = ['GPUFreq', 'Times']
        self.gpusheet.write_row('A1', gheadings, bold)

    def write_excle(self, fields):
        """
        Write out to excel table.
        """
        row = long(fields['col'])

        self.worksheet.write(row, 4, float(fields['time']))
        self.worksheet.write(row, 5, float(fields['perf']))

    def writeCpuinfo(self, cpuinfo):
        for cpu in range(self.cpunum):
            row = 1
            col = cpu * 2
            curr_sorted = sorted(cpuinfo[cpu].items(), key=lambda d:d[0])
            for item in curr_sorted:
                self.cpusheet.write(row, col, item[0])
                self.cpusheet.write(row, col + 1, item[1])
                row += 1

            chart = self.workbook.add_chart({'type': 'pie'})

            # Configure the series. Note the use of the list syntax to define ranges:
            chart.add_series({
                'name': 'Pie sales data',
                'categories': ['Sheet1', 1, col, row, col],
                'values': ['Sheet1', 1, col + 1, row, col + 1],
            })

            # Add a title.
            title = 'CPU' + str(cpu)
            chart.set_title({'name': title})

            # Set an Excel chart style. Colors with white outline and shadow.
            chart.set_style(10)

            # Insert the chart into the worksheet (with an offset).
            chart.set_size({'width': 250, 'height': 200})
            if cpu > 4:
                self.cpusheet.insert_chart('C2', chart, {'x_offset': 270 * (cpu -5), 'y_offset': 300})
            else:
                self.cpusheet.insert_chart('C2', chart, {'x_offset': 270 * cpu, 'y_offset': 100})

    def writeGpuinfo(self, gpuinfo):
        row = 1
        curr_sorted = sorted(gpuinfo.items(), key=lambda d: d[0])
        for item in curr_sorted:
            self.gpusheet.write(row, 0, item[0])
            self.gpusheet.write(row, 1, item[1])
            row += 1


    def finish(self):
        self.workbook.close()
