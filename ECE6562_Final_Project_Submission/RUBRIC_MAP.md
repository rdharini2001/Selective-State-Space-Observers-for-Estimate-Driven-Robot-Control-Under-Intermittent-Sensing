# How the submission addresses the grading rubric

## Technical soundness - 30%

- The report states the unicycle dynamics, odometry-error model, range-bearing model, and feedback equations.
- Dead reckoning and EKF baselines use the same plant and sensing sequence as the recurrent observers.
- The controller acts on the estimated pose in every closed-loop rollout.
- The matched ablation changes selectivity or measurement-mask input while keeping the EKF anchor fixed.
- The report separates physical-log localization from simulated closed-loop control.

## Experimental rigor - 25%

- Six principal observers are evaluated across 24 sensing conditions.
- Ten common evaluation seeds are used in the main experiment.
- Four physical degradation axes are varied independently.
- Open-loop and closed-loop metrics are both reported.
- Top-1 selection failure and regret are reported in addition to correlation.
- Training-seed and second-controller sensitivity analyses are included.
- Confidence intervals and limitations are stated rather than hidden.

## Clarity of writing - 20%

- The report follows abstract, introduction, related work, approach, experiments, discussion, and references.
- Symbols are defined before use.
- Figures are referenced in the text and have descriptive captions.
- The discussion separates successful results, negative results, and limitations.

## Connection to literature - 15%

- The report cites foundational work on EKF localization, pure pursuit, Kanayama tracking, recurrent filters, differentiable filters, structured state-space models, and objective mismatch.
- The project is positioned as a hybrid observer and closed-loop evaluation study rather than as an isolated sequence-model comparison.

## Reproducibility - 10%

- `bash reproduce.sh` runs tests, a fresh closed-loop experiment, and submission checks.
- `bash reproduce.sh --full` reruns the full simulation study from bundled checkpoints.
- `requirements.txt` and `environment.yml` are included.
- Trained checkpoints and audited JSON results are bundled.
- The external MRCLAM data have a downloader and exact evaluation command.
- Demo clips and a complete narration script are included.
