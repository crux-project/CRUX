import utils
import argparse
import os


def model_card(schema, output_dir):
    card = utils.json2dic(schema)
    # keys, _ = utils.scan_dict(card)

    parser = argparse.ArgumentParser(description='Generate a Model Card.')
    parser.add_argument("modelName", help="Name of the model")
    parser.add_argument("modelLocation", help="Path to the model")
    # keys.remove("modelName")
    # for key in keys:
    #     item = "--" + key
    #     parser.add_argument(item)
    args = parser.parse_args()
    items = vars(args)

    context = card["modelContext"]
    context["modelName"] = items["modelName"]
    context["modelLocation"] = items["modelLocation"]
    output = os.path.join(output_dir, args.modelName + ".json")
    utils.save2json(output, card)

    return output


def main():
    # Generate a task card.
    output_dir = "../data/model_cards"
    schema = "../ontology/schemas/model_card.json"
    modelcard = model_card(schema, output_dir)

    # Import the generated task card to MongoDB.
    collection = "modelcard"
    utils.import_json_to_mongodb(modelcard, collection)


if __name__ == "__main__":
    main()
