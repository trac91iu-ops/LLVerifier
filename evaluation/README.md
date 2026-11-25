# evaluation/

Semantic-fidelity metrics for Table 1, computed from the five frozen v1 runs listed in `runs.txt`.

## State Trans. (state rules)

```
venv/bin/python -B evaluation/propose_mappings.py --jobs 8   # once; skips models that already have a mapping
venv/bin/python -B evaluation/state_trans.py                 # deterministic, about one second
```

1. `propose_mappings.py` asks the LLM (`codex-main` through the project gateway) to align the names of each distinct
   generated model with the gold model: actions, attributes, principals, quoted constants, and attribute values that
   the two models encode differently (for example `true`/`false` against `'on'`/`'off'`). One file per distinct model:
   `mappings/<protocol>/<sha256[:12]>.json`. 145 runs give 119 distinct models. The LLM only aligns names. It does not
   judge the rules. A guardrail checks that every generated name is answered and every target is a gold name.
2. A human checks each mapping file, edits `mapping` if needed, writes a reason in `review_note`, and sets
   `"reviewed": true`. Existing mapping files are never overwritten.
3. `state_trans.py` renames each generated model into the gold vocabulary and compares the state rules (the `eq`/`ceq`
   of `mod SYSTEM`) one by one (`rules.py`). Output goes to `results/state_trans/`:
   `table.md`, `per_protocol.csv`, `per_run.csv`, `summary.json`, and `details/<protocol>.md`. The details show,
   for every distinct model, which generated rule matched which gold rule. Use them to audit the numbers.

### Definitions

A state rule is read as its trigger message, its guards (attribute values on the left-hand side plus the `ceq`
condition), its updates (attribute values the right-hand side changes) and the messages it emits.

- **Effect match**: same trigger action and arguments, same updates, same emitted messages, after renaming variables.
- **Exact match**: effect match, plus the guards agree in the direction being measured. For accuracy, the generated rule
  fires only where the gold rule fires. For recall, it fires wherever the gold rule fires.
- **Accuracy** = generated rules that match some gold rule / generated rules.
  **Recall** = gold rules matched by some generated rule / gold rules.
- Per protocol, the five runs are averaged. The All row averages the 29 protocols. `summary.json` also gives the
  pooled values (all rules together) and the values over loaded runs only. Broadlink's four runs that did not load
  are scored, because their rules are still text.

Normalizations that make two rules with the same meaning compare equal:

- Variables are renamed by unification. Variables that name principals inside attribute paths are tried in every
  assignment.
- A `Device`/`Cloud` variable becomes the constant when the model has only one device/cloud. A message argument
  that is that constant is dropped, because it can take only one value.
- An attribute whose value is a variable used nowhere else is not a guard.
- Set values are compared in any order. A set update is compared by the items it adds and removes, and `..` inside a
  set is not an item. The entries of a record such as `('key' : K , 'time' : T)` are compared in any order.

Everything else counts as a difference, including:

- message argument order or count;
- a set against a single value, for example `'owners'` as a set against a single `'owner'`;
- a constant against a state variable, for example `'secret'` against the cloud's `'secret'` attribute;
- equivalent conditions written differently.

## Principals and Attributes

```
venv/bin/python -B evaluation/vocabulary.py                  # uses the same mappings; output in results/vocabulary/
```

- **Principals**: the principal constants (`userA`, `deviceB`, `cloudA`, ...) from the initial state and the state rules.
- **Attributes**: owner path plus name, for example `deviceB.'key'` or `cloudA.User.'members'`.
  - Users share one schema, so every user is written `User`.
  - An attribute held by a different principal counts as a different attribute, for example the owner kept in the
    cloud's user record instead of in the device record.
  - Fields inside a set value (a ticket record) are values, not attributes.
- The `system` object (fresh counter, clock) is modelling machinery and is excluded from both.
- Accuracy = generated elements whose mapped name is a gold element / generated elements.
  Recall = gold elements that some generated element maps to / gold elements.
- Averaging is the same as for State Trans.: the five runs for each protocol, then the 29 protocols.
- `details/<protocol>.md` lists, for every distinct model, the elements that differ.

## Propositions (slot propositions)

```
venv/bin/python -B evaluation/propositions.py --jobs 8       # about 30 s; output in results/propositions/
```

The property template, and so the temporal structure, is fixed by the program. What Agent_P generates is the state
proposition that fills each slot.

- **Gold side**: the proposition of each slot is the one the template validation uses
  (`scripts/validate_property_templates.py`, `MAPPING`).
- **Not compared**: `attackerActs`, which the program writes.
- **How a pair is checked**:
  1. The generated proposition is renamed into the gold vocabulary with the model's mapping, including value encodings.
  2. Both propositions are evaluated with Maude `search` on the reachable states of the gold model. The search goes
     up to 12 events and skips states beyond the checker's bound (`boundReached`).
  3. At depth 12, most gold state spaces are complete. Broadlink, Philips, Kevo and Netvue are unbounded and are cut
     there.
- **Precise**: the generated proposition never holds where gold is false, and it holds somewhere if gold does.
- **Recalled**: gold never holds where the generated proposition is false.
- **Accuracy** = precise generated slots / generated slots. **Recall** = recalled gold slots / gold slots.
- **Labels**: each slot is labelled
  - `literal` (same text after renaming),
  - `same meaning` (equivalent on the gold states, written differently),
  - `generated narrower` or `generated wider`,
  - `different`, or `not generated`.
- `details/<protocol>.md` shows every distinct pair.
- Runs where Agent_P did not run (Broadlink's four load failures) score 0, and the optional `victimOwner` of Philips,
  which is never generated, counts against recall. `summary.json` also gives the values over loaded runs only.

## Table 1

```
venv/bin/python -B evaluation/make_table.py                  # writes results/table1.tex
```

Compile and Flaw Repro. come from `scripts/eval_table.py`. In the All IoT row they count the protocols at 5/5, and the
other columns average the protocols. A stage that produced nothing scores 0.

## Flaw (counterexample replayed in the gold model)

```
venv/bin/python -B evaluation/flaw_repro.py --jobs 6         # several minutes; output in results/flaw_repro/
```

A returned counterexample is not enough. A wrong slot proposition can make the property trivially violated: in
delegationFlaw2, `attackerAuthorized` never holds, so legitimate use counts as an attack. Each reported flaw is
therefore judged by gold semantics:

1. **Full counterexample.** It is taken from `modelCheck` on the generated model: the prefix and one round of the
   cycle, with every event and state. `counterexample.txt` is not used, because it holds only the prefix.
2. **Reported step.** The step where the generated checker sees the violation is found with the generated property:
   the first `k >= 1` with A at state k and B at state k+1. Later events are dropped. In delegationFlaw2 the cycle
   even contains the real attack, but the reported violation is legitimate use before the revocation.
3. **Replay.** The remaining events are renamed with the mapping and replayed on the gold rules. The flaw is real if
   some subsequence of them that ends with the reported event is a gold execution whose last step violates the gold
   property. Earlier events may be skipped, because counterexamples contain unrelated steps that can be impossible
   in the gold model (August: gold allows pressing the button only once, and the diagram does not say so).
4. **Score.** Accuracy = real flaws / runs that reported a flaw ("--" if none did). Recall = real flaws / runs. The All
   row averages the protocols; for accuracy, only the protocols that reported a flaw.

## Trace Equiv. (gold attack replayed in the generated model)

```
venv/bin/python -B evaluation/trace_equiv.py --jobs 8        # several minutes; output in results/trace_equiv/
```

Trace Equiv. asks whether the generated model can execute the gold attack.

- **Gold trace.** The trace is taken in full from `modelCheck` on the gold rules and gold checker: the prefix, then
  one round of the cycle, with every event. `comparison.md` is not used. Its trace comes from `lib/postProcess.maude`,
  which prints only the prefix and drops events that change no state. In Imou, the attacker's bind is in the cycle,
  so that trace stops before the attack completes.
- **Rename.** Events are renamed into the generated vocabulary by inverting the mapping. A gold name that several
  generated names map to may be any of them. Data arguments are left free.
- **Replay.** Replay works as in `flaw_repro.py`: events in order, any of them may be skipped. The gold attack is
  present if some subsequence of the gold trace violates the generated property in the generated model. The generated
  property is the generated checker; whether its propositions are right is measured by Propositions.
- **Scoring.** A model that did not load scores 0. Per protocol, the score is the percent of the five runs. The All
  row averages the protocols.

## Trace Equiv. (manual review)

1. `python evaluation/trace_equiv_review.py` writes `results/trace_equiv_review/data.json` (gold attack cut at the violation, every distinct generated model with its rules, mapping and counterexample).
2. Review in `review/index.html` (published with `data.json` beside it); one verdict per distinct model, stored in the artifact database collection `verdicts`.
3. Export the verdicts (ArtifactData list, `out_dir` `results/trace_equiv_manual/export`), then `python evaluation/trace_equiv_manual.py results/trace_equiv_manual/export`.
4. `python evaluation/make_table.py --manual-trace`.

## Performance

`python evaluation/performance.py [--jobs N]` reads `<protocol>/run.json` of the five runs (`runs.txt`) and writes
`results/performance/`. Time is `elapsed_seconds` (the whole pipeline for one protocol; Maude takes about 0.5 s of it),
tokens are `tokens_this_run` (input and output, retries included), both averaged over the five runs. States is the
number of distinct system states S reachable within the checker bound: a copy of `rules.maude` whose rules fire only
from states with counter < 5 and time < 3, listed with `search init =>* V:Vertex`; a vertex E @ S also records the
last event, and vertices reached by different events with the same S count once (the vertex counts stay in the CSV).
Mean over the runs whose model loaded, and the gold model counted the same way. A full run takes about 17 minutes. The trace length (`check.events`) is kept in the CSV but
not used in Table 1: it is the first counterexample of Maude's depth-first search and depends on rule order.
