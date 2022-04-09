import trans2json_utils as utils
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


def get_path(folder):
    """
    Get paths of all XRDML files in folder.
    :param folder: path of the input folder.
    :return: a list of paths.
    """
    paths = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file[-5:] != 'xrdml' or 'XRDML':
                continue
            paths.append(os.path.join(root, file))

    return paths


def batch_processing(folder, schema):
    """
    Batch convert XRDML files to JSON files.
    :param folder: path of the input folder.
    :param schema: path of JSON schema.
    :return:
    """
    files = get_path(folder)

    for file in files:
        output = file[:-5] + "json"
        output = output.replace("xrdml", "data_cards", 1)

        index = output.rfind("/") + 1
        if not os.path.exists(output[:index]):
            os.makedirs(output[:index])

        data_card(schema, file, output)


def main():
    schema = "../ontology/schemas/data_card.json"
    data = "../data/xrdml/"

    batch_processing(data, schema)


if __name__ == "__main__":
    main()
