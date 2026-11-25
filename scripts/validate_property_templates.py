#!/usr/bin/env python3
"""Check that src/property_templates.py reproduces the golden checkers.

For every golden protocol, the golden checker's own propositions are
plugged into the template subtype it belongs to; both checkers are model-checked on
the golden rules.maude and their results (verdict and counterexample events) compared.
Usage: python scripts/validate_property_templates.py [protocol ...]
"""
import os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / 'benchmark/golden_data/formalModels'
sys.path.insert(0, str(ROOT / 'src'))
from property_templates import renderChecker

# protocol: (subtype, {slot: golden proposition}, attacker)
MAPPING = {
    **{p: ('OWN-remote', {'attackerLocal': l, 'attackerOwner': o}, 'userC') for p, l, o in [
        ('August', 'ap9', 'ap10'), ('Beurer', 'ap6', 'ap7'), ('Broadlink', 'ap6', 'ap7'),
        ('CloudEdgeCAC', 'ap7', 'ap8'), ('CloudEdgeRTE', 'ap7', 'ap8'), ('Ezviz', 'ap7', 'ap8'),
        ('Govee', 'ap6', 'ap7'), ('Imou', 'ap7', 'ap8'), ('Kevo', 'ap9', 'ap10'), ('Meross', 'ap6', 'ap7'),
        ('Midea', 'ap6', 'ap7'), ('Netvue', 'ap9', 'ap10'), ('Sunlogin', 'ap6', 'ap7'),
        ('Switchbot', 'ap6', 'ap7'), ('TPLink', 'ap4', 'ap5'), ('Wemo', 'ap7', 'ap8'), ('iRobot', 'ap9', 'ap11')]},
    'Philips': ('OWN-remote', {'attackerLocal': 'ap4', 'attackerOwner': 'ap5', 'victimOwner': 'ap2'}, 'userC'),
    'MaagKwikset': ('OWN-stealth', {'deviceTrustsAttacker': 'ap5', 'cloudRecordsTrust': 'ap6'}, 'userC'),
    'MaagLevel': ('OWN-stealth', {'deviceTrustsAttacker': 'ap3', 'cloudRecordsTrust': 'ap4'}, 'userC'),
    **{p: ('CTRL-direct', {'deviceOn': on, 'attackerAuthorized': auth}, 'userC') for p, on, auth in [
        ('Aqara', 'ap5', 'ap4'), ('Dyson', 'ap5', 'ap6'), ('TuyaMatter', 'ap5', 'ap4'), ('Xiaomi', 'ap5', 'ap6'),
        ('TuyaCAC', 'ap5', 'ap6'), ('Huawei', 'ap6', 'ap7'), ('delegationFlaw1', 'ap7', 'ap6'),
        ('delegationFlaw2', 'ap5', 'ap4')]},
    'MQTTFlaw1': ('CTRL-revoked', {'deviceOn': 'ap2', 'attackerAuthorized': 'ap1'}, 'userA'),
    'A2A': ('CTX-isolation', {'attackerReadsVictimData': 'ap4', 'victimContextTampered': 'ap5'}, 'clientB'),
}
TEMPLATE_VARS = {'N', 'Vtx', 'P', 'E', 'S', '..', '...', '....', '.....', '......', '.......'}
EVENT = re.compile(r"^\$ \w+ '[^']*' \w+(?: \| .*)?$")


def maudeBinary():
    arch = {'aarch64': 'arm64', 'amd64': 'x86_64'}.get(os.uname().machine.lower(), os.uname().machine.lower())
    bundled = ROOT / f'Maude-3.5.1-macos-{arch}'
    tmp = Path(tempfile.mkdtemp(prefix='maude-bin-')) / 'maude'
    shutil.copyfile(bundled / 'maude', tmp)
    tmp.chmod(0o700)
    return tmp, bundled


def goldenParts(protocol, slots):
    live = '\n'.join(l for l in (GOLD / protocol / 'checker.maude').read_text().splitlines()
                     if not l.strip().startswith('---'))
    patterns = {}
    for slot, ap in slots.items():
        m = re.search(rf'^eq E @ S (.*?)\s*\|= {ap} = true', live, re.M)
        if not m:
            raise ValueError(f'{protocol}: no state definition for {ap}')
        patterns[slot] = m.group(1)
    decls = []
    for line in re.findall(r'^vars? .+ : \w+ \.$', live.split('mod CHECK')[0], re.M):
        names = line.split(':')[0].split()[1:]
        kept = [n for n in names if n not in TEMPLATE_VARS]
        if kept:
            decls.append(f"vars {' '.join(kept)} : {line.split(':')[1].strip()}")
    forbid = bool(re.search(r'eq basic = .*~ sp', live))
    return patterns, '\n'.join(decls), forbid


def check(binary, lib, directory):
    out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', str(Path(directory) / 'checker.maude')],
                         stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=directory, timeout=900,
                         env=dict(os.environ, MAUDE_LIB=str(lib))).stdout
    tail = out.split('reduce in PostProcess', 1)[-1]
    events = [l.strip() for l in tail.splitlines() if EVENT.match(l.strip())]
    verdict = 'true' if re.search(r'^result Bool: true', tail, re.M) else ('counterexample' if events else 'error')
    return verdict, events


def validate(protocol, binary, lib, work):
    subtype, slots, attacker = MAPPING[protocol]
    patterns, decls, forbid = goldenParts(protocol, slots)
    d = work / protocol
    d.mkdir(parents=True)
    shutil.copyfile(GOLD / protocol / 'rules.maude', d / 'rules.maude')
    (d / 'checker.maude').write_text(renderChecker(subtype, patterns, attacker, decls, forbid))
    gold = check(binary, lib, GOLD / protocol)
    tmpl = check(binary, lib, d)
    if 'error' in (gold[0], tmpl[0]):
        status = 'ERROR'
    elif gold == tmpl:
        status = 'same'
    elif gold[0] == tmpl[0] == 'counterexample' and tmpl[1][:len(gold[1])] == gold[1]:
        status = 'same (golden trace is a cut prefix)'
    else:
        status = 'DIFFERENT'
    return protocol, subtype, forbid, gold, tmpl, status


def main(protocols):
    binary, lib = maudeBinary()
    work = Path(tempfile.mkdtemp(prefix='template-check-'))
    (work / 'lib').symlink_to(GOLD / 'lib')
    with ThreadPoolExecutor(6) as ex:
        results = list(ex.map(lambda p: validate(p, binary, lib, work), protocols or sorted(MAPPING)))
    for p, subtype, forbid, gold, tmpl, status in results:
        print(f'{p:16} {subtype:13} {"~sp" if forbid else "   "} golden={gold[0]:14}({len(gold[1]):2} events) '
              f'template={tmpl[0]:14}({len(tmpl[1]):2} events)  {status}')
    print(f'work dir: {work}')
    return 0 if all(r[-1].startswith('same') for r in results) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
