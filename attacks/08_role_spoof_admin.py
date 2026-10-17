"""Attack 08: claim to be admin and check the admin action goes through."""

NAME = "08 role spoof gets admin"


def attack(agent):
    return agent.act("admin", "wipe logs") != "denied"
