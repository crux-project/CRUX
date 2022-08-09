import sys
import pandas as pd
import os
import pymongo
from bson.objectid import ObjectId
from gensim.models import Word2Vec
import numpy as np
import ast

sys.path.append("ast2vec")
import ast2vec as a2v
import python_ast_utils

if not os.path.exists('./txt/'):
    os.makedirs('./txt/')

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]

test = pd.read_csv('csv/test.csv')
models = test['m.id'].unique()
datas = test['d.id'].unique()


# Overall performance function
def perform(a, b):
    return a - 0.1 * b


# Get the average vector for a node's information.
def get_vec_mean(info, vec_size):
    vec_sum = np.zeros(vec_size)
    n = 0
    for term in info:
        vec = np.array(w2v_model.wv[term])
        vec_sum += vec
        n += 1
    vec_mean = list(vec_sum / n)

    return vec_mean


# Transfer a Python script into vector based on AST
def ast_to_vec(f):
    with open(f, "r") as src:
        tree = python_ast_utils.ast_to_tree(ast.parse(src.read()))
        model = a2v.load_model()
        x = model.encode(tree)

    return x.detach().numpy().tolist()


# def break_list(minfo, in_list):
#     for i in in_list:
#         minfo.append(i)
#
#     return minfo
#
#
# Parse information for the node with type "model"
# models_info = []
# for m in models:
#     model = db.modelcard.find_one({"_id": ObjectId(m)})
#     context = model["modelContext"]
#     descript = model["modelDescription"]
#
#     model_info = [context["modelName"],
#                   context["contributor"]["username"],
#                   context["modelDate"]["modelYear"]]
#     model_info = break_list(model_info, descript["inputParameters"])
#     model_info = break_list(model_info, descript["outputParameters"])
#     model_info = break_list(model_info, descript["hyperParameters"])
#
#     model.append(model_info)


# Parse information for the node with type "data"
datas_info = []
for d in datas:
    data = db.datacard.find_one({"_id": ObjectId(d)})

    context = data["dataContext"]
    data_info = [context["center"]["centerName"],
                 context["contributor"]["username"]]
    sampleID = data["dataContent"]["sampleID"]
    sample = db.sample.find_one({"_id": sampleID})
    data_info.append(sample["sampleName"])

    datas_info.append(data_info)


# Training Word2Vec model
w2v_model = Word2Vec(datas_info, vector_size=256, min_count=1, window=3, sg=1, workers=4)
w2v_model.save('./w2v_model')


# Node: Encode model as 0, data as 1
n = 0
with open('txt/node.txt', 'a+') as f:
    for m in models:
        model = db.modelcard.find_one({"_id": ObjectId(m)})
        script = "../" + model["modelContext"]["modelLocation"]

        f.write(m + '\t' + str(0) + '\t' + str(ast_to_vec(script)) + '\n')

    for d in datas:
        f.write(d + '\t' + str(1) + '\t' + str(get_vec_mean(datas_info[n], 256)) + '\n')
        n += 1


# Test: (model, data) [runningTimes, f1_score, precision, recall]
with open('txt/edge.txt', 'a+') as f:
    for line in test.values:
        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))


# Top5: (model, data) [runningTimes, f1_score, precision, recall]
test['performance'] = test.apply(lambda test: perform(test['r.precision'], test['r.f1_score']), axis=1)
test['rank'] = test['performance'].groupby(test['d.id']).rank(ascending=False, method='first').astype(int)

test.to_csv('csv/test_rank.csv')

with open('txt/top5.txt', 'a+') as f:
    for line in test.values:
        if line[-1] > 5:
            continue

        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))
