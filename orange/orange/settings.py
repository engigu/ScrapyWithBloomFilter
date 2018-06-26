# -*- coding: utf-8 -*-

BOT_NAME = 'orange'

SPIDER_MODULES = ['orange.spiders']
NEWSPIDER_MODULE = 'orange.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

ITEM_PIPELINES = {
    'orange.pipelines.OrangePipeline': 301,
}

# 配置过滤器为基于redis的布隆过滤器
# DUPEFILTER_CLASS = 'BloomFilterRedis_ex.BloomRedisDupeFilter.BloomRedisDupeFilter'
# DUPEFILTER_CLASS = 'BloomFilterRedis.BloomRedisDupeFilter.BloomRedisDupeFilter'

# ---------------
# 1. 该区域的配置,对应文件夹为 BloomFilterRedis, BloomFilterRedis_ex
# 2. 实现的功能仅为利用redis实现去重，不能实现增量效果，适用于代爬取链接已知，
#    可以构造出来场景。
################################################
# 第一种：提供两种hash函数加密选择，设置《 BloomFilterRedis文件夹下 》如下：
# 布隆过滤器的哈希列表，默认为8个，定义在GeneralHashFunctions中
# BLOOM_HASH_FUNC_LIST = ["rs_hash", "js_hash", "pjw_hash", "elf_hash", "bkdr_hash", "sdbm_hash", "djb_hash", "dek_hash"]

# 第二种：《 BloomFilterRedis_ex 》无需设置函数，位于BloomFilterRedis_ex文件夹内

# bloom_redis 配置
# TODO 暂时没解决，或者采用URL，优先读取URL
BLOOM_REDIS_URL = 'redis://localhost:6379/10'
# BLOOM_REDIS_HOST = 'localhost'
# BLOOM_REDIS_PORT = 6379
# BLOOM_REDIS_DB = 10

# bloom 默认string的key名字，默认是格式是  eg: bloom_filter:Spider1:0
# 末尾数字区分块
# BLOOM_KEY = 'orange'
# 过滤器采用的块数目（默认单块大小256M）
# BLOOM_BLOCK_NUM = 1
DUPEFILTER_DEBUG = True
################################################

# ---------------
# 1. 基于scrapy-redis实现的布隆过滤器
# 2. 替代scrapy-redis默认的set类型去重，实现去重+增量
# 3. bloom_redis配置与scrapy-redis默认在同一张表，配置方法一样
################################################
DUPEFILTER_CLASS = "orange.scrapy_redis_bloom.BloomRedisDupeFilter.RFPDupeFilter"
# redis调度器替换原本scrapy改写的queue
SCHEDULER = "orange.scrapy_redis_bloom.scheduler.Scheduler"
# redis是否持久化到本地磁盘
SCHEDULER_PERSIST = True

# # redis配置
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
REDIS_URL = 'redis://localhost:6379/11'

################################################


# 设置为爬取策略广度优先
# DEPTH_PRIORITY = 1

# 设置下载延迟
# DOWNLOAD_DELAY = 1

# CONCURRENT_REQUESTS = 10  # 并发
LOG_LEVEL = 'INFO'
