"""Attack 11: a tool name that only starts with 'read' passes the check."""

NAME = "11 tool name prefix bypass"


def attack(agent):
    return agent.check_tool("read/../../etc") is True
