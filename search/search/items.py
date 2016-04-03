# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SearchItem(Item):
    # define the fields for your item here like:
    Title = Field()
    Content = Field()
    URL = Field()
    Images = Field()
    image_urls = Field()
    images = Field()
    pass
