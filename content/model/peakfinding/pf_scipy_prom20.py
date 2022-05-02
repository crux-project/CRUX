import xmltodict
import numpy as np
from scipy.signal import find_peaks
import sys
import os


def peak_finding(input, output="../testdata/pk_scipy.txt"):
    """
    :param input: Path to XRDML file.
    :param output: Path to the output txt file.
    :return: Peaklist with positions and intensities
    """

    x, y = detect_x_y(input)
    peaks, _ = find_peaks(y, prominence=20)
    peak_position = []
    peak_intensity = []

    index = output.rfind("/") + 1
    if not os.path.exists(output[:index]):
        os.makedirs(output[:index])

    f = open(output, 'w')
    f.write('pos' + '\t' + 'int')

    for peak in peaks:
        position = format(x[peak], '.4f')
        intensity = format(y[peak], '.2f')
        peak_position.append(position)
        peak_intensity.append(intensity)
        f.write('\n' + str(position) + '\t' + str(intensity))
    f.close()

    return peak_position, peak_intensity


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


def main():
    # input = "../content/data/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.xrdml"
    # input = "../content/data/xrdml/NC-State/CaCO3-TiO2/Single scan HTK1200_1100鳦_121.XRDML"
    # input = "../content/data/xrdml/NC-State/Mn-O/MnO2_Unmilled_Air_25to1100øC.XRDML"
    # input = "../content/data/xrdml/UNSW/A Basic Calibration BBHD Program-3_1.xrdml"
    # output = "../testdata/ps_1000.txt"
    input = sys.argv[1]
    output = sys.argv[2]
    peak_finding(input, output)


if __name__ == "__main__":
    main()
