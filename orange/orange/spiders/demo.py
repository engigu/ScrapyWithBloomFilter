# -*- coding: utf-8 -*-
import scrapy, os, sys
# from orange.items import OrangeItem
# path = os.path.realpath(__name__).split(os.path.sep)[:-1]
# path.append('scrapy_redis_bloom_ex')
# sys.path.append(os.path.sep.join(path))
# print(sys.path)
from ..scrapy_redis_bloom.spiders import RedisSpider


class OrangeSpiderSpider(RedisSpider):
    name = "orange"
    allowed_domains = ["baidu.com"]
    # start_urls = ['http://baike.baidu.com/item/橘子水']
    redis_key = 'orange:start_urls'

    def parse(self, response):
        item = {}
        title = response.xpath('//title/text()').extract()
        item['title'] = title
        hrefs = response.xpath('//div[@class="main-content"]//a/@href')
        yield item
        for href in hrefs:
            new_url = href.extract()
            # print new_url
            if "view" in new_url or "item" in new_url:
                yield scrapy.Request(url="http://baike.baidu.com" + new_url, callback=self.parse,
                                     meta={"url": "http://baike.baidu.com" + new_url})


class Spider1(RedisSpider):
    name = "spider1"
    redis_key = "scrapyWithBloomfilter_demo:start_urls"
    start_urls = [
        'http://tieba.baidu.com/p/4855113094?pn=1',
        'http://tieba.baidu.com/p/4855113094?pn=2',
        'http://tieba.baidu.com/p/4855113094?pn=3',
        'http://tieba.baidu.com/p/4855113094?pn=4',

        'http://tieba.baidu.com/p/4855113094?pn=2',  # 这四个URL已爬，将被去重
        'http://tieba.baidu.com/p/4855113094?pn=2',
        'http://tieba.baidu.com/p/4855113094?pn=2',
        'http://tieba.baidu.com/p/4855113094?pn=3',

        'http://tieba.baidu.com/p/4855113094?pn=5',
        'http://tieba.baidu.com/p/4855113094?pn=6',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        print('We Get: %s' % response.url)
