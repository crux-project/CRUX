import ast
import python_ast_utils
import ast2vec
import pandas as pd
import pymongo
import os
from bson.objectid import ObjectId

if not os.path.exists('./txt/'):
    os.makedirs('./txt/')

test = pd.read_csv('../CRUX/gnn/input/csv/test.csv')
models = test['m.id'].unique()
datas = test['d.id'].unique()

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def ast_to_vec(f):
    with open(f, "r") as src:
        tree = python_ast_utils.ast_to_tree(ast.parse(src.read()))
        model = ast2vec.load_model()
        x = model.encode(tree)

    return x.detach().numpy().tolist()


n = 0
with open('txt/node.txt', 'a+') as f:
    for m in models:
        model = db.modelcard.find_one({"_id": ObjectId(m)})
        script = model["modelContext"]["modelLocation"][17:]

        f.write(m + '\t' + str(0) + '\t' + str(ast_to_vec(script)) + '\n')
        n += 1
    for d in datas:
        f.write(d + '\t' + str(1) + '\t' + '\n')
        n += 1
