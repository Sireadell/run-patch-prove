"""Run every attack in attacks/ against the helper agent and write report_<mode>.json.

Usage: python run_attacks.py broken      (the agent with holes)
       python run_attacks.py patched     (the agent after its fix)

BROKEN = the attack got through (bad). HELD = the agent resisted (good).
Exit code 1 if any attack broke the agent.
"""
import glob
import importlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(path):
    name = os.path.basename(path)[:-3]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "broken"
    if mode not in ("broken", "patched"):
        sys.exit("mode must be 'broken' or 'patched'")
    agent_cls = importlib.import_module(f"agent.{mode}_agent").HelperAgent

    results = []
    for path in sorted(glob.glob(os.path.join(HERE, "attacks", "*.py"))):
        mod = load(path)
        error = None
        try:
            broke = bool(mod.attack(agent_cls()))
        except Exception as e:  # a bug in the attack itself, not a hole in the agent
            broke, error = False, repr(e)
        results.append({"attack": mod.NAME, "broken": broke, "error": error})
        print(f"{'BROKEN' if broke else 'HELD  '}  {mod.NAME}" + (f"  (test error: {error})" if error else ""))

    broken = sum(r["broken"] for r in results)
    status = "RED" if broken else "GREEN"
    print(f"\nRESULT: {broken} of {len(results)} attacks broke the agent -> {status}")
    report = {"agent": mode, "status": status, "broken": broken, "total": len(results), "results": results}
    with open(os.path.join(HERE, f"report_{mode}.json"), "w") as f:
        json.dump(report, f, indent=2)
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
