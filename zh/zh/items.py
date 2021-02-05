# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhItem(scrapy.Item):
    name = scrapy.Field()
    win = scrapy.Field()
    revenue = scrapy.Field()
