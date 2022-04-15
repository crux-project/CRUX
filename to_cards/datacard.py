import utils
import xmltodict
import os


def data_card(schema, input, output):
    """
    Mapping to JSON file.
    :param schema: path of JSON schema.
    :param input: path of input XRDML file.
    :param output: path of output JSON file.
    :return:
    """
    card = utils.json2dic(schema)
    f = open(input, mode='r', encoding='utf-8')
    raw = xmltodict.parse(f.read())

    context = card["dataContext"]
    content = card["dataContent"]
    xrd = raw["xrdMeasurements"]["xrdMeasurement"]

    context["center"]["centerName"] = input.split('/')[3]
    context["contributors"]["dataLocation"] = input
    content["header"] = xrd["scan"]["header"]
    content["status"] = xrd.get("@status")
    content["sampleMode"] = xrd.get("@sampleMode")
    content["sampleOffset"] = xrd.get("sampleOffset")
    content["usedWavelength"] = xrd.get("usedWavelength")

    if content["header"]["source"].get("instrumentID"):
        del content["header"]["source"]["instrumentID"]

    utils.save2json(output, card)


def xrdml2json_batch(inputs, outputs, schema):
    """
    Batch convert XRDML files to JSON files.
    :param inputs: path of the folder for XRDML files.
    :param outputs: path of the folder for JSON files(datacards).
    :param schema: path of JSON(card) schema.
    :return:
    """
    files = utils.get_path(inputs)

    for input in files:
        output = input[:-5] + "json"
        output = output.replace(inputs, outputs, 1)

        index = output.rfind("/") + 1
        if not os.path.exists(output[:index]):
            os.makedirs(output[:index])

        data_card(schema, input, output)


def main():
    data = "../data/xrdml/"
    datacards = "../data/data_cards/"

    # Convert XRDML data to JSON (Done)
    schema = "../ontology/schemas/data_card.json"
    xrdml2json_batch(data, datacards, schema)

    # Import JSON files to MongoDB (Done)
    collection = "datacard"
    utils.import2mongodb_batch(datacards, collection)


if __name__ == "__main__":
    main()
