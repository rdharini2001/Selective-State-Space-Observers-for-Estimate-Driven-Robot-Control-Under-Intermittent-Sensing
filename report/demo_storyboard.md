# Demo video — storyboard & narration (target 5–7 min)

Solo presenter, screen recording with voiceover. Assets referenced are in `figures/` and
`report/`. Suggested tools: OBS / QuickTime / Zoom for screen+webcam; or just narrate over slides.
Times are cumulative targets. Read the **[SAY]** lines roughly verbatim; **[SHOW]** is what's on
screen.

---

### 0:00–0:35 — Hook & question
- **[SHOW]** Title slide, then `figures/demo_trajectory.gif` looping.
- **[SAY]** "We choose robot state estimators by how accurately they estimate — position RMSE on
  logged data. But estimators aren't used on logged data; they're dropped into a control loop,
  where their output *steers the robot*. So here's the question this project answers: does
  low estimation error actually mean good control? I'll show you a case where the answer is no."

### 0:35–1:30 — The testbed
- **[SHOW]** `figures/fig_trajectory.png` (reference figure-eight, landmarks, three trajectories).
- **[SAY]** "A differential-drive robot tracks a figure-eight with pure-pursuit control. It gets
  noisy, biased wheel odometry, plus range-and-bearing measurements to known landmarks — but only
  *intermittently*: landmarks go out of range, drop out, and periodically black out completely.
  The controller acts on the *estimate*, so estimation error and tracking error are coupled. Grey
  is dead reckoning — it drifts off. Blue is an EKF, green is our learned selective state-space
  observer; both track well."

### 1:30–2:45 — The observer zoo
- **[SHOW]** README observer table, then a slide of the residual-observer diagram
  (base integrator + recurrent correction; readout initialized near zero).
- **[SAY]** "I compare dead reckoning, an EKF, and learned *residual* observers: each wraps a base
  integrator — dead reckoning or the EKF — and adds a recurrent correction. The recurrent core is
  either a GRU or a compact *selective* state-space cell, the Mamba idea, whose input-dependent
  gates let it decide how much to trust a measurement — perfect for sensing that comes and goes.
  Every learned observer starts equal to its analytic prior and only learns to correct it. Ten
  seeds, four degradation axes, everything in simulation — no datasets."

### 2:45–3:30 — Blackout recovery (mechanism)
- **[SHOW]** `figures/fig_timeseries.png`.
- **[SAY]** "Here's the mechanism. During each shaded blackout, dead reckoning's error ratchets up
  and never comes back. The EKF and the physics-anchored learned observer stay bounded and snap
  back when measurements return. Whatever error the estimator accumulates in a gap, the controller
  inherits."

### 3:30–4:30 — Degradation sweeps
- **[SHOW]** `figures/fig_sweeps.png`.
- **[SAY]** "Sweeping each axis: the learned EKF-residual observers hug the EKF and pull ahead
  exactly where measurements are frequent but *mis-modeled* — heavy range noise, big gyro bias,
  where a fixed filter's noise assumptions break. Cross-track error drops about 26 to 29 percent
  there. But under long blackouts or with only two landmarks, they *don't* help — there's nothing
  to correct when measurements are gone. So the win is real but regime-specific, and I report it
  that way."

### 4:30–5:45 — The punchline: objective mismatch
- **[SHOW]** `figures/fig_mismatch.png` (both panels).
- **[SAY]** "Now the core result. Left: open-loop estimation error versus closed-loop tracking
  across every condition. On average they agree — Spearman 0.89 — so RMSE isn't useless. But the
  magnitude correlation is only 0.44, and look right: the observer with the *best* open-loop RMSE
  is *not* the best controller in 29 percent of conditions. And under compound stress" —
  **[SHOW]** compound-stress table (Table 3 in the PDF) — "the learned observer cuts open-loop
  error by 43 percent yet is 10 percent *worse* at actual tracking than the plain EKF. That's
  objective mismatch — the thing Lambert and colleagues found for model-based RL — showing up in
  state estimation."

### 5:45–6:30 — Why, and the takeaway
- **[SHOW]** `figures/fig_ablation.png`.
- **[SAY]** "Two ablations explain it. Remove selectivity or measurement-mask awareness and
  open-loop RMSE barely moves — but closed-loop control collapses, because the observer can't tell
  present measurements from absent ones. And the physics prior is load-bearing: the same learned
  cell on a dead-reckoning base is a great open-loop estimator but unstable in the loop; on an EKF
  base it's stable. The takeaway is simple and under-practiced: **evaluate learned filters in the
  loop, not just on RMSE.** Everything reproduces with one command. Thanks."

---

## Recording checklist
- [ ] Loop `demo_trajectory.gif` full-screen for the hook.
- [ ] Have `report/paper.pdf` open to Tables 1 and 3 and all five figures.
- [ ] Optional live moment: run `bash reproduce.sh` and show the training/eval logs scrolling, then
      cut to the finished figures (mention it's a few minutes on one CPU core).
- [ ] Keep total 5–7 min; the mismatch section (4:30–5:45) is the part to protect if you run long.
