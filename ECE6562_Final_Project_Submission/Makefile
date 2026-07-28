.PHONY: verify full train demo report clean

verify:
	bash reproduce.sh

full:
	bash reproduce.sh --full

train:
	bash reproduce.sh --train --full

demo:
	PYTHONPATH=src python scripts/make_demo_assets.py

report:
	cd report && pdflatex -interaction=nonstopmode ECE6562_Final_Project_Report.tex && pdflatex -interaction=nonstopmode ECE6562_Final_Project_Report.tex

clean:
	rm -f results/nominal.json results/compound_hard.json results/objective_mismatch.json
	rm -f results/sweep_*.json results/timeseries.json results/trajectory.json
	rm -rf results/enhanced
	rm -f report/*.aux report/*.bbl report/*.blg report/*.log report/*.out
