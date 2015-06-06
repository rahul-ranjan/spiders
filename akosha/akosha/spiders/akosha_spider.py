from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import time
import functools
import csv

class AkoshaSpider(Spider):
	name = "akosha"
	allowed_domains = ["akosha.com"]
	start_urls = ["http://www.akosha.com"]
	
	def parse(self, response):
		sel = Selector(response)
		with open('companies.csv') as fin:
			reader = csv.reader(fin)
			for u in reader:
				url = "http://www.akosha.com/"+u[0].replace(" ","-").replace(".","-").replace("--","-").replace(",","-")+"-customer-care-"+u[1]+".html"
				try:	yield Request(''.join(url).replace("--","-"),functools.partial(self.listing_parse,url=''.join(url)))
				except: print "Exception caught in"+str(url)

	def listing_parse(self, response, url):
		sel = Selector(response)
		name = ''.join(sel.xpath('/html/body/div[2]/div[1]/div/div/div[1]/h1/text()').extract()).encode('ascii','ignore')
		phone = ''.join(sel.xpath('//*[@id="phoneSupport"]/p[2]/span/text()').extract()).encode('ascii','ignore')
		email = ''.join(sel.xpath('//*[@id="emailSupport"]/a/text()').extract()).encode('ascii','ignore')
		address = ''.join(sel.xpath('//*[@id="address"]/p[2]/span/text()').extract()).strip().replace("\n","").replace("\t","").encode('ascii','ignore')
		print name,phone,email,address
		with open('data.csv', 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			data = [[name,phone,email,address]]
			a.writerows(data)