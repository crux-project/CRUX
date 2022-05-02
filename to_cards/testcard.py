import pymongo
import utils
import sys
import os
import time

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def test_card(schema, task_name):
    task = db.taskcard.find_one({'taskName': task_name})
    num = 0

    for datacard in db["datacard"].find():
        num += 1
        for modelcard in db["modelcard"].find(
                {"intendedUse.intendedTasks.taskName": task_name}):
            card = utils.json2dic(schema)
            card["taskID"] = task["_id"]
            card["dataID"] = datacard["_id"]
            card["modelID"] = modelcard["_id"]

            input = datacard["dataContext"]["dataLocation"]
            model = modelcard["modelContext"]["modelLocation"]
            model_name = model.split('/')[-1][:-3]
            output = input.replace("data", "test/" + model_name, 1)[:-6] + ".txt"
            command = "python3 " + model + " \"" + input + "\" \"" + output + "\""

            print(str(num) + ". " + input)
            start = time.time()
            os.system(command)
            end = time.time()
            rt = end - start
            card["performance"]["runningTime(s)"] = rt

            card["outputLocation"] = output
            utils.import_to_mongodb(card, "testcard")


def main():
    schema = "../ontology/schemas/test_card.json"
    task = sys.argv[1]
    test_card(schema, task)


if __name__ == "__main__":
    main()
