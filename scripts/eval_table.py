#!/usr/bin/env python3
"""Aggregate one or more full end-to-end runs (run_all_e2e.py output dirs) into the evaluation table.

Every number is computed from files the pipeline wrote: summary.json (verdicts, golden verdicts, event counts,
coverage issues), <protocol>/run.json (load status, time, tokens, input hash) and <protocol>/stages.json (one
record per guardrail attempt). Runs must share the same input per protocol; the script stops otherwise.
Writes table.csv, table.md, table.tex and summary.json into OUT_DIR.
Usage: python scripts/eval_table.py OUT_DIR RUN_DIR [RUN_DIR ...]
"""
import csv, json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPLAY = {'philips': 'Philips Hue'}
COLUMNS = ['protocol', 'property', 'runs', 'load', 'counterexample', 'golden_match', 'pass_at_1', 'first_try',
           'retries', 'coverage_warnings', 'events', 'golden_events', 'time_s', 'tokens_k']


def load_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def guardrail(stages):
    """(retries, every stage passed its guardrail on the first attempt) from stages.json."""
    failed = [e for e in stages or [] if 'attempt' in e and e.get('error')]
    return len(failed), not failed


def protocol_rows(runs):
    names = sorted({r['protocol'] for run in runs for r in run['summary']})
    rows = []
    for name in names:
        samples = []
        for run in runs:
            row = next((r for r in run['summary'] if r['protocol'] == name), None)
            if row is None:
                sys.exit(f'{name} missing from {run["dir"]}')
            manifest = load_json(run['dir'] / name / 'run.json', {})
            retries, first = guardrail(load_json(run['dir'] / name / 'stages.json'))
            samples.append(dict(row, manifest=manifest, retries=retries, first_try=first))
        hashes = {s['manifest'].get('input_sha256') for s in samples}
        if len(hashes) != 1:
            sys.exit(f'{name}: runs used different inputs {hashes}')
        n = len(samples)
        match = sum(s['verdict'] == s['golden_verdict'] for s in samples)
        events = [s['events'] for s in samples if s['verdict'] == 'counterexample']
        rows.append(dict(
            protocol=name, property=samples[0]['subtype'], runs=n,
            load=sum(s['status'] == 'validated' for s in samples),
            counterexample=sum(s['verdict'] == 'counterexample' for s in samples),
            golden_match=match, pass_at_1=round(100 * match / n, 1),
            first_try=sum(s['first_try'] for s in samples), retries=sum(s['retries'] for s in samples),
            coverage_warnings=sum(bool(s['coverage_issues']) for s in samples),
            events=statistics.median(events) if events else None, golden_events=samples[0]['golden_events'],
            time_s=round(statistics.mean(s['manifest'].get('elapsed_seconds', 0) for s in samples), 1),
            tokens_k=round(statistics.mean(s['manifest'].get('tokens_this_run', 0) for s in samples) / 1000, 1)))
    return rows


def aggregate(rows):
    n, p = rows[0]['runs'], len(rows)
    total = lambda k: sum(r[k] for r in rows)
    return dict(protocols=p, runs_per_protocol=n, samples=n * p,
                load=total('load'), counterexample=total('counterexample'), golden_match=total('golden_match'),
                pass_at_1=round(100 * total('golden_match') / (n * p), 1),
                success_in_any_run=sum(r['golden_match'] > 0 for r in rows),
                success_in_every_run=sum(r['golden_match'] == n for r in rows),
                first_try=total('first_try'), retries=total('retries'), coverage_warnings=total('coverage_warnings'),
                time_s=round(statistics.mean(r['time_s'] for r in rows), 1),
                tokens_k=round(statistics.mean(r['tokens_k'] for r in rows), 1))


def frac(k, n):
    return f'{k}/{n}'


def markdown(rows, agg):
    head = ['Protocol', 'Property', 'Load', 'CEX', '= golden', 'Pass@1 (%)', '1st-try guardrail', 'Retries',
            'Coverage warn.', 'Events (median)', 'Golden events', 'Time (s)', 'Tokens (k)']
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in rows:
        n = r['runs']
        lines.append('| ' + ' | '.join(map(str, [
            DISPLAY.get(r['protocol'], r['protocol']), r['property'], frac(r['load'], n), frac(r['counterexample'], n),
            frac(r['golden_match'], n), r['pass_at_1'], frac(r['first_try'], n), r['retries'],
            frac(r['coverage_warnings'], n), r['events'] if r['events'] is not None else '--', r['golden_events'],
            r['time_s'], r['tokens_k']])) + ' |')
    s = agg['samples']
    lines.append('| ' + ' | '.join(map(str, [
        f"**All ({agg['protocols']})**", '', frac(agg['load'], s), frac(agg['counterexample'], s),
        frac(agg['golden_match'], s), agg['pass_at_1'], frac(agg['first_try'], s), agg['retries'],
        frac(agg['coverage_warnings'], s), '', '', agg['time_s'], agg['tokens_k']])) + ' |')
    return '\n'.join(lines) + '\n'


def latex(rows, agg):
    n = agg['runs_per_protocol']
    tex = lambda s: str(s).replace('_', r'\_').replace('%', r'\%')
    out = [r'\begin{table*}[t]', r'\centering', r'\scriptsize',
           rf'\caption{{End-to-end results over {n} independent run{"s" if n > 1 else ""} per protocol.}}',
           r'\label{tab:pilot_eval_matrix}',
           r'\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}} ll ccccc ccc cc @{}}', r'\hline\hline',
           r'\textbf{Protocol} & \textbf{Property} & \textbf{Load} & \textbf{CEX} & \textbf{= $M_{\mathrm{gold}}$} & '
           r'\textbf{Pass@1 (\%)} & \textbf{1st try} & \textbf{Retries} & \textbf{Cov.\ warn.} & \textbf{Events} & '
           r'\textbf{Gold events} & \textbf{Time (s)} & \textbf{Tokens (k)} \\', r'\hline']
    for r in rows:
        k = r['runs']
        out.append(' & '.join(map(tex, [
            DISPLAY.get(r['protocol'], r['protocol']), r['property'], frac(r['load'], k), frac(r['counterexample'], k),
            frac(r['golden_match'], k), r['pass_at_1'], frac(r['first_try'], k), r['retries'],
            frac(r['coverage_warnings'], k), r['events'] if r['events'] is not None else '--', r['golden_events'],
            r['time_s'], r['tokens_k']])) + r' \\')
    s = agg['samples']
    out += [r'\hline', ' & '.join(map(tex, [
        rf"\textbf{{All ({agg['protocols']})}}", '', frac(agg['load'], s), frac(agg['counterexample'], s),
        frac(agg['golden_match'], s), agg['pass_at_1'], frac(agg['first_try'], s), agg['retries'],
        frac(agg['coverage_warnings'], s), '', '', agg['time_s'], agg['tokens_k']])) + r' \\',
        r'\hline\hline', r'\end{tabular*}', r'\end{table*}']
    return '\n'.join(out) + '\n'


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    out = Path(argv[0]).resolve()
    runs = [dict(dir=Path(d).resolve(), summary=load_json(Path(d) / 'summary.json')) for d in argv[1:]]
    for run in runs:
        if run['summary'] is None:
            sys.exit(f'{run["dir"]} has no summary.json')
    rows = protocol_rows(runs)
    agg = aggregate(rows)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'table.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLUMNS); w.writeheader(); w.writerows(rows)
    (out / 'table.md').write_text(markdown(rows, agg))
    (out / 'table.tex').write_text(latex(rows, agg))
    rel = lambda p: str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    (out / 'summary.json').write_text(json.dumps(dict(runs=[rel(r['dir']) for r in runs], aggregate=agg, protocols=rows),
                                                 indent=2) + '\n')
    print(markdown(rows, agg))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
