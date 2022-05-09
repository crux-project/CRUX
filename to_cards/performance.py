import numpy as np
import math
import sys
from collections import Counter
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def get_pos(file):
    pos = []
    index = [3, 1] if "Jade" in file else [1, 0]

    f = open(file, 'r')
    lines = f.readlines()[index[0]:]
    if "Jade" in file:
        lines = lines[:-3]
    for line in lines:
        line = line.strip('\n').split('\t')
        pos.append(line[index[1]])

    pos = np.array(pos).astype(float).tolist()

    return pos


def intersection(l1, l2, err):
    count = 0
    i = 0
    j = 0

    err = float(err)
    while i < len(l1) and j < len(l2):
        diff = abs(l1[i] - l2[j])
        if diff > err and l1[i] > l2[j]:
            j += 1
        elif diff > err and l1[i] < l2[j]:
            i += 1
        else:
            i += 1
            j += 1
            count += 1

    return count


def generate_matric(groundtruth, predict, err):
    metrics = {}

    p = get_pos(groundtruth)
    pp = get_pos(predict)
    tp = intersection(p, pp, err)
    # tp = list(set(p) & set(pp))

    recall, precision, f1 = f1_score(tp, len(p), len(pp))

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
        c_similarity = None
    else:
        c_similarity = dotprod / (magA * magB)

    return c_similarity


def jaccard_similarity(p, pp, tp):
    union = list(set(p) | set(pp))

    if len(union) == 0:
        j_similarity = None
    else:
        j_similarity = tp / len(union)

    return j_similarity


def insert2testcard(err=0.01):
    for testcard in db.testcard.find():
        previous = testcard["performance"]
        predict = testcard["outputLocation"]
        groundtruths = predict.split('/')

        if groundtruths[6] in ["BCdT - PT", "BSc - PT", "BZnV - BSc - PT"]:
            groundtruths[3] = "Jade"
        elif groundtruths[6] == "CaCO3-TiO2":
            groundtruths[3] = "pf_scipy_prom30"
        elif groundtruths[6] == "Mn-O":
            groundtruths[3] = "pf_scipy_prom40"
        else:
            groundtruths[3] = "pf_scipy_prom300"
        groundtruth = "/".join(groundtruths)

        matrics = generate_matric(groundtruth, predict, err)
        current = {**previous, **matrics}
        db.testcard.update_one(testcard, {"$set": {"performance": current,
                                                   "groundtruth": groundtruth,
                                                   "allowedError": err}})


def main():
    error = sys.argv[1]
    insert2testcard(error)


if __name__ == '__main__':
    main()
