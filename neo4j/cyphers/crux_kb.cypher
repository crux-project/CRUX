//1/3 - Create index for each collection.
CREATE INDEX ON :Datacard(id);
CREATE INDEX ON :Modelcard(id);
CREATE INDEX ON :Taskcard(id);
CREATE INDEX ON :Testcard(id);
CREATE INDEX ON :Sample(id);
CREATE INDEX ON :User(id);
CREATE INDEX ON :Center(id);
CREATE INDEX ON :Peaklist(id);
CREATE INDEX ON :Instrument(id);


//2/3 - Load from JSON files and set properties.
// Datacard
WITH "file:/JSON/crux_datacard.json" AS url
CALL apoc.load.json(url) YIELD value AS data
MERGE (d:Datacard {id:data._id.`$oid`})
SET
d.dataLocation = data.dataContext.dataLocation,
d.centerName = data.dataContext.center.centerName,
d.contributorID = data.dataContext.contributor.userID.`$oid`,
d.instrumentID = data.dataContext.instrument.instrumentID.`$oid`,
d.centerID = data.dataContext.center.centerID.`$oid`,
d.sampleID = data.dataContent.sampleID.`$oid`,
d.tasks = [];
WITH "file:/JSON/crux_datacard.json" AS url
CALL apoc.load.json(url) YIELD value AS data
UNWIND data.analysis AS task
MERGE (d:Datacard {id:data._id.`$oid`})
SET d.tasks = d.tasks + task.`$oid`;

// Modelcard
WITH "file:/JSON/crux_modelcard.json" AS url
CALL apoc.load.json(url) YIELD value AS model
MERGE (m:Modelcard {id:model._id.`$oid`})
SET
m.modelName = model.modelContext.modelName,
m.modelLicense = model.modelContext.license,
m.contributorID = model.modelContext.contributor.userID.`$oid`,
m.trainingDataID = model.Modelcard.trainingData.dataID.`$oid`,
m.taskID = model.intendedTasks.taskID.`$oid`,
m.dependencyID = [];
WITH "file:/JSON/crux_modelcard.json" AS url
CALL apoc.load.json(url) YIELD value AS model
UNWIND keys(model.dependencies) AS depends
MERGE (m:Modelcard {id:model._id.`$oid`})
SET m.dependencyID = m.dependencyID + model.dependencies[depends].modelID.`$oid`;

// Taskcard
WITH "file:/JSON/crux_taskcard.json" AS url
CALL apoc.load.json(url) YIELD value as task
MERGE (ta:Taskcard {id:task._id.`$oid`})
SET ta.taskName = task.taskName;

// Testcard
WITH "file:/JSON/crux_testcard.json" AS url
CALL apoc.load.json(url) YIELD value as test
MERGE (te:Testcard {id:test._id.`$oid`})
SET
te.dataID = test.dataID.`$oid`,
te.modelID = test.modelID.`$oid`,
te.taskID = test.taskID.`$oid`,
te.f1_score = test.performance.F1_score,
te.output = test.output.peaklist.`$oid`;

// Sample
WITH "file:/JSON/crux_sample.json" AS url
CALL apoc.load.json(url) YIELD value as sample
MERGE (s:Sample {id:sample._id.`$oid`})
SET
s.sampleName = sample.sampleName,
s.centerID = sample.centerID.`$oid`;

// User
WITH "file:/JSON/crux_user.json" AS url
CALL apoc.load.json(url) YIELD value AS user
MERGE (u:User {id:user._id.`$oid`})
SET
u.username = user.username,
u.centerID = [];
WITH "file:/JSON/crux_user.json" AS url
CALL apoc.load.json(url) YIELD value AS user
UNWIND user.affiliation AS center
MERGE (u:User {id:user._id.`$oid`})
SET u.centerID = u.centerID + center.`$oid`;
WITH "file:/JSON/crux_user.json" AS url
CALL apoc.load.json(url) YIELD value AS user
UNWIND user.instrument AS instrument
MERGE (u:User {id:user._id.`$oid`})
SET u.instrumentID = u.instrumentID + instrument.`$oid`;

// Center
WITH "file:/JSON/crux_center.json" AS url
CALL apoc.load.json(url) YIELD value as center
MERGE (c:Center {id:center._id.`$oid`})
SET c.centerName = center.centerName;
WITH "file:/JSON/crux_center.json" AS url
CALL apoc.load.json(url) YIELD value as center
UNWIND center.instrument AS instrument
MERGE (c:Center {id:center._id.`$oid`})
SET c.instrumentID = c.instrumentID + instrument.`$oid`;

// Peaklist
WITH "file:/JSON/crux_peaklist.json" AS url
CALL apoc.load.json(url) YIELD value as peaklist
MERGE (p:Peaklist {id:peaklist._id.`$oid`})
SET
p.testID = peaklist.testID.`$oid`,
p.sampleID = peaklist.sampleID.`$oid`;

// Instrument
WITH "file:/JSON/crux_instrument.json" AS url
CALL apoc.load.json(url) YIELD value as instrument
MERGE (i:Instrument {id:instrument._id.`$oid`})
SET
i.instrumentName = instrument.instrumentName;


//3/3 - Create relations.
// test-model
MATCH (te:Testcard), (m:Modelcard)
WHERE te.modelID = m.id
CREATE (te)-[:invoke]->(m);

// test-task
MATCH (te:Testcard), (t:Taskcard)
WHERE te.taskID = t.id
CREATE (te)-[:usedFor]->(t);

// test-data
MATCH (te:Testcard), (d:Datacard)
WHERE te.dataID = d.id
CREATE (te)-[:testedWith]->(d);

// test-peaklist
MATCH (te:Testcard), (p:Peaklist)
WHERE te.output = p.id
CREATE (p)-[:calculatedBy]->(te);

// data-user
MATCH (d:Datacard), (u:User)
WHERE d.contributorID = u.id
CREATE (d)-[:uploadedBy]->(u);

// data-center
MATCH (d:Datacard), (c:Center)
WHERE d.centerID = c.id
CREATE (d)-[:ownedBy]->(c);

// data-sample
MATCH (d:Datacard), (s:Sample)
WHERE d.sampleID = s.id
CREATE (d)-[:extractedFrom]->(s);

// data-task
MATCH (d:Datacard), (ta:Taskcard)
WHERE ta.id in d.tasks
CREATE (d)-[:canBeUsedTo]->(ta);

// model-user
MATCH (m:Modelcard), (u:User)
WHERE m.contributorID = u.id
CREATE (m)-[:createdBy]->(u);

// model-task
MATCH (m:Modelcard), (ta:Taskcard)
WHERE m.taskID = ta.id
CREATE (m)-[:usedFor]->(ta);

// model-data
MATCH (m:Modelcard), (d:Datacard)
WHERE m.trainingDataID = d.id
CREATE (m)-[:trainedWith]->(d);

// model-model
MATCH (m1:Modelcard), (m2:Modelcard)
WHERE m1.id in m2.dependencyID
CREATE (m1)<-[:dependOn]-(m2);

// user-center
MATCH (u:User), (c:Center)
WHERE c.id in u.centerID
CREATE (u)-[:affiliatedTo]->(c);

// sample-center
MATCH (s:Sample), (c:Center)
WHERE s.centerID = c.id
CREATE (s)-[:ownedBy]->(c);

// peaklist-sample
MATCH (p:Peaklist), (s:Sample)
WHERE p.sampleID = s.id
CREATE (p)-[:isPropertyOf]->(s);

// instrument-user
MATCH (i:Instrument), (u:User)
WHERE i.id in u.instrumentID
CREATE (i)-[:UsedBy]->(u);

// instrument-data
MATCH (i:Instrument), (d:Datacard)
WHERE d.instrumentID = i.id
CREATE (i)-[:appliedTo]->(d);

// instrument-center
MATCH (i:Instrument), (c:Center)
WHERE i.id in c.instrumentID
CREATE (i)-[:UsedBy]->(c);
