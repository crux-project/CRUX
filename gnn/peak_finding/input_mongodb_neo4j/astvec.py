import sys
import ast
import numpy as np

sys.path.append("ast2vec/")
import ast2vec as a2v
import python_ast_utils


# Transfer a Python script into vector based on AST
def ast_to_vec(f):
    with open(f, "r") as src:
        tree = python_ast_utils.ast_to_tree(ast.parse(src.read()))
        model = a2v.load_model()
        x = model.encode(tree)

    return x.detach().numpy().tolist()


def main():
    # file = "../input_solo/source_code/scipy_peak.py"
    file = "../input_solo/source_code/peakutils_peaks.py"

    ast_vec = np.array(ast_to_vec(file))
    print(np.mean(ast_vec[:64]))
    print(np.mean(ast_vec[64:128]))
    print(np.mean(ast_vec[128:192]))
    print(np.mean(ast_vec[192:]))


if __name__ == "__main__":
    main()
