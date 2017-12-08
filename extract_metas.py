# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 22:00:42 2017

@author: Lully

Constitution et retraitement des données pour constituer une base de catalogues de vente
Source : données de la BnF

"""

from SPARQLWrapper import SPARQLWrapper, JSON


def req2results(urlroot, req):
    sparql = SPARQLWrapper(urlroot)
    sparql.setQuery(req)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
    print(result["label"]["value"])
    

if __name__ == '__main__':
    url= "http://data.bnf.fr/sparql"
    request = """PREFIX frbr-rda: <http://rdvocab.info/uri/schema/FRBRentitiesRDA/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            select ?manif ?contribURI ?titre where {
              ?manif a frbr-rda:Manifestation;
                dcterms:title ?titre;
                rdarelationships:expressionManifested ?expression.
            ?expression owl:sameAs ?expr.
              ?expr dcterms:contributor ?contribURI.
              ?contribURIFOAF owl:sameAs ?contribURI.
              ?contribURIFOAF a foaf:Organization.
              ?contribURIFOAF foaf:name ?orgName
              FILTER contains(?titre, "vente")
            }
            
            LIMIT 50
            """
    req2results(url,request)