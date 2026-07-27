# Experiment card

## Synthetic benchmark

- Plant: differential-drive/unicycle, 0.1 s integration.
- Controller: pure pursuit; controller acts on the observer estimate.
- Sensors: noisy biased odometry and range-bearing observations to a known map.
- Intermittency: periodic complete blackouts plus active-landmark sparsity.
- Main observers: dead reckoning, EKF, GRU-DR, selective SSM-DR, SSM-EKF, GRU-EKF.
- Conditions: 4 axes x 6 levels = 24 conditions.
- Evaluation randomness: 10 seeds per observer-condition.
- Training: 200 simulated trajectories x 200 steps; three initializations evaluated for SSM-EKF.

## Offline model-selection proxies

- Position RMSE.
- Heading RMSE.
- Exact normalized controller-command disagreement.
- Local Control Sensitivity Error (LCSE): controller Jacobian times pose error.
- Counterfactual Error Replay: shadow dynamics driven by logged error traces.

## Decision metrics

- Global and within-condition rank correlation.
- Top-1 winner disagreement.
- Selection regret: closed-loop cost of the proxy-selected observer minus the oracle closed-loop cost.
- Paired bootstrap over conditions.

## Physical dataset

- Dataset: UTIAS MRCLAM Dataset 1, Robot 1.
- Raw segment: 600 s, 6,000 aligned 0.1 s steps.
- Available map: 15 static landmarks.
- Physical observations used: 1,878 landmark measurements.
- Ground truth: Vicon pose.
- Raw experiment: DR and EKF covariance variants on physical logs.
- Zero-shot stress test: original learned checkpoints on an eight-landmark subset without retraining.
- Calibrated replay: empirical odometry residuals, range-bearing residuals, and measurement counts/timing
  resampled into a simulated closed-loop plant.

## Scope boundaries

The raw MRCLAM evaluation is real-data localization, not real closed-loop control. The empirical replay
is not hardware-in-the-loop. It is intended to test whether conclusions survive more realistic sensor
statistics while retaining controlled closed-loop counterfactuals.

## Secondary controller sensitivity

- Controllers: pure pursuit and Kanayama.
- Matching: identical five evaluation seeds, plant, observer checkpoints, conditions, active-landmark draws, and actuator limits.
- Purpose: assess whether the best observer and replay-selection failure are controller-dependent.
- Output: `results/enhanced/second_controller_kanayama.json` plus seed-level JSONL.
- Scope: secondary synthetic sensitivity with fewer seeds than the primary study.
