import utils
import xmltodict


def data_card(schema, input):
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

    context["center"]["centerName"] = input.split('/')[3]
    context["dataLocation"] = input
    content["header"] = xrd["scan"]["header"]
    content["status"] = xrd.get("@status")
    content["sampleMode"] = xrd.get("@sampleMode")
    content["sampleOffset"] = xrd.get("sampleOffset")
    content["usedWavelength"] = xrd.get("usedWavelength")

    if content["header"]["source"].get("instrumentID"):
        del content["header"]["source"]["instrumentID"]

    return card


def data_card_batch(inputs, schema):
    """
    Batch convert XRDML files to JSON files.
    :param inputs: path of the folder for XRDML files.
    :param schema: path of JSON(card) schema.
    :return: bunch of datacards
    """
    files = utils.get_path(inputs)

    cards = []
    for input in files:
        card = data_card(schema, input)
        cards.append(card)

    return cards


def main():
    # Generate data cards.
    data = "../content/data/xrdml/"
    schema = "../ontology/schemas/data_card.json"
    datacards = data_card_batch(data, schema)

    # Import JSON files to MongoDB (Done for 289)
    collection = "datacard"
    utils.import_to_mongodb(datacards, collection)


if __name__ == "__main__":
    main()
