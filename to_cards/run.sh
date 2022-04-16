#!/bin/bash

#python3 taskcard.py "Peak Finding" --input_format xrdml\
#                                   --output_format txt\
#                                   --input_parameters positions intensities\
#                                   --ouput_parameters peaklist


python3 modelcard.py --modelName peakfinding_scipy\
                     --modelLocation ../data/model/peakfinding_scipy.py\
                     --inputFormat xrdml\
                     --outputFormat txt\
                     --inputParameters positions intensities\
                     --outputParameters peaklist\
                     --taskName "Peak Finding"


