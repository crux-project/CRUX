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
      (s:Sample{sampleName: "CaCO3-TiO2"})-[:extractedFrom]-(d)-[:ownedBy]-(c:Center{centerName: "NC-State"}),
      (um:User)-[:createdBy]-(m:Modelcard),
      (ta)-[:usedFor]-(te)-[:invoke]-(m)-[:dependOn]->(md:Modelcard{modelName: "peakutils.peak.index"}),
      (ud:User)-[:uploadedBy]-(d),
      (te)-[:calculatedBy]-(p:Peaklist)
RETURN s, c, d, m, md, ta, te, um, ud, p LIMIT 15
