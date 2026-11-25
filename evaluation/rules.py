"""Parse the state rules of a Maude model (the eq/ceq statements of mod SYSTEM) and compare two models rule by rule.

A state rule is read as
  trigger  the message on the left-hand side (sender, action, receiver, arguments),
  guards   the attribute values the left-hand side requires, plus the ceq condition,
  updates  the attribute values the right-hand side changes,
  emits    the messages on the right-hand side.
An attribute whose value is a variable used nowhere else in the rule is no requirement and is dropped from the guards.

Two rules have the same effect when trigger, updates and emits are equal after renaming the variables of one rule into
the other (found by unifying the two rules position by position). Exact matching additionally compares the guards.
A generated rule r is precise for gold rule g when r fires only where g fires (guards(g) is a subset of guards(r)),
and g is recalled by r when r fires wherever g fires (guards(r) is a subset of guards(g)). So a generated rule that
merges two gold cases recalls both, and a gold rule split into two generated cases is recalled by neither half alone.
"""
import re
from dataclasses import dataclass, field
from itertools import permutations

TOKEN = re.compile(r"'[^'\s]*'|[A-Za-z_][A-Za-z0-9_]*|\.{2,}|[0-9]+|\S")
QID = re.compile(r"'[^'\s]*'$")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*$")
ELLIPSIS = re.compile(r"\.{2,}$")
BUILTIN = {'nils', 'true', 'false', 'none', 'idle', 'ep', 'if', 'and', 'or', 'not', 'xor', 'empty'}


def tokens(s):
    return TOKEN.findall(s)


def norm(s):
    return ' '.join(tokens(s))


def split_top(s, sep):
    """Split s at sep where it is outside parentheses."""
    out, depth, cur, i = [], 0, '', 0
    while i < len(s):
        c = s[i]
        depth += (c == '(') - (c == ')')
        if depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur, i = '', i + len(sep)
            continue
        cur += c
        i += 1
    return [x.strip() for x in out + [cur] if x.strip()]


def strip_parens(s):
    s = s.strip()
    while s.startswith('(') and s.endswith(')'):
        depth = 0
        for i, c in enumerate(s):
            depth += (c == '(') - (c == ')')
            if depth == 0 and i < len(s) - 1:
                return s
        s = s[1:-1].strip()
    return s


def parse_map(s, prefix, out):
    """Flatten an attribute set into out[(principal, key, ...)] = value; False if s is not an attribute set."""
    items = split_top(strip_parens(s), ',')
    if not items or not all(ELLIPSIS.match(i) or len(split_top(i, ' : ')) > 1 for i in items) \
            or all(ELLIPSIS.match(i) for i in items):
        return False
    for item in items:
        if ELLIPSIS.match(item):
            continue
        key, *value = split_top(item, ' : ')
        value = ' : '.join(value)
        if not parse_map(value, prefix + (norm(key),), out):
            out[prefix + (norm(key),)] = value_norm(value)
    return True


def item_norm(item):
    """A set item; an attribute record such as ('key' : K , 'time' : T) gets its entries sorted by key."""
    entries = split_top(strip_parens(item), ',')
    if len(entries) > 1 and all(' : ' in e for e in entries):
        return '( ' + ' , '.join(sorted(norm(e) for e in entries)) + ' )'
    return norm(strip_parens(item))


def value_norm(v):
    """Whitespace-normalized value; a set value (top-level commas) is kept as a sorted tuple of items."""
    items = split_top(strip_parens(v), ',')
    return item_norm(items[0]) if len(items) == 1 else tuple(sorted(item_norm(i) for i in items))


@dataclass
class Msg:
    sender: str
    action: str
    receiver: str
    args: tuple

    def key(self):
        return (self.sender, self.action, self.receiver) + self.args


def parse_msg(s):
    head, _, args = s.partition('|') if '|' in s else (s, '', '')
    parts = head.split()
    if len(parts) < 3:
        raise ValueError(f'cannot read message: {s!r}')
    return Msg(parts[0], parts[1], ' '.join(parts[2:]), tuple(norm(a) for a in split_top(strip_parens(args), ';')))


def parse_soup(s):
    """Objects (as flattened attribute dicts) and messages of a soup term."""
    attrs, objects, msgs, i, depth = {}, [], [], 0, 0
    s = s.strip()
    while i < len(s):
        c = s[i]
        if c == '<' and depth == 0:
            j, d = i + 1, 0
            while j < len(s) and not (d == 0 and s[j] == '>' and s[j - 1] == ' '):
                d += (s[j] == '(') - (s[j] == ')')
                j += 1
            name, _, body = s[i + 1:j].partition('|')
            objects.append(norm(name))
            parse_map(body, (norm(name),), attrs)
            i = j + 1
        elif c == '$' and depth == 0:
            j, d = i + 1, 0
            while j < len(s) and not (d == 0 and s[j] in '<$'):
                d += (s[j] == '(') - (s[j] == ')')
                j += 1
            msgs.append(parse_msg(s[i + 1:j].strip()))
            i = j
        else:
            i += 1
    return attrs, objects, msgs


@dataclass
class Rule:
    text: str
    trigger: Msg | None
    pre: dict
    post: dict
    post_objects: list
    emits: list
    conds: list = field(default_factory=list)


def find_eq(s):
    depth = 0
    for i, c in enumerate(s):
        depth += (c == '(') - (c == ')')
        if depth == 0 and c == '=' and s[i - 1] in ' \n' and s[i + 1:i + 2] in (' ', '\n'):
            return i
    raise ValueError(f'no = in {s!r}')


def parse_rule(stmt):
    body = stmt.split(None, 1)[1].rstrip()[:-1]
    k = find_eq(body)
    lhs, rhs = body[:k], body[k + 1:]
    conds = []
    if stmt.startswith('ceq'):
        rhs, _, cond = rhs.partition(' if ')
        conds = [norm(c) for c in split_top(cond, '/\\')]
    pre, _, lmsgs = parse_soup(lhs)
    post, post_objects, emits = parse_soup(rhs)
    return Rule(' '.join(stmt.split()), lmsgs[0] if lmsgs else None, pre, post, post_objects, emits, conds)


@dataclass
class Model:
    variables: dict
    init: str
    rules: list


def statements(text):
    out, cur = [], ''
    for line in text.splitlines():
        line = line.split('***')[0].rstrip()
        if not line.strip():
            continue
        cur = (cur + '\n' + line) if cur else line.strip()
        if line.endswith(' .') or line.strip() == '.':
            out.append(cur.strip())
            cur = ''
    return out


def load_model(path):
    text = path.read_text()
    m = re.search(r'^mod SYSTEM is\b[^\n]*$(.*?)^endm', text, re.S | re.M)  # A2A has a comment after `is`
    if not m:
        raise ValueError(f'{path}: no mod SYSTEM')
    variables, init, rules = {}, '', []
    for st in statements(m.group(1)):
        head = st.split(None, 1)[0]
        if head in ('var', 'vars'):
            names, _, sort = st[len(head):-1].rpartition(':')
            for n in names.split():
                variables[n] = sort.strip()
        elif st.startswith('eq init'):
            init = st
        elif head in ('eq', 'ceq'):
            rules.append(parse_rule(st))
    return Model(variables, init, rules)


# ---------------------------------------------------------------- names, for the mapping step

def inventory(model):
    """Names used by the state rules and the initial state, by category."""
    acts, attrs, principals, consts = set(), set(), set(), set()
    var = model.variables

    def ident(t):
        return IDENT.match(t) and t not in var and t not in BUILTIN and not ELLIPSIS.match(t)

    def values(v):
        for t in (v if isinstance(v, tuple) else (v,)):
            toks = tokens(t)
            for i, x in enumerate(toks):
                if QID.match(x):
                    consts.add(x)
                elif ident(x) and not (i + 1 < len(toks) and toks[i + 1] == '('):
                    principals.add(x)

    for r in model.rules:
        for d in (r.pre, r.post):
            for path, v in d.items():
                if ident(path[0]):
                    principals.add(path[0])
                for p in path[1:]:
                    (attrs.add(p) if QID.match(p) else principals.add(p) if ident(p) else None)
                values(v)
        for msg in ([r.trigger] if r.trigger else []) + r.emits:
            acts.add(msg.action)
            for p in (msg.sender, msg.receiver):
                if ident(p):
                    principals.add(p)
            for a in msg.args:
                values(a)
        for c in r.conds:
            values(c)
    init_attrs, _, _ = parse_soup(model.init.split('@', 1)[1].rstrip(' .')) if '@' in model.init else ({}, [], [])
    for path, v in init_attrs.items():
        principals.add(path[0])
        for p in path[1:]:
            (attrs.add(p) if QID.match(p) else principals.add(p))
        values(v)
    consts -= attrs | acts
    return dict(actions=sorted(acts), attributes=sorted(attrs), principals=sorted(principals), constants=sorted(consts))


# ---------------------------------------------------------------- comparison

def rename_tok(s, sub):
    return ' '.join(sub.get(t, t) for t in tokens(s))


def rename_val(v, sub):
    return tuple(sorted(rename_tok(x, sub) for x in v)) if isinstance(v, tuple) else rename_tok(v, sub)


def device_constants(model, prefix):
    attrs, objects, _ = parse_soup(model.init.split('@', 1)[1].rstrip(' .')) if '@' in model.init else ({}, [], [])
    names = set(objects) | {p[1] for p in attrs if len(p) > 1}
    return sorted(n for n in names if n.startswith(prefix))


def updates_of(pre, post, post_objs):
    """What the right-hand side changes. A set-valued attribute is described by the items it adds and removes, so
    adding a user to an owner set is the same update however the rest of the set is written. A rest-of-set
    placeholder (.., ...) is not an item."""
    out = {}
    for p, v in post.items():
        old = pre.get(p)
        if old == v:
            continue
        if old is not None and (isinstance(old, tuple) or isinstance(v, tuple)):
            a, b = list(old if isinstance(old, tuple) else (old,)), list(v if isinstance(v, tuple) else (v,))
            added = [x for x in b if x not in a or a.remove(x)]
            a = list(old if isinstance(old, tuple) else (old,))
            removed = [x for x in a if x not in b or b.remove(x)]
            added, removed = [x for x in added if not ELLIPSIS.match(x)], [x for x in removed if not ELLIPSIS.match(x)]
            out[p] = ('+',) + tuple(sorted(added)) + ('-',) + tuple(sorted(removed))
        else:
            out[p] = v
    out.update({p: '<removed>' for p in pre if p not in post and p[0] in post_objs})
    return out


@dataclass
class Canon:
    trigger: tuple | None
    guards: frozenset
    updates: dict
    emits: tuple
    variables: set
    pre: dict
    post: dict
    post_objs: set


def canon(rule, model, mapping, values=(), actions=None):
    """Apply the name mapping and the value mapping, replace Device/Cloud variables by the model's only device/cloud,
    drop message arguments that are that only device/cloud (they can take one value and carry no information), and
    drop wildcard guards. values holds (gold attribute, generated value, gold value) for differently encoded values.
    actions maps action names; it is applied only at the action position, since a name can be both an action and an
    attribute."""
    sub, only = dict(mapping), set()
    for sort, prefix in (('Device', 'device'), ('Cloud', 'cloud')):
        consts = device_constants(model, prefix)
        if len(consts) == 1:
            const = mapping.get(consts[0], consts[0])
            only.add(const)
            sub.update({v: const for v, s in model.variables.items() if s == sort})
    variables = {v for v in model.variables if v not in sub}
    rp = lambda path: tuple(rename_tok(p, sub) for p in path)
    recode = {(a, norm(g)): norm(o) for a, g, o in values}
    rv = lambda path, v: recode.get((path[-1], v), v) if isinstance(v, str) else v
    pre = {rp(p): rv(rp(p), rename_val(v, sub)) for p, v in rule.pre.items()}
    post = {rp(p): rv(rp(p), rename_val(v, sub)) for p, v in rule.post.items()}
    act = lambda a: (actions or {}).get(a, a)
    msg = lambda m: (rename_tok(m.sender, sub), act(m.action), rename_tok(m.receiver, sub)) + tuple(
        a for a in (rename_tok(a, sub) for a in m.args) if a not in only)
    trigger = msg(rule.trigger) if rule.trigger else None
    emits = tuple(sorted(msg(m) for m in rule.emits))
    conds = [rename_tok(c, sub) for c in rule.conds]
    count = {}
    for t in [*(x for p in pre for x in p), *(x for p in post for x in p), *(trigger or ()), *(x for e in emits for x in e),
              *conds, *(x for v in [*pre.values(), *post.values()] for x in (v if isinstance(v, tuple) else (v,)))]:
        for tok in tokens(t):
            count[tok] = count.get(tok, 0) + 1
    wild = {p for p, v in pre.items() if isinstance(v, str) and v in variables and count[v] == 1}
    pre = {p: v for p, v in pre.items() if p not in wild}
    post_objs = {rename_tok(o, sub) for o in rule.post_objects}
    guards = frozenset(list(pre.items()) + [('if', c) for c in conds])
    return Canon(trigger, guards, updates_of(pre, post, post_objs), emits, variables, pre, post, post_objs)


def unify(a, b, sub, avars, bvars):
    """Extend sub (variables of a -> variables of b) so that term a equals term b; False if impossible.
    Set values (tuples) are tried in every item order, up to six items."""
    if isinstance(a, tuple) != isinstance(b, tuple):
        return False
    if isinstance(a, tuple):
        if len(a) != len(b) or len(a) > 6:
            return False
        for perm in permutations(a):
            trial = dict(sub)
            if unify(' '.join(perm), ' '.join(b), trial, avars, bvars):
                sub.update(trial)
                return True
        return False
    ta, tb = tokens(a), tokens(b)
    if len(ta) != len(tb):
        return False
    new, used = {}, set(sub.values())
    for x, y in zip(ta, tb):
        if x in avars:
            cur = sub.get(x, new.get(x))
            if cur is None:
                if y not in bvars or y in used:
                    return False
                new[x] = y
                used.add(y)
            elif cur != y:
                return False
        elif x != y:
            return False
    sub.update(new)
    return True


def align(r, g, seed=None):
    """Rename r's variables into g's; returns the renamed r (trigger, guards, updates, emits)."""
    sub = dict(seed or {})
    if r.trigger and g.trigger and r.trigger[1] == g.trigger[1] and len(r.trigger) == len(g.trigger):
        for x, y in zip(r.trigger, g.trigger):
            unify(x, y, sub, r.variables, g.variables)
    for _ in range(2):
        for side_r, side_g in ((r.pre, g.pre), (r.post, g.post)):
            for path, v in sorted(side_r.items(), key=str):
                gp = tuple(sub.get(t, t) for t in path)
                if gp in side_g:
                    unify(v, side_g[gp], sub, r.variables, g.variables)
                elif len(path) == len(gp):
                    for cand in side_g:
                        if len(cand) == len(path) and unify(' '.join(path), ' '.join(cand), dict(sub), r.variables, g.variables):
                            if unify(' '.join(path), ' '.join(cand), sub, r.variables, g.variables):
                                unify(v, side_g[cand], sub, r.variables, g.variables)
                            break
        for er, eg in zip(r.emits, g.emits):
            if er[1] == eg[1] and len(er) == len(eg):
                for x, y in zip(er, eg):
                    unify(x, y, sub, r.variables, g.variables)
    full = {v: sub.get(v, '?' + v) for v in r.variables}
    rn = lambda t: rename_tok(t, full)
    rp = lambda path: tuple(rn(p) for p in path)
    guards = frozenset((rp(k), rename_val(v, full)) if k != 'if' else (k, rn(v)) for k, v in r.guards)
    updates = updates_of({rp(p): rename_val(v, full) for p, v in r.pre.items()},
                         {rp(p): rename_val(v, full) for p, v in r.post.items()}, {rn(o) for o in r.post_objs})
    emits = tuple(sorted(tuple(rn(x) for x in e) for e in r.emits))
    trigger = tuple(rn(x) for x in r.trigger) if r.trigger else None
    return trigger, guards, updates, emits


def path_vars(c):
    """Variables naming a principal inside an attribute path, e.g. UserX in cloudA / UserX / 'members'."""
    return sorted({t for d in (c.pre, c.post) for path in d for t in path if t in c.variables})


def compare(r, g):
    """(same effect, r precise for g, g recalled by r) for canonical rules r (generated) and g (gold).
    Rules with different trigger actions never match. Otherwise the variables that name principals inside attribute
    paths are tried in every assignment to g's (up to four of them), and the best outcome is kept."""
    if (r.trigger is None) != (g.trigger is None) or (r.trigger and r.trigger[1] != g.trigger[1]):
        return False, False, False
    rv, gv = path_vars(r), path_vars(g)
    seeds = [{}]
    if 0 < len(rv) <= 4:
        seeds += [{a: b for a, b in zip(rv, perm) if b is not None}
                  for perm in permutations(gv + [None] * len(rv), len(rv))]
    best = (False, False, False)
    for seed in seeds:
        trigger, guards, updates, emits = align(r, g, seed)
        effect = trigger == g.trigger and updates == g.updates and emits == g.emits
        res = (effect, effect and g.guards <= guards, effect and guards <= g.guards)
        if res > best:
            best = res
            if all(res):
                break
    return best
