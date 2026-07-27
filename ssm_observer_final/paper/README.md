# Paper builds

Two anonymous NeurIPS-style drafts are included:

- `workshop4.tex` / `workshop4.pdf`: four pages of main text plus references, intended for the Robot Learning Workshop format.
- `main.tex` / `main.pdf`: expanded six-page audit draft with the physical-log trajectory figure and fuller discussion.

Both versions use self-contained manual references and compile with:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error workshop4.tex
pdflatex -interaction=nonstopmode -halt-on-error workshop4.tex

pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Numerical claims are sourced from `results/enhanced/` and the corrected original result JSON files.
