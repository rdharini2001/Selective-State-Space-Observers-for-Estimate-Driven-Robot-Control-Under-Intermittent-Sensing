# Paper revision guide

## Recommended title

**Replay Accuracy Is Not Enough: An Audited Closed-Loop Evaluation Protocol for Learned Robot State Observers**

## Recommended story

1. Observer papers optimize and rank models on replay, but deployment is feedback-coupled.
2. A controlled benchmark shows that replay RMSE preserves broad ordering yet can fail at top-1 selection.
3. Task-aware log-only proxies are tested, not merely proposed; none universally substitutes for rollouts.
4. Matched ablations overturn the original causal interpretation: the EKF anchor is load-bearing, while
   selectivity is regime-dependent.
5. Training-seed analysis demonstrates hidden uncertainty under stress.
6. A matched secondary controller study shows that the closed-loop oracle itself is controller-dependent.
7. Physical MRCLAM logs expose the fixed-map/ordered-slot transfer limitation and calibrate a more realistic
   replay benchmark.
8. The field contribution is a reproducible evaluation checklist, metrics, code, and negative results.

## Claims to use

- “Position RMSE is a strong coarse proxy but an incomplete deployment selector.”
- “LCSE reduces the observed number of top-1 failures, but uncertainty is too wide to claim dominance.”
- “The anchor is more consistently important than selectivity.”
- “Selectivity trades off bias correction against blackout/sparsity robustness.”
- “The current learned representation is not map-cardinality- or permutation-general.”
- “Observer selection is partly controller-specific; the five-seed controller study is secondary evidence.”

## Claims to avoid

- “Our Mamba observer is state of the art.”
- “Selectivity and masks are necessary for stability.”
- “Real-world closed-loop validation.”
- “LCSE solves objective mismatch.”
- “The 144 observer-condition points are independent samples.”

## Highest-value next experiments

1. Replace ordered landmark slots with a permutation-invariant innovation-set encoder and train on randomized maps.
2. Train all learned observers with five seeds and use a hierarchical bootstrap.
3. Expand the two-controller result to more seeds, controller-gain shifts, and a third controller.
4. Run Robot 1-5 and multiple MRCLAM datasets; train on one robot/dataset and test on another.
5. Add a small hardware loop or ROS/Gazebo replay with real timing and actuator dynamics.
