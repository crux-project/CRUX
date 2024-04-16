import ast
import json
from ast2json import ast2json


def main():
    with open("./brain_tumor.py", "r") as source:
        tree = ast.parse(source.read())
        tree = ast2json(tree)

    # print(ast.dump(tree))

    with open('ast.json', 'w') as f:
        json.dump(tree, f, indent=4)


if __name__ == "__main__":
    main()
