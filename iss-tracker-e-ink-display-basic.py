#!/usr/bin/python3
#RaspberryConnect.com
#ISS Tracking for e-ink display
#
#Iss tracking data from http://open-notify.org/Open-Notify-API/ISS-Location-Now/
#
#then nearest city list in the file worldcities_lonlat.csv
#is supplied by https://simplemaps.com/data/world-cities
#
#see Readme file for more information.

import json, urllib.request, time #used for getting the locations
from haversine import haversine, Unit #used to calculate nearest location
import csv						#used to load the world locations list
from PIL import Image, ImageDraw,ImageFont #image library
import traceback				#e-ink driver
from inky import InkyPHAT


def iss_long_lat():
    """Get the ISS data from the tracking API"""
    url = "http://api.open-notify.org/iss-now.json"
    details = urllib.request.urlopen(url)
    result = json.loads(details.read())
    loc =result["iss_position"]
    lat = loc["latitude"]
    lon = loc["longitude"]
    return lon,lat

def dist(start,end):
    x = haversine(start,end)
    return x

def getGeoData():
    """Load city long lat list"""
    with open('/home/pi/isstracker/worldcities_lonlat.csv','r') as f:
        l = csv.reader(f)
        cities = list(l)
    return cities

def CalcLoc(data,sz,iss):
    """Go through city list to find the closest destination to the ISS"""
    country = ""
    city = ""
    citydist = 0
    mindist = 99999999
    for i in range(sz):
        d = dist((float(data[i][2]),float(data[i][3])),(float(iss[1]),float(iss[0])))
        if d < mindist:
            city = data[i][0]
            country = data[i][5]
            citydist = d
            mindist = d
    return (country,city,round(citydist,2))

def updateeink(issdetails,mapdot,trail):
    """update location text and map to the e-ink screen"""
    issx = int(mapdot[0])
    issy = int(mapdot[1])   
    inky_display = InkyPHAT("yellow")

    palette = [255,255,255,
               0,0,0,
              255,0,0]

    font10 = ImageFont.truetype('/home/pi/isstracker/FreeSans.ttf', 10)
    font14 = ImageFont.truetype('/home/pi/isstracker/FreeSans.ttf', 14)
    font16 = ImageFont.truetype('/home/pi/isstracker/FreeSans.ttf', 16)
    font18 = ImageFont.truetype('/home/pi/isstracker/FreeSans.ttf', 18)


    im = Image.open('/home/pi/isstracker/small-world-map.png')
    d = ImageDraw.ImageDraw(im)

    taille_pt = 3
    isspos = (int(mapdot[0])-taille_pt,int(mapdot[1])-taille_pt,int(mapdot[0])+taille_pt,int(mapdot[1])+taille_pt)
    d.ellipse(isspos,fill = 2)
    for item in point2ellipse(trail,1): 
        d.ellipse(item,fill = 2)

    d.text((3,80), 'à ' + str(round(issdetails[2])) + ' Km de ' + issdetails[1] + ' ('+ issdetails[0] + ')', font = font18, fill = 2)


    from uptime import uptime
    uptime = round(uptime()/60,1)
    d.text((0,70), "ut : "+str(uptime)+ " min",  font = font10, fill = 1)




    inky_display.set_image(im)
    inky_display.show()

def point2ellipse(trail,size):
    #draw an ellipse of size size on the given points
    #(int(mapdot[0])-taille_pt,int(mapdot[1])-taille_pt,int(mapdot[0])+taille_pt,int(mapdot[1])+taille_pt)
    a=[]
    for item in trail:
        a.append( (int(item[0])-size,int(item[1])-size,int(item[0])+size,int(item[1])+size)  )
    return(a) 

def mapdot(self):
    #position of red dot on mini map
    #scale long lat coords to 120 x 60 image
    x = round((float(self[0])+180)/(360/212))
    y = round((180-(float(self[1])+90))/(180/103))
    return [x,y]

def main():
    geodata = getGeoData() #Global city Longitude & Latidude list
    geosz = len(geodata) #get total rows in list
    trail = []        #list to display trail
    while True:
        iss_lola = iss_long_lat() #Current Iss location
        loc = CalcLoc(geodata,geosz,iss_lola) #Closest City/Town
        mapxy = mapdot(iss_lola)
        if len(trail) >= 60: #length of trail in points
            trail.pop(0) 
        #add new red dot coords to trail list.
        trail.append((int(mapxy[0]),int(mapxy[1])))
        #print(trail)
        updateeink(loc,mapxy,trail)
        time.sleep(180) #wait 3 minutes

if __name__== '__main__':
    try:
        main()
    except: #if the screen fails to initiate exit
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()
