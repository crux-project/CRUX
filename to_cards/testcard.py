import pymongo
import utils
import os
import time
import argparse
import multiprocessing

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def test_card(schema, task, datacard, modelcard):
    taskcard = db.taskcard.find_one({'taskName': task})

    db.datacard.update_one(
        {'_id': datacard["_id"]},
        {'$addToSet': {'analysis': taskcard["_id"]}}
    )

    card = utils.json2dic(schema)
    card["taskID"] = taskcard["_id"]
    card["dataID"] = datacard["_id"]
    card["modelID"] = modelcard["_id"]

    input = datacard["dataContext"]["dataLocation"]
    model = modelcard["modelContext"]["modelLocation"]
    model_name = modelcard["modelContext"]["modelName"]
    output = input.replace("data", "test/" + model_name, 1)[:-6] + ".txt"
    card["outputLocation"] = output

    if model_name == "Jade" and os.path.exists(output):
        utils.import_to_mongodb(card, "testcard")
    elif model_name != "Jade":
        execute(input, output, model, card)
        utils.import_to_mongodb(card, "testcard")


def test_card_mp(temp):
    return test_card(temp[0], temp[1], temp[2], temp[3])


def test_card_task(task, schema="../ontology/schemas/test_card.json"):
    num = 0
    list = []

    for datacard in db["datacard"].find():
        num += 1
        for modelcard in db["modelcard"].find(
                {"intendedUse.intendedTasks.taskName": task}):
            temp = (schema, task, datacard, modelcard)
            list.append(temp)

    num_cpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cpu)
    pool.map(test_card_mp, list)


def test_card_model_data(model, data, task, schema="../ontology/schemas/test_card.json"):
    datacard = db.datacard.find_one({"dataContext.dataLocation": data})
    modelcard = db.modelcard.find_one({"modelContext.modelName": model})

    test_card(schema, task, datacard, modelcard)


def execute(input, output, model, card):
    command = "python3 " + model + " \"" + input + "\" \"" + output + "\""

    start = time.time()
    os.system(command)
    end = time.time()
    rt = end - start
    card["performance"]["runningTime(s)"] = rt


def get_input():
    parser = argparse.ArgumentParser(description='Specify the execute range.')

    parser.add_argument("task",
                        help="Task name.")

    parser.add_argument("-d", "--data",
                        dest="data",
                        help="Path to XRDML data.")

    parser.add_argument("-m", "--model",
                        dest="model",
                        help="Path to the script.")

    inputs = vars(parser.parse_args())

    return inputs


def main():
    inputs = get_input()
    task = inputs["task"]

    if inputs["data"] and inputs["model"]:
        model = inputs["model"]
        data = inputs["data"]
        test_card_model_data(model, data, task)
    else:
        test_card_task(task)


if __name__ == "__main__":
    main()
