# Scientific audit of the original submission

## High-severity issues corrected

### 1. The headline 29% mismatch statistic omitted a principal observer

The original `CORE` list excluded `gru_ekf`, even though GRU-EKF was often the strongest observer.
With all six main observers, the winner mismatch is **5/24 (20.8%)**, not 7/24 (29%). The global
Spearman and Pearson correlations become 0.923 and 0.477, respectively.

### 2. The selectivity and mask ablations were confounded by the anchor

The original paper compared EKF-anchored SSM-EKF with no-selectivity/no-mask models anchored to dead
reckoning, then attributed the large closed-loop difference to selectivity or masks. Matched EKF-anchor
ablations do not support that claim. At nominal conditions, all three are nearly tied. Effects change
sign by degradation regime.

### 3. Single-training-seed uncertainty was hidden

Three SSM-EKF training initializations are now evaluated. Nominal results are stable, but long-blackout
and high-noise performance vary materially. All main text should distinguish evaluation-seed uncertainty
from training-seed uncertainty.

### 4. “Mamba” was too strong a label

The recurrent cell is a compact selective diagonal SSM inspired by selective state-space modeling. It is
not a full Mamba block and should not be marketed as one.

### 5. The original paper documented a proxy failure but offered no evaluation alternative

The revised package adds exact controller disagreement, a local controller-Jacobian sensitivity metric,
counterfactual error replay, top-1 agreement, and selection regret. Importantly, it reports when these
alternatives fail rather than choosing a favorable metric after the fact.

### 6. Controller dependence was untested

A matched five-seed secondary analysis now compares pure pursuit with Kanayama control. The closed-loop
oracle changes in 8/24 conditions, and replay position RMSE misselects the Kanayama observer in 7/24.
The seed-bootstrap interval is wide, so this supports controller dependence without being a primary,
high-precision estimate.

## Remaining limitations

- Learned models still use eight ordered landmark slots and were trained on one synthetic map.
- The physical-data experiment is open-loop localization; closed-loop physical deployment is not shown.
- MRCLAM-calibrated replay uses physical sensor statistics but simulated dynamics.
- The simulator has known data association and a known map.
- Only SSM-EKF currently has three complete training seeds in the bundled results.
- The second-controller sensitivity has five matched evaluation seeds, fewer than the primary analysis.
- Twenty-four conditions are too few to establish definitive superiority of one proxy; bootstrap
  intervals should be interpreted descriptively.

## Strongest defensible paper contribution

The strongest contribution is an **audited evaluation protocol for learned state observers**:

1. pair replay and closed-loop evaluation under matched degradations;
2. include every deployment candidate in model selection;
3. report rank correlation, top-1 agreement, absolute and relative selection regret;
4. separate evaluation and training randomness;
5. use matched ablations;
6. include a physical-log stress test and disclose representation failures;
7. test whether observer selection transfers across controllers;
8. treat task-aware offline metrics as baselines, not replacements for closed-loop evaluation.
