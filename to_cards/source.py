import argparse
import utils
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def source_info(schema):
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
    parser = argparse.ArgumentParser(description='Generate Source Information for an author.')

    argus = {}
    for key in keys:
        item = "--" + key
        if key in ["positions", "affiliation"]:
            argus[key] = parser.add_argument(item, action='append')
        else:
            argus[key] = parser.add_argument(item)

    args = parser.parse_args()
    items = vars(args)

    return items


def main():
    # Generate Source Information for an author.
    schema = "../ontology/schemas/source.json"
    source = source_info(schema)

    # Import the generated model card to MongoDB.
    collection = "source"
    utils.import_to_mongodb(source, collection)


if __name__ == "__main__":
    main()
