#!/usr/bin/env bash
# Single-command reproduction of the entire study:
#   train the model zoo -> run all evaluations -> objective-mismatch analysis
#   -> figures -> compile the PDF report.
# Usage:  bash reproduce.sh
set -e
cd "$(dirname "$0")"
export PYTHONPATH=src
export OMP_NUM_THREADS=1

echo "=== [1/5] training the observer zoo (6 learned models) ==="
python3 scripts/run_train.py

echo "=== [2/5] evaluating (nominal + 4 degradation sweeps, 10 seeds) ==="
python3 scripts/run_eval.py all

echo "=== [3/5] objective-mismatch analysis ==="
python3 scripts/run_mismatch.py

echo "=== [4/5] figures ==="
python3 scripts/run_plots.py

echo "=== [5/5] compiling report (if pdflatex present) ==="
if command -v pdflatex >/dev/null 2>&1; then
  ( cd report && cp -f ../figures/*.png . && pdflatex -interaction=nonstopmode paper.tex >/dev/null && pdflatex -interaction=nonstopmode paper.tex >/dev/null )
  echo "report/paper.pdf written"
else
  echo "pdflatex not found; skipping PDF (figures + results are in figures/ and results/)"
fi
echo "=== done. See results/, figures/, report/paper.pdf ==="
