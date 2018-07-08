# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re



class MzituPipeline(object):
    def process_item(self, item, spider):
        return item


class MzituImgPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):

        item = request.meta.get('item')
        type_name = strip(item['type_name'])
        img_box_name = strip(item['img_box_name'])
        img_guid = request.url.split('/')[-1]
        filename = '{0}/{1}/{2}'.format(type_name, img_box_name, img_guid)
        return filename

    def get_media_requests(self, item, info):
        referer = item['url']
        yield Request(url=item['img_url'], meta={'item': item, 'referer': referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item





def strip(path):
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path