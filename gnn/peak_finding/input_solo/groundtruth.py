import sys
from scipy.signal import find_peaks

sys.path.append('../../..')
import crux_ie.utils as utils


def get_model(input):
    sampleName = input.split('/')[6]

    if sampleName in ["BCdT - PT", "BSc - PT", "BZnV - BSc - PT"]:
        gt_model = "Jade"
    elif sampleName == "CaCO3-TiO2":
        gt_model = 30
    elif sampleName == "Mn-O":
        gt_model = 40
    else:
        gt_model = 30

    return gt_model


def peak_finding(input, p):
    """
    :param input: Path to XRDML file.
    :return: Peaklist with positions and intensities
    """
    x, y = utils.get_xy(input)
    peaks, _ = find_peaks(y, prominence=p)
    peak_position = []
    peak_intensity = []

    for peak in peaks:
        position = format(x[peak], '.4f')
        intensity = format(y[peak], '.2f')
        peak_position.append(position)
        peak_intensity.append(intensity)

    return peak_position, peak_intensity


def jade_pos(file):
    pos = []
    f = open(file, 'r')
    lines = f.readlines()[3:][:-3]

    for line in lines:
        line = line.strip('\n').split('\t')
        pos.append(line[1])

    pos = [float(x) for x in pos] if pos != [''] else []

    return pos


def get_gt(gt_model, file):
    if gt_model == "Jade":
        file = file.replace("xy", "Jad1", 1)
        x = jade_pos(file)
        y = []
    else:
        x, y = peak_finding(file, gt_model)

    return x, y


def main():
    folder = sys.argv[1]
    files = utils.get_path(folder)

    for file in files:
        gt_model = get_model(file)
        x, y = get_gt(gt_model, file)

        output = file.replace("xy", "groundtruth", 1)
        utils.ptint_xy(x, y, output)


if __name__ == "__main__":
    main()
