//Clear all
MATCH (n)
DETACH DELETE n

//Export RDF file
//Notice: N10s is conflict with APOC
:POST http://localhost:7474/rdf/crux-kb/cypher
{ "cypher" : "MATCH (n) RETURN n" , "format": "RDF/XML" }

//Example 1
MATCH (te:Testcard)-[:testedWith]-(d:Datacard)-[:canBeUsedTo]-(ta:Taskcard{taskName: "peak_finding"}),
      (s:Sample{sampleName: "BCdT - PT"})-[:extractedFrom]-(d)-[:ownedBy]-(c:Center{centerName: "NASA"}),
      (um:User)-[:createdBy]-(m:Modelcard)-[:dependOn]->(md:Modelcard{modelName: "peakutils.peak.index"}),
      (ta)-[:usedFor]-(te)-[:invoke]-(m),
      (ud:User)-[:uploadedBy]-(d),
      (te)-[:calculatedBy]-(p:Peaklist)
RETURN s, c, d, m, md, ta, te, um, ud, p

//Example 2
MATCH (te:Testcard)-[:testedWith]-(d:Datacard)-[:canBeUsedTo]-(ta:Taskcard{taskName: "peak_finding"}),
      (s:Sample{sampleName: "CaCO3-TiO2"})-[:extractedFrom]-(d)-[:ownedBy]-(c:Center{centerName: "North Carolina State University"}),
      (um:User)-[:createdBy]-(m:Modelcard),
      (ta)-[:usedFor]-(te)-[:invoke]-(m)-[:dependOn]->(md:Modelcard{modelName: "peakutils.peak.index"}),
      (ud:User)-[:uploadedBy]-(d),
      (te)-[:calculatedBy]-(p:Peaklist)
RETURN s, c, d, m, md, ta, te, um, ud, p LIMIT 15

// Generate input for GNN
MATCH (m:Modelcard)
RETURN m.id

MATCH (d:Datacard)
RETURN d.id

MATCH (m:Modelcard)-[r:testedWith]-(d:Datacard)
WHERE r.f1_score is not null
RETURN  m.id, d.id, r.runningTimes, r.f1_score, r.precision, r.recall

// Get the count for each node type
CALL apoc.meta.stats() YIELD labels
RETURN labels

// Get the count for each relation type
CALL apoc.meta.stats() YIELD relTypesCount
RETURN relTypesCount
