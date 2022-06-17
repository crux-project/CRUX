import os

cmd = "cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 datacard.py -file " \
      "'../content/data/xrdml/NASA/BZnZr - BIn - BSc - PT/2.5Bi(Zn0.5Zr0.5)O3 - 5BiInO3 - 32.5BiScO3 - " \
      "60PbTiO3_1100C.xrdml' "
res = os.system(cmd)
