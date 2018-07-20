import os
import signal
import sys
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

    # instance = None
    stop_signal = False

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
        BloomFileOperate.stop_signal = True

    def _auto_save(self):
        """自动保存bloom文件，去重数量过大时候，不宜设置过短时间"""
        while True:
            with open(defaults.BLOOM_FILE_PATH + defaults.BLOOM_FILE_NAME, 'wb') as fp:
                self.bf.tofile(fp)
            if BloomFileOperate.stop_signal:
                print('--->>> pybloom file saving and exit ...')
                break
            print('--->>> auto_save_period', self.save_period)
            time.sleep(self.save_period)

    def save(self):
        t = Thread(target=self._auto_save)
        t.setDaemon(False)
        t.start()
        # t.join()


def quit(signum, frame):
    BloomFileOperate.stop_signal = True


signal.signal(signal.SIGINT, quit)  # 退出信号注册
signal.signal(signal.SIGTERM, quit)


if __name__ == '__main__':
    f = BloomFileOperate()
    print(f.is_exist(455))
    # f.load_bfobj()
