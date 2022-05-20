import pymongo
import os

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def ranking_list():
    for datacard in db["datacard"].find():
        condition = {"dataID": datacard["_id"], "groundtruth": {"$ne": "outputLocation"}}
        list = db.testcard.find(condition, {"_id": 0, "modelID": 1, "performance": 1}
                                ).sort("performance.F1_score", -1)

        data = datacard["dataContext"]["dataLocation"]
        models = []
        for l in list:
            model = db.modelcard.find_one({'_id': l['modelID']})
            l["modelName"] = model["modelContext"]["modelName"]
            models.append(l)

        output_to_txt(data, models)


def output_to_txt(input, models):
    output = input.replace("data", "ranking", 1)[:-6] + ".txt"

    index = output.rfind("/") + 1
    if not os.path.exists(output[:index]):
        os.makedirs(output[:index])

    f = open(output, 'w')
    f.write("XRDML file: " + input + '\n')
    f.write("Groundtruth: " + str(models[0]["modelName"]) + '\n')
    f.write("%-20s\t\t%-20s\n"
            % ("model", "F1_score") + "-" * 85)

    for m in models[1:]:
        f.write("\n%-20s\t\t%-20s"
                % (str(m["modelName"]), str(m["performance"]["F1_score"])))
    f.close()


def main():
    ranking_list()


if __name__ == '__main__':
    main()