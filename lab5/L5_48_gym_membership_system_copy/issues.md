# Static Code Analysis Issues

**Project:** Gym Membership System  
**File under analysis:** `gym_membership_system.py`

> **Important:** The first analysis attempt did not successfully scan the Python source file. Pylint reported `F0001: No module named gym_membership_system.py`, Bandit reported that the file was not found and scanned 0 lines, and Flake8 reported `E902 FileNotFoundError`. These are path/command execution problems, not confirmed defects in the program. Locate the file and rerun all three tools before completing this table.

| Issue | Type / Tool | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| 1 | Pending — Bandit | TBD | No valid Bandit findings yet; the file was not found and 0 lines were scanned. | Rerun Bandit from the directory containing the Python file; document and fix the actual finding. |
| 2 | Pending — Pylint | TBD | No valid Pylint findings yet; Pylint could not locate the module. | Rerun Pylint with the correct file path and record the actual finding. |
| 3 | Pending — Flake8 | TBD | No valid Flake8 findings yet; the source file was not found. | Rerun Flake8 with the correct file path and record the actual finding. |
| 4 | Pending — to be determined | TBD | At least one additional genuine issue must be identified from the successful reports or code inspection. | Inspect the source and reports, then document and fix a real issue. |

## Notes

- Do not count missing-file errors as defects in the program itself.
- Replace the pending rows with genuine findings after the tools successfully scan the source.
- Record the original line numbers and the fix applied.
- Rerun all tools after changes and retain both before-fix and after-fix reports.
