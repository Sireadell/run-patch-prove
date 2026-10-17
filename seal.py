"""Seal a report: add a SHA-256 fingerprint of its contents.

Usage: python seal.py report_broken.json    -> sealed_broken.json
Anyone can check a sealed report offline with verify.py. Changing any
character in the file changes the fingerprint, so verify.py prints INVALID.
This proves the file was not edited after sealing. It does not prove who made it.
"""
import hashlib
import json
import os
import sys


def fingerprint(report):
    body = {k: v for k, v in report.items() if k != "seal"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    src = sys.argv[1]
    with open(src) as f:
        report = json.load(f)
    report["seal"] = fingerprint(report)
    out = os.path.join(os.path.dirname(os.path.abspath(src)), os.path.basename(src).replace("report_", "sealed_"))
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"sealed -> {os.path.basename(out)}  seal={report['seal'][:16]}...")


if __name__ == "__main__":
    main()
