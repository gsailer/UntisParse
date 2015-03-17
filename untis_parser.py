#!/usr/bin/env python
#
# Untis Info Vertretungsplan Parser
# written by @neo_hac0x March 2015

import urllib
from datetime import date
from bs4 import BeautifulSoup
from json import JSONEncoder as jsonEncode
 
year = date.today().year
month = date.today().month
day = date.today().day
week = str(date(year, month, day).isocalendar()[1])
base_url = "http://www.akg-bensheim.de/akgweb2011/content/Vertretung/w/"
 
url = base_url + week + "/w00000.htm"

def getVertretungsplan():
    try:
        vertretungsplan_request = urllib.urlopen(url)
        return vertretungsplan_request.read()
 
    except Exception as e:
        return e

def strike(lst, field):
    strk = lst.select("strike")
    for s in strk:
        vertretung[field] = s.string
        print "STRIKE!"
 
def encodeandlog(data, filename):
    jsonData = jsonEncode().encode(data)
    with open(filename, "w") as f:
        f.write(jsonData)
 
doc = BeautifulSoup(getVertretungsplan())
 
vertretung_root = {}
max_rows = len(doc.find_all("tr"))
 
for i in range(1,max_rows):
    tr = doc.select("tr:nth-of-type(" + str(i) +")")
    vertretung = {}
    for element in tr:
        td = element.select("td.list")
        i = 0
        for e in td:
            i = i+1
            #DEBUG: print str(i) + " " + e.string
 
            if i == 1:
                if "---" in e.string:
                    strike(e, "klasse")
                else:
                    vertretung["klasse"] = e.string
            elif i == 2:
                if "---" in e.string:
                    strike(e, "datum")
                else:
                    vertretung["datum"] = e.string
            elif i == 3:
                if "---" in e.string:
                    strike(e, "stunden")
                else:
                    vertretung["stunden"] = e.string
            elif i == 4:
                if "---" in e.string:
                    strike(e, "art")
                else:
                    vertretung["art"] = e.string
            elif i == 5:
                if "---" in e.string:
                    strike(e, "verFach")
                else:
                    vertretung["verFach"] = e.string
            elif i == 6:
                if "---" in e.string:
                    strike(e, "fach")
                else:
                    vertretung["fach"] = e.string
            elif i == 7:
                if "---" in e.string:
                    strike(e, "verRaum")
                else:
                    vertretung["verRaum"] = e.string
            elif i == 8:
                if "---" in e.string:
                    strike(e, "raum")
                else:
                    vertretung["raum"] = e.string
            elif i == 9:
                if "---" in e.string:
                    strike(e, "comment")
                else:
                    vertretung["comment"] = e.string
                # Write the gathered data for one class to the dict
                vertretung_root[vertretung["klasse"].encode('UTF-8')] = vertretung
            else:
                print "[!] Something went wrong."
 
encodeandlog(vertretung_root, "vertretung.json")
 
#DEBUG: print vertretung_root