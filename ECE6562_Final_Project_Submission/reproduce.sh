#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH=src
export OMP_NUM_THREADS=1

FULL=0
TRAIN=0
for arg in "$@"; do
  case "$arg" in
    --full) FULL=1 ;;
    --train) TRAIN=1 ;;
    *) echo "Unknown option: $arg"; exit 2 ;;
  esac
done

echo "[1/5] Running unit and regression tests"
pytest -q

echo "[2/5] Running a fresh closed-loop smoke experiment"
python scripts/smoke_test.py

if [[ "$TRAIN" == "1" ]]; then
  echo "[3/5] Retraining all recurrent observers"
  python scripts/run_train.py --backend torch --force
elif [[ "$FULL" == "1" ]]; then
  echo "[3/5] Using bundled checkpoints"
else
  echo "[3/5] Checking bundled checkpoints"
fi

if [[ "$FULL" == "1" ]]; then
  echo "[4/5] Reproducing the complete simulation study"
  rm -f results/nominal.json results/compound_hard.json results/objective_mismatch.json
  rm -f results/sweep_dropout_len.json results/sweep_sig_r.json results/sweep_n_landmarks.json results/sweep_gyro_bias.json
  rm -f results/timeseries.json results/trajectory.json
  rm -rf results/enhanced
  NSEED=10 python scripts/run_eval.py all
  python scripts/run_mismatch.py
  python scripts/run_proxy_analysis.py --seeds 10 --bootstrap 3000
  python scripts/run_matched_ablation.py
  python scripts/run_ssm_training_seed_eval.py
  python scripts/run_second_controller.py --seeds 5
  python scripts/run_plots.py
  python scripts/make_enhanced_figures.py
  cp -f figures/enhanced/fig_matched_ekf_ablation.png figures/
  cp -f figures/enhanced/fig_training_seed_robustness.png figures/
  cp -f figures/enhanced/fig_controller_sensitivity.png figures/
  python scripts/make_demo_assets.py
  if command -v pdflatex >/dev/null 2>&1; then
    (cd report && pdflatex -interaction=nonstopmode ECE6562_Final_Project_Report.tex >/dev/null && pdflatex -interaction=nonstopmode ECE6562_Final_Project_Report.tex >/dev/null)
  fi
else
  echo "[4/5] Verifying bundled report results and demo assets"
  if [[ ! -f demo/nominal_tracking.mp4 || ! -f demo/blackout_tracking.mp4 ]]; then
    python scripts/make_demo_assets.py
  fi
fi

echo "[5/5] Checking final submission package"
python scripts/check_submission.py

echo "Done. Open report/ECE6562_Final_Project_Report.pdf and demo/VIDEO_SCRIPT.md."
