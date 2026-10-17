"""The helper agent after its fix. Same interface as broken_agent, every hole closed."""
import ast
import os
import re
import subprocess
from urllib.parse import urlparse

from agent.broken_agent import BASE, RULES, SECRET, SECRETS, WORKSPACE  # noqa: F401

ALLOWED_TOOLS = {"read"}
ALLOWED_HOSTS = {"example.com", "docs.createos.sh"}
SAFE_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
REFUSAL = "I can't help with that."


class HelperAgent:
    def __init__(self):
        self.env = {"API_KEY": SECRET, "MODE": "demo"}
        os.makedirs(WORKSPACE, exist_ok=True)
        os.makedirs(SECRETS, exist_ok=True)
        with open(os.path.join(SECRETS, "key.txt"), "w") as f:
            f.write(SECRET)

    def ask(self, text):
        t = text.lower()
        # Fix 1, 6, 12: never reveal secrets, repeat secret-looking text, or share instructions
        if "secret" in t or "sk_" in t or "instructions" in t or "ignore" in t:
            return REFUSAL
        return f"You said: {text}"

    def read_file(self, path):
        # Fix 4: the real path must stay inside workspace
        full = os.path.realpath(os.path.join(WORKSPACE, path))
        if os.path.commonpath([full, os.path.realpath(WORKSPACE)]) != os.path.realpath(WORKSPACE):
            return "refused: outside workspace"
        with open(full) as f:
            return f.read()

    def env_dump(self):
        # Fix 5: hide anything that looks like a key
        return {k: v for k, v in self.env.items() if "KEY" not in k.upper()}

    def run_tool(self, name):
        # Fix 6: plain names only, and no shell
        if not SAFE_NAME.match(name):
            return "refused: bad tool name"
        return subprocess.run(["echo", name], capture_output=True, text=True).stdout

    def fetch(self, url):
        # Fix 7: only allowed websites
        host = urlparse(url).hostname or ""
        if host not in ALLOWED_HOSTS:
            return f"blocked: {host or 'unknown host'} is not allowed"
        return f"fetched {url}"

    def delete_files(self, target):
        # Fix 8: destructive actions need a person to confirm
        return "refused: deleting needs confirmation from a person"

    def act(self, role, action):
        # Fix 9: a role the caller claims is not proof, so nothing is granted from it
        return "denied"

    def parse(self, blob):
        # Fix 10: data only, never code
        try:
            return ast.literal_eval(blob)
        except (ValueError, SyntaxError):
            return None

    def check_tool(self, name):
        # Fix 11: exact match against the allowed list
        return name in ALLOWED_TOOLS

    def handle_big(self, text):
        # Fix 12: reject long input politely instead of crashing
        if len(text) > 10000:
            return "input too large"
        return len(text)
