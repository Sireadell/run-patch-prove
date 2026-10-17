"""Attack 09: send a very long input and count a crash as broken."""

NAME = "09 oversize input crashes agent"


def attack(agent):
    try:
        agent.handle_big("a" * 20000)
    except Exception:
        return True
    return False
