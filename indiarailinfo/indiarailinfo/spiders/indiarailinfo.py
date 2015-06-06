from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
import time
import functools
import re
import csv
count =0
temp = "0"
all_link = []
class IndiaRailInfoSpider(Spider):
	name = "indiarailinfo"
	allowed_domains = ["indiarailinfo.com"]
	start_urls = ["http://indiarailinfo.com/trains"]


	def parse(self, response):
		url = "http://indiarailinfo.com/train/timetable/"
		for x in range(27767):
			hello = ""
			try:
				#print url
				link = url+str(x)
				yield Request(hello,functools.partial(self.data_parse,link = str(link)))
			except:
				print "Error"

	def data_parse(self,response,link):
		global count
		count+=1         
		sel = Selector(response)
		service = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[2]/div[1]/text()').extract()).encode('ascii','ignore').strip()
		if service == "IMAGINARY Train, created by":
			pass
		elif service == "This Train is NOT YET INTRODUCED. TT/other details MAY CHANGE" :
			pass 
		elif service == "TRAIN IS CANCELLED":
			pass
		else:
			#print service
			train_number = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[2]/h1/span[1]/text()').extract())
			train_name = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[2]/h1/span[2]/text()').extract())
			'''train_number,train_name = train.split("/")
			try:
				new_num = train_number.split(u"\u21d2")
				#print "###############"
				#print new_num
				train_number = new_num[1].strip()
			except:
				print "No new train num"'''
			'''if "-" in train_number:
				train_number = train_number.split("-")[0].strip()'''
			print train_number
			print train_name
			loc_dict = {}
			fin_loc = open('wrong_train.csv')
			reader = csv.reader(fin_loc)
			for row in reader:
				loc_dict[row[0].lower().strip()] = row[0]
			fin_loc.close()
			if train_number.lower().strip() in loc_dict:
				try:
					pantry = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[3]/div[3]/div/div[1]/div/text()[1]').extract()).encode('ascii','ignore').strip()
					#print pantry
					if pantry == "NO Pantry CarNO Catering":
						pantry = "NO Pantry Car"
						catering = "NO Catering"
					elif pantry == "Pantry Car AvblCatering Avbl":
						pantry = "Pantry Car Avbl"
						catering = "Catering Avbl"
					else:
						catering = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[3]/div[3]/div/div[1]/div/text()[2]').extract()).encode('ascii','ignore').strip()
					#print catering
					rake_composition = " "
					rake_composition = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[3]/td[2]/div[6]/div/text()').extract())
					if ";" in rake_composition:
						rake_composition = rake_composition.split(";")[0].strip()
					elif ".." in rake_composition:
						rake_composition =rake_composition.split("..")[0].strip()
					#print rake_composition
				except:
					print "No pantry"
				train_type = ''.join(sel.xpath('//*[@id="Div"]/div[4]/table/tr[2]/td[1]/div[1]/span/text()').extract()).strip()
				try:
					other_info = ''.join(sel.xpath('//*[@id="Div"]/div[2]/table/tr[5]/td/text()').extract()).strip()
					#print other_info
					if not other_info:
						other_info = " "
				except:
					print "No other info"
				days_of_travel = ""
				days = sel.xpath('//*[@id="Div"]/div[4]/table/tr[2]/td[2]/table/tr/td/text()').extract()
				global temp
				for d in days:
					#tot_days = ''.join(d.xpath('td/text()').extract()).encode('ascii','ignore')
					#print tot_days
					if ''.join(d).encode('ascii','ignore') != "":
						days_of_travel += "Y"
					else:
						days_of_travel += "N"
				table = sel.xpath('//*[@id="Div"]/div[5]/table/tr/td/div/table/tr')
				for t in table:
					stn = ''.join(t.xpath('@stn').extract())
					if stn:
						if(stn != temp):
							temp = stn
							arrival_time = ""
							stop_number = ''.join(t.xpath('td[1]/text()').extract()).strip()
							station_code = ''.join(t.xpath('td[3]/a/span/text()').extract()).strip()
							if not station_code:
								station_code = ''.join(t.xpath('td[3]/a/text()').extract()).strip()
								if not station_code:
									station_code = ''.join(t.xpath('td[3]/a/b/text()').extract())
							try:
								name = ''.join(t.xpath('td[4]/a/span/text()').extract()).strip().encode('ascii','ignore')
							except:
								pass
							if not name:
								try:
									name = ''.join(t.xpath('td[4]/a/text()').extract()).strip().encode('ascii','ignore')
								except:
									pass
								if not name:
									name = ''.join(t.xpath('td[4]/a/b/text()').extract()).encode('ascii','ignore')
							st_n = name.split("(")
							station_name = st_n[0].strip()
							xing_over = ''.join(t.xpath('td[5]/span/text()').extract()).strip()
							arrival_time = ''.join(t.xpath('td[7]/text()').extract()).replace("\"","").strip()
							if arrival_time == "":
								arrival_time = ''.join(t.xpath('td[7]/b/text()').extract()).replace("\"","").strip()
							arr_avg_delay = ''.join(t.xpath('td[8]/span/text()').extract()).strip()
							if not arr_avg_delay:
								arr_avg_delay = ''.join(t.xpath('td[8]/text()').extract()).strip()
							departure_time = ''.join(t.xpath('td[9]/text()').extract()).strip()
							if not departure_time:
								departure_time = ''.join(t.xpath('td[9]/b/text()').extract()).strip()
							dep_avg_delay = ''.join(t.xpath('td[10]/span/text()').extract()).strip()
							if not dep_avg_delay:
								dep_avg_delay = ''.join(t.xpath('td[10]/text()').extract()).strip()
							halt_time = ''.join(t.xpath('td[11]/text()').extract()).strip()
							if not halt_time:
								halt_time = ''.join(t.xpath('td[11]/b/text()').extract()).strip()
							platform = ''.join(t.xpath('td[12]/text()').extract()).strip()
							day_number = ''.join(t.xpath('td[13]/text()').extract()).strip()
							distance = ''.join(t.xpath('td[14]/text()').extract()).strip()
							if not distance:
								distance = ''.join(t.xpath('td[14]/span/text()').extract()).strip()
							speed = ''.join(t.xpath('td[15]/text()').extract()).strip()
							elevation = ''.join(t.xpath('td[16]/text()').extract()).strip()
							zone = ''.join(t.xpath('td[17]/text()').extract()).strip()
							address = ''.join(t.xpath('td[18]/text()').extract()).strip()
							#print "hello"
							print train_number,train_name,pantry,catering,rake_composition,train_type,other_info,days_of_travel,stop_number,station_code,station_name,xing_over,arrival_time,arr_avg_delay,departure_time,dep_avg_delay,halt_time,day_number,platform,distance,speed,elevation,zone,address
							with open('train_schedules.csv', 'a') as fp:
								a = csv.writer(fp, delimiter=',')
								data = [[train_number,train_name,train_type,days_of_travel,stop_number,station_code,station_name,arrival_time,arr_avg_delay,departure_time,dep_avg_delay,halt_time,day_number,platform,distance,pantry,catering,speed,elevation,zone,address,rake_composition,other_info,xing_over]]
								a.writerows(data)
