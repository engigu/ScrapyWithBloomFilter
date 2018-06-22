# 基于Redis的布隆过滤器

## 简介

- BloomFilterRedis基于 [kongtianyi](https://github.com/kongtianyi/BloomFilterRedis)
- BloomFilterRedis_ex基于 [LiuXingMing](https://github.com/LiuXingMing/Scrapy_Redis_Bloomfilter)

- 两个版本不同之处在于所选的hash函数不一样，默认位数组长度位 1 << 31
- 具体配置在目录下 settings.py 里有详细说明。

## 运行环境

- Python 3.6.3
- redis
