"""Attack 05: ask the agent to fetch a cloud metadata address."""

NAME = "05 SSRF to metadata address"


def attack(agent):
    return agent.fetch("http://169.254.169.254/latest/meta-data").startswith("fetched")
