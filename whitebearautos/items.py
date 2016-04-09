# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WhitebearautosItem(scrapy.Item):
    year = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    interior = scrapy.Field()
    stock = scrapy.Field()
    engine = scrapy.Field()
    vin = scrapy.Field()
    transmission = scrapy.Field()
    odometer = scrapy.Field()
    body_style = scrapy.Field()
