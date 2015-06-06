from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import BaseSpider, Rule
from scrapy.http import Request
from austintexas.items import AustintexasItem
import html2text
import json
import time
import functools
import pickle
import re
import lxml.html as lh
act_count = 0
class TraveltexSpider(Spider):
	name = "austintexas"
	allowed_domains = ["austintexas.org"]
	start_urls = ["http://www.austintexas.org/sitemap.xml"]
 	
	def parse(self, response):
		#response.selector.remove_namespaces()		
		sel = Selector(response)
		xxs = XmlXPathSelector(response)
		hxs = HtmlXPathSelector(response)
		listing_url = hxs.xpath('//urlset/url/loc/text()').re(r'http://www.austintexas.org/listings/.*')
		#print listing_url
		fobj = open("url",'wb')
		pickle.dump(listing_url,fobj)
		fobj.close()
		fobj = open("url",'r')
		urls=pickle.load(fobj)
		fobj.close()
		for url in urls:
			try:	yield Request(str(url),functools.partial(self.listing_parse,url=str(url)))
			except: print "Exception caught in"+str(url)
	def listing_parse(self, response, url):
		global act_count
		item = AustintexasItem()		
		sel = Selector(response)
		hxs = HtmlXPathSelector(response)
		listing_info = {}		
		listing_name = ''.join(sel.xpath('//*[@id="sv-bodyContainer"]/div[1]/div[2]/div[1]/h1/text()').extract()).replace(".","")
		print listing_name
		address = (''.join(sel.xpath('//*[@id="sv-bodyContainer"]/div[1]/div[2]/div[1]/ul/li[1]/text()').extract())).replace("\n","").replace("\t","").replace("\r","")
		print "Address: "+address
		listing_info.update({"Address":address})
		tele_number = ""
		tele_key = ""
		tollfree_key = ""
		tollfree_num = ""
		fax_key = ""
		fax_num = ""
		website = ""		
		info_details = sel.xpath('//*[@id="sv-bodyContainer"]/div[1]/div[2]/div[1]/ul/li')
		for info in info_details:
			tele_key = ''.join(info.xpath('span[1]/text()').extract())
			if tele_key == "Tel:":
				tele_key = tele_key.replace(":","")
				print tele_key
				tele_number = ''.join(info.xpath('text()[2]').extract()).replace("\n","").replace("\t","").replace("\r","")
				print tele_number
				tollfree_key = ''.join(info.xpath('span[2]/text()').extract()).replace(":","")
				print tollfree_key
				tollfree_num = (''.join(info.xpath('text()[3]').extract())).replace("\n","").replace("\t","").replace("\r","")
				print tollfree_num
				if not tollfree_key:
					listing_info.update({tele_key:tele_number})
				else:
					listing_info.update({tele_key:tele_number,tollfree_key:tollfree_num})
			fax_key = ''.join(info.xpath('span/text()').extract())
			if fax_key == "Fax:":
				fax_key = fax_key.replace(":","")
				print fax_key
				fax_num = ''.join(info.xpath('text()').extract()).replace("\n","").replace("\t","")
				print fax_num
				listing_info.update({fax_key:fax_num})
			#Condition to be matched in website
			website_key = ''.join(info.xpath('a/text()').extract())
			if website_key =="Website":
				website = ''.join(info.xpath('a/@href').extract())
				print website_key+": "+website
				listing_info.update({website_key:website})
		details_section = sel.xpath('//*[@id="sv-bodyContainer"]/div[1]/div[2]/div[4]/div/div')
		details = ""
		meeting_facility_html = ""
		events_html = ""
		details_dict = {}
		amenities_dict = {}
		print "####################################################"
		for detail in details_section:
			details_id = ''.join(detail.xpath('@id').extract())
			if details_id == "detailsPane":
				details_key = "Details"
				details = ''.join(detail.xpath('p/text()').extract()).encode('ascii','ignore').replace("\r","").replace("\n","")
				print "Details: "+details
				print "####################################################"
				details_dict.update({details_key:details})
			elif details_id == "amenitiesPane":
				amenities_list = sel.xpath('//*[@id="amenitiesPane"]/ul/li')
				amenities_key = "Amenities"
				for amenity in amenities_list:		
					sub_amenity_key = ''.join(amenity.xpath('a/text()').extract())
					print "Amenities: "+sub_amenity_key
					amenity_id = ''.join(amenity.xpath('a/@href').extract()).replace("#","")
					amenity_id = "listing_detail_"+amenity_id
					#print "Amenities id: "+amenity_id
					amenities_details = sel.xpath('//*[@id="listing_detail_subtab"]/div')
					for amenities in amenities_details:
						details_id = ''.join(amenities.xpath('@id').extract())							
						if details_id == amenity_id:
							#print "Details id: "+details_id
							xpathid = '//*[@id="listing_detail_subtab"]/div[@id="'+str(details_id)+'"]'
							amenity_details = (hxs.xpath(xpathid).extract()[0]).encode('ascii','ignore')
							amenities_html = html2text.html2text(amenity_details)
							print amenities_html
							print "####################################################"
							amenities_dict.update({sub_amenity_key:amenities_html})
				details_dict.update({amenities_key:amenities_dict})
			elif details_id == "meetingfacilitiesPane":
				#meeting_facility = detail.xpath('node()').extract()
				meeting_key = "Meeting Facilities"
				meeting_facility = (hxs.xpath('//*[@id="meetingfacilitiesPane"]').extract()[0]).encode('ascii','ignore')
				meeting_facility_html = html2text.html2text(meeting_facility)
				print meeting_facility_html
				print "####################################################"
				details_dict.update({meeting_key:meeting_facility_html})
			elif details_id == "eventsPane":
				events_key = "Events"
				events = (hxs.xpath('//*[@id="eventsPane"]').extract()[0]).encode('ascii','ignore')
				events_html = html2text.html2text(events)
				print events_html
				print "####################################################"
				details_dict.update({events_key:events_html})
			elif details_id == "specialoffersPane":
				special_offer_key = "Special Offers"
				special_offer = (hxs.xpath('//*[@id="specialoffersPane"]').extract()[0]).encode('ascii','ignore')
				special_offer_html = html2text.html2text(special_offer)
				print special_offer_html
				print "####################################################"
				details_dict.update({special_offer_key:special_offer_html})

		data={}
		listing_all = {}
		listing_all.update(details_dict)
		listing_all.update(listing_info)
		data.update({listing_name:listing_all})
	 	dict_main={}
	    dict_main={"_source":"austintexas.org","_url":url,"_attempt_time":time.time(),"_title":listing_name,"_data":data} 
		fobj = open("/home/rahul/cognitive/austintexas/austintexas/spiders/listings/"+listing_name.replace("/","")+str(act_count)+".json",'a',0)		
		json.dump(dict_main,fobj)
		act_count+=1	
		print "Listings Record Added : "+str(act_count)
		fobj.close()











