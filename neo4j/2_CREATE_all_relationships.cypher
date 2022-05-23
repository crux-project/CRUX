//2. CREATE all relationships
// test-model 
MATCH (te:test), (m:model)
WHERE te.modelID = m.id
CREATE (te)-[:invoke]->(m);

// test-task
MATCH (te:test), (t:task)
WHERE te.taskID = t.id
CREATE (te)-[:usedFor]->(t);

// test-data
MATCH (te:test), (d:data)
WHERE te.dataID = d.id
CREATE (d)<-[r1:testedWith]-(te);

// model-model
MATCH (m1:model), (m2:model)
WHERE m1.id in m2.dependencies
CREATE (m1)<-[:dependOn]-(m2);