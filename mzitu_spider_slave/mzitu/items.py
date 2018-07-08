# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    # 套图url
    # define the fields for your item here like:
    type_name = scrapy.Field()  # 分类名
    img_box_name = scrapy.Field()  # 套图名
    img_url = scrapy.Field()  # 套图url
    url = scrapy.Field()

