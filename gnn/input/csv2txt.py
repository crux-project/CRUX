import sys
import pandas as pd
import os
import pymongo
from bson.objectid import ObjectId
from gensim.models import Word2Vec
import numpy as np
import ast
from statistics import mean
import xmltodict

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

# print("model: " + str(len(models)))
# print("data: " + str(len(datas)))


# Overall performance function
def perform(a, b, c):
    return a + b - 0.1 * c


# Get the average vector for a node's information.
def get_vec_mean(info, vec_size, w2v_model):
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


def break_list(minfo, in_list):
    for i in in_list:
        minfo.append(i)

    return minfo


# Get x and y from raw data
def detect_x_y(input):
    f = open(input, mode='r', encoding='utf-8')
    dic = xmltodict.parse(f.read())

    dp = dic["xrdMeasurements"]["xrdMeasurement"]["scan"]["dataPoints"]
    y = dp["intensities"]["#text"]
    y = list(map(float, y.split()))

    if type(dp["positions"]) == list:
        sp = float(dp["positions"][0]["startPosition"])
        ep = float(dp["positions"][0]["endPosition"])
    else:
        sp = float(dp["positions"]["startPosition"])
        ep = float(dp["positions"]["endPosition"])

    x = np.arange(sp, ep, (ep - sp) / len(y))

    return x, y


# Parse information for the node with type "model"
models_info = []
for m in models:
    model = db.modelcard.find_one({"_id": ObjectId(m)})
    context = model["modelContext"]
    descript = model["modelDescription"]

    model_info = [context["modelName"],
                  context["contributor"]["username"],
                  context["modelDate"]["modelYear"]]
    model_info = break_list(model_info, descript["inputParameters"])
    model_info = break_list(model_info, descript["outputParameters"])
    model_info = break_list(model_info, descript["hyperParameters"])

    models_info.append(model_info)


# Parse information for the node with type "data"
datas_info = []
for d in datas:
    data = db.datacard.find_one({"_id": ObjectId(d)})

    context = data["dataContext"]
    location = "../" + context["dataLocation"]
    x, y = detect_x_y(location)
    minx = str(min(x))
    maxx = str(max(x))
    miny = str(min(y))
    maxy = str(max(y))
    meany = str(mean(y))
    data_info = [context["center"]["centerName"],
                 context["contributor"]["username"],
                 minx, maxx, miny, maxy, meany]
    sampleID = data["dataContent"]["sampleID"]
    sample = db.sample.find_one({"_id": sampleID})
    data_info.append(sample["sampleName"])

    datas_info.append(data_info)

# Training Word2Vec model
w2v_model_datas = Word2Vec(datas_info, vector_size=256, min_count=1, window=3, sg=1, workers=4)
w2v_model_datas.save('./w2v_model_datas')
w2v_model_models = Word2Vec(models_info, vector_size=256, min_count=1, window=3, sg=1, workers=4)
w2v_model_models.save('./w2v_model_models')

# Node: Encode model as 0, data as 1

with open('txt/node.txt', 'a+') as f:
    n = 0
    for m in models:
        model = db.modelcard.find_one({"_id": ObjectId(m)})
        script = "../" + model["modelContext"]["modelLocation"]

        ast_vec = np.array(ast_to_vec(script))
        info_vec = np.array(get_vec_mean(models_info[n], 256, w2v_model_models))
        model_vec = (ast_vec + info_vec) / 2

        f.write(m + '\t' + str(0) + '\t' + str(model_vec.tolist()) + '\n')
        n += 1

    n = 0
    for d in datas:
        f.write(d + '\t' + str(1) + '\t' + str(get_vec_mean(datas_info[n], 256, w2v_model_datas)) + '\n')
        n += 1

# Test: (model, data) [runningTimes, f1_score, precision, recall, cosine similarity, jaccard similarity]
with open('txt/edge.txt', 'a+') as f:
    for line in test.values:
        performance = [line[2], line[3], line[4], line[5], line[6], line[7]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))

# Top5: (model, data) [runningTimes, f1_score, precision, recall, cosine similarity, jaccard similarity]
test['performance'] = test.apply(
    lambda test: perform(test['r.f1_score'], test['r.cosineSimilarity'], test['r.runningTimes']), axis=1)
test['rank'] = test['performance'].groupby(test['d.id']).rank(ascending=False, method='first').astype(int)

test.to_csv('csv/test_rank.csv')

with open('txt/top5.txt', 'a+') as f:
    for line in test.values:
        if line[-1] > 5:
            continue

        performance = [line[2], line[3], line[4], line[5], line[6], line[7]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))
