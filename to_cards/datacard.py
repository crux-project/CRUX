"""
This module generates a data card for each dataset and a Center/Sample instance
if it does not exist. The input can be a file or a folder.

For contributors’ information, we suppose the relation between user and center is 1:1.
"""

import utils
import argparse
import xmltodict
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def data_card(input, schema="../ontology/schemas/data_card.json"):
    """
    Mapping to JSON file.
    :param schema: path of JSON schema.
    :param input: path of input XRDML file.
    :return: a datacard
    """
    card = utils.json2dic(schema)
    f = open(input, mode='r', encoding='utf-8')
    raw = xmltodict.parse(f.read())

    context = card["dataContext"]
    content = card["dataContent"]
    xrd = raw["xrdMeasurements"]["xrdMeasurement"]

    # ToDo: hardcode to get centerName and sampleName
    centerName = input.split('/')[4]
    sampleName = input.split('/')[5]

    # If center existed, get its id, or create one and get its id.
    context["center"]["centerName"] = centerName
    centerDoc = {"centerName": centerName}
    db.center.replace_one(centerDoc, centerDoc, upsert=True)
    center = db.center.find_one({'centerName': centerName})
    context["center"]["centerID"] = center["_id"]

    # Store information for sample
    sampleDoc = {"sampleName": sampleName, "centerID": center["_id"]}
    db.sample.replace_one(sampleDoc, sampleDoc, upsert=True)
    sample = db.sample.find_one({"sampleName": sampleName})
    content["sampleID"] = sample["_id"]

    # Get contributor's information
    contributor = context["contributors"]
    user = db.user.find_one({"affiliation": {"$in": [center["_id"]]}})
    contributor["username"] = user["username"]
    contributor["userID"] = user["_id"]

    # Other information
    context["dataLocation"] = input
    content["header"] = xrd["scan"]["header"]
    content["status"] = xrd.get("@status")
    content["sampleMode"] = xrd.get("@sampleMode")
    content["sampleOffset"] = xrd.get("sampleOffset")
    content["usedWavelength"] = xrd.get("usedWavelength")

    # if content["header"]["source"].get("instrumentID"):
    #     del content["header"]["source"]["instrumentID"]

    return card


def data_card_batch(inputs, schema="../ontology/schemas/data_card.json"):
    """
    Batch convert XRDML files to JSON files.
    :param inputs: path of the folder for XRDML files.
    :param schema: path of JSON(card) schema.
    :return: bunch of datacards
    """
    files = utils.get_path(inputs)

    cards = []
    for input in files:
        card = data_card(input, schema)
        cards.append(card)

    return cards


def get_input():
    """
    Get input from a file or a folder.
    :return: [inputpath, 'file'/'folder']
    """
    parser = argparse.ArgumentParser(description='Raw data for datacard.')

    parser.add_argument("-file", "--input_file",
                        dest="file",
                        help="Path to input file.")

    parser.add_argument("-folder", "--input_folder",
                        dest="folder",
                        help="Path to input folder.")

    inputs = vars(parser.parse_args())

    if inputs['file']:
        input = [inputs['file'], 'file']
    elif inputs['folder']:
        input = [inputs['folder'], 'folder']

    return input


def main():
    # Generate data cards.
    input = get_input()

    if input[1] == "file":
        datacards = data_card(input[0])
    else:
        datacards = data_card_batch(input[0])

    # Import JSON files to MongoDB
    collection = "datacard"
    utils.import_to_mongodb(datacards, collection)


if __name__ == "__main__":
    main()
