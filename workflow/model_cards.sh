#!/bin/bash
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