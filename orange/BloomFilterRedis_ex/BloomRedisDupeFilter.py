# -*- encoding: utf-8 -*-

import logging
from .BloomfilterOnRedis import BloomFilterRedis
from scrapy.utils.request import request_fingerprint
from scrapy.dupefilters import BaseDupeFilter
from . import connection

# default bloom filter config
BLOOM_KEY = 'bloom_filter:%(spider_name)s:%(no)s'
BLOOM_BLOCK_NUM = 1


class BloomRedisDupeFilter(BaseDupeFilter):

    def __init__(self, server, key, blockNum, debug=False):
        self.BFR = BloomFilterRedis(server=server, key=key, blockNum=blockNum)
        self.server = server
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        key = settings.get('BLOOM_KEY', BLOOM_KEY)
        block_num = settings.get('BLOOM_BLOCK_NUM', BLOOM_BLOCK_NUM)
        debug = settings.getbool('DUPEFILTER_DEBUG')
        server = connection.bloom_filter_from_settings(settings)

        return cls(server, key, block_num, debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        # use scrapy's default request_fingerprint
        fp = request_fingerprint(request)
        # print(request.callback)
        spider_name = str(request.callback).split("'")[1]
        # exist
        if self.BFR.is_exists(spider_name, fp):
            return True
        # not exist
        return False  # have'nt seen

    # def request_seen(self, request):
    #     # use scrapy's default request_fingerprint
    #     fp = request_fingerprint(request)
    #     print(request.callback)
    #     spider_name = str(request.callback).split("'")[1]
    #     result = self.BFR.is_exists(spider_name, fp)
    #     # 存在
    #     if result:
    #         return True
    #     # 不存在，加入redis bitmap
    #     self.BFR.insert(spider_name,fp)
    #     return False  # have'nt seen

    def close(self, reason):
        # self.server.pool.disconnect()
        # no need to worry redis pool disconnection
        pass

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('bloom_filter/filtered', spider=spider)
