# -*- coding: utf-8 -*-

import redis
from . import GeneralHashFunctions


class BloomFilterRedis:

    def __init__(self, key, host, port, db, hash_func_list, blockNum, from_url=None):
        # redis-bitmap的key
        self.key = key
        # redis连接信息
        self.pool = redis.from_url(from_url) if from_url else \
            redis.ConnectionPool(host=host, port=port, db=db)
        self.handle = redis.StrictRedis(connection_pool=self.pool, charset='utf-8')

        # 分区块数目，默认为 1
        self.blockNum = blockNum
        # 哈希函数列表
        self.hash_func_list = hash_func_list

    @classmethod
    def random_generator(cls, hash_value):
        '''
        将hash函数得出的函数值映射到[0, 2^31-1]区间内,大约256M
        '''
        return hash_value % (1 << 31)

    def do_filter(self, spider_name, item):
        '''
        检查是否是新的条目，是新条目则更新bitmap并返回True，是重复条目则返回False
        '''
        flag = False
        for hash_func_str in self.hash_func_list:
            block_No = str(int(item[0:2], 16) % self.blockNum)
            name = self.key % {'spider_name': spider_name, 'no': block_No}
            # 获得到hash函数对象
            hash_func = getattr(GeneralHashFunctions, hash_func_str)
            # 计算hash值
            hash_value = hash_func(item)
            # 将hash值映射到[0, 2^32]区间
            real_value = BloomFilterRedis.random_generator(hash_value)
            # bitmap中对应位是0，则置为1，并说明此条目为新的条目
            if self.handle.getbit(name, real_value) == 0:
                self.handle.setbit(name, real_value, 1)
                flag = True
        # 当所有hash值在bitmap中对应位都是1，说明此条目重复，返回False
        return flag
