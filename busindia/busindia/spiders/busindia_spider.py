from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import json
import time
import functools
import re
import csv
from busindia.cityinfo import cityinfo
count = 0
c1 = 0
c2 = 0
c3=0
class BusIndiaSpider(Spider):
	name = "busindia"
	#download_delay = 2
	allowed_domains = ["busindia.com"]
	start_urls = ["http://www.busindia.com/bus/"]


	def parse(self, response):
		#response.selector.remove_namespaces()
		global count	
		with open('busIndia_citypair.csv') as fin1:
			reader1 = csv.reader(fin1)
			for row in reader1:
				city1 = row[0].upper()
				city2 = row[1].upper()
				placeID1 = ""
				placeID2= ""
				placeCode1 = ""
				placeCode2 = ""
				placeName1 = ""
				placeName2 = ""
				placeIDAndCodeAndPlaceName1 = ""
				placeIDAndCodeAndPlaceName2 = ""
				searchPlaceName1 = ""
				searchPlaceName2 = ""
				try:
					#print cityinfo(city1,city2)
					data1,data2 = cityinfo(city1,city2)
					placeID1,placeCode1,placeName1,placeIDAndCodeAndPlaceName1,searchPlaceName1 = data1.split(".")
					placeID2,placeCode2,placeName2,placeIDAndCodeAndPlaceName2,searchPlaceName2 = data2.split(".")
				except:
					print "Er"
				try:
					if placeID1 != "" and placeID2 != "" and placeCode1 != "" and placeCode2 != "":
						#print placeID1,placeCode1,placeName1,placeIDAndCodeAndPlaceName1,searchPlaceName1
						#print placeID2,placeCode2,placeName2,placeIDAndCodeAndPlaceName2,searchPlaceName2
						yield FormRequest(url="http://www.busindia.com/bus/busBooking_Availability", method="POST", formdata={'radOnewayOrReturnTrip':'0', 'matchFromPlace':placeName1,'matchToPlace':placeName2,'radBookingType':'BUS','txtOnwardDate':'04/02/2015','selectFromPlace':placeID1,'selectToPlace':placeID2,'selectCategory':'0','selectCorp':'0','selectOnwardTimeSlab':'	00:00-23:59','selectReturnTimeSlab':'00:00-23:59','hiddenBusAdvSearchFlag':'N','hiddenCurrentDate':'31/01/2015','hiddenFromPlaceCode':placeCode1,'hiddenFromPlaceID':placeID1,'hiddenFromPlaceInfo':placeIDAndCodeAndPlaceName1,'hiddenFromPlaceName':placeName1,'hiddenJourneyType':'O','hiddenMaxNoOfPassengers':'16','hiddenMaxValidReservDate':'27/02/2015','hiddenOnwardJourneyDate':'04/02/2015','hiddenOnwardSearchDay':'J','hiddenOnwardTimeSlab':'00:00-23:59','hiddenReturnSearchDay':'J','hiddenToPlaceCode':placeCode2,'hiddenToPlaceID':placeID2,'hiddenToPlaceInfo':placeIDAndCodeAndPlaceName2,'hiddenToPlaceName':placeName2,'hiddenTotalPassengers':'1','txtReturnDate':'DD/MM/YYYY'}, callback=functools.partial(self.data_parse,city1=city1,city2 = city2))
				except:
					print "Data is not available"+city1+"-"+city2
					
	
	def data_parse(self,response,city1,city2):
		sel = Selector(response)
		global c1,c2,c3
		print "###############"+city1,city2
		c3+=1
		print "Total : "+str(c3)
		error = ''.join(sel.xpath('/html/body/form/div[4]/div/div[3]/div[3]/div[3]/text()').extract())
		print error
		#time.sleep(5)
		if (error == "Onward Services are not available on this date." or error == "Direct Onward Services are not available for the selected date. Please choose a Stopover above for additional services."):
			c2+=1
			pass
			#city_err1 = ''.join(sel.xpath('//*[@id="maindiv"]/div[1]/b[1]/text()').extract())
			#city_err2 = ''.join(sel.xpath('//*[@id="maindiv"]/div[1]/b[2]/text()').extract())
			#print "Error: "+city_err1+"-"+city_err2+":"+str(c2)
		else:
			buses = sel.xpath('/html/body/form/div[4]/div/div[3]/div[3]/div')
			#print response.body
			for b in buses:
				bus_id = ""
				bus_id = b.xpath('div/ul/li[1]/span/text()').extract()
				if bus_id:
					corporation_name = ""
					departure_date = ""
					departure_time = ""
					arrival_time = ""
					arrival_date = ""
					bus_type = ""
					bus_route_via = ""
					total_time = ""
					fare = ""
					c1+=1
					cit1 = ""
					cit2 = ""
					cit1 = ''.join(sel.xpath('/html/body/form/div[4]/div/div[3]/div[3]/div[1]/b[1]/text()').extract())
					cit2 = ''.join(sel.xpath('/html/body/form/div[4]/div/div[3]/div[3]/div[1]/b[2]/text()').extract())
					#print cit1,cit2	
					corporation_name = ''.join(b.xpath('div/ul/li[1]/span/text()').extract())
					departure_date = ''.join(b.xpath('div/ul/li[2]/span[1]/text()').extract())
					departure_time = ''.join(b.xpath('div/ul/li[2]/span[2]/text()').extract())
					arrival_date = ''.join(b.xpath('div/ul/li[3]/span[1]/text()').extract())
					arrival_time = ''.join(b.xpath('div/ul/li[3]/span[2]/text()').extract())
					bus_type = ''.join(b.xpath('div/ul/li[4]/span[1]/text()').extract())
					bus_route_via = ''.join(b.xpath('div/ul/li[4]/span[2]/text()').extract())
					total_time = ''.join(b.xpath('div/ul/li[4]/text()').extract()).replace("\n","").replace("\t","").strip()
					fare = ''.join(b.xpath('div/ul/li[5]/span/span[2]/text()').extract())
					if corporation_name != "" and fare !="":
						with open('busindia_wednesday.csv', 'a') as fp:
							#print city1,city2,corporation_name,departure_date,departure_time,arrival_date,arrival_time,bus_type,bus_route_via,total_time,fare
							a = csv.writer(fp, delimiter=',')
							data = [[city1,city2,corporation_name,departure_date,departure_time,arrival_date,arrival_time,bus_type,bus_route_via,total_time,fare]]
							a.writerows(data)
					else:
						print "Error In : "+city1+" to "+city2
		#print "Schedules dumped : "+str(c1)
