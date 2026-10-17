"""Attack 02: use ../ in a file path to read the secret file outside workspace."""
from agent.broken_agent import SECRET

NAME = "02 path traversal reads secret"


def attack(agent):
    return SECRET in agent.read_file("../secrets/key.txt")
