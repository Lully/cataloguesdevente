# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 22:00:42 2017

@author: Lully

Constitution et retraitement des données pour constituer une base de catalogues de vente
Source : données de la BnF

"""

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
from urllib import request, parse
from lxml import etree

ns = {"srw":"http://www.loc.gov/zing/srw/", "mxc":"info:lc/xmlns/marcxchange-v2", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


def record2field(record,field):
    tag = field[0:3]
    subfields = []
    result = []
    if (field.find("$")>-1):
        subfields = field.split("$")[1:]
    xpathf = f"//mxc:datafield[@tag='{tag}']"
    for field in record.xpath(xpathf,namespaces=ns):
        for subf in subfields:
            xpaths = f"mxc:subfield[@code='{subf}']"
            for sub in field.xpath(xpaths,namespaces=ns):
                result.append(sub.text)
    result = "~".join(result)
    return result
                
        

def check143(manif):
    query = parse.quote(f'bib.persistentid all "{manif}"')
    url = f'http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query={query}&recordSchema=intermarcxchange&maximumRecords=20&startRecord=1'
    #print(url)
    record = etree.parse(request.urlopen(url))
    f143a = record2field(record,"143$a")
    f143b = record2field(record,"143$b")
    f143j = record2field(record,"143$j")
    f143d = record2field(record,"143$d")
    f143m = record2field(record,"143$m")
    return [f143a,f143b,f143j,f143d,f143m]

def req2results(urlroot, req):
    
    sparql = SPARQLWrapper(urlroot)
    sparql.setQuery(req)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        manif = result["manif"]["value"]
        orgURI = result["orgURI"]["value"]
        orgName = result["orgName"]["value"]
        title = result["title"]["value"]
        manif = manif.replace("http://data.bnf.fr/","")
        [f143a,f143b,f143j,f143d,f143m] = check143(manif)
        if (f143a != ""):
            print(manif)
            print([f143a,f143b,f143j,f143d,f143m])
    

if __name__ == '__main__':
    url= "http://data.bnf.fr/sparql"
    req = """PREFIX frbr-rda: <http://rdvocab.info/uri/schema/FRBRentitiesRDA/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            select distinct ?manif ?orgURI ?orgName ?title where {
              ?manif a frbr-rda:Manifestation;
                dcterms:title ?title;
                rdarelationships:expressionManifested ?expression.
            ?expression owl:sameAs ?expr.
              ?expr dcterms:contributor ?orgURI.
              ?orgURIFOAF owl:sameAs ?orgURI.
              ?orgURIFOAF a foaf:Organization.
              ?orgURIFOAF foaf:name ?orgName
              FILTER contains(?title, "vente")
            }
            
            LIMIT 500
            """
    req2results(url,req)