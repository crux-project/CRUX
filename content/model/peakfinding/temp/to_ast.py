import ast


def main():
    with open("../pf_peakutils_dist150.py", "r") as source:
        tree = ast.parse(source.read())

    # print(ast.dump(tree))

    with open('ast.txt', 'w') as f:
        f.write(ast.dump(tree))


if __name__ == "__main__":
    main()
