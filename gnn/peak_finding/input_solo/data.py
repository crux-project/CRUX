import xmltodict
import numpy as np
import sys
from statistics import mean
from gensim.models import Word2Vec

sys.path.append('../../..')
import crux_ie.utils as utils

datas_info = {}
w2v_info = []


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
    x = x.tolist()

    # length = ceil((ep - sp) / step), may overflow
    if len(x) > len(y):
        x = x[:-1]

    return x, y


def data_info(x, y, file):
    minx = str(min(x))
    maxx = str(max(x))
    miny = str(min(y))
    maxy = str(max(y))
    meany = str(mean(y))

    centerName = file.split('/')[5]
    sampleName = file.split('/')[6]
    data_num = file.split('/')[-1][:-4]

    if centerName == "NASA":
        username = "Benjamin A. Kowalski"
    elif centerName == "North Carolina State University":
        username = "Jacob Jones"
    else:
        username = "Anonymous"

    info = [centerName, username, sampleName, minx, maxx, miny, maxy, meany]

    datas_info[data_num] = info
    w2v_info.append([centerName, username, sampleName])


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


def main():
    # Trans raw data to x and y
    folder = sys.argv[1]
    files = utils.get_path(folder)

    i = 0
    for file in files:
        x, y = detect_x_y(file)

        output = file.replace("data", "xy", 1)
        filename = output.split("/")[-1]
        output = output.replace(filename, str(i) + ".txt", 1)
        utils.ptint_xy(x, y, output)
        print(str(i) + '\t' + file)
        data_info(x, y, output)

        i += 1

    # Training w2v model for datasets
    w2v_data = Word2Vec(w2v_info, vector_size=5, min_count=1, window=3, sg=1, workers=4)
    w2v_data.save('./289/w2v_data')

    # Output into node.txt
    with open('289/input/node.txt', 'a+') as f:
        for key in datas_info:
            w2v_vec = get_vec_mean(datas_info[key][:3], 5, w2v_data)
            datas_info[key] = w2v_vec + datas_info[key][3:]

            f.write(key + '\t' + str(1) + '\t' + str(datas_info[key]).replace("'", "") + '\n')


if __name__ == "__main__":
    main()
