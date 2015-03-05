# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WhitebearautosItem(scrapy.Item):
    year = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    miles = scrapy.Field()
    engine = scrapy.Field()
    vin = scrapy.Field()
    ext_color = scrapy.Field()
    int_color = scrapy.Field()
    stock_number = scrapy.Field()
    transmission = scrapy.Field()
    marketing_text = scrapy.Field()
    url_of_the_vehicle_detail_page = scrapy.Field()
    vehicle_image = scrapy.Field()

