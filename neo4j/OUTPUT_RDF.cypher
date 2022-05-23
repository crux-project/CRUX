//OUTPUT RDF
:POST http://localhost:7474/rdf/neo4j/cypher
{ "cypher" : "MATCH (n) RETURN n LIMIT 10" , "format": "RDF/XML" }