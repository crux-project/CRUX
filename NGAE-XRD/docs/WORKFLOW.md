# Workflow map

This package mirrors the implemented Chapter 6 flow:

1. CSV ingest
2. Simulation of paired 1D profiles (sigma=0.01 clean, sigma=0.05 noisy)
3. Recurrence-plot transform via pyts
4. NGAE training/inference
5. LSD line-segment extraction and 2theta mapping
6. Evaluation by matched fraction

Use `ngae_xrd.pipeline.run_pipeline` or `scripts/run_pipeline.py` to orchestrate.
