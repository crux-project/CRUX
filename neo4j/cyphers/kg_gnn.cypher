//1/3 - Create index for each collection.
CREATE INDEX ON :Datacard(id);
CREATE INDEX ON :Modelcard(id);
CREATE INDEX ON :Testcard(id);


//2/3 - Load from JSON files and set properties.
// Datacard
WITH "file:/JSON/crux_datacard.json" AS url
CALL apoc.load.json(url) YIELD value AS data
MERGE (d:Datacard {id:data._id.`$oid`})
SET
d.dataLocation = data.dataContext.dataLocation,
d.centerName = data.dataContext.center.centerName,
d.contributorID = data.dataContext.contributor.userID.`$oid`,
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

// Testcard
WITH "file:/JSON/crux_testcard.json" AS url
CALL apoc.load.json(url) YIELD value as test
MERGE (te:Testcard {id:test._id.`$oid`})
SET
te.dataID = test.dataID.`$oid`,
te.modelID = test.modelID.`$oid`,
te.taskID = test.taskID.`$oid`,
te.runningTimes = test.performance.`runningTime(s)`,
te.f1_score = test.performance.`F1_score`,
te.precision = test.performance.precision,
te.recall = test.performance.recall,
te.output = test.output.peaklist.`$oid`;

//3/3 - Create relations.
// model-data
MATCH (m:Modelcard), (d:Datacard), (te:Testcard)
WHERE te.modelID = m.id AND te.dataID = d.id
CREATE (m)-[:testedWith{runningTimes:te.runningTimes, f1_score:te.f1_score, precision:te.precision, recall:te.recall}]->(d);

