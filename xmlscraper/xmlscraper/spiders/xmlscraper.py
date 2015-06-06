from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import html2text
import json
import time
import functools
import pickle
from selenium import webdriver
import re
import lxml.html as lh
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
act_count = 0
class TraveltexSpider(Spider):
	name = "xmlscraper"
	allowed_domains = [""]
	start_urls = ["file://127.0.0.1/home/rahul/routofy_spiders/xmlscraper/xmlscraper/spiders/useragentswitcher.xml"]
 	
	def parse(self, response):
		#response.selector.remove_namespaces()		
		sel = Selector(response)
		xxs = XmlXPathSelector(response)
		hxs = HtmlXPathSelector(response)
		folder = hxs.xpath('//useragentswitcher/folder')
		for f in folder:
			desc = ''.join(f.xpath('@description').extract())
			if desc == "Spiders - Search":
				continue
			if desc == "Miscellaneous":
				continue
			if desc == "UA List :: About":
				continue
			useragent = f.xpath('useragent')
			for u in useragent:
				listing_url = ''.join(u.xpath('@useragent').extract())
				url = "'"+listing_url+"'"
				with open(r'useragent.txt','a') as fp:
					fp.seek(0, 2)
					fp.write(url)
			legacy_folder = f.xpath('folder/useragent')
			for leg in legacy_folder:
				listing_url = ''.join(leg.xpath('@useragent').extract())
				url = "'"+listing_url+"'"
				with open(r'useragent.txt','a') as fp:
					fp.seek(0, 2)
					fp.write(url)