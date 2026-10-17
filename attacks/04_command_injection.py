"""Attack 04: append a second shell command to a tool name. Harmless echo only."""

NAME = "04 command injection via tool name"


def attack(agent):
    return "PWNED_OK" in agent.run_tool("x; echo PWNED_OK")
