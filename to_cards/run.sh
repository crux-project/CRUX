#!/bin/bash
echo "Step 1/4 - Generating Datacards......"
python3 datacard.py


echo "Step 2/4 - Generating Taskcards......"
python3 taskcard.py peak_finding --input_format xrdml\
                                   --output_format txt\
                                   --input_parameters positions intensities\
                                   --output_parameters peaklist


echo "Step 3/4 - Generating Modelcards......"
python3 modelcard.py --modelName peakfinding_scipy\
                     --modelLocation ../data/model/peakfinding_scipy.py\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --taskName peak_finding


python3 modelcard.py --modelName peakfinding_peakutils\
                     --modelLocation ../data/model/peakfinding_peakutils.py\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --taskName peak_finding


echo "Step 4/4 - Generating Testcards......"
python3 testcard.py