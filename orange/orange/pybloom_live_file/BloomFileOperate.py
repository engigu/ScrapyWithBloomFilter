import os
import time
from threading import Thread
import pybloom_live

try:
    from . import defaults
except:
    import defaults

FILE_PATH = defaults.BLOOM_FILE_PATH


class BloomFileOperate(object):
    """使用pybloom_live实现去重、保存和载入"""

    _instance = None

    def __init__(self, capacity=100000, error_rate=0.0001, save_period=3):
        self.capacity = capacity
        self.error_rate = error_rate
        self.save_period = save_period
        self.stop_signal = False
        self.bf = self.load_bfobj()  # init load bloom obj
        self.save()

    # 暂时不能使用单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(BloomFileOperate, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

    def load_bfobj(self):
        """load bloom file obj"""
        files_list = os.walk(defaults.BLOOM_FILE_PATH)
        files_list_str = str(list(files_list))
        # bloom file not exist --> first run
        if defaults.BLOOM_FILE_NAME not in files_list_str:
            print('init')
            return pybloom_live.BloomFilter(capacity=self.capacity, error_rate=self.error_rate)

        # bloom file exist
        with open(defaults.BLOOM_FILE_PATH + defaults.BLOOM_FILE_NAME, 'rb') as fp:
            print('load_bfobj', defaults.BLOOM_FILE_PATH + defaults.BLOOM_FILE_NAME)
            return pybloom_live.BloomFilter.fromfile(fp)

    def is_exist(self, strings):
        return self.bf.add(strings)

    def stop(self):
        self.stop_signal = True

    def _save(self):
        while True:
            with open(defaults.BLOOM_FILE_PATH + defaults.BLOOM_FILE_NAME, 'wb') as fp:
                self.bf.tofile(fp)
            if self.stop_signal:
                print('--->>> bloom file saving and logout ...')
                break
            print('--->>> save_period', self.save_period)
            time.sleep(self.save_period)

    def save(self):
        t = Thread(target=self._save)
        t.setDaemon(False)
        t.start()
        # t.join()


if __name__ == '__main__':
    f = BloomFileOperate()
    print(f.is_exist(455))
    # f.load_bfobj()
