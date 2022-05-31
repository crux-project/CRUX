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
    center = input.split('/')[4]

    context["center"]["centerName"] = center
    context["dataLocation"] = input
    content["header"] = xrd["scan"]["header"]
    content["status"] = xrd.get("@status")
    content["sampleMode"] = xrd.get("@sampleMode")
    content["sampleOffset"] = xrd.get("sampleOffset")
    content["usedWavelength"] = xrd.get("usedWavelength")

    if content["header"]["source"].get("instrumentID"):
        del content["header"]["source"]["instrumentID"]

    contributor = context["contributors"]
    if center == "NC-State":
        contributor["username"] = "Jacob L. Jones"
    elif center == "UIUC":
        contributor["username"] = "Mauro Sardela"

    user = db.source.find_one({'name': contributor["username"]})
    if user:
        contributor["userID"] = user["_id"]

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
    else:
        input = [inputs['folder'], 'folder']

    return input


def main():
    # Generate data cards.
    # input = "../content/data/xrdml/"
    input = get_input()

    if input[1] == "file":
        datacards = data_card(input[0])
    else:
        datacards = data_card_batch(input[0])

    # Import JSON files to MongoDB (Done for 289)
    collection = "datacard"
    utils.import_to_mongodb(datacards, collection)


if __name__ == "__main__":
    main()
