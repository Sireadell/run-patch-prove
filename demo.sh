#!/bin/sh
# Run, patch, prove: the whole flow in one go. Run inside the sandbox.
cd "$(dirname "$0")" || exit 1

echo "== 1. RUN: attack the broken agent =="
python3 run_attacks.py broken
python3 seal.py report_broken.json

echo
echo "== 2. PATCH: the fixed agent, same 12 attacks =="
python3 run_attacks.py patched
python3 seal.py report_patched.json

echo
echo "== 3. PROVE: check both reports offline =="
python3 verify.py sealed_broken.json
python3 verify.py sealed_patched.json

echo
echo "== 4. Change one character in a report, then check again =="
sed 's/GREEN/GREEM/' sealed_patched.json > /tmp/tampered.json
python3 verify.py /tmp/tampered.json
