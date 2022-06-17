# -*- codingL utf-8 -*-
# @Time : 6/8/22 3:47 PM
# @Author : YIYANG BIAN
# @File : pegasus_workflow.py

import logging
from pathlib import Path
from pegasus.api import *

logging.basicConfig(level=logging.DEBUG)

# --- Specify Input Files -----------


# --- Specify Executables -----------
generate_sourcecard = Transformation(
    name="generate_source",
    site="local",
    pfn="/Users/bianyiyang/airflow/dags/CRUX/workflow_pegasus/generate_source.py",
    is_stageable=True,
)

generate_datacard = Transformation(
    name="generate_datacard",
    site="local",
    pfn="/Users/bianyiyang/airflow/dags/CRUX/workflow_pegasus/generate_datacard.py",
    is_stageable=True,
)

generate_taskcard = Transformation(
    name="generate_taskcard",
    site="local",
    pfn=Path(".").resolve() / "CRUX/to_cards/taskcard.py",
    is_stageable=True,
)

generate_modelcard = Transformation(
    name="modelcard.py",
    site="local",
    pfn=Path(".").resolve() / "CRUX/to_cards/modelcard.py",
    is_stageable=True,
)

generate_testcard = Transformation(
    name="testcard.py",
    site="local",
    pfn=Path(".").resolve() / "CRUX/to_cards/testcard.py",
    is_stageable=True,
)

generate_performancecard = Transformation(
    name="performance.py",
    site="local",
    pfn=Path(".").resolve() / "CRUX/to_cards/performance.py",
    is_stageable=True,
)

generate_ranking = Transformation(
    name="ranking.py",
    site="local",
    pfn=Path(".").resolve() / "CRUX/to_cards/ranking.py",
    is_stageable=True,
)


tc = TransformationCatalog().add_transformations(generate_sourcecard,generate_datacard,generate_taskcard,generate_modelcard,generate_testcard,generate_performancecard,generate_ranking)

# --- Build Workflow ---------------
wf = Workflow("peakfinding-workflow")

fa = File("f.a")
fb = File("f.b")
peakfinding_job1 = Job(generate_sourcecard).add_args("-a","generate_soucrcecard","-T","3","-i",fa,"-o",fb).add_inputs(fa).add_outputs(fb)

fc = File("f.c")
peakfinding_job2 = Job(generate_datacard).add_args("-a","generate_datacard","-T","3","-i",fb,"-o",fc).add_inputs(fb).add_outputs(fc)

fd = File("f.d")
peakfinding_job3 = Job(generate_taskcard).add_args("-a","generate_taskcard","-T","3","-i",fc,"-o",fd).add_inputs(fc).add_outputs(fd)

fe = File("f.e")
peakfinding_job4 = Job(generate_modelcard).add_args("-a","generate_modelcard","-T","3","-i",fd,"-o",fe).add_inputs(fd).add_outputs(fe)

ff = File("f.f")
peakfinding_job5 = Job(generate_testcard).add_args("-a","generate_testcard","-T","3","-i",fe,"-o",ff).add_inputs(fe).add_outputs(ff)

fg = File("f.g")
peakfinding_job6 = Job(generate_performancecard).add_args("-a","generate_performancecard","-T","3","-i",ff,"-o",fg).add_inputs(ff).add_outputs(fg)

fh = File("f.h")
peakfinding_job7 = Job(generate_ranking).add_args("-a","generate_rankingcard","-T","3","-i",fg,"-o",fh).add_inputs(fg).add_outputs(fh)

wf.add_transformation_catalog(tc)
wf.add_jobs(peakfinding_job1, peakfinding_job2,peakfinding_job3,peakfinding_job4,peakfinding_job5,peakfinding_job6,peakfinding_job7)

try:
    wf.write()
    wf.graph(include_files=True, label="xform-id", output="graph.png")
except PegasusClientError as e:
    print(e)

# view rendered workflow
from IPython.display import Image
Image(filename='graph.png')

# Run the Workflow
try:
    wf.plan(submit = True)\
        .wait()
except PegasusClientError as e:
    print(e)