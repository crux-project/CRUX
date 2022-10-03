import numpy as np
import sys
import time
import peakutils.peak as peakutils_peaks
from scipy.signal import find_peaks as scipy_peaks
from sklearn.model_selection import ParameterGrid

sys.path.append('../..')
import crux_ie.performance as performance
import crux_ie.utils as utils


# Get peak list by Scipy/Peakutils
def get_peaklist(txt_file, model, **kwargs):
    x, y = utils.get_xy(txt_file)

    if model == "Scipy":
        peaks, _ = scipy_peaks(y, **kwargs)

    if model == "Peakutils":
        peaks = peakutils_peaks.indexes(np.array(y), **kwargs)

    peak_position = []
    peak_intensity = []

    for peak in peaks:
        position = format(x[peak], '.4f')
        intensity = format(y[peak], '.2f')
        peak_position.append(position)
        peak_intensity.append(intensity)

    peak_position = [float(i) for i in peak_position] \
        if peak_position != [''] else []
    peak_intensity = [float(i) for i in peak_intensity] \
        if peak_intensity != [''] else []

    return peak_position, peak_intensity


# Generate parameter grid
def grid_para(model):
    if model == "Scipy":
        param_grid = {
            'distance': [1, 100, 150, 200, 250, 300, 350],
            'prominence': [0, 20, 30, 40, 200, 300, 400, 1000],
            'threshold': [0, 0.5],
            'height': [0, 50],
            'width': [0, 5]
        }
    elif model == "Peakutils":
        param_grid = {
            'min_dist': [1, 100, 150, 200, 250, 300, 350],
            'thres': [0.3, 0.7]
        }

    return list(ParameterGrid(param_grid))


# Add metrics based on groundtruth and prediction.
def get_performance(gt, pred, metrics, err):
    tp = performance.intersection(gt, pred, err)

    recall, precision, f1 = performance.f1_score(tp, len(gt), len(pred))

    metrics["F1_score"] = f1
    metrics["precision"] = precision
    metrics["recall"] = recall
    metrics["cosineSimilarity"] = performance.cosine_similarity(gt, pred)
    metrics["jaccardSimilarity"] = performance.jaccard_similarity(gt, pred, tp)


# Execute peak finding algorithm
def execute(file, model, gt, parameter):
    metrics = {}

    start = time.time()
    position, intensity = get_peaklist(file, model, **parameter)
    end = time.time()

    metrics["runningTime(s)"] = end - start
    get_performance(gt, position, metrics, 0.01)

    return metrics


def get_model_info(model, para):
    scipy_ast = [0.12365612242138013, 0.1071741455089068,
                 -0.12319925657357089, 0.16431758872931823]
    peakutils_ast = [0.12472915911348537, 0.10950502653577132,
                     -0.1329570177476853, 0.16341272392310202]

    # Information for model title
    model_info = [0] if model == "Peakutils" else [1]

    # Information for ast
    if model == "Peakutils":
        model_info += peakutils_ast
    elif model == "Scipy":
        model_info += scipy_ast

    # Information for parameters
    if model == "Peakutils":
        model_info += [para['min_dist'], para['thres'], 0, 0, 0]
    elif model == "Scipy":
        model_info += [para['distance'], para['threshold'],
                       para['prominence'], para['height'],
                       para['width']]

    return model_info


def main():
    folder = sys.argv[1]
    # model = sys.argv[2]
    files = utils.get_path(folder)
    models_info = {}

    for file in files:
        gt_path = file.replace("xy", "groundtruth", 1)
        gt_pos, gt_int = utils.get_xy(gt_path)
        data_num = file.split('/')[-1][:-4]

        i = 289
        for model in ["Peakutils", "Scipy"]:
            for parameter in grid_para(model):
                # Information for model
                model_info = get_model_info(model, parameter)
                models_info[i] = model_info

                # Information for performance
                metrics = execute(file, model, gt_pos, parameter)

                # Delete tests without performance
                if sum(list(metrics.values())[1:]) == 0:
                    continue

                print("(" + str(i) + "," + str(data_num) + ")" + '\t' + str(metrics.values())[12:-1])
                i += 1

    # Output into node.txt
    with open('./289/input/node.txt', 'a+') as f:
        for key in models_info.keys():
            f.write(str(key) + '\t' + str(0) + '\t' + str(models_info[key]).replace("'", "") + '\n')


if __name__ == "__main__":
    main()
