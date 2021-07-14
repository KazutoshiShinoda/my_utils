class Statistics(object):
    def __init__(self):
        self.num_update = 0
        self.stat = {}

    def update_dict(self, stat_dict):
        for key, value in stat_dict.items():
            self.stat[key] = self.stat.get(key, 0) + value
        self.num_update += 1

    def mean(self):
        mean_stat = {}
        for key, value in self.stat.items():
            mean_stat[key] = value / self.num_update
        mean_stat['NumOfUpdates'] = self.num_update
        return mean_stat

    def reset(self):
        self.num_update = 0
        self.stat = {}
