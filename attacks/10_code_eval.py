"""Attack 10: send code instead of data. Harmless call that only reads the working folder name."""

NAME = "10 runs code it is given"


def attack(agent):
    try:
        result = agent.parse("__import__('os').getcwd()")
    except Exception:
        return False
    return isinstance(result, str)
