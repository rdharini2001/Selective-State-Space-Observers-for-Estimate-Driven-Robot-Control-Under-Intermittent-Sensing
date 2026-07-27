# Changelog

## v0.2.0 - audited strong-submission package

- Corrected principal observer set to include GRU-EKF.
- Corrected winner mismatch from 29% to 20.8%.
- Added controller disagreement, LCSE, counterfactual error replay, selection regret, and bootstrap analysis.
- Added matched EKF-anchor no-selectivity and no-mask models and experiments.
- Added PyTorch trainer with legacy NumPy checkpoint export.
- Added three-seed SSM-EKF robustness study.
- Added a matched five-seed pure-pursuit/Kanayama controller-dependence sensitivity with paired bootstrap.
- Added UTIAS MRCLAM loader, physical-log experiment, empirical-noise replay, and zero-shot transfer stress test.
- Added tests, enhanced figures, experiment/audit documentation, and revised NeurIPS manuscript.
- Removed unsupported claims that mask awareness/selectivity is universally necessary.
