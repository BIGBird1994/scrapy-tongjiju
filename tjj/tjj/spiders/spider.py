from tjj.items import TjjItem
import scrapy
import re
import copy


class spider(scrapy.Spider):
    name = 'tjj'
    start_urls =[]
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    cookie = {
        'AD_RS_COOKIE': '20081684'
    }

    def start_requests(self):
        yield scrapy.Request('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html',
                             headers=self.header, cookies=self.cookie, callback=self.parse_province, dont_filter=True)

    def parse_province(self, response):
        # print response.body
        for data in response.xpath('//tr[@class="provincetr"]/td'):
            item = TjjItem()
            item['province_name'] = data.xpath('a/text()').extract_first()
            href = data.xpath('a/@href').extract_first()
            next_url = response.urljoin(href)
            yield scrapy.Request(next_url, meta={'item': item},
                                 headers=self.header, cookies=self.cookie, callback=self.parse_city, dont_filter=True)

    def parse_city(self, response):
        for data in response.xpath('//tr[@class="citytr"]'):
                item = copy.deepcopy(response.meta['item'])
                item['city_name'] = data.xpath('td[2]/a/text()').extract_first()
                item['city_code'] = data.xpath('td[1]/a/text()').extract_first()
                href = data.xpath('td[1]/a/@href').extract_first()
                next_url = response.urljoin(href)
                yield scrapy.Request(next_url, meta={'item': item},
                                     headers=self.header, cookies=self.cookie, callback=self.parse_county)

    def parse_county(self, response):

        for data in response.xpath('//tr[@class="countytr"]'):
            item = copy.deepcopy(response.meta['item'])
            item['county_code'] = data.xpath('td[1]/a/text()').extract_first()
            item['county_name'] = data.xpath('td[2]/a/text()').extract_first()
            href = data.xpath('td[1]/a/@href').extract_first()
            next_url = response.urljoin(href)
            yield scrapy.Request(next_url, meta={'item': item},
                                 headers=self.header, cookies=self.cookie, callback=self.parse_town, dont_filter=True)

    def parse_town(self, response):
        for data in response.xpath('//tr[@class="towntr"]'):
            item = copy.deepcopy(response.meta['item'])
            item['town_code'] = data.xpath('td[1]/a/text()').extract_first()
            item['town_name'] = data.xpath('td[2]/a/text()').extract_first()
            href = data.xpath('td[1]/a/@href').extract_first()
            next_url = response.urljoin(href)
            yield scrapy.Request(next_url, meta={'item': item},
                                 headers=self.header, cookies=self.cookie, callback=self.parse_community, dont_filter=True)

    def parse_community(self, response):
        for data in response.xpath('//tr[@class="villagetr"]'):
            item = copy.deepcopy(response.meta['item'])
            item['village_code'] = data.xpath('td[1]/text()').extract_first()
            item['Urban_rural_code'] = data.xpath('td[2]/text()').extract_first()
            item['village_name'] = data.xpath('td[3]/text()').extract_first()
            print item
            yield item
