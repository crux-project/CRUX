#!/bin/bash

python3 taskcard.py peak_finding --input_format xrdml\
                                   --output_format txt\
                                   --input_parameters positions intensities\
                                   --output_parameters peaklist


python3 modelcard.py --modelName peakfinding_scipy\
                     --modelLocation ../data/model/peakfinding_scipy.py\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --taskName peak_finding


