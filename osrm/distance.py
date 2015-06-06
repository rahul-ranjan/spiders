#########################################################
#This script calculates distance between two            #
#cities using osrm                                      #
#                                                       #
#Author:- Rahul                                         #
#########################################################


import simplejson
import urllib2
import csv
from csv import DictReader, DictWriter
def get_location():
    loc_dict = {}
    fin_loc = open('lat_long.csv')
    reader = csv.reader(fin_loc)
    for row in reader:
        loc_dict[row[0].lower()] = row[1]+','+row[2]
    fin_loc.close()
    return loc_dict

if __name__ == "__main__":
    
    geo_loc = get_location()
    count=0
    with open('city_pair.csv') as fin1:
    	reader1 = DictReader(fin1)
        for line1 in reader1:
            driving_time=0
            driving_distance=0
            loc1=""
            loc2=""
            try:
            	loc1=geo_loc[line1['City1'].lower()]
            except: print "Lat Long Not Available "+line1['City1']
            try:
            	loc2=geo_loc[line1['City2'].lower()]
            except: 
                with open('error.csv', 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [[line1['City1'],line1['City2']]]
                    a.writerows(data)
            try:        
                url = "http://localhost:5000/viaroute?loc="+str(loc1)+"&loc="+str(loc2)
                result = simplejson.load(urllib2.urlopen(url))
            except:
                with open('error.csv', 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [[line1['City1'],line1['City2']]]
                    a.writerows(data)
            try:
            	driving_time = result['route_summary']['total_time']
            	driving_distance = result['route_summary']['total_distance']
            except: 
            	count+=1
            	print "No routes found"+str(count)
                with open('error.csv', 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [[line1['City1'],line1['City2']]]
                    a.writerows(data)
            print "Distance between "+line1['City1']+" to "+line1['City2']+ " = "+str(driving_distance)
            print "Travel Time between "+line1['City1']+" to "+line1['City2']+ " = "+str(driving_time)
            if driving_distance !=0:
                with open('distances.csv', 'a') as fp:
    			    a = csv.writer(fp, delimiter=',')
    			    data = [[line1['City1'],line1['City2'],driving_distance,driving_time]]
    			    a.writerows(data)
            else:
                with open('error.csv', 'a') as fp:
                    a = csv.writer(fp, delimiter=',')
                    data = [[line1['City1'],line1['City2']]]
                    a.writerows(data)

