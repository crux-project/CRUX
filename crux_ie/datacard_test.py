"""
This module generates a data card for each dataset and a Center/Sample instance
if it does not exist. The input can be a file or a folder.

For contributors’ information, we suppose the relation between user and center is 1:1.
"""

import utils
import argparse
import xmltodict


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

    # Other information
    context["dataLocation"] = input
    content["header"] = xrd["scan"]["header"]
    content["status"] = xrd.get("@status")
    content["sampleMode"] = xrd.get("@sampleMode")
    content["sampleOffset"] = xrd.get("sampleOffset")
    content["usedWavelength"] = xrd.get("usedWavelength")

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

    # Save dic to JSON
    utils.save2json("../testdata/test.json", datacards)


if __name__ == "__main__":
    main()
