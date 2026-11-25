#!/bin/python3
"""Deterministic splitting of a Mermaid sequence diagram into labeled blocks.

Each top-level `alt`/`opt`/... block, and each message outside any block, becomes
one block `B1`, `B2`, ... The label is written into the diagram text so the LLM can
tag every generated rule with the block it comes from (see `stripLabels`).
"""
import re
from dataclasses import dataclass, field

OPEN = re.compile(r'^(alt|opt|loop|par|critical|rect|break)\b\s*(.*)$')
MSG = re.compile(r'^(\w+)\s*(-->>|->>)\s*(\w+)\s*:\s*(.*)$')
LABEL = re.compile(r'\[(B\d+)\]')
SKIP = ('%%', '```', 'sequenceDiagram', 'autonumber', 'actor', 'participant')
NOOP = re.compile(r'\b(ignored?|no (state )?change|without (a )?(response|reply)|rejected)\b', re.I)


@dataclass
class Block:
    id: str
    kind: str          # 'action': starts with an initiated message; 'auto': notes only; 'unconditional': message outside blocks
    head: str
    start: int         # 1-based line numbers in the original input
    end: int
    lines: list[str] = field(default_factory=list)

    def hasStateChange(self) -> bool:
        return any(s.startswith('Note') and not NOOP.search(s) for s in self.lines)


def splitDiagram(text: str) -> list[Block]:
    blocks: list[Block] = []
    depth = 0
    cur: Block | None = None
    for no, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith(SKIP):
            continue
        if OPEN.match(s):
            depth += 1
            if depth == 1:
                cur = Block(f'B{len(blocks) + 1}', 'auto', s, no, no)
                continue
        elif s == 'end':
            depth -= 1
            if depth == 0 and cur is not None:
                cur.end = no
                first = next((l for l in cur.lines if not l.startswith('Note')), '')
                if (m := MSG.match(first)) and m.group(2) == '->>':
                    cur.kind = 'action'
                blocks.append(cur)
                cur = None
                continue
        if cur is not None:
            cur.lines.append(s)
        elif MSG.match(s) and MSG.match(s).group(2) == '->>':
            blocks.append(Block(f'B{len(blocks) + 1}', 'unconditional', s, no, no, [s]))
    return blocks


def annotate(text: str, blocks: list[Block]) -> str:
    """Write each block label into its head line: `alt [B1] cond`, `A->>B: [B2] msg`."""
    heads = {b.start: b for b in blocks}
    out = []
    for no, raw in enumerate(text.splitlines(), 1):
        if b := heads.get(no):
            if b.kind == 'unconditional':
                raw = re.sub(r'(:\s*)', rf'\g<1>[{b.id}] ', raw, count=1)
            else:
                raw = re.sub(r'^(\s*\w+)\b', rf'\g<1> [{b.id}]', raw, count=1)
        out.append(raw)
    return '\n'.join(out) + ('\n' if text.endswith('\n') else '')


def stripLabels(code: str) -> tuple[str, list[str]]:
    """Split `[B1] rule [B2] rule ...` into unlabeled code and one label per chunk.

    Raises ValueError when text precedes the first label or a label is missing.
    """
    parts = LABEL.split(code)
    if parts[0].strip():
        raise ValueError(f'Every rule must start with its block label such as `[B1]`; found unlabeled text: {parts[0].strip()[:80]}')
    labels, chunks = parts[1::2], parts[2::2]
    if not labels:
        raise ValueError('Every rule must start with its block label such as `[B1]`; no label found.')
    return '\n'.join(c.strip() for c in chunks) + '\n', labels


def coverage(blocks: list[Block], stateLabels: list[str], eventLabels: list[str]) -> list[str]:
    issues = []
    for b in blocks:
        nState, nEvent = stateLabels.count(b.id), eventLabels.count(b.id)
        if b.kind in ('action', 'unconditional') and nEvent == 0:
            issues.append(f'{b.id} ({b.kind}, line {b.start}): no event rule for the initiated message')
        if b.kind == 'auto' and nEvent > 0:
            issues.append(f'{b.id} (auto, line {b.start}): {nEvent} event rule(s) for a block without an initiated message')
        if b.hasStateChange() and nState == 0:
            issues.append(f'{b.id} ({b.kind}, line {b.start}): has state-changing notes but no state rule')
    return issues
