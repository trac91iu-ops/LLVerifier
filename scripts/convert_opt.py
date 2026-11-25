"""Rewrite inner blocks of the diagram inputs to the authoring convention: the outer `alt` says who can act;
an inner block with one outcome is `opt`, with several outcomes `alt`/`else`; "ignored" branches are dropped.
A branch is "ignored" when its body is only Notes that diagram.NOOP recognizes (no message, no state change).
Usage: python scripts/convert_opt.py [--write] [protocol ...]   (default: report only)
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'src'))
from diagram import NOOP

INPUT = ROOT / 'sequence_diagram/input'
OPEN = re.compile(r'^(\s*)(alt|opt|loop|par|critical|rect|break)\b\s*(.*)$')
ELSE = re.compile(r'^(\s*)else\b\s*(.*)$')
END = re.compile(r'^\s*end\s*$')


def parse(lines, i, depth):
    """Parse lines[i:] into a list of items until an unmatched else/end; return (items, next index)."""
    items = []
    while i < len(lines):
        l = lines[i]
        if ELSE.match(l) or END.match(l):
            return items, i
        m = OPEN.match(l)
        if m:
            indent, kind, cond = m.groups()
            branches, i = [], i + 1
            body, i = parse(lines, i, depth + 1)
            branches.append([cond, body])
            while i < len(lines) and ELSE.match(lines[i]):
                body, j = parse(lines, i + 1, depth + 1)
                branches.append([ELSE.match(lines[i]).group(2), body]); i = j
            assert i < len(lines) and END.match(lines[i]), f'unbalanced block at line {i + 1}'
            items.append(dict(kind=kind, indent=indent, branches=branches, depth=depth, end=lines[i]))
            i += 1
        else:
            items.append(l); i += 1
    return items, i


def ignored(body):
    """Only Notes, and every sentence of every Note says nothing happens."""
    lines = [x for x in body if isinstance(x, str) and x.strip() and not x.strip().startswith('%%')]
    def noop(note):
        text = note.split(':', 1)[1] if ':' in note else note
        sentences = [s for s in re.split(r'(?<=\.)\s+', text.strip()) if s.strip()]
        return all(NOOP.search(s) for s in sentences)
    return all(isinstance(x, str) for x in body) and lines and \
        all(l.strip().startswith('Note') and noop(l) for l in lines)


def render(items, notes):
    out = []
    for it in items:
        if isinstance(it, str):
            out.append(it); continue
        kind, branches = it['kind'], it['branches']
        if it['depth'] >= 1 and kind == 'alt':
            kept = [b for b in branches if not ignored(b[1])]
            dropped = len(branches) - len(kept)
            if not kept:
                notes.append(f"KEPT AS IS (every branch ignored): alt {branches[0][0]}")
                kept = branches
            elif dropped:
                notes.append(f"dropped {dropped} ignored branch(es) under: {branches[0][0]}")
            kind = 'opt' if len(kept) == 1 else 'alt'
            if kind == 'opt' and kept[0] is not branches[0]:
                notes.append(f"opt condition taken from the else branch: {kept[0][0]}")
            branches = kept
        out.append(f"{it['indent']}{kind} {branches[0][0]}".rstrip())
        out += render(branches[0][1], notes)
        for cond, body in branches[1:]:
            out.append(f"{it['indent']}else {cond}".rstrip())
            out += render(body, notes)
        out.append(it['end'])
    return out


def convert(text):
    lines = text.split('\n')
    items, i = parse(lines, 0, 0)
    assert i == len(lines), f'stray else/end at line {i + 1}'
    notes = []
    return '\n'.join(render(items, notes)), notes


if __name__ == '__main__':
    write = '--write' in sys.argv
    names = [a for a in sys.argv[1:] if a != '--write'] or sorted(d.name for d in INPUT.iterdir() if (d / 'diagram.md').exists())
    for name in names:
        p = INPUT / name / 'diagram.md'
        new, notes = convert(p.read_text())
        changed = new != p.read_text()
        print(f"{name:16} {'changed' if changed else 'unchanged'}  " + ' | '.join(n for n in notes if not n.startswith('dropped')))
        if write and changed:
            p.write_text(new)
