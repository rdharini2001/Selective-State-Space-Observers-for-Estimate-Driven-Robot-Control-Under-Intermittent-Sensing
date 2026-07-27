# Submission-strengthening report

## What changed

The original project was framed as an architecture comparison centered on a compact selective SSM. The audited version is framed as an evaluation paper: **how should learned state observers be selected when their estimates drive a feedback controller?** This is a stronger and more reusable contribution because it produces a protocol, failure metrics, matched ablations, real-log stress tests, and code that other observer papers can adopt.

## Scientific corrections

1. The original 29% top-1 mismatch omitted GRU-EKF. With all six deployment candidates, replay position RMSE selects a different closed-loop winner in 5/24 conditions (20.8%).
2. The original selectivity and mask ablations changed the analytic anchor, confounding recurrence design with model-based stabilization. Same-EKF-anchor retraining shows regime-dependent effects rather than universal necessity.
3. The original compound-stress story was overstated. GRU-EKF is best in both replay and closed loop. The valid counterexample is within SSM-EKF: 43% lower replay RMSE than EKF with 10% worse closed-loop cross-track error.
4. The compact cell is described as a selective diagonal SSM inspired by S4/Mamba, not as a full Mamba block.
5. Training-seed uncertainty is reported separately from evaluation-seed uncertainty.

## New field-facing contributions

- Six-observer, 24-condition paired replay/closed-loop benchmark.
- Top-1 agreement, absolute regret, and relative regret as deployment-selection metrics.
- Three task-aware offline baselines: exact command disagreement, local controller-sensitivity error, and counterfactual error replay.
- Negative result: no tested log-only scalar consistently replaces actual rollouts.
- Matched EKF-anchor ablations for selectivity and measurement-mask input.
- Three SSM-EKF training initializations.
- Matched pure-pursuit/Kanayama sensitivity showing controller-dependent observer choice.
- UTIAS MRCLAM physical-log localization, zero-shot map-transfer stress test, and physical-residual-calibrated simulation.
- PyTorch training backend with legacy NumPy checkpoint export, regression tests, reproducible result JSON, and publication figures.

## Primary numbers safe to report

- Position RMSE vs. pure-pursuit closed-loop cross-track RMSE: Spearman 0.923; top-1 failures 5/24; mean regret 0.0051 m; maximum regret 0.0347 m.
- LCSE: 3/24 observed failures, but the paired condition-bootstrap interval for improvement overlaps zero; do not claim superiority.
- Matched nominal ablation: selective+mask 0.199 m, non-selective+mask 0.203 m, selective/no-mask 0.195 m.
- SSM-EKF training seeds: nominal 0.189-0.199 m; long blackout 0.231-0.336 m.
- Secondary matched controller sensitivity: oracle changes in 8/24 conditions; pose RMSE misselects 7/24 under Kanayama; maximum regret 0.092 m. This uses five seeds and must remain secondary.
- MRCLAM Robot 1, 600 s: 6,000 aligned steps and 1,878 landmark observations; dead reckoning 3.392 m and best tested 15-landmark EKF 1.357 m position RMSE.

## Claims to avoid

- The selective SSM is state of the art.
- Selectivity or explicit masks are universally necessary for stability.
- A controller-aware replay metric solves objective mismatch.
- MRCLAM-calibrated replay is a real closed-loop robot experiment.
- The current learned observer generalizes across maps or landmark order.
- Five evaluation seeds establish controller dependence precisely.

## Highest-value next work before a main-track submission

1. Replace ordered landmark slots with a permutation-invariant innovation-set encoder and train on randomized maps and landmark cardinalities.
2. Train every learned observer with at least five initialization seeds and use a hierarchical bootstrap over training seed, environment seed, and condition.
3. Extend the matched controller analysis to ten or more seeds, gain sweeps, and a third controller.
4. Evaluate multiple MRCLAM robots and datasets, including dataset 9 occlusions, with train-on-one/test-on-another experiments.
5. Add a ROS/Gazebo timing/actuator study or a small physical closed-loop demonstration.

## Recommended paper choice

Use `paper/Replay_Accuracy_Not_Enough_NeurIPS2026_Workshop_4pp.pdf` for the workshop submission. Use the expanded audit draft and the full result package for supplementary material and rebuttal preparation.
