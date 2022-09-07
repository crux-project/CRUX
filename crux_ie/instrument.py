"""
This module generates an instrument card for each instrument file and link to
user and the user's affiliation(s)
"""

import argparse
import utils
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def instrument_info(schema):
    card = utils.json2dic(schema)
    keys, paths = utils.scan_dict(card)

    items = set_para(keys)

    for i in range(len(items)):
        key = keys[i]
        if items[key]:
            path = paths[i]
            utils.dict_set(card, path, items[key])

    return card


def set_para(keys):
    parser = argparse.ArgumentParser(description='Generate Card for an instrument file.')

    argus = {}
    for key in keys:
        item = "--" + key
        # There may be more than one other measurement conditions.
        if key in ["others"]:
            argus[key] = parser.add_argument(item, action='append')
        elif key == "instrumentName":
            argus[key] = parser.add_argument(key)
        else:
            argus[key] = parser.add_argument(item)

    args = parser.parse_args()
    items = vars(args)

    return items


def main():
    # Generate a instrument card.
    schema = "../ontology/schemas/instrument.json"
    card = instrument_info(schema)

    # Import the generated card to MongoDB.
    collection = "instrument"
    utils.import_to_mongodb(card, collection)


if __name__ == "__main__":
    main()
