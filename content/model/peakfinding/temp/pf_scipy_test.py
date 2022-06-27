import xmltodict
import numpy as np
from scipy.signal import find_peaks
import sys

sys.path.append('..')
import crux_ie.performance as performance


def peak_finding(input, dist, prom):
    x, y = detect_x_y(input)
    peaks, _ = find_peaks(y, distance=dist, prominence=prom)
    peak_position = []

    for peak in peaks:
        position = format(x[peak], '.4f')
        peak_position.append(float(position))

    return peak_position


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


def write_to_file(input, dist, prom, err, p, f):
    pp = peak_finding(input, dist, prom)
    tp = performance.intersection(p, pp, err)
    recall, precision, f1 = performance.f1_score(tp, len(p), len(pp))
    recall, precision, f1 = round(recall, 5), round(precision, 5), round(f1, 5)
    f.write("\n%-10s\t\t%-10s\t\t%-15s\t\t%-15s\t\t%-15s"
            % (str(dist), str(prom), str(recall), str(precision), str(f1)))


def main():
    input = "../content/data/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.xrdml"
    groundtruth = "../content/test/Jade/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    p = performance.get_pos(groundtruth)
    err = 0.005

    output = "../testdata/tune_para_" + str(err) + ".txt"
    f = open(output, 'w')
    f.write("XRDML file: " + input + '\n')
    f.write("Package: Scipy" + '\n')
    f.write("Allowed Error: " + str(err) + '\n')
    f.write("%-10s\t\t%-10s\t\t%-15s\t\t%-15s\t\t%-15s\n"
            % ("distance", "prominence", "recall", "precision", "f1_score") + "-" * 85)

    for dist in range(100, 351, 10):
        write_to_file(input, dist, None, err, p, f)
        for prom in range(100, 1001, 50):
            write_to_file(input, None, prom, err, p, f)
            write_to_file(input, dist, prom, err, p, f)
    f.close()


if __name__ == "__main__":
    main()
