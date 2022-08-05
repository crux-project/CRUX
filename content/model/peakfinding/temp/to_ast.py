import ast
import json
from ast2json import ast2json
import ast2vec



def main():
    with open("../pf_peakutils_dist150.py", "r") as source:
        tree = ast.parse(source.read())
        tree = ast2json(tree)

    # print(ast.dump(tree))

    with open('ast.json', 'w') as f:
        json.dump(tree, f, indent=4)
        # f.write(ast.dump(tree))


if __name__ == "__main__":
    main()
