#!/usr/bin/env python3
"""Assemble Table 1 (LaTeX) from the computed results.

  Compile                 sequence_diagram/output/eval-astra-20261105/table/table.csv (scripts/eval_table.py):
                          k/5 per protocol; the All IoT row counts the protocols at 5/5
  Principals, Attributes  evaluation/results/vocabulary/per_protocol.csv (evaluation/vocabulary.py)
  Prop. Proposition       evaluation/results/propositions/per_protocol.csv (evaluation/propositions.py)
  Flaw Repro.             evaluation/results/trace_equiv_manual/per_protocol.csv (the manual review,
                          evaluation/trace_equiv_manual.py): runs whose counterexample is the gold attack, k/5; with
                          --auto-flaw evaluation/results/flaw_repro/per_protocol.csv (evaluation/flaw_repro.py) instead,
                          only as a hint before the review is done. The All IoT row counts the protocols at 5/5
  Time, Tokens, States    evaluation/results/performance/per_protocol.csv (evaluation/performance.py)
  Percentages are means over the five runs; the All IoT row is the mean over the protocols.
CloudEdgeRTE is left out (its flaw is not expressible by the property templates), as are the agent protocols.
Writes evaluation/results/table1.tex and prints it.
Usage: python evaluation/make_table.py [--auto-flaw]
"""
import csv, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
E2E = ROOT / 'sequence_diagram/output/eval-astra-20261105/table/table.csv'
DISPLAY = {'philips': 'Philips Hue'}
SKIP = {'CloudEdgeRTE', 'A2A', 'MCP'}
COLUMNS = 12


def read(path):
    return {r['protocol']: r for r in csv.DictReader(open(path)) if r['protocol'] not in SKIP}


def num(x):
    if x in (None, ''):
        return '--'
    x = float(x)
    return '100' if x == 100 else f'{x:.1f}'


def main():
    auto = '--auto-flaw' in sys.argv
    e2e = read(E2E)
    src = dict(voc=read(HERE / 'results/vocabulary/per_protocol.csv'),
               prop=read(HERE / 'results/propositions/per_protocol.csv'),
               flaw=read(HERE / ('results/flaw_repro/per_protocol.csv' if auto else
                                 'results/trace_equiv_manual/per_protocol.csv')),
               perf=read(HERE / 'results/performance/per_protocol.csv'))
    names = sorted(e2e, key=str.lower)
    if any(set(names) != set(s) for s in src.values()):
        raise SystemExit('the result files cover different protocols')
    flaw = {p: int(src['flaw'][p]['reproduced' if auto else 'present']) for p in names}
    percent = [('voc', 'principals_acc'), ('voc', 'principals_rec'), ('voc', 'attributes_acc'),
               ('voc', 'attributes_rec'), ('prop', 'acc'), ('prop', 'rec')]
    perf = [('perf', 'time_s'), ('perf', 'tokens_k'), ('perf', 'states')]
    fixed = lambda x: '--' if x in (None, '') else f'{float(x):.1f}'
    line = lambda row: '  ' + ' & '.join(row) + r' \\'
    rows = [line([DISPLAY.get(p, p), f"{e2e[p]['load']}/{e2e[p]['runs']}", *(num(src[s][p][k]) for s, k in percent),
                  f"{flaw[p]}/{e2e[p]['runs']}", *(fixed(src[s][p][k]) for s, k in perf)]) for p in names]

    def mean(s, k):
        return round(statistics.mean(float(src[s][p][k]) for p in names if src[s][p][k] not in (None, '')), 1)

    full = lambda count: sum(count(p) == int(e2e[p]['runs']) for p in names)
    total = line([rf'\textbf{{All IoT ({len(names)})}}', f"{full(lambda p: int(e2e[p]['load']))}/{len(names)}",
                  *(num(mean(s, k)) for s, k in percent), f'{full(flaw.get)}/{len(names)}',
                  *(fixed(mean(s, k)) for s, k in perf)])
    out = [r'\begin{table*}[t]', r'  \centering', r'  \scriptsize', r'  \setlength{\tabcolsep}{0pt}',
           r'  \caption{End-to-end evaluation over five independent runs per protocol. Acc.\ and Rec.\ are accuracy '
           r'and recall in percent. The row All IoT counts the protocols that succeed in all five runs.}',
           r'  \label{tab:pilot_eval_matrix}',
           r'  \begin{tabular*}{\linewidth}{@{\extracolsep{\fill}} l c cccc cc c ccc @{}}', r'  \hline\hline',
           r'  \rule{0pt}{2.5ex} & \textbf{Grammar} & \multicolumn{4}{c}{\textbf{Semantic Fidelity vs.\ $M_{\mathrm{gold}}$}} & '
           r'\multicolumn{3}{c}{\textbf{Verification}} & \multicolumn{3}{c}{\textbf{Performance}} \\',
           r'  \cline{2-2} \cline{3-6} \cline{7-9} \cline{10-12}',
           r'  \rule{0pt}{2.3ex}\textbf{Protocol} & \textbf{Compile} & \multicolumn{2}{c}{\textbf{Principals}} & '
           r'\multicolumn{2}{c}{\textbf{Attributes}} & \multicolumn{2}{c}{\textbf{Prop. Proposition}} & \textbf{Flaw} & '
           r'\textbf{Time} & \textbf{Tokens} & \textbf{States} \\',
           r'   & \textbf{($k$/5)} & \textbf{Acc. (\%)} & \textbf{Rec. (\%)} & \textbf{Acc. (\%)} & \textbf{Rec. (\%)} & '
           r'\textbf{Acc.} & \textbf{Rec.} & \textbf{Repro.\ ($k$/5)} & \textbf{(s)} & \textbf{(k)} & \textbf{Ave.} \\',
           r'  \hline', rf'  \multicolumn{{{COLUMNS}}}{{l}}{{\rule{{0pt}}{{2.5ex}}\textit{{\textbf{{IoT Protocol}}}}}} \\',
           r'  \hline', *rows, r'  \hline', total, r'  \hline\hline', r'  \end{tabular*}', r'\end{table*}']
    text = '\n'.join(out) + '\n'
    (HERE / 'results/table1.tex').write_text(text)
    print(text)


if __name__ == '__main__':
    main()
