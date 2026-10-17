"""Check a sealed report offline. Prints VALID or INVALID.

Usage: python verify.py sealed_patched.json
Exit code 0 = VALID, 1 = INVALID.
"""
import json
import sys

from seal import fingerprint


def main():
    path = sys.argv[1]
    try:
        with open(path) as f:
            report = json.load(f)
        ok = report.get("seal") == fingerprint(report)
    except (OSError, ValueError):
        ok = False
    if ok:
        print(f"VALID    {path}  agent={report['agent']}  status={report['status']}  "
              f"{report['broken']} of {report['total']} attacks broke it")
    else:
        print(f"INVALID  {path}  the file was changed after it was sealed")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
