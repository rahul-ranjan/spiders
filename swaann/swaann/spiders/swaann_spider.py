from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import json
import functools
import re
import csv

class SwaannSpider(Spider):
	name = "swaann"
	allowed_domains = ["swaann.com"]
	start_urls = ["http://swaann.com/"]

	def parse(self, response):
		sel = Selector(response)
		with open('url1.csv') as fin1:
			reader = csv.reader(fin1)
			for row in reader:
				#url = row[1]
				name = row[0]
				for x in range(1,3):
					if x == 1:
						url = row[1]
						try:	yield Request(str(url),functools.partial(self.data_parse,url=url,name=name),meta = {'dont_redirect': True,"handle_httpstatus_list" : [301, 302, 303]})
						except Exception, e:
							raise
					else:
						ur = row[1][0:-1]
						url = ur+"-P2/"
						try:	yield Request(str(url),functools.partial(self.data_parse,url=url,name=name),meta = {'dont_redirect': True,"handle_httpstatus_list" : [301, 302, 303]})
						except Exception, e:
							raise

	def data_parse(self, response,url,name):	
		sel = Selector(response)
		div = sel.xpath('//*[@id="div_result"]/div[2]/div[1]/div[@class="listing-cont"]')
		for d in div:
			title = ''.join(d.xpath('div/a/text()').extract()).encode('ascii','ignore')
			phone = ''.join(d.xpath('span[2]/text()').extract()).encode('ascii','ignore')
			address = ''.join(d.xpath('span[4]/text()').extract()).encode('ascii','ignore')
			with open('swaann.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				data = [[name,title,phone,address]]
				a.writerows(data)
