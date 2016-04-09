# -*- coding: utf-8 -*-
import urlparse

from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from w3lib.html import replace_escape_chars, remove_tags

from whitebearautos.items import WhitebearautosItem


class WhitebearautosspiderSpider(Spider):
    name = 'whitebearautos'
    allowed_domains = ['whitebearautos.com']
    start_urls = ['http://www.whitebearautos.com/inventory/view/Used/']

    def parse(self, response):
        # process each car link
        urls = response.xpath('//h2/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = Request(absolute_url, callback=self.parse_car)
            yield request

        # process next page
        next_page_url = response.xpath('.//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = Request(absolute_next_page_url)
        yield request

    def parse_car(self, response):
        l = ItemLoader(item=WhitebearautosItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)

        car_data = response.xpath('.//*[@class="cardata"]//text()').extract()
        if len(car_data) is 8:
            year, __, make, __, model, __, trim, __ = car_data
        elif len(car_data) is 7:
            year, __, make, __, model, __, trim = car_data
        else:
            year, __, make, __, model, __ = car_data
            trim = ''

        l.add_value('year', year)
        l.add_value('make', make)
        l.add_value('model', model)
        l.add_value('trim', trim)

        l.add_value('url', response.url)

        l.add_xpath('price', './/*[@class="single clearfix"]/span/text()')

        l.add_xpath('color', '//label[text()="Color:"]/following-sibling::span/text()')
        l.add_xpath('interior', '//label[text()="Interior:"]/following-sibling::span/text()')
        l.add_xpath('stock', '//label[text()="Stock#:"]/following-sibling::span/text()')
        l.add_xpath('engine', '//label[text()="Engine:"]/following-sibling::span/text()')
        l.add_xpath('vin', '//label[text()="VIN:"]/following-sibling::span/text()')
        l.add_xpath('transmission', '//label[text()="Transmission:"]/following-sibling::span/text()')
        l.add_xpath('odometer', '//label[text()="Odometer:"]/following-sibling::span/text()')
        l.add_xpath('body_style', '//label[text()="Body Style:"]/following-sibling::span/text()')

        return l.load_item()
