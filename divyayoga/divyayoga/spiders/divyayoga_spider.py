from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import functools
import csv

class DivyaYogaSpider(Spider):
	name = "divyayoga"
	allowed_domains = ["divyayoga.com"]
	start_urls = ["http://www.divyayoga.com/search_dropdown.php?search2=true&district=All%20States&state=All%20States"]

	def parse(self, response):
		sel = Selector(response)
		div = sel.xpath('//*[@id="result_table"]/tr')
		for d in div:
			state = ''.join(d.xpath('td[2]/text()').extract()).strip().encode('ascii','ignore').replace("\n","").strip()
			district = ''.join(d.xpath('td[3]/text()').extract()).strip().encode('ascii','ignore').replace("\n","").strip()
			phone = d.xpath('td[5]/text()').extract()
			address = ''.join(d.xpath('td[4]/text()').extract()).strip().encode('ascii','ignore').replace("\n","").strip().replace("\r","").replace("\t","").strip()
			with open('divyayoga.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				data = [[state,district,address]+phone]
				a.writerows(data)
					