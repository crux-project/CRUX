//1. LOAD all cards(nodes)
//load dataCard
WITH "file:/crux_datacard.json" AS url
CALL apoc.load.json(url) YIELD value
CREATE (d:data {id:value._id.`$oid`})
SET d.contributorName = value.dataContext.contributors.username,
d.dataLocation = value.dataContext.dataLocation,
d.centerName = value.dataContext.center.centerName,
d.authorName = value.dataContent.header.author.name,
d.taskID = value.analysis.task_1.taskID;

//load modelCard
WITH "file:/crux_modelcard.json" AS url
CALL apoc.load.json(url) YIELD value
CREATE (m:model {id: value._id.`$oid`})
SET m.modelName = value.modelContext.modelName,
m.modelLicense = value.modelContext.license,
m.modelLocation = value.modelContext.modelLocation,
m.taskID = value.intendedUse.intendedTasks.taskID.`$oid`,
m.dataID = value.trainingData.dataID.`$oid`,
m.modelID = value.dependencies.modelID.`$oid`,
m.dependencies = [];
WITH "file:/crux_modelcard.json" AS url
CALL apoc.load.json(url) YIELD value
WITH value AS val
UNWIND keys(val.dependencies) AS depends
MERGE (m:model {id: val._id.`$oid`})
SET m.dependencies = m.dependencies + val.dependencies[depends].modelID.`$oid`;

//load taskCard
WITH "file:/crux_taskcard.json" AS url
CALL apoc.load.json(url) YIELD value
CREATE (t:task {id:value._id.`$oid`})
SET t.taskName = value.taskName;

//load testCard
WITH "file:/crux_testcard.json" AS url
CALL apoc.load.json(url) YIELD value
CREATE (te:test {id:value._id.`$oid`})
SET te.dataID = value.dataID.`$oid`,
te.modelID = value.modelID.`$oid`,
te.taskID = value.taskID.`$oid`,
te.f1_score = value.performance.F1_score,
te.outputLocation = value.outputLocation