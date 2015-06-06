from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import time
import functools
import re
import csv
count = ""
class ErailPriceSpider(Spider):
	name = "erailprice"
	allowed_domains = ["erail.in"]
	start_urls = ["http://www.erail.in"]

	def parse(self, response):
		#response.selector.remove_namespaces()
		#url = "http://www.erail.in/rail/getTrainRoute2.aspx?TrainID="
		#print response.body
		fin1 = csv.reader(open("rail_error.csv", "rb"))
		for array in fin1:
			first_item = ""
			second_item = ""
			train_number = array[4]
			from_station = array[13]
			to_station = array[14]
			try:
				yield Request("http://erail.in/data.aspx?Action=GetTrainFare&train="+train_number+"&from="+from_station+"&to="+to_station+"&adult=1&child=0&sfemale=0&smale=0",functools.partial(self.latlng_parse,train_number=str(train_number),from_station=str(from_station),to_station=str(to_station)))
			except:
				print "Error"

	def latlng_parse(self,response,train_number,from_station,to_station):
		sel = Selector(response)
		table1 = sel.xpath('/html/body/div[1]/table/tr')
		table1_header = sel.xpath('/html/body/div[1]/table/tr[1]/th/text()').extract()
		table1_adultfare = sel.xpath('/html/body/div[1]/table/tr[2]/td/b/text()').extract()
		adult_fare_list = ['0','@','0','@','0','@','0','@','0','@','0','@','0','@','0','@','0']
		for x in range(0,len(table1_header)):
			#fares = table1_header[x]+"@"+table1_adultfare[x].replace(",","")
			try:
				if table1_header[x].strip() == "1A":
					adult_fare_list[0] = table1_adultfare[x].replace(",","")
			except:
				print "1A error"
			try:
				if table1_header[x].strip() == "2A":
					adult_fare_list[2] = table1_adultfare[x].replace(",","")
			except:
				print "2A error"
			try:
				if table1_header[x].strip() == "FC":
					adult_fare_list[4] = table1_adultfare[x].replace(",","")
			except:
				print "FC error"
			try:
				if table1_header[x].strip() == "3A":
					adult_fare_list[6] = table1_adultfare[x].replace(",","")
			except:
				print "3A error"
			try:
				if table1_header[x].strip() == "3E":
					adult_fare_list[8] = table1_adultfare[x].replace(",","")
			except:
				print "3E error"
			try:
				if table1_header[x].strip() == "CC":
					adult_fare_list[10] = table1_adultfare[x].replace(",","")
			except:
				print "CC error"
			try:
				if table1_header[x].strip() == "SL":
					adult_fare_list[12] = table1_adultfare[x].replace(",","")
			except:
				print "SL error"
			try:
				if table1_header[x].strip() == "2S":
					adult_fare_list[14] = table1_adultfare[x].replace(",","")
			except:
				print "2S error"
			try:
				if table1_header[x].strip() == "GN":
					#print "hello"
					adult_fare_list[16] = table1_adultfare[x].replace(",","")
			except:
				print "GN Error"
			#print table1_adultfare[x]
		#print table1_header,table1_adultfare
		'''with open('fares.csv', 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			data = [[train_number,from_station,to_station,''.join(fare_list)]]
			a.writerows(data)
			fp.close()'''
		#1A@2A@FC@3A@3E@CC@SL@2S@GN
		table2 = sel.xpath('/html/body/div[2]/table/tr')
		table2_header = sel.xpath('/html/body/div[2]/table/tr[1]/th/text()').extract()
		_1A = "1A,0,0,0,0,0,0"
		_2A = "2A,0,0,0,0,0,0"
		_FC = "FC,0,0,0,0,0,0"
		_3A = "3A,0,0,0,0,0,0"
		_3E = "3E,0,0,0,0,0,0"
		_CC = "CC,0,0,0,0,0,0"
		_SL = "SL,0,0,0,0,0,0"
		_2S = "2S,0,0,0,0,0,0"
		_GN = "GN,0,0,0,0,0,0"
		all_fare_list = []
		for t in table2:
			price = t.xpath('td')
			fares = []
			for p in price:
				prices = ''.join(p.xpath('b/text()').extract())
				if not prices:
					no_info = ''.join(p.xpath('text()').extract())
					if "-" in no_info:
						prices = "-"
				if prices != "":
					fares.append(prices)
			if fares != []:
				#print fares
				#print "hello"
				all_fare_list.append(fares)
		#print all_fare_list
		for x in range(0,len(table2_header)):
			train_class = ''.join(table2_header[x])
			for f in range(0,len(all_fare_list)):
				train_class += ","+all_fare_list[f][x].replace(",","").replace("-","0")
			#print ''.join(train_class)
			try:
				if "1A" in train_class:
					_1A = train_class
			except:
				print "1A error"
			try:
				if "2A" in train_class:
					_2A = train_class
			except:
				print "2A error"
			try:
				if "FC" in train_class:
					_FC = train_class
			except:
				print "FC error"
			try:
				if "3A" in train_class:
					_3A = train_class
			except:
				print "3A error"
			try:
				if "3E" in train_class:
					_3E = train_class
			except:
				print "3E error"
			try:
				if "CC" in train_class:
					_CC = train_class
			except:
				print "CC error"
			try:
				if "SL" in train_class:
					_SL = train_class
			except:
				print "SL error"
			try:
				if "2S" in train_class:
					_2S = train_class
			except:
				print "2S error"
			try:
				if "GN" in train_class:
					_GN = train_class
			except:
				print "GN Error"
		with open('fares.csv', 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			data = [[train_number,from_station,to_station,''.join(adult_fare_list),_1A,_2A,_FC,_3A,_3E,_CC,_SL,_2S,_GN]]
			a.writerows(data)
			fp.close()
		#print all_fare_list
		'''temp = ""
		for ax in all_fare_list:
			temp += ''.join(ax)+","
		with open('fares.csv', 'a') as fp:
	            a = csv.writer(fp, delimiter=',')
	            data = [[train_number,from_station,to_station,''.join(adult_fare_list),''.join(temp)]]
	            a.writerows(data)'''

		'''if count != header:

			if table_header:
				header = t.xpath('text()')
				print header
			if not train_class:
					continue
			#adult_price = t.xpath("td"+"["+i+"]"+"/text()").re(r'\d+')
			adult_price = t.xpath("td/text()").re(r'\d+')
			if not adult_price:
				continue
			child_price = t.xpath("td/text()").re(r'\d+')
			if not child_price:
			adult_tatkal_price = t.xpath("td/text()").re(r'\d+')
			child_tatkal_price = t.xpath("td/text()").re(r'\d+')
			senior_female_price = t.xpath("td/text()").re(r'\d+')
			senior_male_price = t.xpath("td/text()").re(r'\d+')
			i+=1
			table_header = t.xpath('th')
			h = []
			for s in table_header:
				train_class = ''.join(s.xpath('text()').extract())
				if not train_class:
					continue
				else:
					h.append(train_class)
			prices = t.xpath('td')
			for p in prices:
				fares = t.xpath('text()').re(r'\d+')
				if not fares:
					continue
				else:
					for x in h:

			tot = 
			print train_class,fare
			with open('erail_latlong.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				data = [[station_code,lat,lng,station_name]]
				a.writerows(data)
			count=0
			s2=[]'''
