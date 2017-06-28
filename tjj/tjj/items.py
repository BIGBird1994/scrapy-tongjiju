# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TjjItem(scrapy.Item):

    province_name = scrapy.Field()
    city_name = scrapy.Field()
    county_name = scrapy.Field()
    village_name = scrapy.Field()
    town_name = scrapy.Field()
    city_code = scrapy.Field()
    county_code = scrapy.Field()
    village_code = scrapy.Field()
    town_code = scrapy.Field()
    Urban_rural_code = scrapy.Field()
    pass
