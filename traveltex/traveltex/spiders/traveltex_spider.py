from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from urlparse import urljoin
import html2text
import json
import pickle
from selenium import webdriver
import lxml.html as lh
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import time
from selenium import selenium
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
city = []
city_url = ""
s = 0
class TraveltexSpider(Spider):
	name = "traveltex"
	allowed_domains = ["traveltex.com"]
	start_urls = ["http://www.traveltex.com/cities-regions/"]
 	def __init__(self):
        	self.driver = webdriver.Firefox()
	def parse(self, response):
		global city
		file_name = "city"
		fobj = open(file_name,'r')
		city=pickle.load(fobj)
		#print city[0]
		fobj.close()
		i=0	
		#print "City: "+str(i+1)
		global city_url
		print "City Name: "+str(city[0])
		for c in city:
			city_url = "http://www.traveltex.com/cities/"+c+"/activities/"
			#yield Request(city_url, self.parse_city)
			
			#get_url =self.driver.get(city_url)	
			self.driver.find_element_by_id("ContentPlaceHolderDefault_cp_content_CitiesBinding_4_btnViewall").click()
			time.sleep(5)
			html=self.driver.page_source
			doc = lh.fromstring(html)
			division = doc.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_CitiesBinding_4_up1"]/div[2]/div')
			#print html
			for d in division:
			 i+=1
			 print "Count: "+str(i)	
			 activity_name = ''.join(d.xpath('h3/a/text()')).encode("ascii","ignore")
			 #print activity_name
			 activity_name=activity_name.lower()
			 activity_name=activity_name.replace("'","")
			 #activity_name=activity_name.replace("","")
			 activity_name=activity_name.replace("& ","")
			 activity_name=activity_name.replace("&","")
			 activity_name=activity_name.replace(",","")
			 activity_name=activity_name.replace("/","")
			 activity_name=activity_name.replace("`","")
			 activity_name=activity_name.replace("(","")
			 activity_name=activity_name.replace(")","")
			 activity_name=activity_name.replace('"',"")
			 activity_name=activity_name.replace("!","")
			 activity_name=activity_name.replace(".","")
			 activity_name=activity_name.replace(" ","-")
			 print "From list(selenium): "+activity_name
			 activity_url = "http://www.traveltex.com/activities/"+activity_name+"/"
			 yield Request(activity_url, self.parse_activity)
		
	def parse_activity(self, response):
		global s		
		s+=1
		print "In Parse: "+str(s)
		#print "Parse Call"+str(s)		

		sel = Selector(response)
		base_url = "www.traveltex.com"
		#sites = sel.xpath('//div')
		description_text = ""
		activity_name = ''.join(sel.xpath('//*[@itemprop="name"]/text()').extract())
		print "Inside parse : "+activity_name
		city_region = ''.join(sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_regionName"]/text()').extract()).encode('ascii','ignore')
		#print city_region		
		city_name = ''.join(sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_CityName"]/text()').extract()).encode('ascii','ignore')
		#print city_name
		description = sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_lblDescription"]/p')
		for desc in description:
			description_text += ''.join(desc.xpath('text()').extract()).encode('ascii','ignore')
			activity_url = ''.join(desc.xpath('a/@href').extract()).encode('ascii','ignore')
		#print description_text
		#print activity_url
		places_url =""
		places = sel.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[2]/div/div[2]/ul/li')
		for place in places:
			places_name = ''.join(place.xpath('strong/span/text()').extract()).encode('ascii','ignore')
			places_url_relative = ''.join(place.xpath('a/@href').extract()).encode('ascii','ignore')
			if places_url_relative:
			 places_url = base_url + places_url_relative
			 #print places_name
			 #print places_url
		likes_suggestion = sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_UcRecomendations_8_dlPages"]/tr/td')
		for like in likes_suggestion:
			likes_name = ''.join(like.xpath('span/span/text()').extract()).encode('ascii','ignore')
			likes_category = ''.join(like.xpath('p/span[1]/text()').extract()).encode('ascii','ignore')
			likes_city = ''.join(like.xpath('p/span[3]/text()').extract()).encode('ascii','ignore')
			likes_url_relative = ''.join(like.xpath('a/@href').extract()).encode('ascii','ignore')
			likes_url = base_url + likes_url_relative
			#print "Likes name: "+likes_name
			#print "Likes Category: "+likes_category
			#print "Likes city: "+likes_city
			#print "Likes url: "+likes_url
		activities_addr = ""
		activities_strt_addr = ''.join(sel.xpath('//*[@class="street"]/text()').extract()).encode('ascii','ignore')
		activities_strt_rgn = ''.join(sel.xpath('//*[@itemprop="addressRegion"]/text()').extract()).encode('ascii','ignore')
		activities_addr = activities_strt_addr + " " + activities_strt_rgn
		#print activities_addr
		activities_phone = ''.join(sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_lblPhone"]/text()').extract()).encode('ascii','ignore')
		activities_tollfree = ''.join(sel.xpath('//*[@class="tollfree"]/text()').extract()).encode('ascii','ignore')
		activities_phone_number = activities_phone + ","+activities_tollfree
		#print activities_phone_number
		activity_category = ''.join(sel.xpath('//*[@id="ContentPlaceHolderDefault_cp_content_UcActivity_4_ucRecentVisitedPages_9_dlPages_lblPassionpoint_0"]/text()').extract()).encode('ascii','ignore')
		#print activity_category	 
