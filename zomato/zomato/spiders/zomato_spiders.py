from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import json
import functools
import re
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
import csv
import HTMLParser

class ZomatoSpider(Spider):
	name = "zomato"
	allowed_domains = ["zomato.com"]
	start_urls = ["https://www.zomato.com/ncr/saravana-bhavan-connaught-place-new-delhi"]
	
	def parse(self, response):
		sel = Selector(response)
		with open('zomato5.csv') as fin1:
			reader = csv.reader(fin1)
			for row in reader:
				rev = ""
				rev = row[11]
				if rev == "":
					rev = "500"
				id = row[0]
				name = 	row[1]
				phone = row[2]
				address = row[3]
				cost = row[4]
				hours = row[5]
				known = row[6]
				estab = row[7]
				cuisine = row[8]
				highlight = row[9]
				link = row[10]
				try:
					yield FormRequest(url="https://www.zomato.com/php/social_load_more.php", method="POST", formdata={'entity_id':id, 'profile_action':'reviews-dd','page':'0','limit':rev}, callback=functools.partial(self.data_parse,id=id,name=name,phone=phone,address=address,cost=cost,hours=hours,known=known,estab=estab,cuisine=cuisine,highlight=highlight,link=link))
				except Exception, e:
					raise
		#except: print "Exception caught
	def data_parse(self, response, id,name,phone,address,cost,hours,known,estab,cuisine,highlight,link):	
		sel = Selector(response)
		jsonresponse = json.loads(response.body_as_unicode())
		hello= jsonresponse["html"].encode('ascii','ignore')
		sel1 = Selector(text=hello)
		rev = sel1.xpath('/html/body/div')
		for r in rev:
			rev_name = ''.join(r.xpath('div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a/text()').extract()).encode('ascii','ignore')
			tot_reviews = ''.join(r.xpath('div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/text()').extract()).encode('ascii','ignore')
			followers = ''.join(r.xpath('div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]/text()').extract()).encode('ascii','ignore')
			reviews = ''.join(r.xpath('div/div[3]/div/div[1]/div[1]/text()').extract()).strip().replace("\n","").encode('ascii','ignore')
			date = ''.join(r.xpath('div/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/a[1]/time/@datetime').extract()).strip().encode('ascii','ignore')
			#Dump in CSV (JSON recommended)
			with open('zomato8.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				data = [[id,name,phone,address,cost,hours,known,estab,cuisine,highlight,rev_name,tot_reviews,followers,date,reviews]]
				a.writerows(data)
		