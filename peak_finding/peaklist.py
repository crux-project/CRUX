from __future__ import division, print_function
import sys
import os
import numpy as np
from scipy.signal import find_peaks


# Arguments
GSASII_path = '/Users/mandy/g2full/GSASII'
project = 'pkfit.gpx'
instrument = 'NC_Empyrean.prm'
refined_output = 'pkfit.txt'
tthetas = [29, 37, 57, 60]
datadir = "../data"
PathWrap = lambda fil: os.path.join(datadir, fil)


# auto search by Scipy
def auto_finding(dic, output):
    # todo: search key/value in json tree
    dp = dic["xrdMeasurements"]["xrdMeasurement"]["scan"]["dataPoints"]
    y = dp["intensities"]["#text"]
    y = list(map(int, y.split()))
    sp = float(dp["positions"][0]["startPosition"])
    ep = float(dp["positions"][0]["endPosition"])
    x = np.arange(sp, ep, (ep - sp) / len(y))
    peaks, _ = find_peaks(y)
    peak_position = []
    peak_intensity = []
    f = open(output, 'w')
    f.write('pos' + '\t' + 'int' + '\t' + '\n')

    for peak in peaks:
        position = format(x[peak], '.4f')
        intensity = format(y[peak], '.2f')
        peak_position.append(position)
        peak_intensity.append(intensity)
        f.write(str(position) + '\t' + str(intensity) + '\t' + '\n')
    f.close()

    return peak_position, peak_intensity


# Validate peaklist with GSAS-II
def val_with_gsas2(gsas2_peak_file, our_pos, our_int):
    f = open(gsas2_peak_file)
    line = f.readline()
    count = 1
    peak_position = []
    peak_intensity = []

    while line:
        if count <= 3:
            count += 1
            line = f.readline()
            continue
        a = line.split()
        position = format(float(a[0]), '.4f')
        intensity = format(float(a[3]), '.2f')
        peak_position.append(position)
        peak_intensity.append(intensity)
        line = f.readline()
    f.close()

    count = 0
    err = 0.1
    for i in range(len(peak_position)):
        for j in range(len(our_pos)):
            diff = abs(float(peak_position[i]) - float(our_pos[j]))
            if diff < err and peak_intensity[i] == our_int[j]:
                count += 1
                break

    print("GSAS-II got %d peaks, we detected %d peaks, %d of them are overlap. "
          "(Allowed error in position: %.2f)"
          %(len(peak_position), len(our_pos), count, err))


def GSAS2(xrdml_file, instrument, output):
    # Load GSAS-II
    sys.path.insert(0, GSASII_path)
    import GSASIIscriptable as G2sc

    # Create a GSAS-II project
    gpx = G2sc.G2Project(newgpx=PathWrap(project))

    # Add powder diffraction datasets (histograms) to the project
    hist = gpx.add_powder_histogram(xrdml_file, instrument)

    # Refine peaks
    for i in range(len(tthetas)):
        hist.add_peak(1, ttheta=tthetas[i])
    hist.set_peakFlags(area=True)
    hist.refine_peaks()
    hist.set_peakFlags(area=True, pos=True)
    hist.refine_peaks()
    hist.set_peakFlags(area=True, pos=True, sig=True, gam=True)
    hist.refine_peaks()

    # Export peak list
    hist.Export_peaks(output)

    # Save GSAS-II project
    gpx.save()
