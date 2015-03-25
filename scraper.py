import sys

html = open(sys.argv[1]).read()

from bs4 import BeautifulSoup
h = BeautifulSoup(html)

val_fixes = {
    # Type declaration
    "dctypes:Dataset" : ["(dctypes:Dataset)"],
    
    # Type declaration
    "void:Dataset or dcat:Distribution" :
        ["(void:Dataset)", "(dcat:Distribution)"],
    
    # Date created
    "rdfs:Literal encoded using the relevant ISO 8601 Date and Time compliant string and typed using the appropriate XML Schema datatype": ["."],
    
    # Language
    "http://lexvo.org/id/iso639-3/{tag}": ["."],
    
    # Concept descriptors
    "IRI of type skos:Concept": ["IRI"],
    
    # Update frequency
    "IRI of type dctypes:Frequency": ["IRI"],
    
    # Distribution description
    "IRI of Distribution Level description": ["IRI"],
    
    # File format
    "IRI or xsd:String": ["."]
    
}

prop_fixes = {
    # Other dates
    "pav:createdOn or pav:authoredOn or pav:curatedOn":
        ["###BROKEN FIX ME###"],
    
    # Contributors
    "dct:contributor or or pav:createdBy or pav:authoredBy or pav:curatedBy" : 
        ["dct:contributor", "pav:createdBy", "pav:authoredBy", "pav:curatedBy"],
    
    # Data source provenance
    "dct:source or pav:retrievedFrom or prov:wasDerivedFrom":
        ["dct:source","pav:retrievedFrom","prov:wasDerivedFrom"]
}

SummaryLevelShape = 0
VersionLevelShape = 1
DistributionLevelShape = 2

def get_shex(elem, lev, prop, val):
    rule = "\n\t#" + elem + "\n"
    rule += "\t`" + lev + "` "
    if("NOT" in lev):
        rule += "!"
    rule += prop + " "
    rule += val
    rule += ";"
    print rule

def get_shape(shape):
    for row in h.find_all("tr")[1:]:

        cols = row.find_all("td")

        if(len(cols) < 6):
            print "\n\n#" + cols[0].get_text().strip()
            continue

        elem = cols[0].get_text().strip()
        lev = cols[3 + shape].get_text().strip()
        prop = cols[1].get_text().strip()
        val = cols[2].get_text().strip()

        if(prop in prop_fixes):
            for fix in prop_fixes[prop]:
                get_shex(elem, lev, fix, val)
            continue

        if(val in val_fixes):
            for fix in val_fixes[val]:
                get_shex(elem, lev, prop, fix)
            continue

        if(val and " " not in val and " " not in prop):
            get_shex(elem, lev, prop, val)

        else:
            get_shex(elem, lev, "###SORT THIS OUT###", "###SORT THIS OUT###")

print """
PREFIX cito: <http://purl.org/spar/cito/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dctypes: <http://purl.org/dc/dcmitype/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX freq: <http://purl.org/cld/freq/>
PREFIX idot: <http://identifiers.org/idot/>
PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
PREFIX pav: <http://purl.org/pav/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schemaorg: <http://schema.org/>
PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX void-ext: <http://ldf.fi/void-ext#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""
print "<SummaryLevelShape> {"
get_shape(SummaryLevelShape)
print "}\n\n<VersionLevelShape> {"
get_shape(VersionLevelShape)
print "}\n\n<DistributionLevelShape> {"
get_shape(DistributionLevelShape)
print "}"

    
