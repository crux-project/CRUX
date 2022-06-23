#!/bin/bash
#echo "Step 1 - Generating source infomation (user and center)......"
#python3 source.py --username "Jacob L. Jones"\
#                  --affiliation "NC-State"\
#                  --positions "Kobe Distinguished Professor, Materials Science and Engineering"\
#                  --positions "Director, Science and Technologies for Phosphorus Sustainability (STEPS) Center"\
#                  --positions "Director, Research Triangle Nanotechnology Network"\
#                  --address "3072B Engineering Building I, Raleigh, NC"\
#                  --phone 919-515-4557\
#                  --email jacobjones@ncsu.edu
#
#python3 source.py --username "Mauro Sardela"\
#                  --affiliation "UIUC"\
#                  --positions "Director, Central Research Facilities, Materials Research Laboratory"\
#                  --address "104 S. Goodwin Avenue – Urbana IL 61801"\
#                  --website www.mrl.illinois.edu\
#                  --phone 217-244-0547\
#                  --email sardela@illinois.edu\
#                  --office "#SC2014"
#
#python3 source.py --username "Benjamin A. Kowalski"\
#                  --affiliation "NASA"\
#                  --email benjamin.kowalski@nasa.gov
#
#python3 source.py --username "Anonymous"\
#                  --affiliation "UNSW"\
#
#python3 source.py --username "SciPy"\
#                  --affiliation "The SciPy community"\
#                  --website https://scipy.org\
#                  --email scipy-dev@python.org
#
#python3 source.py --username "PeakUtils"\
#                  --affiliation "The PeakUtils community"\
#                  --website https://peakutils.readthedocs.io\
#                  --email lucashnegri@gmail.com
#
#python3 source.py --username "Mengying Wang"\
#                  --affiliation "CWRU"\
#                  --website wangmengying.me\
#                  --email mxw767@case.edu
#
#
#echo "Step 2 - Generating data cards......"
#python3 datacard.py -folder "../content/data/xrdml/"
## python3 datacard.py -file "../content/data/xrdml/NC-State/CaCO3-TiO2/Single scan HTK1200_1100鳦_121.XRDML"
#
#
#echo "Step3 - Generating task cards......"
#python3 taskcard.py peak_finding --input_format xrdml\
#                                 --output_format txt\
#                                 --input_parameters positions intensities\
#                                 --output_parameters peaklist
#
#
#echo "Step 4 - Generating model cards......"
#python3 modelcard.py --modelName scipy.signal.find_peaks\
#                     --username "SciPy"\
#                     --license "BSD 3-Clause "New" or "Revised" License"\
#                     --modelDate 02/05/2022\
#                     --modelVersion 1.8.0\
#                     --modelType "Find peaks inside a signal based on peak properties."\
#                     --paperOrResource https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html\
#                     --modelLocation https://github.com/scipy/scipy/blob/v1.8.0/scipy/signal/_peak_finding.py#L723-L1003\
#                     --inputFormat nparray\
#                     --outputFormat nparray\
#                     --inputParameters x height threshold distance prominence width wlen rel_height plateau_size\
#                     --outputParameters peaks properties
#
#
#python3 modelcard.py --modelName peakutils.peak.index\
#                     --username "PeakUtils"\
#                     --license "MIT license"\
#                     --modelDate 01/23/2020\
#                     --modelVersion 1.3.3\
#                     --modelType "Peak detection routine."\
#                     --paperOrResource https://peakutils.readthedocs.io/en/latest/reference.html#module-peakutils.peak\
#                     --modelLocation https://bitbucket.org/lucashnegri/peakutils\
#                     --dependencies numpy scipy\
#                     --inputFormat nparray\
#                     --outputFormat nparray\
#                     --inputParameters y thres min_dist thres_abs\
#                     --outputParameters "Array containing the numeric indexes of the peaks that were detected."
#
#python3 modelcard.py --modelName Jade\
#                     --inputFormat xrdml\
#                     --outputFormat txt\
#                     --outputParameters peaklist\
#                     --taskName peak_finding
#
#for distance in 150 200 250 300
#do
#python3 modelcard.py --modelName pf_scipy_dist$distance\
#                     --username "Mengying Wang"\
#                     --modelLocation ../content/model/peakfinding/pf_scipy_dist$distance.py\
#                     --dependencies scipy.signal.find_peaks\
#                     --inputFormat xrdml\
#                     --outputFormat txt\
#                     --inputParameters positions intensities\
#                     --outputParameters peaklist\
#                     --hyperParameters min_dist=$distance\
#                     --taskName peak_finding
#
#python3 modelcard.py --modelName pf_peakutils_dist$distance\
#                     --username "Mengying Wang"\
#                     --modelLocation ../content/model/peakfinding/pf_peakutils_dist$distance.py\
#                     --dependencies peakutils.peak.index\
#                     --inputFormat xrdml\
#                     --outputFormat txt\
#                     --inputParameters positions intensities\
#                     --outputParameters peaklist\
#                     --hyperParameters thres=0.02/max\(intensities\) distance=$distance\
#                     --taskName peak_finding
#done
#
#
#for prominence in 20 30 40 200 300 400 1000
#do
#python3 modelcard.py --modelName pf_scipy_prom$prominence\
#                     --username "Mengying Wang"\
#                     --modelLocation ../content/model/peakfinding/pf_scipy_prom$prominence.py\
#                     --dependencies scipy.signal.find_peaks\
#                     --inputFormat xrdml\
#                     --outputFormat txt\
#                     --inputParameters positions intensities\
#                     --outputParameters peaklist\
#                     --hyperParameters prominence=$prominence\
#                     --taskName peak_finding
#done
#
#
echo "Step 5 - Generating test cards......"
python3 testcard.py peak_finding
# python3 testcard.py peak_finding -m pf_scipy_prom200 -d "../content/data/xrdml/NASA/BCdT - PT/10Bi(Cd0.5Ti0.5)O3 - 90PbTiO3 - 1100C.xrdml"


echo "Step 6 - Generating performance (Allowed error: 0.01)......"
python3 performance.py 0.01


echo "Step 7 - Generating ranking lists......"
python3 ranking.py


