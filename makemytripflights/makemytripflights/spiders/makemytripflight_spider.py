from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import time
import functools
import re
import csv
count =0
links = []
class MakemytripSpider(Spider):
	name = "makemytripflight"
	allowed_domains = ["makemytrip.com"]
	start_urls = ["http://www.makemytrip.com/flights/browse-flights.html"]

	def parse(self, response):
		with open('url.csv') as fin:
			reader = csv.reader(fin)
			for row in reader:
				url = str(row[0])
				try:
					yield Request(url,functools.partial(self.table_parse,url = str(url)))
				except:
					print "Error"
	def table_parse(self, response,url):
		global links
		sel = Selector(response)
		table = sel.xpath('//*[@id="block-mmt_flt_schedule-flight_schedule_block"]/div/div/div[2]/p[@class="clearFix flt-dtls-row pad_row "]')
		
		for t in table:
			from_airport = ''.join(t.xpath('span[1]/span[1]/text()').extract())
			to_airport = ''.join(t.xpath('span[1]/span[3]/text()').extract())
			flight_operator = ''.join(t.xpath('span[3]/text()').extract()).strip()
			flight_name = flight_operator.split('(')[0].strip()
			flight_number = flight_operator.split('(')[1].replace(")","").strip()
			time = ''.join(t.xpath('span[4]/text()').extract())
			days = t.xpath('span[5]/span')
			days_of_travel = ""
			for d in days:
				day = ''.join(d.xpath('text()').extract())
				if "-" in day:
					days_of_travel+="N"
				else:
					days_of_travel+="Y"
			dur = ''.join(t.xpath('span[6]/text()').extract())
			duration=dur.split('&')[0].strip()
			stop = dur.split('&')[1].strip()
			link = ''.join(t.xpath('a/@onclick').extract()).replace("location.href =","").replace("'","").strip()
			print from_airport,to_airport,flight_name,flight_number,time,days_of_travel,duration,stop,link
			with open('seo_flights.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				data = [[from_airport,to_airport,flight_name,flight_number,time,days_of_travel,duration,stop,url,link]]
				a.writerows(data)

