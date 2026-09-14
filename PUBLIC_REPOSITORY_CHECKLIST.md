# Public repository checklist

This package is ready to become a clean public repository after the following
human actions:

1. Create an empty GitHub repository without an auto-generated README, license,
   or `.gitignore`.
2. Upload the contents of this extracted project—not the enclosing folder.
3. Verify that `prepare.py`, `train.py`, and `program.md` match the pinned
   upstream source recorded in `INTEGRITY_SHA256.txt`.
4. Keep the provenance and MIT terms in `UPSTREAM_LICENSE_NOTICE.md`.
5. Replace the GitHub and contact placeholders in `README.md`, `CITATION.cff`, and `launch/LINKEDIN_LAUNCH_PACKAGE.md`.
6. Run `uv sync && uv run python -m unittest discover -s tests -v` and preserve the output.
7. Verify the included protected-holdout evidence with its `SHA256SUMS.txt`
   before repeating the public result.
8. Report the machine action and the human authorization separately.
9. Use MONAHINGA™, not the registration symbol.

Suggested repository description:

> An evidence gate for autonomous AI research: intelligence proposes,
> Artificial Stupidity challenges, evidence adjudicates, and a human authorizes.

Public claim before named human authorization:

> Under a predeclared six-run H100 protocol, every candidate beat every
> baseline on both validation and a sequestered holdout; the machine escalated
> the empirically passing result for named human review.

Public claim after a passing empirical rerun and named review:

> Under the predeclared six-run H100 protocol, every candidate run beat every
> baseline run on both validation and a sequestered holdout; a named human then
> reviewed the one-line diff and authorized KEEP.
