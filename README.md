# 基于Redis的布隆过滤器

## 1.只实现去重(BloomFilterRedis文件夹、BloomFilterRedis_ex文件夹)

- 实现的功能仅为利用redis实现去重，不能实现增量效果，适用于代爬取链接已知，可以构造出来场景。可以构造出来场景。
- BloomFilterRedis文件夹基于 [kongtianyi](https://github.com/kongtianyi/BloomFilterRedis)
- BloomFilterRedis_ex文件夹基于 [LiuXingMing](https://github.com/LiuXingMing/Scrapy_Redis_Bloomfilter)

- 两个版本不同之处在于所选的hash函数不一样，默认位数组长度位 1 << 31
- 具体配置在目录下 settings.py 里有详细说明。

## 2.实现去重和增量(scrapy_redis_bloom文件夹)

- scrapy_redis_bloom文件夹是基于scrapy-redis实现的布隆过滤器
- 替代scrapy-redis默认的set类型去重，实现去重+增量
- bloom_redis配置与scrapy-redis默认在同一张表，配置方法一样
- 具体配置在目录下 settings.py 里有详细说明。

- 默认hash函数seeds采用质数表，hash函数个数k，其设置都在defaults.py->`HASH_SEEDS_LIST`和`HASH_DEFAULT_K`进行设置


## 3.运行环境

- Python 3.6.3
- redis
- scrapy-redis 0.6.8


## 4.bloom默认设置

- 默认区块大小是 1 << 31，大约是256M，在defaults.py->`BIT_SIZE`里进行设置默认
- `blockNum`为bloom分块数，默认 1 块，在defaults.py->`BLOOM_BLOCK`_NUM里进行设置settings.py->`SCHEDULER_DUPEFILTER_KEY`里进行设置，
  自定义键名带上`spider`与`no`格式符号（no表示分块所处的序号，由取模计算出）eg: `spider1:BRFPDupeFilter:0`
- _scheduler.py为requests队列与bloom公用同一个redis表，scheduler.py为requests队列与bloom分开配置redis，此时是两个redis连接


## 5.代码运行

- 需要代码clone调试，需要在settings.py和defaults.py
- demo.py里内置两个测试函数，`scrapy crawl orange` 为url寻找类，`scrapy crawl spider1` 为url构造生成类

## 6.Other

- 代码由参考前辈们的很多项目，自己改动很少，采用的项目均已设置连接跳转
- scrapy_redis_bloom文件夹是自己给基于scrapy_redis项目项目源码改写，改动地方均已#TODO进行标注，可以与scrapy_redis源码对比查看
