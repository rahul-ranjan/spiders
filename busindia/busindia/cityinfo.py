import csv
from csv import DictReader, DictWriter
import json

def cityinfo(city1,city2):
		place1 = ""
		place2 = ""
		with open("bus_India.json") as fhandle:
			content = fhandle.read()
			x=json.loads(content)
			placeID1 = ""
			placeName1 =""
			placeCode1 = ""
			placeIDAndCodeAndPlaceName1=""
			searchPlaceName1=""
			placeID2 = ""
			placeName2 = ""
			placeCode2= ""
			placeIDAndCodeAndPlaceName2=""
			searchPlaceName2=""
			place_name=x["fromPlaceList"]
			for place in place_name:
				if place["placeName"] == city1:
					placeID1 = place['placeID'].replace("\t","")
					placeCode1 = place['placeCode'].replace("\t","")
					placeName1 = place['placeName'].replace("\t","")
					placeIDAndCodeAndPlaceName1 = place['placeIDAndCodeAndPlaceName'].replace("\t","")
					searchPlaceName1 = place['searchPlaceName'].replace("\t","")
					place1 = placeID1+"."+placeCode1+"."+placeName1+"."+placeIDAndCodeAndPlaceName1+"."+searchPlaceName1
	        	else:
	        		placeID1 = ""
	        		placeName1 =""
	        		placeCode1 = ""
	        		placeIDAndCodeAndPlaceName1=""
	        		searchPlaceName1=""
	        for place in place_name:
	        	if place["placeName"] == city2:
	        		placeID2 = place['placeID'].replace("\t","")
	        		placeCode2 = place['placeCode'].replace("\t","")
	        		placeName2 = place['placeName'].replace("\t","")
	        		placeIDAndCodeAndPlaceName2 = place['placeIDAndCodeAndPlaceName'].replace("\t","")
	        		searchPlaceName2 = place['searchPlaceName'].replace("\t","")
	        		place2 = placeID2+"."+placeCode2+"."+placeName2+"."+placeIDAndCodeAndPlaceName2+"."+searchPlaceName2
	        	else:
					placeID2 = ""
					placeName2 = ""
					placeCode2= ""
					placeIDAndCodeAndPlaceName2=""
					searchPlaceName2=""
		#print place1
		#print place2
		#if placeID1 != "" and placeID2 != "":
		return place1,place2