import pymongo
import utils
import time
import argparse
import multiprocessing
import subprocess

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def test_card(schema, task, datacard, modelcard, peak_schema = "../ontology/schemas/peaks.json"):
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

    peaks = utils.json2dic(peak_schema)
    peaks["x"], peaks["y"] = execute(input, model, card)
    peaks["testID"] = utils.import_to_mongodb(card, "testcard")
    peaks["sampleID"] = datacard["dataContent"]["sampleID"]

    peakID = utils.import_to_mongodb(peaks, "peaklist")
    db.testcard.update_one(
        {'_id': peaks["testID"]},
        {'$set': {'output': {"peaklist": peakID}}}
    )


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


def execute(input, model, card):
    command = "python3 " + model + " \"" + input + "\""

    start = time.time()
    peaks = subprocess.check_output(command, shell=True)
    end = time.time()
    rt = end - start
    card["performance"]["runningTime(s)"] = rt

    peaks = peaks.decode().split("\n")
    x = peaks[0][2:-2].split("', '")
    y = peaks[1][2:-2].split("', '")

    return x, y


def get_input():
    parser = argparse.ArgumentParser(description='Specify the execute range.')

    parser.add_argument("task",
                        help="Task name.")

    parser.add_argument("-d", "--dataPath",
                        dest="data",
                        help="Path to XRDML data.")

    parser.add_argument("-m", "--modelName",
                        dest="model",
                        help="Model name.")

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
