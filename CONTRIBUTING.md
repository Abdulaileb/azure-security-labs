# Contributing a Lab

This is a personal learning portfolio, but the lab standard is intentionally repeatable.

1. Copy `templates/lab-template` into a new `lab-NN-topic` folder.
2. Write the objective and threat or control model before running commands.
3. Record only sanitized identifiers and outputs.
4. Add a repeatable verification script.
5. Document one controlled failure when it is safe to do so.
6. Record detection, root cause, remediation, and residual risk in `findings.md`.
7. Run the relevant script and `git diff --check`.
8. Rebuild the lab from memory and note anything you could not reproduce.

Use `Status: Planned`, `In progress`, or `Complete` accurately. A complete lab needs evidence for both the intended configuration and the security control being tested.
