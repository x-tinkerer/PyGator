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

    def writeGpuinfo(self, gpuinfo):
        row = 1
        curr_sorted = sorted(gpuinfo.items(), key=lambda d: d[0])
        for item in curr_sorted:
            self.gpusheet.write(row, 0, item[0])
            self.gpusheet.write(row, 1, item[1])
            row += 1

    def add_chart(self):
        # Create a new chart object.
        chart = self.workbook.add_chart({'type': 'line'})

        chart.set_x_axis({
            'name': 'Size',
            'name_font': {'size': 14, 'bold': True},
            'num_font': {'italic': True},
        })

        # Add a series to the chart.
        avg_col = self.listsize + 1
        arr_str = '=Sheet1!$L$2:$L$' + str(avg_col)
        chart.add_series({
            'name': 'Write',
            'values': arr_str,
            'marker': {
                'type': 'square',
                'size': 4,
                'border': {'color': 'black'},
                'fill': {'color': 'red'},
            },
        })

        # Add a series to the chart.
        arr_str = '=Sheet1!$M$2:$M$' + str(avg_col)
        chart.add_series({
            'name': 'Read',
            'values': arr_str,
            'marker': {
                'type': 'square',
                'size': 4,
                'border': {'color': 'blue'},
                'fill': {'color': 'red'},
            },
        })

        self.worksheet.insert_chart('L20', chart)

    def finish(self):
        self.workbook.close()
