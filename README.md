# Selective State-Space Observers for Estimate-Driven Robot Control Under Intermittent Sensing

A differential-drive robot tracks a figure-eight reference using pure-pursuit control, estimating
its pose from noisy odometry and *intermittent* range–bearing landmark measurements. We compare
classical (dead reckoning, EKF) and learned recurrent-residual observers (GRU and a selective,
Mamba-style diagonal state-space cell) **inside the control loop**, and ask the central question:

> **Does open-loop estimation accuracy (RMSE) predict closed-loop tracking performance?**

<img width="620" height="600" alt="demo_trajectory" src="https://github.com/user-attachments/assets/221cc7a5-1f44-4ccd-8714-3e1a6b274a9d" />

## Install

```bash
pip install -r requirements.txt        # numpy, scipy, matplotlib, autograd
```

> Note: the learned models use [`autograd`](https://github.com/HIPS/autograd) (pure NumPy
> autodiff), not PyTorch — the whole project runs on a single CPU core with no GPU.

## Reproduce everything with one command

```bash
bash reproduce.sh
```

This trains the six learned observers, runs the nominal evaluation and all four degradation
sweeps (10 seeds each), computes the objective-mismatch statistics, regenerates every figure, and
compiles `report/paper.pdf`. Total runtime is a few minutes on one CPU core. Trained models are
checkpointed to `results/models/`, so re-running skips already-trained models; delete that folder
to force a clean retrain.

Run individual stages:

```bash
export PYTHONPATH=src
python3 scripts/run_train.py                 # train the zoo (resumable)
python3 scripts/run_eval.py all              # nominal + sweeps -> results/*.json
python3 scripts/run_mismatch.py              # objective-mismatch analysis
python3 scripts/run_plots.py                 # figures -> figures/*.png
```

## Repository layout

```
src/ssm_obs/            # the library ("dumb code": generic utilities, direct library use)
  dynamics.py           # unicycle kinematics, biased/noisy odometry, range-bearing sensing
  sim.py                # simulator, reference path, blackout schedule, closed/open-loop rollouts
  controllers.py        # pure-pursuit (primary) and Kanayama (ablation) — both act on the ESTIMATE
  ekf.py                # dead reckoning and the EKF baseline
  nn_core.py            # featurization, GRU cell, selective diagonal SSM cell, Adam
  models.py             # learned residual observer (base integrator + recurrent correction)
  data.py               # domain-randomized expert rollouts for training
  train.py              # BPTT training loop (autograd) + the model-zoo Spec
  metrics.py            # position/heading RMSE, cross-track, effort, recovery, divergence
  experiments.py        # model zoo, observer factory, eval conditions, degradation axes
  plotting.py           # all publication figures
  persist.py            # save/load trained models (.npz + .json)
scripts/                # thin runners (train / eval / mismatch / plots)
results/                # metrics JSON + trained models (regenerated)
figures/                # figures (regenerated)
report/                 # paper.tex + paper.pdf (the ~10-page report)
reproduce.sh            # one-command pipeline
```

## Observers

| name | base (anchor) | recurrent cell | notes |
|------|---------------|----------------|-------|
| `dead_reckoning` | — | — | odometry integration only |
| `ekf` | — | — | analytic motion + range-bearing updates |
| `gru_dr` | dead reckoning | GRU | learned residual |
| `ssm_dr` | dead reckoning | selective SSM | learned residual |
| `ssm_ekf` | EKF | selective SSM | covariance-aware hybrid |
| `gru_ekf` | EKF | GRU | hybrid |
| `ssm_dr_nosel` | dead reckoning | SSM (no selectivity) | ablation |
| `ssm_dr_nomask` | dead reckoning | selective SSM (no mask) | ablation |

Each learned observer's readout is initialized near zero, so it *starts* equal to its analytic
prior and only learns a correction.

## Key results

- **EKF is a strong baseline** (nominal closed-loop cross-track 0.21 m, zero divergence).
- **Dead-reckoning-residual learned observers** estimate well open-loop (0.28–0.33 m, 4–5× better
  than raw DR) but control **worse** than the EKF (0.69–0.91 m cross-track, high variance) — good
  open-loop RMSE did not survive the loop.
- **EKF-residual hybrids** help most where measurements are frequent but mis-modeled: −26% cross-track
  at the highest range noise, −29% at the largest gyro bias. They do **not** help under long blackouts
  or extreme landmark sparsity.
- **Objective mismatch:** global Spearman ρ = 0.89 but Pearson r = 0.44; the best open-loop estimator
  is not the best controller in **29%** of conditions.
- **Compound stress:** learned EKF-residual observers cut open-loop RMSE ~43% while the selective
  SSM-EKF is 10% *worse* on closed-loop cross-track — the sharpest mismatch instance.
- **Ablations:** removing selectivity or mask-awareness barely changes open-loop RMSE but is
  catastrophic closed-loop (cross-track 2.3–3.3 m) — invisible to off-loop metrics, fatal in the loop.
