import sys
from bs4 import BeautifulSoup

table = BeautifulSoup(open(sys.argv[1]).read())

val_fixes = {
    # Type declaration
    "dctypes:Dataset" :
        "(dctypes:Dataset)",
    
    # Type declaration
    "void:Dataset or dcat:Distribution" :
        "(void:Dataset, dcat:Distribution)",
    
    # Date created
    "rdfs:Literal encoded using the relevant ISO 8601 Date and Time compliant string and typed using the appropriate XML Schema datatype":
        ".",
    
    # Language
    "http://lexvo.org/id/iso639-3/{tag}":
        ".",
    
    # Concept descriptors
    "IRI of type skos:Concept":
        "IRI",
    
    # Update frequency
    "IRI of type dctypes:Frequency":
        "IRI",
    
    # Distribution description
    "IRI of Distribution Level description": 
        "IRI",
    
    # File format
    "IRI or xsd:String":
        "."   
}

prop_fixes = {
    # Other dates
    "pav:createdOn or pav:authoredOn or pav:curatedOn":
        "###BROKEN FIX ME###",
    
    # Contributors
    "dct:contributor or or pav:createdBy or pav:authoredBy or pav:curatedBy" : 
        "(dct:contributor, pav:createdBy, pav:authoredBy, pav:curatedBy)",
    
    # Data source provenance
    "dct:source or pav:retrievedFrom or prov:wasDerivedFrom":
        "(dct:source, pav:retrievedFrom, prov:wasDerivedFrom)"
}

cardinality_fixes = {
    ("dct:license", "IRI"):"+",
    ("dct:creator", "IRI"):"+",
    ("(dct:contributor, pav:createdBy, pav:authoredBy, pav:curatedBy)", "IRI"):"+",
    ("dcat:keyword", "xsd:string"): "+",
    ("dct:rights", "xsd:string"): "+",
    ("dct:references", "IRI"): "+",
    ("dcat:theme", "IRI"): "+",
    ("dct:conformsTo", "IRI"): "+",
    ("cito:citesAsAuthority", "IRI"): "+",
    ("dct:hasPart", "IRI"): "+"
}

shapes = {
    "SummaryLevelShape": 0,
    "VersionLevelShape": 1,
    "DistributionLevelShape": 2
}


def get_shex(elem, lev, prop, val, cardinality):
    rule = "\n    #" + elem + "\n"
    rule += "    `" + lev + "` "
    if("NOT" in lev):
        rule += "!"
    rule += prop + " "
    rule += val
    rule += cardinality
    rule += ";"
    print rule

def get_shape(shape):
    print "<" + shape + "> {"
    for row in table.find_all("tr")[1:]:
        
        cols = row.find_all("td")

        if(len(cols) < 6):
            print "\n\n  #" + cols[0].get_text().strip()
            continue

        elem = cols[0].get_text().strip()
        lev = cols[3 + shapes[shape]].get_text().strip()
        prop = cols[1].get_text().strip()
        val = cols[2].get_text().strip()
        cardinality = ""

        if(prop in prop_fixes):
            prop = prop_fixes[prop]

        if(val in val_fixes):
            val = val_fixes[val]
            
        if((prop, val) in cardinality_fixes):
            cardinality = cardinality_fixes[(prop, val)]
            

        if(val and prop):
            get_shex(elem, lev, prop, val, cardinality)

        else:
            get_shex(elem, lev, "###SORT THIS OUT###", "###SORT THIS OUT###")
    print "}\n"

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

get_shape("SummaryLevelShape")
get_shape("VersionLevelShape")
get_shape("DistributionLevelShape")

    
