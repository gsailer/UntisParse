#!/usr/bin/env python
#
# Untis Info Vertretungsplan Parser
# v 2.1
# written by @sublinus October 2015

import urllib
from datetime import date
from bs4 import BeautifulSoup
from json import JSONEncoder as jsonEncode
# for debug decorator
from functools import wraps

year = date.today().year
month = date.today().month
day = date.today().day
week = str(date(year, month, day).isocalendar()[1])
base_url = "http://www.akg-bensheim.de/akgweb2011/content/Vertretung/w/"
 
url = base_url + week + "/w00000.htm"
#### debug decorator ####
def d(fn):
    @wraps(fn)
    def wrapper(*v, **k):
        print "DEBUG"
        print "Function: %s" %fn.__name__
        print "Arguments Given: %s %s" %(v, k)
        return fn(*v, **k)
    return wrapper
########

class Vertretung(object):
    def __init__(self, klasse, datum, std, art, fach, rpl_fach, room, rpl_room, comment):
        self.klasse = klasse
        self.datum = datum
        self.std = std
        self.art = art
        self.fach = fach
        self.rpl_fach = rpl_fach
        self.room = room
        self.rpl_room = rpl_room
        self.comment = comment

def getVertretungsplan():
    try:
        vertretungsplan_request = urllib.urlopen(url)
        return vertretungsplan_request.read()
 
    except Exception as e:
        return e

doc = BeautifulSoup(getVertretungsplan()) 
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

vertretungsplan = []

for i in range(1,max_rows):
    tr = doc.select("tr:nth-of-type(" + str(i) +")")
    for element in tr:
        td = element.select("td.list")
        if len(td) <= 0:
            continue
        args = []
        for e in td:
            if e.string is "":
                args.append(" ")
            else:        
                args.append(e.string)
        
        v = Vertretung(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
        vertretungsplan.append(v)
# test case 
klassen = []        
for x in vertretungsplan:
    if x.klasse in klassen:
        continue
    klassen.append(x.klasse)

for x in klassen:
    print x
