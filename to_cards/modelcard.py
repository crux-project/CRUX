"""
This module generates a model card for each model(script of package).
"""

import utils
import argparse
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def model_card(schema):
    card = utils.json2dic(schema)
    keys, paths = utils.scan_dict(card)

    items = set_para(keys)

    if items["taskName"]:
        result = db.taskcard.find_one({'taskName': items["taskName"]})
        items["taskID"] = result["_id"]

    dep = items["dependencies"] if items["dependencies"] else "None"
    for i in range(len(dep)):
        if dep == "None":
            break
        result = db.modelcard.find_one({'modelContext.modelName': dep[i]})
        card["dependencies"].setdefault(dep[i], {})
        card["dependencies"][dep[i]]["modelID"] = result["_id"] if result else None

    for i in range(len(items)):
        key = keys[i]
        if items[key] and key != "dependencies":
            path = paths[i]
            utils.dict_set(card, path, items[key])

    return card


def set_para(keys):
    parser = argparse.ArgumentParser(description='Generate a Model Card.')

    argus = {}
    for key in keys:
        item = "--" + key
        argus[key] = parser.add_argument(item)

    argus["inputParameters"].nargs = "+"
    argus["outputParameters"].nargs = "+"
    argus["dependencies"].nargs = "+"
    argus["hyperParameters"].nargs = "+"

    args = parser.parse_args()
    items = vars(args)

    return items


def main():
    # Generate a model card.
    schema = "../ontology/schemas/model_card.json"
    modelcard = model_card(schema)

    # Import the generated model card to MongoDB.
    collection = "modelcard"
    utils.import_to_mongodb(modelcard, collection)


if __name__ == "__main__":
    main()
