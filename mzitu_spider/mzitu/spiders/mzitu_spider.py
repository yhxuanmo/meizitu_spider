from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from mzitu.items import ImgBoxItem


class MzituSpiser(Spider):

    name = 'mzitu'
    start_urls = ['http://www.mzitu.com/',]


    def parse(self, response):
        sel = Selector(response)
        typy_tag = sel.xpath('//ul[@id="menu-nav"]/li')

        for tag in typy_tag:
            # 排除首页的url
            if tag.xpath('./a/text()').extract_first() != '首页':
                if tag.xpath('./a/text()').extract_first() == '妹子自拍':
                    continue
                if tag.xpath('./a/text()').extract_first() == '每日更新':
                    continue
                # 分类的url
                type_url = tag.xpath('./a/@href').extract_first()
                # 分类名
                type_name = tag.xpath('./a/text()').extract_first()
                yield Request(url=type_url,callback=self.type_url_parse, meta={'type_name':type_name})


    def type_url_parse(self, response):
        # 分页类页面解析
        sel = Selector(response)
        curent_url = response.url
        max_page = sel.xpath('//div[@class="nav-links"]/a[@class="page-numbers"]')[-1].xpath('./text()').extract_first()

        for i in range(1,int(max_page)+1):

            yield Request(url= curent_url+'page/'+ str(i) + '/',
                          callback=self.img_box_url_parse,
                          meta={'type_name':response.meta.get('type_name')}
                          )


    def img_box_url_parse(self, response):
        # 套图url解析
        sel = Selector(response)
        img_box_lis = sel.xpath('//ul[@id="pins"]/li')
        item = ImgBoxItem()
        type_name = response.meta.get('type_name')
        for li in img_box_lis:
            # 套图url
            item['img_box_url'] = li.xpath('./a/@href').extract()[0]
            # 套图名称
            item['img_box_name'] = li.xpath('./span/a/text()').extract()[0]
            # 分类名
            item['type_name'] = type_name
            yield item

