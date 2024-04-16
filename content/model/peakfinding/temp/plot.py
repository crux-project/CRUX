import numpy as np
import xmltodict
import matplotlib.pyplot as plt
import performance


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


def loadData(file):
    x = []
    # y = []

    f = open(file, 'r')
    lines = f.readlines()[1:-1]
    for line in lines:
        line = line.strip('\n').split('\t')
        x.append(line[0])
        # y.append(line[1])

    x = np.array(x).astype(float).tolist()
    # y = np.array(y).astype(float).tolist()

    return x


#def plot(rawdata, f1, f2, f3, f4, title):
def plot(title):
    # x, y = loadData(rawdata)
    x, y = detect_x_y("../../../data/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.xrdml")
    # x1 = [13.0294, 22.0414, 31.4344, 38.7316, 44.9809, 50.5253, 55.9744, 65.6342, 70.1497, 74.5509]
    # y1 = [1780, 7856, 15344, 4957, 3108, 1706, 3374, 1201, 696, 854]
    x1 = loadData("../../../groundtruth/xrdml/NASA/BCdT - PT/280.txt")
    y1 = np.interp(x1, x, y)
    x2 = loadData("280m.txt")
    y2 = np.interp(x2, x, y)
    x3 = loadData("280mm.txt")
    y3 = np.interp(x3, x, y)
    # x3, y3 = loadData(f3)
    # x4, y4 = loadData(f4)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("position", fontdict={'size':13})
    plt.ylabel("intensity", fontdict={'size':13})
    # plt.title(title, fontsize=15)
    # plt.plot(x, y, linestyle='--', alpha=0.5, linewidth=0.8)
    plt.plot(x, y, linestyle='--', alpha=0.4, linewidth=1.2)

    # plt.scatter(x1, y1, s=50, c='#FBBC05', label="Annotated by domain expert")
    plt.scatter(x1, y1, s=40,  c='#689F38', alpha=1, marker="d", label="Annotated by domain expert")
    # plt.scatter(x2, y2, s=30, c='#4285F4', marker="d", label="25")
    # plt.scatter(x2, y2, s=35, c='#34A853', marker="x", label="30")
    plt.scatter(x2, y2, s=30, c='#FF5722', alpha=1, marker="x", label="ModsNet")
    plt.scatter(x3, y3, s=25, c='#4285F4', marker="+", label="Linear Regression")
    # plt.scatter(x1, y1, s=30, c='#EA4336', marker="+")
    plt.legend(loc="best", prop={'size':12})
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # plt.scatter(x1+x2+x3+x4, y1+y2+y3+y4, c="r", alpha=0.4)
    plt.savefig("test.svg", dpi=300)
    plt.show()
    print(performance.generate_matric(x1, x3, 0.1))


def main():
    rawdata = "../testdata/list.txt"

    # ptitle = "Peak Results by Peakutils"
    # pf150 = "../../../test/pf_peakutils_dist150/xrdml/NASA/BCdT - PT/280.txt"
    # pf200 = "../../../test/pf_peakutils_dist200/xrdml/NASA/BCdT - PT/280.txt"
    # pf250 = "../../../test/pf_peakutils_dist250/xrdml/NASA/BCdT - PT/280.txt"
    # pf300 = "../../../test/pf_peakutils_dist300/xrdml/NASA/BCdT - PT/280.txt"
    # plot(rawdata, pf150, pf200, pf250, pf300, ptitle)

    # stitle = "Peak Results by Scipy"
    # sf150 = "../../../test/pf_scipy_dist150/xrdml/NASA/BCdT - PT/280.txt"
    # sf200 = "../../../test/pf_scipy_dist200/xrdml/NASA/BCdT - PT/280.txt"
    # sf250 = "../../../test/pf_scipy_dist250/xrdml/NASA/BCdT - PT/280.txt"
    # sf300 = "../../../test/pf_scipy_dist300/xrdml/NASA/BCdT - PT/280.txt"
    # plot(rawdata, sf150, sf200, sf250, sf300, stitle)

    title = "Peak Results(F1_score=0.82759)"
    sf200 = "../testdata/ps_200.txt"
    sf300 = "../testdata/ps_300.txt"
    sf400 = "../testdata/ps_400.txt"
    sf1000 = "../testdata/ps_1000.txt"
    plot(title)

    # sf300 = "../testdata/ps_1000.txt"
    # plot(rawdata, sf300, stitle)

if __name__ == '__main__':
    main()