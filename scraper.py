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

def get_shex(elem, lev, prop, val):
    rule = "\n\t#" + elem + "\n"
    rule += "\t`" + lev + "` "
    if("NOT" in lev):
        rule += "!"
    rule += prop + " "
    rule += val
    rule += ";"
    print rule

for row in h.find_all("tr")[1:]:
    
    cols = row.find_all("td")
    
    if(len(cols) < 6):
        print "\n\n#" + cols[0].get_text().strip()
        continue
    
    elem = cols[0].get_text().strip()
    lev = cols[3].get_text().strip()
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
    
