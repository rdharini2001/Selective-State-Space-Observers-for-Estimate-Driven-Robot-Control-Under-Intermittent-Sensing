#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH=src
export OMP_NUM_THREADS=1

pytest
python scripts/run_train.py --backend torch
python scripts/run_proxy_analysis.py --seeds 10 --bootstrap 3000
python scripts/run_matched_ablation.py
python scripts/run_ssm_training_seed_eval.py
if [[ "${RUN_SECOND_CONTROLLER:-0}" == "1" ]]; then
  python scripts/run_second_controller.py --seeds 5
else
  echo "Set RUN_SECOND_CONTROLLER=1 to reproduce the slower matched-controller sensitivity."
fi
python scripts/make_enhanced_figures.py

if [[ -n "${MRCLAM_DATA_DIR:-}" ]]; then
  python scripts/run_mrclam.py --data-dir "$MRCLAM_DATA_DIR" --robot 1 --duration 600 --seeds 12 --replay-steps 800
  MRCLAM_DATA_DIR="$MRCLAM_DATA_DIR" python scripts/make_enhanced_figures.py
else
  echo "Set MRCLAM_DATA_DIR to reproduce the physical-log experiment."
fi

echo "Enhanced results are in results/enhanced, figures/enhanced, and paper/."
