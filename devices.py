class M80(object):
    def __init__(self):
        self.dev = 'M80'
        self.cpu_num = 10
        self.clusters = 3
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 2


class M95(object):
    def __init__(self):
        self.dev = 'M80'
        self.cpu_num = 10
        self.clusters = 3
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 2


class M86(object):
    def __init__(self):
        self.dev = 'M86'
        self.cpu_num = 8
        self.clusters = 2
        self.cluster_0 = 4
        self.cluster_1 = 4
        self.cluster_2 = 0


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
