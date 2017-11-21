# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#该文件定义了待抓取域的模型

import scrapy

class UniversityItem(scrapy.Item):                                 #是一个模板  需要将期中的内容替换为爬虫运行时想要存储的待抓取国家信息
    # define the fields for your item here like:
    name = scrapy.Field()
    rank = scrapy.Field(serializer=int)
    country = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    undergraduate_num = scrapy.Field()
    postgraduate_num = scrapy.Field()
    website = scrapy.Field()