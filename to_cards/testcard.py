import pymongo
import utils
import os

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def test_card(schema, task_name):
    task = db.taskcard.find_one({'taskName': task_name})
    cards = []
    num = 0

    for datacard in db["datacard"].find():
        num += 1
        for modelcard in db["modelcard"].find():
            card = utils.json2dic(schema)
            card["taskID"] = task["_id"]
            card["dataID"] = datacard["_id"]
            card["modelID"] = modelcard["_id"]

            data = datacard["dataContext"]["dataLocation"]
            model = modelcard["modelContext"]["modelLocation"]
            command = "python3 " + model + " \"" + data + "\""
            print(str(num) + ". " + data)
            os.system(command)

            cards.append(card)

    return cards


def main():
    # Generate a test card.
    schema = "../ontology/schemas/test_card.json"
    testcards = test_card(schema, "Peak Finding")

    # Import the generated test card to MongoDB.
    collection = "testcard"
    utils.import_to_mongodb(testcards, collection)


if __name__ == "__main__":
    main()

