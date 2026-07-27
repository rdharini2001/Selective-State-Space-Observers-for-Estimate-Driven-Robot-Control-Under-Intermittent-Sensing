# Closed-Loop Evaluation of Learned Robot State Observers

This repository is a substantially strengthened and audited version of the original
**Selective State-Space Observers for Estimate-Driven Robot Control Under Intermittent Sensing** project.

The central contribution is now an **evaluation protocol and benchmark**, not a claim that a compact
selective SSM is universally superior. It asks a deployment-relevant question:

> When an observer is selected from logged replay data, does that choice remain optimal after the observer is placed inside a feedback loop?

The package contains:

- six principal classical/learned observers evaluated across 24 sensing degradations;
- corrected top-1 model-selection and regret analysis including GRU-EKF;
- four offline selection proxies, including local controller-sensitivity error;
- matched EKF-anchor selectivity and mask ablations;
- three training-initialization seeds for SSM-EKF;
- a matched pure-pursuit/Kanayama secondary-controller sensitivity;
- physical-log localization on UTIAS MRCLAM Robot 1;
- MRCLAM-calibrated closed-loop replay using physical sensor residuals and observation timing;
- a zero-shot learned-observer stress test on an eight-landmark MRCLAM subset;
- a maintained PyTorch training backend, tests, paper source, figures, and result JSON files.

## Main audited findings

1. **Replay RMSE is useful but incomplete.** Across six observers and 24 conditions,
   open-loop position RMSE has global Spearman correlation 0.923 with closed-loop cross-track RMSE,
   but selects the wrong top observer in 5/24 conditions (20.8%).
2. **Controller awareness is not automatically sufficient.** Exact command disagreement and a
   counterfactual error replay perform worse than pose RMSE as top-1 selectors. A local
   controller-sensitivity score reduces the observed failures to 3/24, but its bootstrap interval
   overlaps no improvement and its worst regret is larger. The defensible result is therefore that
   no tested log-only scalar replaces closed-loop evaluation.
3. **The original selectivity claim was confounded.** With the same EKF anchor, nominal cross-track
   RMSE is 0.199 m (selective), 0.203 m (non-selective), and 0.195 m (mask-free). Selectivity helps
   under high gyro bias but hurts under long blackouts and two-landmark sensing. The analytic anchor,
   rather than selectivity alone, is the dominant stabilizing factor.
4. **Training seed matters under stress.** Across three SSM-EKF initializations, nominal means span
   only 0.189-0.199 m, while long-blackout means span 0.231-0.336 m.
5. **Observer selection is controller-dependent.** In a matched five-seed sensitivity, switching from
   pure pursuit to Kanayama changes the closed-loop oracle in 8/24 conditions. Replay RMSE misselects
   the Kanayama observer in 7/24 conditions, with maximum regret 0.092 m. The paired seed-bootstrap
   interval for the oracle-change fraction is wide (0.208-0.625), so this is a secondary result.
6. **Real-data transfer remains unsolved.** On 600 s of UTIAS MRCLAM Robot 1 data, the best simple
   15-landmark EKF obtains 1.357 m position RMSE versus 3.392 m for dead reckoning. Zero-shot learned
   checkpoints on an eight-landmark subset reach 2.60-2.62 m but have worse heading error, exposing
   the map/slot-specific representation as a major limitation rather than hiding it.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=src            # Windows PowerShell: $env:PYTHONPATH="src"
```

The default training backend is PyTorch. Existing NumPy checkpoints can be evaluated without
`autograd`; this fixes compatibility problems in the original repository on modern Python/NumPy.

## Reproduce the strengthened study

### Fast verification using bundled checkpoints/results

```bash
pytest
python scripts/run_proxy_analysis.py --seeds 10 --bootstrap 3000
python scripts/run_matched_ablation.py
python scripts/run_ssm_training_seed_eval.py
# Optional, slower matched-controller sensitivity:
python scripts/run_second_controller.py --seeds 5
python scripts/make_enhanced_figures.py
```

### Physical-log experiment

```bash
python scripts/download_mrclam.py --output data/external/MRCLAM_Dataset1 --robots 1
python scripts/run_mrclam.py \
  --data-dir data/external/MRCLAM_Dataset1 \
  --robot 1 --duration 600 --seeds 12 --replay-steps 800
```

The raw-log section uses real odometry, range-bearing measurements, and Vicon ground truth.
The closed-loop section is explicitly a **real-noise-calibrated simulation**: dynamics are simulated,
while sensor residuals and observation timing are resampled from the physical log.

### Train models

```bash
python scripts/run_train.py --backend torch
```

To retrain selected models:

```bash
python scripts/run_train.py --backend torch --force ssm_ekf gru_ekf
```

## Repository layout

```text
src/ssm_obs/
  controller_metrics.py     task-aware offline metrics and selection regret
  mrclam.py                 physical-log loader and empirical-noise replay
  torch_train.py            maintained PyTorch trainer, legacy checkpoint export
  controllers.py            closed-loop and time-indexed offline controllers
  dynamics.py, sim.py       unicycle simulation and intermittent sensing
  ekf.py                    dead reckoning and EKF
  models.py, nn_core.py     recurrent residual observers and NumPy inference
  experiments.py            observer specifications and degradation conditions
scripts/
  run_proxy_analysis.py     corrected six-observer proxy/regret study
  run_matched_ablation.py   same-anchor selectivity/mask study
  run_ssm_training_seed_eval.py
  run_second_controller.py  matched pure-pursuit/Kanayama sensitivity
  run_mrclam.py             real logs + real-noise-calibrated replay
  download_mrclam.py
  make_enhanced_figures.py
results/enhanced/           seed-level and aggregate JSON results
figures/enhanced/           new publication figures
paper/                      NeurIPS workshop manuscript and compiled PDF
docs/                       audit, experiment card, and revision guidance
tests/                      regression tests
```

## What this paper should and should not claim

**Supported:** replay metrics can preserve broad rankings while failing at top-1 observer selection;
physics anchoring is consistently valuable; selectivity is regime-dependent; single-seed conclusions
are fragile under harder sensing; the current ordered landmark representation transfers poorly.

**Not supported:** selectivity or mask awareness is universally necessary; the compact cell is a full
Mamba architecture; the MRCLAM-calibrated replay is a hardware closed-loop experiment; any tested
offline metric has replaced actual closed-loop evaluation.

See `docs/SCIENTIFIC_AUDIT.md` and `docs/PAPER_REVISION_GUIDE.md` before changing claims.
