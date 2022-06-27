"""
This module generates a User instance for each user and a Center
instance(s) for the user’s affiliation(s) if it does not exist.
"""

import argparse
import utils
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def user_info(schema):
    card = utils.json2dic(schema)
    keys, paths = utils.scan_dict(card)

    items = set_para(keys)

    for i in range(len(items)):
        key = keys[i]
        if items[key]:
            path = paths[i]
            utils.dict_set(card, path, items[key])

    if not card["affiliation"]:
        return card

    # Generate a Center instance for each affiliation if it does not exist.
    for center in card["affiliation"]:
        doc = {"centerName": center}
        db.center.replace_one(doc, doc, upsert=True)

    # Replace centerName with centerID in the user's information.
    card["affiliation"] = [centerid(i) for i in card["affiliation"]]

    return card


def centerid(center_name):
    center = db.center.find_one({'centerName': center_name})
    return center["_id"]


def set_para(keys):
    parser = argparse.ArgumentParser(description='Generate Source Information for an author.')

    argus = {}
    for key in keys:
        item = "--" + key
        # There can be more than one position or affiliation.
        if key in ["positions", "affiliation"]:
            argus[key] = parser.add_argument(item, action='append')
        else:
            argus[key] = parser.add_argument(item)

    args = parser.parse_args()
    items = vars(args)

    return items


def main():
    # Generate Source Information for an author.
    schema = "../ontology/schemas/user.json"
    user = user_info(schema)

    # Import the generated model card to MongoDB.
    collection = "user"
    utils.import_to_mongodb(user, collection)


if __name__ == "__main__":
    main()
