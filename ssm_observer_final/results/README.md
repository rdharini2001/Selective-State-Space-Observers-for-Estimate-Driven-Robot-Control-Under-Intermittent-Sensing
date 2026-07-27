# Results directory

Use `enhanced/` for all paper claims in the revised submission.

The JSON files directly under `results/` are retained from the original project because several
reproduction scripts use their seed-level sweep summaries. In particular, `objective_mismatch.json`
is a **legacy five-observer analysis** and must not be used for the revised headline statistic.
The corrected six-observer selection analysis is `enhanced/proxy_analysis.json`.

`models/ssm_dr_nosel*` and `models/ssm_dr_nomask*` are the original confounded DR-anchor ablations.
The matched same-EKF-anchor checkpoints are `models/ssm_ekf_nosel*` and
`models/ssm_ekf_nomask*` and are the only selectivity/mask ablations used by the revised paper.
