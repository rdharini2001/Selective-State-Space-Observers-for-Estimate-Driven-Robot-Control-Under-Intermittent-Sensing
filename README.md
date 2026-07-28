# ECE 6562 Final Project

## Closed-Loop Evaluation of Robot State Observers Under Intermittent Sensing

**Student:** Dharini Raghavan (`draghavan7`)  
**Course:** ECE 6562 - Autonomous Control of Robotic Systems, Summer 2026

This project studies a practical model-selection question: an observer may estimate a robot pose accurately on a fixed log, but will it still give the best trajectory tracking after its estimate is placed inside a feedback controller?

A differential-drive robot tracks a figure-eight path using pure-pursuit control. The robot receives biased wheel odometry and intermittent range-bearing measurements to known landmarks. Six observers are compared:

1. dead reckoning;
2. an extended Kalman filter (EKF);
3. a GRU residual on dead reckoning;
4. a selective state-space residual on dead reckoning;
5. a GRU residual on the EKF; and
6. a selective state-space residual on the EKF.

The main experiments vary blackout duration, range noise, landmark availability, and gyroscope bias. Every condition is evaluated with common random seeds in both open-loop replay and closed-loop control. The repository also contains matched ablations, training-seed checks, a second-controller sensitivity study, and a physical-log extension using UTIAS MRCLAM.

## Main result

Replay position RMSE is a useful screening metric, but it is not a complete deployment criterion. Across six observers and 24 operating conditions, it has a global Spearman correlation of 0.923 with closed-loop cross-track RMSE, yet it selects a different closed-loop winner in 5 of 24 conditions. The strongest and most consistent design choice is the analytic EKF anchor; the benefit of selectivity depends on the sensing regime.

## Submission contents

```text
report/
  ECE6562_Final_Project_Report.pdf   final course report
  ECE6562_Final_Project_Report.tex   report source
  references.bib                    bibliography

demo/
  nominal_tracking.mp4              nominal simulation clip
  blackout_tracking.mp4             long-blackout simulation clip
  demo_trajectory.gif               short looping preview
  VIDEO_SCRIPT.md                   exact 5-7 minute narration and visuals

src/ssm_obs/                        simulation, observers, controllers, metrics
scripts/                            training, evaluation, plotting, and checks
tests/                              regression tests
results/reference/                  audited results used in the report
results/models/                     bundled observer checkpoints
figures/                            report-ready figures
```

## Installation

Python 3.10-3.12 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## One-command verification

The following command runs the tests, performs a fresh closed-loop smoke experiment, verifies every reported result file, checks the report and video assets, and prints a submission summary:

```bash
bash reproduce.sh
```

This is the command the grader should use first. It normally finishes in under two minutes because the trained checkpoints and audited result files are included.

## Full experimental reproduction

To rerun the complete simulation study from the bundled checkpoints:

```bash
bash reproduce.sh --full
```

This command reruns the nominal experiment, all four degradation sweeps, the corrected observer-selection analysis, matched ablations, training-seed evaluation, figures, and demo clips. Runtime depends on the machine.

To retrain all recurrent observers before evaluation:

```bash
bash reproduce.sh --train --full
```

## Useful individual commands

```bash
# Unit and regression tests
pytest -q

# Fresh nominal and degradation evaluation
PYTHONPATH=src NSEED=10 python scripts/run_eval.py all

# Corrected six-observer selection analysis
PYTHONPATH=src python scripts/run_proxy_analysis.py --seeds 10 --bootstrap 3000

# Same-anchor selectivity and measurement-mask ablations
PYTHONPATH=src python scripts/run_matched_ablation.py

# Three independently trained SSM-EKF checkpoints
PYTHONPATH=src python scripts/run_ssm_training_seed_eval.py

# Secondary Kanayama-controller sensitivity
PYTHONPATH=src python scripts/run_second_controller.py --seeds 5

# Regenerate video clips
PYTHONPATH=src python scripts/make_demo_assets.py
```

## Physical-log extension

The raw UTIAS MRCLAM data are not redistributed. Download and evaluate Robot 1 with:

```bash
python scripts/download_mrclam.py --output data/external/MRCLAM_Dataset1 --robots 1
PYTHONPATH=src python scripts/run_mrclam.py \
  --data-dir data/external/MRCLAM_Dataset1 \
  --robot 1 --duration 600 --seeds 12 --replay-steps 800
```

The raw-log experiment uses physical odometry, physical range-bearing observations, and Vicon ground truth. The separate empirical-noise replay uses simulated robot dynamics with noise and observation timing sampled from the physical log; it is not described as a hardware closed-loop experiment.

## Reproducibility notes

- All simulation seeds are fixed and recorded in the scripts.
- The same random seed and active-landmark subset are used when observers are compared within a condition.
- Confidence intervals in the main study are computed across ten evaluation seeds.
- Bundled JSON files preserve aggregate and, where needed, seed-level results.
- The report distinguishes original simulation results, secondary sensitivity analyses, and the physical-log extension.

## Known limitations

The robot and map are simulated in the main experiment, the recurrent models use a fixed ordered landmark representation, and only three training initializations were available for the SSM-EKF robustness study. The second-controller study uses five evaluation seeds and is reported as a sensitivity analysis rather than a definitive result. These limitations are discussed in the report.
