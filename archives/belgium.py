__author__ = 'gregjan'
from collection import Collection
from bs4 import BeautifulSoup
from lxml import etree
import re

class BelgiumFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        tree = etree.parse("bel.xml")
        inventory = tree.getroot()
        nodes = ftext(inventory,inputs.strip())
        print("|"+str(inputs)+"|")
        print( len(nodes) )
        num = len(nodes)

        self.results_url = "/adsearch?general="+inputs
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self

def findresult(inputs):
    tree = etree.parse("bel.xml")
    inventory = tree.getroot()
    nodes = ftext(inventory,inputs['general'])
    return getresult(nodes)

# belgium
def getresult(nodes):
    result = {}
    results = []
    for node in nodes:
        result["id"] = node.get("number")
        result["type"] = node.get("type")
        result["quantity"] = node.get("quantity")
        result["date_range1"] = node.get("date_range1")
        result["date_range2"] = node.get("date_range2")
        result["date"] = xstr(result["date_range1"]) + " " + xstr(result["date_range2"])
        result["detail"] = " ".join(node.text.strip().replace("\n","").split()[1:])
        series = []
        lnote = node.xpath("../note")
        if len(lnote)>0:
             result["lnote"] = " ".join( lnote[0].text.strip().replace("\n","").split()[1:])
        for p in node.iterancestors("series"):
            series.append(p.get("title"))
        result["series"] = " -> ".join(series[::-1])
        for p in node.iterancestors("collection"):
            title = p.get("title")
            result["collection"] = title
            note = p.find(".//note")
            if note!=None:
                result["cnote"] = note.text.strip().replace("\n","")
        results.append(result)
        result={}
    nresults = sorted(results, key=lambda k: int(k['id']))
    return nresults

def ftitle(inventory,title):
    results = set()
    nodes = inventory.find(".//collection[@title='" + title + "']")
    for node in nodes.iter("item"):
        results.add(node)
    return results

def fseries(inventory,title):
    results = set()
    nodes = inventory.find(".//series[@title='" + title + "']")
    for node in nodes.iter("item"):
        results.add(node)
    return results

def fdate(inventory,date):
    results = set()
    date = int(date)
    for node in inventory.iter("item"):
        date1 = node.get("date_range1")
        date2 = node.get("date_range1")
        if date1 != None:
            lower = int(date1.split("-")[0])
            upper = int(date1.split("-")[1])
            if date<=upper and date >=lower:
                results.add(node)
                continue

        if date2 != None:
            lower = int(date2.split("-")[0])
            upper = int(date2.split("-")[1])
            if date<=upper and date >=lower:
                results.add(node)
                continue

    return results

def ftype(inventory,type):
    results = set()
    for node in inventory.iter("item"):
        if type == "other":
            if node.get("type") in ["part","object","report","printed", "printed parts"]:
                results.add(node)
        elif node.get("type") == type:
            results.add(node)
    return results

def ftext(inventory,text):
    results = set()
    for node in inventory.iter("item"):
        if re.match(r'.*'+text+'.*',node.text.replace('\n',' '),re.I):
            results.add(node)
    return results

def fname(inventory,name):
    results = set()
    for node in inventory.iter("item"):
        if node.get("name") != None:
            if name.lower() in node.get("name").lower():
                results.add(node)
    return results

# util
# deal with str(None)
def xstr(s):
    if s is None:
        return ''
    return str(s)
