# ECE 6562 final project video

## Target length

6 minutes 20 seconds. Record at 1080p if possible; 720p is acceptable. Use a screen recording with voice-over. A talking-head opening is optional, but the simulation and quantitative results should remain the main focus.

## Files to keep open before recording

1. `demo/nominal_tracking.mp4`
2. `demo/blackout_tracking.mp4`
3. `figures/fig_sweeps.png`
4. `figures/fig_proxy_scatter_compact.png`
5. `figures/fig_proxy_failures_compact.png`
6. `figures/fig_matched_ekf_ablation.png`
7. `figures/fig_training_seed_robustness.png`
8. `figures/fig_mrclam_real_trajectory.png`
9. the repository `README.md`

Do not spend video time scrolling through source files. Show the repository structure and the reproduction command briefly, then return to the simulation and results.

---

## 0:00-0:35 - Opening question

**Show:** A simple title card, followed by the first few seconds of `nominal_tracking.mp4`.

**Say:**

> This project asks a basic question about autonomous control. We usually select a robot state observer by running it on a fixed log and choosing the model with the lowest position error. In deployment, however, that estimate drives the controller. A small change in the estimate changes the command, the trajectory, and the measurements that arrive next. I wanted to test whether the best observer on replay is also the best observer in closed loop.

Keep the title card simple:

**Closed-Loop Evaluation of Robot State Observers Under Intermittent Sensing**  
Dharini Raghavan - ECE 6562

---

## 0:35-1:15 - Plant, sensing, and controller

**Show:** Pause `nominal_tracking.mp4` when the reference path and landmarks are visible. Point to the dashed figure-eight, landmark stars, trajectory panel, and error panel.

**Say:**

> The plant is a differential-drive robot with unicycle kinematics. It tracks a figure-eight using pure-pursuit control. The controller receives the estimated pose rather than the true pose. The robot has wheel odometry with slip, angular-rate bias, and random noise. It also receives range and bearing measurements to known landmarks, but those measurements are intermittent. Landmarks can be outside the sensing range, only a subset may be active, and periodic blackouts remove every landmark measurement.

> The left panel shows the actual closed-loop trajectories. The right panel shows the position-estimation error that the controller is using at each time step.

---

## 1:15-2:00 - Observer designs

**Show:** A single slide or a clean text overlay with the six observer names. Use this order:

- Dead reckoning
- EKF
- GRU residual on dead reckoning
- Selective state-space residual on dead reckoning
- GRU residual on the EKF
- Selective state-space residual on the EKF

**Say:**

> I compare two classical baselines and four recurrent residual observers. Dead reckoning integrates odometry only. The extended Kalman filter predicts with the motion model and corrects with whichever landmarks are available. The recurrent observers do not replace the analytic estimate. They add a small pose correction to either dead reckoning or the EKF. I compare a GRU recurrence with a selective state-space recurrence whose update can depend on the current measurements.

> The most important design comparison is the anchor. A dead-reckoning anchor has no measurement correction of its own. An EKF anchor preserves a complete model-based localization recursion, and the recurrent model only corrects its remaining error.

Avoid describing the method as a large general-purpose model. It is a compact recurrent residual estimator trained specifically for this simulation.

---

## 2:00-2:50 - Nominal simulation demo

**Show:** Play `nominal_tracking.mp4` from the beginning. Let it run without moving the cursor. When the green sensing label changes to a red blackout label, allow the viewer to see the error curves respond.

**Say:**

> Under nominal intermittent sensing, dead reckoning gradually drifts because slip and gyroscope bias accumulate. The EKF remains close to the path because landmark updates correct the drift. The two EKF-anchored residual observers also remain stable. In the nominal ten-seed evaluation, the GRU-EKF observer gives the lowest cross-track RMSE at 0.163 metres, compared with 0.212 metres for the plain EKF.

> The dead-reckoning residual models can have much lower replay error than raw dead reckoning, but their closed-loop trajectories are still noticeably worse. This is the first indication that a good fixed-log estimate does not automatically provide a good feedback signal.

---

## 2:50-3:35 - Long-blackout simulation

**Show:** Play `blackout_tracking.mp4`. Start just before a red blackout interval. If editing the final video, replay one blackout segment once at normal speed rather than speeding it up.

**Say:**

> This second run increases blackout duration, range noise, and gyroscope bias. During a blackout, every observer must coast on odometry. Dead reckoning accumulates a large error. The model-based and hybrid observers recover when measurements return, but their recovery is not identical. The learned correction helps when measurements are available but mismodelled. It cannot create information when sensing is completely absent.

> This distinction is visible in the full sweep: the hybrid observers often help under measurement noise and bias, while the plain EKF can be preferable during the longest blackouts.

---

## 3:35-4:15 - Four degradation sweeps

**Show:** `figures/fig_sweeps.png` full screen. Zoom enough that the axes and legend can be read. Move the cursor only to identify the four panels.

**Say:**

> I evaluated six observers across four physical degradation axes: blackout duration, range noise, active-landmark count, and gyroscope bias. Each level uses ten common random seeds. No learned observer is best everywhere. GRU-EKF is strong over much of the moderate operating range. The EKF becomes competitive or best when blackouts are longest. Sparse landmarks also change the ordering. This result is useful because it shows that observer selection has to match the expected sensing regime.

---

## 4:15-5:05 - Main result: replay selection versus closed-loop selection

**Show:** First `figures/fig_proxy_scatter_compact.png`, then `figures/fig_proxy_failures_compact.png`.

**Say:**

> The central analysis compares replay position RMSE with closed-loop cross-track RMSE over all six observers and 24 operating conditions. The global Spearman correlation is 0.923, so replay RMSE is useful for broad screening. The Pearson correlation is only 0.477, which means that the size of an estimation improvement does not directly predict the size of a control improvement.

> More importantly, the replay winner is not the closed-loop winner in five of the 24 conditions, or 20.8 percent. I also tested heading error, direct command disagreement, a local controller-sensitivity score, and a counterfactual replay score. The local sensitivity score has fewer observed failures, but its confidence interval overlaps no improvement and its worst regret is larger. The data therefore do not support replacing closed-loop evaluation with another single replay number.

Do not use the older 29 percent value. The corrected six-observer result is **5 of 24 conditions, or 20.8 percent**.

---

## 5:05-5:40 - What caused stability

**Show:** `figures/fig_matched_ekf_ablation.png`, followed by `figures/fig_training_seed_robustness.png`.

**Say:**

> I then repeated the architecture ablation while keeping the EKF anchor fixed. The selective, non-selective, and mask-free versions are nearly tied at nominal conditions, and their ordering changes across stress conditions. This means that selectivity is not a universal stability mechanism. The EKF anchor is the more consistent source of stability.

> Training initialization also matters. The three independently trained SSM-EKF models are close at nominal conditions but differ substantially under long blackouts. For that reason, I treat difficult-regime differences cautiously rather than presenting one training run as definitive.

---

## 5:40-6:05 - Physical-log extension

**Show:** `figures/fig_mrclam_real_trajectory.png`.

**Say:**

> As an external check, I evaluated the localization code on 600 seconds of UTIAS MRCLAM Robot 1 data, using physical wheel odometry, physical range-bearing measurements, and Vicon ground truth. Dead reckoning gives 3.392 metres position RMSE. The best EKF setting in the tested grid reduces this to 1.357 metres. The zero-shot recurrent models do not transfer reliably because they use an ordered landmark representation tied to the simulated map. This identifies a clear next step: a permutation-invariant measurement-set encoder trained across randomized maps.

---

## 6:05-6:25 - Reproducibility and conclusion

**Show:** The repository root. Highlight `README.md`, `reproduce.sh`, `report/`, `demo/`, `src/`, `tests/`, and `results/reference/`. Run `bash reproduce.sh` in a terminal beforehand or show a captured successful terminal output.

**Say:**

> The repository includes the complete simulation, trained checkpoints, audited result files, tests, report source, and demo assets. The grader can run the tests and a fresh closed-loop experiment with one command.

> My conclusion is that replay position RMSE is a good first filter, but it should not make the final deployment decision. The leading observers should be tested in a small set of representative closed-loop conditions, because the observer, controller, and sensing regime have to be evaluated as one system.

End on the title and the line:

**Evaluate the observer through the behavior it produces.**

---

# Editing instructions

1. Record the voice-over in a quiet room with the microphone 15-25 cm from your mouth.
2. Record each section separately. This makes it easy to replace one sentence without repeating the full video.
3. Use the two supplied MP4 clips as B-roll. Do not record a terminal while the simulation runs if the text is too small to read.
4. Keep plots on screen for at least 8-10 seconds so the axes can be read.
5. Add short on-screen labels for the four numbers that matter:
   - nominal GRU-EKF cross-track RMSE: **0.163 m**;
   - nominal EKF cross-track RMSE: **0.212 m**;
   - replay/closed-loop Spearman correlation: **0.923**;
   - top-1 selection failures: **5/24 = 20.8%**.
6. Use simple cuts and short fades. Avoid decorative animations that compete with the simulation.
7. Export at 1920x1080 or 1280x720, 30 frames per second, H.264, with AAC audio.
8. Test the final link in an incognito window before submitting it.

# Final video checklist

- [ ] Total length is between 5 and 7 minutes.
- [ ] Narration is clearly audible throughout.
- [ ] Both simulation clips are shown.
- [ ] The four degradation sweeps are shown.
- [ ] The corrected 5/24 result is stated.
- [ ] The matched EKF-anchor ablation is explained accurately.
- [ ] The physical-log experiment is described as localization, not hardware closed-loop control.
- [ ] Limitations and one next step are included.
- [ ] The repository reproduction command is shown.
- [ ] The uploaded link works without requesting access.
