#!/bin/bash
python3 taskcard.py peak_finding --input_format xrdml\
                                 --output_format txt\
                                 --input_parameters positions intensities\
                                 --output_parameters peaklist