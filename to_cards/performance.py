"""
This module computes and inserts performance(F1_score, precision, recall,
cosine similarity, and Jaccard similarity) into testcard.
"""

import math
import sys
from collections import Counter
import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client["crux"]


def intersection(l1, l2, err):
    """
    Compute the number of the common elements in l1 and l2.
    :param l1: the 1st list.
    :param l2: the 2nd list.
    :param err: allowed error.
    :return: the number of the common elements.
    """
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


def generate_matric(p, pp, err):
    metrics = {}
    tp = intersection(p, pp, err)

    recall, precision, f1 = f1_score(tp, len(p), len(pp))

    metrics["F1_score"] = f1
    metrics["precision"] = precision
    metrics["recall"] = recall
    metrics["cosineSimilarity"] = cosine_similarity(p, pp)
    metrics["jaccardSimilarity"] = jaccard_similarity(p, pp, tp)

    return metrics


def f1_score(tp, p, pp):
    """
    Compute recall, precision and f1-score.
    :param tp: true positive.
    :param p: positive labels/items.
    :param pp: positive predictions.
    :return: recall, precision and f1-score.
    """
    f1, recall, precision = None, None, None

    if p != 0:
        recall = tp / p

    if pp != 0:
        precision = tp / pp

    if p != 0 and pp != 0:
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


def get_pred_gt(testcard):
    """
             ｜-predict_peakID-predict(peaklist)-----------------｜
    testcard-｜                                                  ｜
             ｜-dataID-sampleID-sampleName-gt_modelID            ｜
                  ｜----------------------------｜-gt_testID-gt_peakID-gt
    """
    predictID = testcard["output"]["peaklist"]

    dataID = testcard["dataID"]
    datacard = db.datacard.find_one({'_id': dataID})

    sampleID = datacard["dataContent"]["sampleID"]
    sample = db.sample.find_one({'_id': sampleID})
    sampleName = sample["sampleName"]

    if sampleName in ["BCdT - PT", "BSc - PT", "BZnV - BSc - PT"]:
        gt_modelName = "Jade"
    elif sampleName == "CaCO3-TiO2":
        gt_modelName = "pf_scipy_prom30"
    elif sampleName == "Mn-O":
        gt_modelName = "pf_scipy_prom40"
    else:
        gt_modelName = "pf_scipy_prom300"

    gt_modelcard = db.modelcard.find_one({
        "modelContext.modelName": gt_modelName
    })
    gt_modelID = gt_modelcard["_id"]

    gt_testcard = db.testcard.find_one({'$and': [
        {"dataID": dataID},
        {"modelID": gt_modelID}
    ]})
    gt_testID = gt_testcard['_id']

    gt_peaklist = db.peaklist.find_one({"testID": gt_testID})
    groundtruth = gt_peaklist["x"]
    pd_peaklist = db.peaklist.find_one({"_id": predictID})
    predict = pd_peaklist["x"]

    db.testcard.update_one(testcard, {
        "$set": {"groundtruth": gt_peaklist['_id']}
    })

    return predict, groundtruth


def insert2testcard(err=0.01):
    for testcard in db.testcard.find():
        # No performance if the groundtruth is the result itself.
        if testcard["output"]["peaklist"] == testcard["groundtruth"]:
            continue

        predict, groundtruth = get_pred_gt(testcard)
        matrics = generate_matric(groundtruth, predict, err)

        previous = testcard["performance"]
        current = {**previous, **matrics}

        db.testcard.update_one(testcard, {
            "$set": {"performance": current,
                     "allowedError": err}
        })


def main():
    error = sys.argv[1]
    insert2testcard(error)


if __name__ == '__main__':
    main()
