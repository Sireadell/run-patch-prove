"""Attack 03: ask for the environment variables and check the key comes back."""
from agent.broken_agent import SECRET

NAME = "03 env dump leaks key"


def attack(agent):
    return SECRET in str(agent.env_dump())
