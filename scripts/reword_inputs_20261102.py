"""2026-11-02: apply the iRobot wording decisions to the other inputs. Init notes describe relations between
values (same key / a different key per user) instead of literal key values; "set X key to the key" becomes
"sends the key to the device". Every replacement must match exactly once. Usage: python scripts/reword_inputs_20261102.py
"""
from pathlib import Path
INPUT = Path(__file__).resolve().parents[1] / 'sequence_diagram/input'

SHARED = ("Initially the device holds the key 'secret', and the cloud records the key 'secret' for the device.",
          "Initially the device holds a key, and the cloud records the same key for the device.")
SHARED_BINDING = ("Initially the device holds the key 'secret', and the cloud records the binding key 'secret' for the device.",
                  "Initially the device holds a key, and the cloud records the same key as the device's binding key.")
DEVICE_ONLY = ("Initially the device holds the key 'secret'.", "Initially the device holds a key.")
PER_USER = ("Initially the cloud records the key 'secretA' for userA and the key 'secretC' for userC.",
            "Initially the cloud records a different key for each user.")
SET_KEY_ON_DEVICE = ("The user calls an API on the device to set its key to the key", "The user sends the key to the device")

EDITS = {
    **{p: [SHARED] for p in ('August', 'Beurer', 'Govee', 'Kevo', 'Midea', 'Netvue', 'Sunlogin')},
    **{p: [SHARED_BINDING] for p in ('Ezviz', 'Imou', 'Switchbot')},
    **{p: [DEVICE_ONLY] for p in ('Dyson', 'Huawei', 'TuyaCAC', 'Xiaomi')},
    **{p: [PER_USER, SET_KEY_ON_DEVICE] for p in ('TPLink', 'Wemo')},
    'Broadlink': [("Initially the device holds the key 'secret' and is unlocked, and the cloud records the key 'secret' for the device.",
                   "Initially the device holds a key and is unlocked, and the cloud records the same key for the device.")],
    **{p: [("The cloud records the key 'phoneMacA' for userA and the key 'phoneMacC' for userC.",
            "The cloud records a different key for each user."),
           ("The user calls an API to set the device key to the key", "The user sends the key to the device")]
       for p in ('CloudEdgeCAC', 'CloudEdgeRTE')},
    'Meross': [("Initially userA holds the key 'UIDA' and userC holds the key 'UIDC'. The device holds the key 'secret'. "
                "The cloud records the key 'secret' for the device, the key 'UIDA' for userA, and the key 'UIDC' for userC.",
                "Initially each user holds a different key, and the cloud records each user's key. The device holds a key "
                "different from the users' keys, and the cloud records the same key for the device.")],
    'MaagKwikset': [("The cloud signs keys with the secret 'secret', which the device also knows.",
                     "The cloud signs keys with a secret, which the device also knows.")],
    'MaagLevel': [("The cloud holds the cloud key 'secret'.", "The cloud holds a cloud key.")],
    'delegationFlaw1': [("records that the switch trusts userA and holds the key 'secret'.",
                         "records that the switch trusts userA and holds a key."),
                        ("holds the key 'secret' and is bound to the lock.", "holds the same key and is bound to the lock.")],
    'delegationFlaw2': [("records that the lock trusts cloudSmartThing and holds the key 'secret'.",
                         "records that the lock trusts cloudSmartThing and holds a key."),
                        ("holds the key 'secret' and is bound to the lock.", "holds the same key and is bound to the lock.")],
}

if __name__ == '__main__':
    for name, edits in EDITS.items():
        p = INPUT / name / 'diagram.md'
        s = p.read_text()
        for old, new in edits:
            assert s.count(old) == 1, (name, old)
            s = s.replace(old, new)
        p.write_text(s)
        print(f'{name:16} {len(edits)} edit(s)')
