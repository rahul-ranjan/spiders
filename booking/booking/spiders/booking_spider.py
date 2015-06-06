from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import json
import functools
import re
import csv

class BookingSpider(Spider):
	name = "booking"
	allowed_domains = ["booking.com"]
	start_urls = ["http://www.booking.com/searchresults.html?city=-2106102"]

	def parse(self, response):
		sel = Selector(response)
		with open('url1.csv') as fin1:
			reader = csv.reader(fin1)
			for row in reader:
				url = row[0]
				try:	yield Request(str(url),functools.partial(self.data_parse))
				except Exception, e:
					raise
	def data_parse(self, response):	
		sel = Selector(response)
		name = ''.join(sel.xpath('//*[@id="hp_hotel_name"]/text()').extract()).strip().encode('ascii','ignore')
		address = ''.join(sel.xpath('//*[@id="hp_address_subtitle"]/text()').extract()).strip().encode('ascii','ignore')
		rating = ''.join(sel.xpath('//*[@id="wrap-hotelpage-top"]/h1/span[2]/span/i/@title').extract()).strip().encode('ascii','ignore')
		with open('booking.csv', 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			data = [[name,address,rating]]
			a.writerows(data)
