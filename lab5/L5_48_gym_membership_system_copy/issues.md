# Static Code Analysis Issues

**Project:** Gym Membership System  
**File under analysis:** `gym_membership_system.py`

> **Important:** The first analysis attempt did not successfully scan the Python source file. Pylint reported `F0001: No module named gym_membership_system.py`, Bandit reported that the file was not found and scanned 0 lines, and Flake8 reported `E902 FileNotFoundError`. These are path/command execution problems, not confirmed defects in the program. Locate the file and rerun all three tools before completing this table.

| Issue | Type / Tool | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| 1 | Bandit `B324` — weak hash | 47 | `hashlib.md5()` is used to create a hash from the member ID. MD5 is unsuitable when a cryptographic hash is needed for security. | Replace MD5 with SHA-256 if a deterministic digest is required. A hash of a member ID is not automatically a secure authentication mechanism; choose the design based on its purpose. |
| 2 | Bandit `B605` — shell command | 58 | `os.system()` runs a shell command containing `filename`. Shell execution can create command-injection risk when input is not trusted. | Remove the shell command because it is only printing a status message. Use `print()` instead. |
| 3 | Bandit `B307`; Pylint `W0123` — use of `eval` | 42 | `eval(discount_expr)` evaluates a string as Python code, which can execute unintended expressions. | Replace it with an explicit calculation or a validated set of supported discount options. Do not evaluate arbitrary input. |
| 4 | Bandit `B110`; Pylint `W0702`; Flake8 `E722` — broad exception handling | 26 | A bare `except` catches any exception, and `pass` silently ignores it. This can hide errors unrelated to a missing membership. | Catch the expected exception, such as `KeyError`, and handle that case intentionally. Let unexpected errors remain visible. |
| 5 | Bandit `B311` — non-cryptographic random value | 51 | `random.randint()` generates the locker PIN. The standard `random` generator is not designed for security-sensitive values. | If the PIN must be unpredictable for security, use `secrets` (for example, `secrets.randbelow`). If it is only a demonstration value, document that it is not security-sensitive. |
| 6 | Bandit `B105` — hardcoded password-like string | 70 | The string `GYM_CLOUD_PORTAL_SECRET_2026` is embedded in source code and looks like a secret. Bandit flags the pattern; the report alone does not prove that it is a real credential. | Do not store real secrets in source control. If this is a required secret, load it from an environment variable or a secret manager, and avoid printing the secret. If it is only a dummy value, make that clear. |
| 7 | Pylint `W0102` — dangerous mutable default | 15 | `registerMember()` uses `member_log=[]` as a default. The same list object can be reused across calls, causing entries to carry over unexpectedly. | Use `member_log=None` and create a new list inside the function when no list is supplied. |
| 8 | Pylint `C0103` — function naming | 15, 23, 30, 40 | `registerMember`, `cancelMembership`, `checkMembershipStatus`, and `calculateRenewalRate` use camelCase rather than the usual Python snake_case style. | Rename them to `register_member`, `cancel_membership`, `check_membership_status`, and `calculate_renewal_rate`, and update all calls. |
| 9 | Pylint `C0116` — missing function docstrings | 15, 23, 30, 40, 46, 50, 54, 61, 69 | Functions do not have docstrings explaining their purpose. | Add short, accurate docstrings to each function. |
| 10 | Pylint `W0611`; Flake8 `F401` — unused import | 6 | `math` is imported but never used. | Remove `import math` if it is not needed. |
| 11 | Pylint `W0612`; Flake8 `F841` — unused local variables | 31, 41, 63 | `locker_deposit`, `base_fee`, and loop variable `m` are assigned but not used. | Remove genuinely unnecessary variables or use them if they are part of the intended logic. Do not remove a value that the calculation actually needs. |
| 12 | Pylint `C0121`; Flake8 `E711` — comparison with `None` | 32 | The code uses `members.get(m_id) == None`. | Use `members.get(m_id) is None`. |
| 13 | Pylint `R1703`, `R1705` — unnecessary conditional | 34 | An `if/else` returns `True` or `False` directly, and the `else` follows a `return`. | Return the boolean condition directly, provided the behavior stays the same. |
| 14 | Pylint `C0209` — string formatting | 19 | Percent-style formatting is used where an f-string would be clearer. | Replace the formatting expression with an f-string while preserving the message output. |
| 15 | Pylint `W1514`, `R1732` — file handling | 55–57 | The file is opened without an explicit encoding and is manually closed. If an exception occurs before `close()`, the file may not be closed correctly. | Use a context manager such as `with open(filename, "w", encoding="utf-8") as file:`. |
| 16 | Pylint `W0621` — redefined outer name | 61 | The `get_active_summary(members)` parameter has the same name as the global `members` variable. | Rename the parameter to something distinct, such as `member_records`, and use that name consistently inside the function. |
| 17 | Flake8 `E501` — lines too long | 10, 11, 18 | Several source lines exceed Flake8's 79-character limit. | Split long dictionary entries and statements across multiple lines using standard Python formatting. |
| 18 | Pylint `C0304`; Flake8 `W292` — missing final newline | End of file (reported at line 82) | The source file does not end with a newline character. | Add a newline at the end of the file and save it. |

## Notes

- Do not count missing-file errors as defects in the program itself.
- Replace the pending rows with genuine findings after the tools successfully scan the source.
- Record the original line numbers and the fix applied.
- Rerun all tools after changes and retain both before-fix and after-fix reports.
