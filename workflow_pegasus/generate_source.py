
import os
cmd = "cd /Users/bianyiyang/airflow/dags/CRUX/to_cards/ && python3 source.py --name 'Jacob L. Jones'\
                  --affiliation 'North Carolina State University'\
                  --positions 'Kobe Distinguished Professor, Materials Science and Engineering'\
                  --positions 'Director, Science and Technologies for Phosphorus Sustainability (STEPS) Center'\
                  --positions 'Director, Research Triangle Nanotechnology Network'\
                  --address '3072B Engineering Building I, Raleigh, NC'\
                  --phone 919-515-4557\
                  --email jacobjones@ncsu.edu && python3 source.py --name 'Mauro Sardela'\
                  --affiliation 'University of Illinois at Urbana-Champaign'\
                  --positions 'Director, Central Research Facilities, Materials Research Laboratory'\
                  --address '104 S. Goodwin Avenue – Urbana IL 61801'\
                  --website www.mrl.illinois.edu\
                  --phone 217-244-0547\
                  --email sardela@illinois.edu\
                  --office '#SC2014'"
res = os.system(cmd)