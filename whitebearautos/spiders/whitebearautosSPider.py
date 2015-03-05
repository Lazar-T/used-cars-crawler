# -*- coding: utf-8 -*-
import scrapy
from whitebearautos.items import WhitebearautosItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
import urlparse


class WhitebearautosspiderSpider(CrawlSpider):
    name = "whitebearautoSpider"
    allowed_domains = ["whitebearautos.com"]
    seed = 'http://www.whitebearautos.com/used-inventory/index.htm?start=%d'
    start_urls = [seed %i for i in [0, 35, 70, 105, 140, 175, 210, 245, 280, 315]]


    def parse(self, response):
        hxs = Selector(response)
        item_selector = hxs.xpath('//h2/a/@href').extract()
        models = hxs.xpath('//h2/a/span/text()').extract()
        miles = hxs.xpath('//*[@class="mileageValue"]/text()').extract()
        engines = hxs.xpath('//*[@class="engineValue"]/text()').extract()
        ext_colors = hxs.xpath('//*[@class="extColorValue"]/text()').extract()
        stock_numbers = hxs.xpath('//*[@class="stockNumberValue"]/text()').extract()
        
        for url, model, mile, engine, ext_color, stock_number in zip(item_selector, models, miles, engines, ext_colors, stock_numbers):
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          meta={'model': model, 'mile': mile, 'engine': engine, 'ext_color': ext_color, 'stock_number': stock_number},
                          )



    def parse_item(self, response):
        l = ItemLoader(item=WhitebearautosItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)

        year_selector = response.xpath('//h1/span/text()')[1].extract()[0:4]
        l.add_xpath('year', year_selector)
        l.add_value('model', response.meta['model'])
        l.add_xpath('price', '//*[@class="internet"][2]/span/text()[2]')
        l.add_value('miles', response.meta['mile'])
        l.add_value('engine', response.meta['engine'])
        vin_selector = response.xpath('//span[text()="VIN"]/following::dd[1]//text()').extract()
        l.add_value('vin', vin_selector)
        l.add_value('ext_color', response.meta['ext_color'])
        int_color_selector = response.xpath('//span[text()="Int. Color"]/following::dd[1]//text()').extract()
        l.add_value('int_color', int_color_selector)
        l.add_value('stock_number', response.meta['stock_number'])
        transmission_selector = response.xpath('//span[text()="Transmission"]/following::dd[1]//text()').extract()
        l.add_value('transmission', transmission_selector)
        l.add_xpath('marketing_text', '//*[@class="comments truncateComments"]/text()')
        l.add_value('url_of_the_vehicle_detail_page', response.url)
        l.add_xpath('vehicle_image', '/html/body/div[2]/div[1]/div/div[3]/div[3]/div/div[1]/div/div/div[1]/div[1]/img/@src')
        return l.load_item()