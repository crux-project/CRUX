import pandas as pd
import os
import pymongo
from bson.objectid import ObjectId
from gensim.models import Word2Vec
import numpy as np

if not os.path.exists('./txt/'):
    os.makedirs('./txt/')

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]

test = pd.read_csv('csv/test.csv')
models = test['m.id'].unique()
datas = test['d.id'].unique()
content = []


# Overall performance function
def perform(a, b, c, d):
    return 0.4 * b + 0.1 * c + 0.1 * d - 0.01 * a


def break_list(minfo, in_list):
    for i in in_list:
        minfo.append(i)

    return minfo


# Get the average vector for a node's information.
def get_vec_min(info):
    vec_sum = np.zeros(100)
    n = 0
    for term in info:
        vec = np.array(w2v_model.wv[term])
        vec_sum += vec
        n += 1
    vec_min = list(vec_sum / n)

    return vec_min


# Parse information for thr node with type "model"
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

    content.append(model_info)


# Parse information for thr node with type "data"
for d in datas:
    data = db.datacard.find_one({"_id": ObjectId(d)})

    context = data["dataContext"]
    data_info = [context["center"]["centerName"],
                 context["contributor"]["username"]]
    sampleID = data["dataContent"]["sampleID"]
    sample = db.sample.find_one({"_id": sampleID})
    data_info.append(sample["sampleName"])

    content.append(data_info)


# Training Word2Vec model
w2v_model = Word2Vec(content, vector_size=100, min_count=1, window=3, sg=1, workers=4)
w2v_model.save('./w2v_model')


# Node: Encode model as 0, data as 1
n = 0
with open('txt/node.txt', 'a+') as f:
    for m in models:
        f.write(m + '\t' + str(0) + '\t' + str(get_vec_min(content[n])) + '\n')
        n += 1
    for d in datas:
        f.write(d + '\t' + str(1) + '\t' + str(get_vec_min(content[n])) + '\n')
        n += 1


# Test: (model, data) [runningTimes, f1_score, precision, recall]
with open('txt/edge.txt', 'a+') as f:
    for line in test.values:
        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))


# Top5: (model, data) [runningTimes, f1_score, precision, recall]
test['performance'] = test.apply(lambda test: perform(
    test['r.runningTimes'], test['r.f1_score'], test['r.precision'], test['r.recall']), axis=1)
test['rank'] = test['performance'].groupby(test['d.id']).rank(ascending=False, method='first').astype(int)

test.to_csv('csv/test_rank.csv')

with open('txt/top5.txt', 'a+') as f:
    for line in test.values:
        if line[-1] > 5:
            continue

        performance = [line[2], line[3], line[4], line[5]]
        f.write('(' + (str(line[0]) + ',' + (str(line[1]) + ')'
                                             + '\t' + str(performance) + '\n')))
