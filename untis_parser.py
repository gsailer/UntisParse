# Untis Info Vertretungsplan Parser
# v 2.2
# written by @sublinus March 2017

import urllib
from datetime import date
from bs4 import BeautifulSoup
from json import JSONEncoder as jsonEncode

base_url = "http://www.akg-bensheim.de/akgweb2011/content/Vertretung/w/"
week = str(date.today().isocalendar()[1])

url = base_url + week + "/w00000.htm"

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
    
    def display(self):
	return "Klasse: {}\nDatum: {}\nStunde: {}\nArt: {}\nFach: {}\nRaum: {}\nKommentar: {}\n".format(self.klasse, self.datum, self.std, self.art, self.rpl_fach, self.rpl_room, self.comment)

def getVertretungsplan():
    try:
        vertretungsplan_request = urllib.urlopen(url)
        return vertretungsplan_request.read() 
    except Exception as e:
        return e

def parseVertretungsplan():
    doc = BeautifulSoup(getVertretungsplan(), "lxml")
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
                args.append(e.string.encode('utf-8'))        
            v = Vertretung(args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
            vertretungsplan.append(v)
    return vertretungsplan

# test case 
if __name__ == "__main__":
    vertretungsplan = parseVertretungsplan()
    vertretungsplan_by_klasse = sorted(vertretungsplan, key=lambda vertretung: vertretung.std)
    for x in vertretungsplan_by_klasse:
        if x.klasse == "K12":
    	   print x.display()