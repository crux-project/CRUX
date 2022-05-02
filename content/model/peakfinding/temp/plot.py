import numpy as np
import matplotlib.pyplot as plt


def loadData(flie):
    x = []
    y = []

    f = open(flie, 'r')
    lines = f.readlines()[1:]
    for line in lines:
        line = line.strip('\n').split('\t')
        x.append(line[0])
        y.append(line[1])

    x = np.array(x).astype(float).tolist()
    y = np.array(y).astype(float).tolist()

    return x, y


def plot(rawdata, f1, f2, f3, f4, title):
    x, y = loadData(rawdata)
    x1, y1 = loadData(f1)
    x2, y2 = loadData(f2)
    x3, y3 = loadData(f3)
    x4, y4 = loadData(f4)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("position")
    plt.ylabel("intensity")
    plt.title(title, fontsize=13.5)
    plt.plot(x, y, linestyle='--', alpha=0.5, linewidth=0.8)

    plt.scatter(x1, y1, s=50, c='#FBBC05', label="20")
    plt.scatter(x2, y2, s=30, c='#4285F4', marker="d", label="25")
    plt.scatter(x3, y3, s=35, c='#34A853', marker="x", label="30")
    plt.scatter(x4, y4, s=25, c='#EA4336', marker="+", label="40")
    plt.legend(loc="best")

    # plt.scatter(x1+x2+x3+x4, y1+y2+y3+y4, c="r", alpha=0.4)
    # plt.savefig("../testdata/test.png")
    plt.show()


def main():
    rawdata = "../testdata/ncmolist.txt"

    # ptitle = "Peak Results by Peakutils"
    # pf150 = "../../../test/pf_peakutils_dist150/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # pf200 = "../../../test/pf_peakutils_dist200/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # pf250 = "../../../test/pf_peakutils_dist250/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # pf300 = "../../../test/pf_peakutils_dist300/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # plot(rawdata, pf150, pf200, pf250, pf300, ptitle)

    # stitle = "Peak Results by Scipy"
    # sf150 = "../../../test/pf_scipy_dist150/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # sf200 = "../../../test/pf_scipy_dist200/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # sf250 = "../../../test/pf_scipy_dist250/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # sf300 = "../../../test/pf_scipy_dist300/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.txt"
    # plot(rawdata, sf150, sf200, sf250, sf300, stitle)

    title = "Peak Results by Scipy with Various Prominence"
    sf200 = "../testdata/ps_200.txt"
    sf300 = "../testdata/ps_300.txt"
    sf400 = "../testdata/ps_400.txt"
    sf1000 = "../testdata/ps_1000.txt"
    plot(rawdata, sf200, sf300, sf400, sf1000, title)

    # sf300 = "../testdata/ps_1000.txt"
    # plot(rawdata, sf300, stitle)


if __name__ == '__main__':
    main()