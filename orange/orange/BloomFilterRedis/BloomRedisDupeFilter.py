# -*- encoding: utf-8 -*-

import logging
from .BloomFilterRedis import BloomFilterRedis
from scrapy.utils.request import request_fingerprint
from scrapy.dupefilters import BaseDupeFilter

# default bloom filter redis config
BLOOM_REDIS_URL = None
BLOOM_REDIS_HOST = 'localhost'
BLOOM_REDIS_PORT = 6379
BLOOM_REDIS_DB = 9
BLOOM_KEY = 'bloom_filter:%(spider_name)s:%(no)s'
BLOOM_BLOCK_NUM = 1

HASH_FUNC_LIST = ["rs_hash", "js_hash", "pjw_hash", "elf_hash", "bkdr_hash", "sdbm_hash", "djb_hash", "dek_hash"]


class BloomRedisDupeFilter(BaseDupeFilter):

    def __init__(self, key, host, port, db, hash_func_list, blockNum, from_url, debug=False):
        self.bloomFilterRedis = BloomFilterRedis(key=key, host=host, port=port, db=db, blockNum=blockNum,
                                                 hash_func_list=hash_func_list, from_url=from_url)
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        key = settings.get('BLOOM_KEY', BLOOM_KEY)
        url = settings.get('BLOOM_REDIS_URL')
        host = settings.get('BLOOM_REDIS_HOST', BLOOM_REDIS_HOST)
        port = settings.get('BLOOM_REDIS_PORT', BLOOM_REDIS_PORT)
        db = settings.get('BLOOM_REDIS_DB', BLOOM_REDIS_DB)
        block_num = settings.get('BLOOM_BLOCK_NUM', BLOOM_BLOCK_NUM)
        hash_func_list = settings.get('HASH_FUNC_LIST', HASH_FUNC_LIST)
        debug = settings.getbool('DUPEFILTER_DEBUG')
        print('--->>> url', url)

        return cls(key, host, port, db, hash_func_list, block_num, url, debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        # use scrapy's default request_fingerprint
        fp = request_fingerprint(request)
        # print(request.callback)
        spider_name = str(request.callback).split("'")[1]
        result = self.bloomFilterRedis.do_filter(spider_name, fp)
        #
        # with open("allurl.txt", "a") as f:
        #     f.write(request.url + '\n')

        if not result:
            # with open("filted.txt", "a") as f:
            #     f.write(request.url + '\n')
            return True
        return False

    def close(self, reason):
        # self.bloomFilterRedis.pool.disconnect()
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
