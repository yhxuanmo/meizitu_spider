from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from mzitu.items import ImgItem


class MzituSpiser(RedisSpider):

    name = 'mzitu_slave'
    redis_key = 'mzitu:start_urls'


    def parse(self, response):
        sel = Selector(response)
        current_url = response.url
        max_page = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()').extract_first()
        type_name = sel.xpath('//div[@class="currentpath"]/a[@rel="category tag"]/text()').extract_first()
        img_box_name = sel.xpath('//h2[@class="main-title"]/text()').extract_first()

        for i in range(1, int(max_page)+1):
            yield Request(url=current_url + '/' + str(i),
                          callback=self.img_url_parse,
                          meta={'type_name': type_name, 'img_box_name': img_box_name, 'url': current_url})

    def img_url_parse(self, response):
        sel = Selector(response)
        item = ImgItem()
        item['url'] = response.meta.get('url')
        item['type_name'] = response.meta.get('type_name')
        item['img_box_name'] = response.meta.get('img_box_name')
        item['img_url'] = sel.xpath('//div[@class="main-image"]/descendant::img/@src').extract_first()
        return item


