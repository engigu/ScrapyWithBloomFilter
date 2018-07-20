# -*- encoding: utf-8 -*-

import logging

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from .BloomFileOperate import BloomFileOperate


class BloomFileDupeFilter(BaseDupeFilter):

    def __init__(self, server, debug=False):
        self.server = server
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        capacity = settings.get('BLOOM_CAPACITY', defaults.BLOOM_CAPACITY)
        error_rate = settings.get('BLOOM_ERROR_RATE', defaults.BLOOM_ERROR_RATE)
        save_period = settings.get('SAVE_PERIOD', defaults.SAVE_PERIOD)
        debug = settings.getbool('DUPEFILTER_DEBUG')
        server = BloomFileOperate(capacity=capacity, error_rate=error_rate, save_period=save_period)

        return cls(server, debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        # use scrapy's default request_fingerprint
        fp = request_fingerprint(request)
        res = self.server.is_exist(fp)
        if res:
            self.logger.info('过滤了重复请求：%s', request.url)
        return res

    def close(self, reason):
        self.server.stop()

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

        spider.crawler.stats.inc_value('pybloom_live_file/filtered', spider=spider)
