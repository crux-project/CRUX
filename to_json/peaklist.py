from __future__ import division, print_function
import json
import os
import sys
import numpy as np
from scipy.signal import find_peaks
import trans2json as trans

# Arguments
GSASII_path = '/Users/mandy/g2full/GSASII'
project = 'pkfit.gpx'
dataset = 'MnO2_Unmilled_Air_InitialScan.xrdml'
instrument = 'NC_Empyrean.prm'
refined_output = 'pkfit.txt'
auto_output = 'pkauto.txt'
datadir = "./test/peaklist"
tthetas = [29, 37, 57, 60]
PathWrap = lambda fil: os.path.join(datadir, fil)

# Peak fitting by auto search
json_file = trans.xml2json(PathWrap(dataset))
f = open(json_file)
res = f.read()
f.close()
dic = json.loads(res)
# todo: search key/value in json tree
dp = dic["xrdMeasurements"]["xrdMeasurement"]["scan"]["dataPoints"]
y = dp["intensities"]["#text"]
y = list(map(int, y.split()))
sp = float(dp["positions"][0]["startPosition"])
ep = float(dp["positions"][0]["endPosition"])
x = np.arange(sp, ep, (ep - sp) / len(y))
peaks, _ = find_peaks(y)
f = open(PathWrap(auto_output), 'w')
for peak in peaks:
    f.write(str(x[peak]) + '\n')
f.close()

# Load GSAS-II
sys.path.insert(0, GSASII_path)
import GSASIIscriptable as G2sc

# Create a GSAS-II project
gpx = G2sc.G2Project(newgpx=PathWrap(project))

# Add powder diffraction datasets (histograms) to the project
hist = gpx.add_powder_histogram(PathWrap(dataset), PathWrap(instrument))

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
hist.Export_peaks(PathWrap(refined_output))

# Save GSAS-II project
gpx.save()
