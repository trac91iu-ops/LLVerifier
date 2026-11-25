#!/bin/python3
"""Threat-model templates for the initial state.

A threat model belongs to a domain and states what holds before the attack starts:
the roles and their positions (domain level) and how far the owner has set up the
device (stage, chosen by the property subtype). genInit reads it next to the diagram;
the diagram only states protocol-specific facts and exceptions, which take precedence.
Facts stated by neither are absent (empty or false), see init_system.
"""

THREAT_MODELS = {
    'iot': {
        'base': ("userA is the legitimate owner of the device (the victim) and userC is an outsider (the attacker); "
                 "unless the description names other instances, the device is deviceB and the cloud is cloudA. "
                 "The owner is near the device and the attacker is away from it."),
        'stages': {
            'unbound': "The owner has not bound the device yet: no owner is recorded for it.",
            'trusted': "The device trusts the owner, and the cloud records the device's trust in the owner.",
            'authorized': ("The owner has already bound the device: the cloud records the owner as authorized for it "
                           "(associated with it, trusting the owner, or granting a permission). "
                           "The attacker holds no such authorization."),
        },
    },
    'agent': {
        'base': ("clientA is a legitimate client (the victim) and clientB is another client (the attacker); "
                 "unless the description names other instances, the server is serverA."),
        'stages': {
            'fresh': ("Both clients are authenticated. No conversation context exists yet: the server holds no "
                      "context, and no client knows a context identifier or has received any history."),
        },
    },
}

# property subtype -> (domain, stage)
SUBTYPE_SCENARIO = {
    'OWN-remote': ('iot', 'unbound'),
    'OWN-stealth': ('iot', 'trusted'),
    'CTRL-direct': ('iot', 'authorized'),
    'CTRL-revoked': ('iot', 'authorized'),
    'CTX-isolation': ('agent', 'fresh'),
}


def threatModel(subtype: str | None = None, domain: str = 'iot') -> str:
    """Without a subtype (model mode) only the domain level applies."""
    if subtype:
        domain, stage = SUBTYPE_SCENARIO[subtype]
        return THREAT_MODELS[domain]['base'] + ' ' + THREAT_MODELS[domain]['stages'][stage]
    return THREAT_MODELS[domain]['base']
