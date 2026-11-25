# Golden checker update and trace runs

- Updated 26 IoT checkers: removed the scheduling clauses from `fairness`, retained each original final attack condition as `safety`, and changed the declaration and `spec` reference accordingly.
- Preserved predicate definitions, `basic`, the leading next operator in `spec`, and all rules files.
- Left the manually edited iRobot, Philips, and Aqara checkers unchanged. Left A2A unchanged because its formula is an invariant rather than the IoT attack-witness formula.
- Ran all 29 IoT checkers with `Maude-3.5.1-macos-x86_64/maude`, sending `quit` after the loaded postprocessor completed. All produced an event trace.
- Saved postprocessor output in the corresponding `.txt` files in this directory. Full stdout/stderr and the per-model summary are in `run_logs/`.

## Interpretation and limitations

Here `safety` retains the user's naming convention: the eventual formula describes an attack witness. The checked specification remains `O ~ (safety /\ basic)`. A trace is evidence for that precise formula, not an independently audited security verdict.

All runs emitted the same bundled `prelude.maude` META-LEVEL/metaPrettyPrint warnings, including the unchanged iRobot checker. These runs are recorded as `trace_with_runtime_warning`, not warning-free validation.

The existing postprocessor prints the counterexample prefix and an event projection; it does not preserve the counterexample loop. Philips also has an existing `stopAt` cut point for the projected event list. No trace minimization or postprocessor changes were made.
