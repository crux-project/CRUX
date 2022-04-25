#!/bin/bash
echo "Step 1/4 - Generating data cards......"
python3 datacard.py


echo "Step 2/4 - Generating task cards......"
python3 taskcard.py peak_finding --input_format xrdml\
                                 --output_format txt\
                                 --input_parameters positions intensities\
                                 --output_parameters peaklist


echo "Step 3/4 - Generating model cards......"
python3 modelcard.py --modelName scipy.signal.find_peaks\
                     --affiliation "The SciPy community"\
                     --contactInfo "scipy-dev@python.org"\
                     --license "BSD 3-Clause "New" or "Revised" License"\
                     --modelDate 02/05/2022\
                     --modelVersion 1.8.0\
                     --modelType "Find peaks inside a signal based on peak properties."\
                     --paperOrResource https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html\
                     --modelLocation https://github.com/scipy/scipy/blob/v1.8.0/scipy/signal/_peak_finding.py#L723-L1003\
                     --inputFormat nparray\
                     --outputFormat nparray\
                     --inputParameters x height threshold distance prominence width wlen rel_height plateau_size\
                     --outputParameters peaks properties


python3 modelcard.py --modelName peakutils.peak.index\
                     --username "Lucas Hermann Negri"\
                     --contactInfo "lucashnegri@gmail.com"\
                     --license "MIT license"\
                     --modelDate 01/23/2020\
                     --modelVersion 1.3.3\
                     --modelType "Peak detection routine."\
                     --paperOrResource https://peakutils.readthedocs.io/en/latest/reference.html#module-peakutils.peak\
                     --modelLocation https://bitbucket.org/lucashnegri/peakutils\
                     --dependencies numpy scipy\
                     --inputFormat nparray\
                     --outputFormat nparray\
                     --inputParameters y thres min_dist thres_abs\
                     --outputParameters "Array containing the numeric indexes of the peaks that were detected."


for distance in 150 200 250 300
do
python3 modelcard.py --modelName peakfinding_scipy\
                     --modelLocation ../content/model/peakfinding/pf_scipy_dist$distance.py\
                     --dependencies scipy.signal.find_peaks\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --hyperParameters min_dist=$distance\
                     --taskName peak_finding

python3 modelcard.py --modelName peakfinding_peakutils\
                     --modelLocation ../content/model/peakfinding/pf_peakutils_dist$distance.py\
                     --dependencies peakutils.peak.index\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --hyperParameters thres=0.02/max\(intensities\) distance=$distance\
                     --taskName peak_finding
done


echo "Step 4/4 - Generating testdata cards......"
python3 testcard.py peak_finding