""" Test access SWEPUB to see added Value Wikidata SWEPUB

    See Task https://phabricator.wikimedia.org/T216820
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import json

sparql = SPARQLWrapper("http://virhp07.libris.kb.se/sparql/")

sparql.setQuery("""
PREFIX bmc: <http://swepub.kb.se/bibliometric/model#> 
PREFIX swpa_m: <http://swepub.kb.se/SwePubAnalysis/model#>
PREFIX mods_m: <http://swepub.kb.se/mods/model#> 
PREFIX outt_m: <http://swepub.kb.se/SwePubAnalysis/OutputTypes/model#>
PREFIX xlink: <http://www.w3.org/1999/xlink#> 
SELECT DISTINCT xsd:string(?_orgName)
COUNT(DISTINCT ?_workID) as ?c 
?_pubYear
WHERE
{
?CreativeWork bmc:localID ?_workID .
?Publication bmc:localID ?_publicationID .

?Organization rdfs:label ?_orgName .
FILTER(lang(?_orgName) = 'sv' )

?CreativeWork bmc:reportedBy ?Record .
?CreativeWork a bmc:CreativeWork .
?CreativeWork bmc:publishedAs ?Publication .

?CreativeWork bmc:publicationYearEarliest ?_pubYear .
?CreativeWork bmc:hasCreatorShip ?CreatorShip .
?CreatorShip bmc:hasAffiliation ?CreatorAffiliation .
?CreatorAffiliation bmc:hasOrganization ?Organization .

?CreatorShip bmc:hasCreator ?Creator . 
}
ORDER BY xsd:string(?_orgName) ?_pubYear
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# for result in results["results"]["bindings"]:
#     print(result)
#print(results)

with open('data.json', 'w') as outfile:
    json.dump(results, outfile)
