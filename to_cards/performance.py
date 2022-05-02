import numpy as np
import math
from collections import Counter
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def get_pos(flie):
    pos = []

    f = open(flie, 'r')
    lines = f.readlines()[1:]
    for line in lines:
        line = line.strip('\n').split('\t')
        pos.append(line[0])

    pos = np.array(pos).astype(float).tolist()

    return pos


def generate_matric(groundtruth, predict):
    metrics = {}

    p = get_pos(groundtruth)
    pp = get_pos(predict)
    tp = list(set(p) & set(pp))

    recall, precision, f1 = f1_score(len(tp), len(p), len(pp))

    metrics["F1_score"] = f1
    metrics["precision"] = precision
    metrics["recall"] = recall
    metrics["cosineSimilarity"] = cosine_similarity(p, pp)
    metrics["jaccardSimilarity"] = jaccard_similarity(p, pp, tp)

    return metrics


def f1_score(tp, p, pp):
    if p == 0 or pp == 0:
        recall = None
        precision = None
        f1 = None
    else:
        recall = tp / p
        precision = tp / pp
        f1 = 2 * (precision * recall) / (precision + recall)

    return recall, precision, f1


def cosine_similarity(p, pp):
    c1 = Counter(p)
    c2 = Counter(pp)

    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0) ** 2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0) ** 2 for k in terms))

    if magA * magB == 0:
        cosine_similarity = None
    else:
        cosine_similarity = dotprod / (magA * magB)

    return cosine_similarity


def jaccard_similarity(p, pp, tp):
    union = list(set(p) | set(pp))

    if len(union) == 0:
        jaccard_similarity = None
    else:
        jaccard_similarity = len(tp) / len(union)

    return jaccard_similarity


def insert2testcard():
    for testcard in db.testcard.find():
        previous = testcard["performance"]
        predict = testcard["outputLocation"]
        groundtruths = predict.split('/')

        if groundtruths[6] == "CaCO3-TiO2":
            groundtruths[3] = "pf_scipy_prom30"
        elif groundtruths[6] == "Mn-O":
            groundtruths[3] = "pf_scipy_prom40"
        else:
            groundtruths[3] = "pf_scipy_prom300"
        groundtruth = "/".join(groundtruths)

        matrics = generate_matric(groundtruth, predict)
        current = {**previous, **matrics}
        db.testcard.update_one(testcard, {"$set": {"performance": current}})


def main():
    insert2testcard()


if __name__ == '__main__':
    main()
