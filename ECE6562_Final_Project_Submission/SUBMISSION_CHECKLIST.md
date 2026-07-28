# Final submission checklist

## Canvas submission

- [ ] Upload `report/ECE6562_Final_Project_Report.pdf`.
- [ ] Upload the cleaned repository ZIP or provide the private GT GitHub Enterprise link.
- [ ] Add the instructor and TAs as repository collaborators when using GitHub Enterprise.
- [ ] Provide the unlisted video link or upload the video directly.
- [ ] State the video location in the Canvas submission comment.
- [ ] Test the video and repository links in an incognito window.

## Report requirements

- [x] Single-column layout.
- [x] 11-point text.
- [x] One-inch margins.
- [x] Abstract.
- [x] Introduction and contributions.
- [x] Related work with real robotics and estimation references.
- [x] Mathematical system and controller description.
- [x] Experimental protocol and fair baselines.
- [x] Quantitative results with confidence intervals.
- [x] Discussion of successful and unsuccessful parts.
- [x] Limitations and next steps.
- [x] References.

## Code requirements

- [x] Root README with exact reproduction commands.
- [x] `requirements.txt` and `environment.yml`.
- [x] Bundled checkpoints.
- [x] Audited result files.
- [x] Data-download script for the external dataset.
- [x] Regression tests.
- [x] One-command verification through `bash reproduce.sh`.
- [x] Full rerun through `bash reproduce.sh --full`.

## Before creating the final ZIP

Run:

```bash
bash reproduce.sh
```

Then confirm that the final line reads:

```text
Submission check passed
```
