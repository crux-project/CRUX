CALL apoc.periodic.iterate(
"LOAD CSV WITH HEADERS FROM 'file:///kg.csv' AS row RETURN row",
"MERGE (x {index: toInteger(row.x_index)})
ON CREATE SET x.id_source = row.x_id, x.name = row.x_name, x.source = row.x_source
WITH x, row
CALL apoc.create.addLabels(id(x), [row.x_type]) YIELD node AS xNode
WITH xNode, row
MERGE (y {index: toInteger(row.y_index)})
ON CREATE SET y.id_source = row.y_id, y.name = row.y_name, y.source = row.y_source
WITH xNode, y, row
CALL apoc.create.addLabels(id(y), [row.y_type]) YIELD node AS yNode
WITH xNode, yNode, row
CALL apoc.create.relationship(xNode, row.display_relation, {}, yNode) YIELD rel
RETURN count(row)”,
{batchSize:1000, parallel:true, iterateList:true} 
)

Q1: Exploring off-label uses of drugs for hypertension
MATCH (d:drug)-[:`off-label use`]->(disease:disease {name: "hypertension"})
RETURN d, disease;

Q2: Exploring side effects of hypertension drugs
MATCH (d:drug)-[:indication]->(:disease {name: "hypertension"})
MATCH (d)-[:`side effect`]->(e:`effect/phenotype`)
RETURN d.name AS Drug, COLLECT(e.name) AS SideEffects

Q3: Identifying drugs not recommended for Hypertension patients and also target a specific gene/protein named "DRD5"
MATCH (d:drug)-[:contraindication]->(:disease {name: "hypertension"})
MATCH (d)-[:target]->(g:`gene/protein`)
RETURN di, d, g
