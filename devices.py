class M80(object):
    def __init__(self):
        self.dev = 'M80'
        self.cpu_num = 10
        self.clusters = 3
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 2

        self.show_cpu = 1
        self.show_gpu = 1
        self.show_fps = 1
        self.show_temp = 1
        self.show_num = 14

class M95(object):
    def __init__(self):
        self.dev = 'M80'
        self.cpu_num = 10
        self.clusters = 3
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 2

        self.show_cpu = 1
        self.show_gpu = 1
        self.show_fps = 1
        self.show_temp = 1
        self.show_num = 14

class MA02(object):
    def __init__(self):
        self.dev = 'MA02'
        self.cpu_num = 8
        self.clusters = 2
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 0

        self.show_cpu = 1
        self.show_gpu = 1
        self.show_fps = 1
        self.show_temp = 1
        self.show_num = 12

class M86(object):
    def __init__(self):
        self.dev = 'M86'
        self.cpu_num = 8
        self.clusters = 2
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 0

        self.show_cpu = 1
        self.show_gpu = 1
        self.show_fps = 0
        self.show_temp = 0
        self.show_num = 10

class M96(object):
    def __init__(self):
        self.dev = 'M96'
        self.cpu_num = 8
        self.clusters = 2
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 0

        self.show_cpu = 1
        self.show_gpu = 1
        self.show_fps = 1
        self.show_temp = 0
        self.show_num = 10


class Devices(object):
    def __init__(self, name):
        self.dev = name

    def get_device(self):
        if self.dev == 'M80' or self.dev == 'm80':
            return M80()
        if self.dev == 'M86' or self.dev == 'm86':
            return M86()
        if self.dev == 'M95' or self.dev == 'm95':
            return M95()
        if self.dev == 'MA02' or self.dev == 'ma02':
            return MA02()
        if self.dev == 'M96' or self.dev == 'm96':
            return M96()
