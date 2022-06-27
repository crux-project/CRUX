//Clear all
MATCH (n)
DETACH DELETE n

//Export RDF file
//Notice: N10s is conflict with APOC
:POST http://localhost:7474/rdf/crux-kb/cypher
{ "cypher" : "MATCH (n) RETURN n" , "format": "RDF/XML" }

//Example
MATCH (te:Testcard)-[:testedWith]-(d:Datacard)-[:canBeUsedTo]-(ta:Taskcard{taskName: "peak_finding"}),
      (s:Sample{sampleName: "BCdT - PT"})-[:extractedFrom]-(d)-[:ownedBy]-(c:Center{centerName: "NASA"}),
      (um:User)-[:createdBy]-(m:Modelcard)-[:dependOn]->(md:Modelcard{modelName: "peakutils.peak.index"}),
      (ta)-[:usedFor]-(te)-[:invoke]-(m),
      (ud:User)-[:uploadedBy]-(d),
      (te)-[:calculatedBy]-(p:Peaklist)
RETURN s, c, d, m, md, ta, te, um, ud, p
