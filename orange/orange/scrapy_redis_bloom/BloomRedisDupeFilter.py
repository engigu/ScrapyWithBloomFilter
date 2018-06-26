import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from .connection import get_redis_from_settings

from .BloomfilterOnRedis import BloomFilterRedis


# logger = logging.getLogger(__name__)


class RFPDupeFilter(BaseDupeFilter):

    def __init__(self, server, key, blockNum, debug=False):
        self.BFR = BloomFilterRedis(server=server, key=key, blockNum=blockNum)
        self.server = server
        self.logdupes = True
        self.debug = debug
        self.key = key
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        # key = settings.get('BLOOM_KEY', BLOOM_KEY)
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        block_num = settings.get('BLOOM_BLOCK_NUM', defaults.BLOOM_BLOCK_NUM)
        debug = settings.getbool('DUPEFILTER_DEBUG')
        server = get_redis_from_settings(settings)

        return cls(server, key, block_num, debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        # use scrapy's default request_fingerprint
        fp = request_fingerprint(request)
        # exist
        if self.BFR.is_exists(fp):
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

    def close(self, reason=''):
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        # self.server.delete(self.key)
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
