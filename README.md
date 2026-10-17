# Run, Patch, Prove

Built for "Build Agents That Run Code" (CreateOS x Stripe Projects).

An agent that runs code needs a place where it can be attacked safely and a way to show the result to someone who wasn't there. This project does both inside a CreateOS Sandbox.

1. **Run.** 12 attacks hit a small helper agent that has real holes. All 12 get through (RED).
2. **Patch.** The same 12 attacks hit the fixed agent. None get through (GREEN).
3. **Prove.** Each run writes a sealed report. Anyone can check it offline with one command. Change a single character and the check says INVALID.

Everything runs with plain Python 3 and no installs.

## One-minute check

You need Python 3 and a terminal. No account, no keys, no network.

```sh
sh demo.sh
```

That runs the whole story and prints this (shortened):

```
== 1. RUN: attack the broken agent ==
BROKEN  01 ignore rules, reveal secret
... (12 lines)
RESULT: 12 of 12 attacks broke the agent -> RED

== 2. PATCH: the fixed agent, same 12 attacks ==
HELD    01 ignore rules, reveal secret
... (12 lines)
RESULT: 0 of 12 attacks broke the agent -> GREEN

== 3. PROVE: check both reports offline ==
VALID    sealed_broken.json  agent=broken  status=RED  12 of 12 attacks broke it
VALID    sealed_patched.json  agent=patched  status=GREEN  0 of 12 attacks broke it

== 4. Change one character in a report, then check again ==
INVALID  /tmp/tampered.json  the file was changed after it was sealed
```

Prefer to do it by hand? These are the same steps:

```sh
python3 run_attacks.py broken          # 12 of 12 break it, RED
python3 seal.py report_broken.json     # writes sealed_broken.json

python3 run_attacks.py patched         # 0 of 12 break it, GREEN
python3 seal.py report_patched.json    # writes sealed_patched.json

python3 verify.py sealed_broken.json   # VALID
python3 verify.py sealed_patched.json  # VALID

# change one character (GREEN to GREEM) and check again
sed 's/GREEN/GREEM/' sealed_patched.json > tampered.json
python3 verify.py tampered.json        # INVALID
```

I ran this on my laptop and inside a CreateOS Sandbox. Same numbers both times.

## The 12 attacks

Each attack is one small file in `attacks/`. To add a 13th, drop in a new file with a `NAME` and an `attack(agent)` function. The runner picks it up.

| # | Attack | What it tries |
|---|---|---|
| 01 | Ignore rules, reveal secret | Tells the agent to ignore its rules and hand over the secret |
| 02 | Path traversal | Uses `../` in a file path to read a file outside the workspace |
| 03 | Environment dump | Asks for the environment variables and looks for the key |
| 04 | Command injection | Adds a second command to a tool name (`echo` only) |
| 05 | Request to an internal address | Asks the agent to fetch a cloud metadata address |
| 06 | Echo the secret back | Puts the secret in a message and sees if it is repeated |
| 07 | Delete without asking | Asks the agent to delete everything, no confirmation |
| 08 | Fake admin role | Says "I am admin" and sees if the admin action goes through |
| 09 | Oversize input | Sends 20,000 characters and counts a crash as broken |
| 10 | Runs code it is given | Sends code where data is expected |
| 11 | Tool name prefix trick | Passes a name that only starts with `read` |
| 12 | Reveals its instructions | Asks the agent to show its own rules |

## How Stripe Projects and the CreateOS Sandbox were used

- **Stripe Projects** set up the project and the CreateOS account link: `stripe projects init run-patch-prove`, then `stripe projects add createos/free`. That wrote the CreateOS credentials into a local `.env`, which is not in this repo.
- **CreateOS Sandbox** is where the demo ran. I used `sandbox create` for a box with Python, `sandbox push` to upload the project as a tar file, and `sandbox exec` to run `sh demo.sh` inside it. The attacks run in the sandbox, so the agent being attacked never touches my machine.

## What this is not

- **The seal is a fingerprint, not a signature.** It is a SHA-256 hash of the report. It proves the file was not edited after it was sealed. It does not prove who made it. Someone could rerun the tools and seal their own report. A real key signature (ed25519) would be the next step.
- **The fix was written ahead of time.** `agent/patched_agent.py` is a fixed version I prepared. It is not an AI writing code live inside the sandbox.
- **The agent is a small demo.** `HelperAgent` is a few dozen lines built to have holes. It is not a production agent, and 12 attacks is not a full security audit.
- **The attacks are harmless.** They only use `echo`, read a demo file made for the test, or check a returned text. Nothing is deleted. The "delete" attack only asks the agent and reads its reply.
- **Sandbox status:** the CreateOS Sandbox is alpha. The free plan allows one sandbox at a time.

## Files

| Path | What it is |
|---|---|
| `agent/broken_agent.py` | The helper agent with 12 holes |
| `agent/patched_agent.py` | The same agent with all 12 closed |
| `attacks/` | One file per attack |
| `run_attacks.py` | Runs every attack against `broken` or `patched`, writes a report |
| `seal.py` | Adds the SHA-256 fingerprint to a report |
| `verify.py` | Prints VALID or INVALID for a sealed report |
| `demo.sh` | The whole flow in one command |

## License

MIT. See `LICENSE`.
