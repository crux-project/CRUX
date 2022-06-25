//Clear all
MATCH (n)
DETACH DELETE n

//Export RDF file
//Notice: N10s is conflict with APOC
:POST http://localhost:7474/rdf/crux-kb/cypher
{ "cypher" : "MATCH (n) RETURN n" , "format": "RDF/XML" }
