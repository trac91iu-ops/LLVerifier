"""Offline regression tests for the model-only LLMSession pipeline.

Run with: venv/bin/python -B -m unittest discover -s tests -p test_model_pipeline.py -v
"""

import importlib
import json
import re
import os
from pathlib import Path
import sys
import tempfile
import unittest
from copy import deepcopy
from unittest.mock import Mock, call, patch


ROOT = Path(__file__).resolve().parents[1]


def config_data(directory):
    return {
        "VERSION": "unittest",
        "MODE": "useapi",
        "DEBUG": False,
        "VERBOSE": 0,
        "LOG": False,
        "LOGDIR": str(directory),
        "LOGFILE": str(directory / "session.log"),
        "CACHEFILE": str(directory / "cache.json"),
        "OUTDIR": str(directory / "output"),
        "LIBDIR": str(directory / "lib"),
        "ERROR_RETRY": 2,
        "PROVIDERS": {},
        "STRATEGIES": {
            name: {"provider": ["offline", "stub"]}
            for name in ("default", "revise")
        },
    }


# JSON is valid YAML. Never import the developer's real configuration (which
# may print debugging information or contain credentials) for this test module.
with tempfile.TemporaryDirectory(prefix="model-pipeline-import-") as directory:
    directory = Path(directory)
    config_path = directory / "config.yaml"
    config_path.write_text(json.dumps(config_data(directory)), encoding="utf-8")
    sys.path.insert(0, str(ROOT / "src"))
    try:
        with patch.dict(os.environ, {"LLVERIFIER_CONFIG": str(config_path)}):
            interface = importlib.import_module("LLMInterface")
    finally:
        sys.path.remove(str(ROOT / "src"))


DIAGRAM = """```mermaid
sequenceDiagram
    participant C as Cloud
    participant D as Device
    Note over C,D: [Cloud[D]] has owner [User[A]]
    opt Cloud[D].owner == nils
        D->>C: bind(D)
    end
```

Final protocol paragraph: revocation retains cached keys and permits replay.
"""

BLOCK_DIAGRAM = """```mermaid
sequenceDiagram
    actor UserX
    participant Device
    alt The user is near the device
        UserX->>Device: The user presses the button
        alt The button is not pressed
            Note over Device: The device records the press.
        else The button is pressed
            Note over Device: The request is ignored.
        end
    end
    alt The device is pressed
        Note over Device: The device clears the press.
    end
    UserX->>Device: probe(Device)
```
"""


def src_module(name):
    sys.path.insert(0, str(ROOT / "src"))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(ROOT / "src"))


class ModelPipelineTests(unittest.TestCase):
    def test_transitions_reject_unbound_event_arguments(self):
        for name in ("Secret", "FreshSecret", "CurrentTime"):
            code = f"< UserX | ... > < CloudX | ... > => ev4(UserX, CloudX, {name}) ."
            error = interface.checkers.checkTransitions(code)
            self.assertIsNotNone(error)
            self.assertIn(name, error)
        for argument in ("'secret'", "Secret"):
            code = f"< UserX | 'key' : Secret , ... > < CloudX | ... > => ev4(UserX, CloudX, {argument}) ."
            self.assertIsNone(interface.checkers.checkTransitions(code))

    def test_event_declarations_preserve_constants_and_collect_variables(self):
        sys.path.insert(0, str(ROOT / "src"))
        try:
            analysis = importlib.import_module("analyze")
        finally:
            sys.path.remove(str(ROOT / "src"))
        code = "< DeviceX | 'key' : Secret , ... > $ UserX 'callAPI:bind' CloudX | ('device' ; Secret ; 7 ; true ; nils ; deviceA) => < DeviceX | 'key' : Secret , ... > ."
        ast = analysis.parseAST(code, {"DeviceX": "Device", "UserX": "User", "CloudX": "Cloud", "Secret": "Qid"})
        declarations = analysis.giveEvtDecls(analysis.extractEventsFromAST(ast))
        self.assertEqual(len(declarations), 1)
        self.assertIn("ev1(UserX, CloudX, Secret)", str(declarations[0]))
        self.assertIn("'device' ; Secret ; 7 ; true ; nils ; deviceA", str(declarations[0]))

    def test_variable_inference_uses_names_and_preserves_known_types(self):
        sys.path.insert(0, str(ROOT / "src"))
        try:
            synthesis = importlib.import_module("synthesize")
        finally:
            sys.path.remove(str(ROOT / "src"))
        code = "< UserX | 'key' : KeyA , 'counter' : N , ... > $ UserX 'send' DeviceY | KeyA => < UserX | 'key' : KeyA , ... > ."
        ast = synthesis.parseAST(code)
        known = {"N": "Nat", "UserX": "User"}
        infer = Mock(return_value={"DeviceY": "Device", "KeyA": "Qid"})
        types, declarations = synthesis.extractAndNameVariables(infer, "description", code, ast, known)
        infer.assert_called_once_with("description", code, ["DeviceY", "KeyA"])
        self.assertEqual(known, {"N": "Nat", "UserX": "User"})
        self.assertEqual(types, {**known, "DeviceY": "Device", "KeyA": "Qid"})
        for variable in synthesis.extractVarsFromAST(ast):
            self.assertEqual(variable.type_, types[variable.ident])
        self.assertIn("vars KeyA : Qid .", declarations)
        infer.reset_mock()
        synthesis.extractAndNameVariables(infer, "description", code, ast, types)
        infer.assert_not_called()

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="model-pipeline-test-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        config_path = self.directory / "config.yaml"
        config_path.write_text(json.dumps(config_data(self.directory)), encoding="utf-8")
        self.config = interface.CONFIGCLS.load(str(config_path))
        self.session = interface.LLMSession(self.config, context_id="diagram-context")
        for target in ("initOpenAI", "callAPI", "manualAsk"):
            blocker = patch.object(
                interface.LLMSession, target,
                side_effect=AssertionError("External dispatch is forbidden in unit tests"),
            )
            blocker.start()
            self.addCleanup(blocker.stop)

    def stub_dispatch(self, *responses):
        answers = iter(responses)

        def dispatch(messages, strategy=None):
            self.session.msg = deepcopy(messages)
            answer = next(answers)
            self.session.output = answer
            self.session.msg.append({"role": "assistant", "content": answer})
            return answer

        self.session.dispatchRequst = Mock(side_effect=dispatch)
        return self.session.dispatchRequst

    def saved_cache(self):
        return json.loads(Path(self.config.CACHEFILE).read_text(encoding="utf-8"))

    def test_main_passes_entire_input_to_every_agent_without_split(self):
        sys.path.insert(0, str(ROOT / "src"))
        try:
            entry = importlib.import_module("main")
        finally:
            sys.path.remove(str(ROOT / "src"))
        source = self.directory / "diagram.md"
        source.write_text(DIAGRAM, encoding="utf-8")
        out = self.directory / "run"
        with patch.object(entry, "synthesizeRules", return_value=("rules", "template", "events", None)) as synthesize:
            self.assertEqual(entry.main([str(source), "--out", str(out), "--skip-validation"]), 0)
        self.assertEqual(synthesize.call_args.args[1:], (DIAGRAM, None))  # model mode: no property subtype
        self.assertFalse((out / "parsed_input.json").exists())
        self.assertEqual(json.loads((out / "stages.json").read_text()), [])  # main itself makes no LLM call

    def test_source_context_is_appended_only_when_prompt_lacks_it(self):
        dispatch = self.stub_dispatch("first", "second")
        self.session.source_context = DIAGRAM
        self.session.generalAskWithAutoCheck("withInput", [{"role": "user", "content": "rules for\n" + DIAGRAM}])
        self.assertEqual(sum(DIAGRAM in m["content"] for m in dispatch.call_args.args[0]), 1)
        self.session.generalAskWithAutoCheck("withoutInput", [{"role": "user", "content": "atomic propositions"}])
        self.assertIn(DIAGRAM, dispatch.call_args.args[0][-1]["content"])

    def test_retry_validates_and_accepts_last_allowed_revision(self):
        dispatch = self.stub_dispatch("bad draft", "bad repair", "valid")
        checker = Mock(side_effect=lambda answer: None if answer == "valid" else "invalid")
        self.session.mountChecker("testStage", checker)
        self.assertEqual(self.session.generalAskWithAutoCheck(
            "testStage", [{"role": "user", "content": "generate"}]), "valid")
        self.assertEqual(checker.call_args_list, [call("bad draft"), call("bad repair"), call("valid")])
        self.assertEqual(dispatch.call_count, 3)
        self.assertEqual(list(self.saved_cache()["answers"].values()), ["valid"])

    def test_exhausted_retry_checks_final_revision_and_never_caches_invalid_answer(self):
        dispatch = self.stub_dispatch("bad draft", "bad repair", "still invalid")
        checker = Mock(return_value="invalid")
        self.session.mountChecker("testStage", checker)
        with self.assertRaises(ValueError):
            self.session.generalAskWithAutoCheck(
                "testStage", [{"role": "user", "content": "generate"}])
        self.assertEqual(checker.call_args_list, [call("bad draft"), call("bad repair"), call("still invalid")])
        self.assertEqual(dispatch.call_count, 3)
        self.assertEqual(self.session.cache, {})
        self.assertEqual(self.saved_cache()["answers"], {})

    def test_function_cache_distinguishes_prompts_and_reuses_identical_prompt(self):
        dispatch = self.stub_dispatch("first answer", "second answer")
        first = [{"role": "user", "content": "first input"}]
        second = [{"role": "user", "content": "second input"}]
        for prompt, expected in ((first, "first answer"), (second, "second answer"),
                                 (deepcopy(first), "first answer")):
            self.assertEqual(self.session.generalAskWithAutoCheck("testStage", prompt), expected)
        self.assertEqual(dispatch.call_count, 2)
        self.assertEqual(len(self.saved_cache()["answers"]), 2)

    def test_function_cache_includes_original_protocol_context(self):
        dispatch = self.stub_dispatch("first", "second")
        prompt = [{"role": "user", "content": "same derived prompt"}]
        original = deepcopy(prompt)
        for context, answer in (("diagram one", "first"), ("diagram two", "second")):
            self.session.source_context = context
            self.assertEqual(self.session.generalAskWithAutoCheck("testStage", prompt), answer)
        self.assertEqual(prompt, original)
        self.assertEqual(dispatch.call_count, 2)

    def test_cache_round_trip_reuses_matching_context_without_dispatch(self):
        self.stub_dispatch("validated answer")
        prompt = [{"role": "user", "content": "same input"}]
        self.session.generalAskWithAutoCheck("testStage", prompt)
        restored = interface.LLMSession(self.config, context_id="diagram-context")
        restored.dispatchRequst = Mock(side_effect=AssertionError("Cache miss"))
        restored.loadCache()
        self.assertEqual(restored.generalAskWithAutoCheck("testStage", prompt), "validated answer")
        restored.dispatchRequst.assert_not_called()

    def test_legacy_and_mismatched_cache_are_rejected_without_loading_answers(self):
        for saved in (
            {"genPolicy": "legacy answer"},
            {"schema_version": 1, "context_id": "diagram-context", "answers": {}},
            {"schema_version": 2, "context_id": "other-diagram", "answers": {"x": "stale"}},
            {"schema_version": 2, "answers": {"x": "unscoped"}},
        ):
            with self.subTest(saved=saved):
                Path(self.config.CACHEFILE).write_text(json.dumps(saved), encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.session.loadCache()
                self.assertEqual(self.session.cache, {})

    def test_filter_accepts_valid_one_based_ids(self):
        self.stub_dispatch("[2, 1]")
        self.assertEqual(self.session.filterEvents("first event\nsecond event", "protocol"), [2, 1])

    def test_filter_rejects_out_of_range_boolean_and_noninteger_ids(self):
        for answer in ("[0]", "[-1]", "[3]", "[True]", "[False]", "[1, True]",
                       "[1.0]", "['1']", "[]", "(1, 2)"):
            with self.subTest(answer=answer):
                dispatch = self.stub_dispatch(*([answer] * 3))
                with self.assertRaises(ValueError):
                    self.session.filterEvents("first event\nsecond event", "protocol")
                self.assertEqual(dispatch.call_count, 3)
                self.assertEqual(self.session.cache, {})
                self.assertEqual(self.saved_cache()["answers"], {})

    def test_filter_repairs_invalid_ids_before_caching(self):
        self.stub_dispatch("[3]", "[True]", "[2]")
        self.assertEqual(self.session.filterEvents("first\nsecond", "protocol"), [2])
        self.assertEqual(list(self.saved_cache()["answers"].values()), ["[2]"])

    def test_filter_never_evaluates_executable_expression(self):
        marker = self.directory / "injection-executed"
        expression = f"(__import__('pathlib').Path({str(marker)!r}).touch(), [1])[1]"
        self.stub_dispatch(expression, expression, expression)
        try:
            with self.assertRaises(ValueError):
                self.session.filterEvents("first event\nsecond event", "protocol")
        finally:
            self.assertFalse(marker.exists(), "Filter executed an untrusted expression")
        self.assertEqual(self.session.cache, {})
        self.assertEqual(self.saved_cache()["answers"], {})

    def test_diagram_split_labels_blocks_by_kind(self):
        diagram = src_module("diagram")
        blocks = diagram.splitDiagram(BLOCK_DIAGRAM)
        self.assertEqual([(b.id, b.kind, b.start, b.end) for b in blocks],
                         [("B1", "action", 5, 12), ("B2", "auto", 13, 15), ("B3", "unconditional", 16, 16)])
        self.assertTrue(blocks[0].hasStateChange())
        annotated = diagram.annotate(BLOCK_DIAGRAM, blocks)
        self.assertIn("    alt [B1] The user is near the device", annotated)
        self.assertIn("    alt [B2] The device is pressed", annotated)
        self.assertIn("UserX->>Device: [B3] probe(Device)", annotated)
        self.assertEqual(diagram.splitDiagram(DIAGRAM)[0].kind, "action")
        self.assertEqual(diagram.splitDiagram("plain protocol text without a diagram"), [])

    def test_labeled_checker_requires_one_known_label_per_rule(self):
        check = interface.checkers.labeled(interface.checkers.checkTransitions, ["B1", "B2"])
        rule = "< UserX | 'localTo' : DeviceY , ... > => ev1(UserX, DeviceY) ."
        self.assertIsNone(check(f"[B1] {rule}\n[B2] {rule}"))
        self.assertIn("block label", check(rule))
        self.assertIn("Unknown block labels ['B9']", check(f"[B9] {rule}"))
        self.assertIn("followed by 2 rules", check(f"[B1] {rule}\n{rule}"))
        self.assertIn("followed by 0 rules", check(f"[B1]\n[B2] {rule}"))
        self.assertIsNotNone(check("[B1] < UserX | ... > => ev1(UserX, Secret) ."))

    def test_synthesis_traces_every_rule_to_its_block(self):
        synthesis = src_module("synthesize")
        llm = Mock()
        llm.genPolicy.return_value = (
            "[B1] < DeviceY | 'pressed' : false , ... > $ UserX 'pressButton' DeviceY\n"
            "=> < DeviceY | 'pressed' : true , ... > .\n"
            "[B3] < DeviceY | ... > $ UserX 'probe' DeviceY | (DeviceY) => < DeviceY | ... > .")
        llm.genPolicyVars.return_value = {"DeviceY": "Device", "UserX": "User"}
        llm.filterEvents.return_value = [1, 2]
        llm.genInit.return_value = "< userA | 'localTo' : deviceB > < deviceB | 'pressed' : false >"
        llm.genRRLs.return_value = (
            "[B1] < UserX | 'localTo' : DeviceY , ... > => ev1(UserX, DeviceY) .\n"
            "[B3] < UserX | ... > < DeviceY | ... > => ev2(UserX, DeviceY) .")
        rules, _, _, trace = synthesis.synthesizeRules(llm, BLOCK_DIAGRAM)
        policy_desc = llm.genPolicy.call_args.args[0]
        self.assertIn("alt [B1]", policy_desc)
        self.assertIn("[Output labels]", policy_desc)
        self.assertNotIn("[Output labels]", llm.genInit.call_args.args[1])
        self.assertIn("legitimate owner", llm.genInit.call_args.args[2])
        mounted = dict(call.args for call in llm.mountChecker.call_args_list)
        self.assertIsNone(mounted["genPolicy"](llm.genPolicy.return_value))
        self.assertIsNone(mounted["genRRLs"](llm.genRRLs.return_value))
        self.assertNotIn("[B", rules)
        self.assertEqual([r["block"] for r in trace["state_rules"]], ["B1", "B3"])
        self.assertEqual([(r["block"], r["label"]) for r in trace["event_rules"]], [("B1", "rev1"), ("B3", "rev2")])
        self.assertEqual(trace["blocks"][0]["event_rules"], [0])
        self.assertEqual(len(trace["coverage_issues"]), 1)
        self.assertIn("B2 (auto, line 13): has state-changing notes but no state rule", trace["coverage_issues"][0])

    def test_prompt_grammar_matches_parser(self):
        """Every statement in DSLPrompt.Base/StateRule/EventDecl/Condition, checked against parseAST."""
        parse = src_module("AST").parseAST
        dsl = src_module("DSLPrompt")
        for text in ('"(" <Attributes> ")"', '<Set> | <FunCall> | "..."', '<Action> ::= <Qid> | <Var>',
                     '"user" /[A-Z][a-zA-Z0-9_]*/', '/\'[^\']*\'/', '<InternalState>*'):
            self.assertIn(text, dsl.Base + dsl.StateRule)
        self.assertIn('"/"', dsl.Condition)
        self.assertNotIn('"Event"', dsl.Types)
        r = " => ev1(UserY) ."
        accepted = [
            "< cloudA | DeviceX : ('k' : V , ...) >" + r, "< cloudA | UserX : ((UserY , Rest)) >" + r,
            "< cloudA | UserX : (nils) >" + r, "< cloudA | 'm' : (UserY , Rest) >" + r,
            "< UserY | >" + r, "< UserY | nils >" + r, "< UserY | ... , 'a' : 1 >" + r,
            "< UserY | 'k' : encrypt(K , 'x') , 'l' : list('a' ; 'b') , 'q' : 'a b:c' >" + r,
            "< UserY | 'n' : N >" + r, "< userA_1 | ... >" + r,
            "< UserY | ... > $ UserY Act deviceB | (K ; 'x') < deviceB | ... > => < UserY | ... > .",
            "=> ev1(UserY) .", "< userA | ... > => ev1(userA , 'k') .",
            "< UserY | 'n' : N , ... > => < UserY | ... > if (N + 1) / 2 >= 3 .",
            "< UserY | 'n' : N , ... > => < UserY | ... > if N =/= nils .",
        ]
        rejected = [
            "< cloudA | UserX : (UserY , Rest) >" + r, "< cloudA | UserX : nils >" + r,
            "< cloudA | UserX : deviceB >" + r, "< useralice | ... >" + r, "< user_A | ... >" + r,
            "$ UserY 'a' deviceB => < UserY | ... > .", "< userA | ... > => ev1 .",
            "< UserY | 'k' : K , ... > => < UserY | ... > if K == 'x' .",
            "< UserY | 'n' : N , ... > => < UserY | ... > if N > 1 and N < 3 .",
        ]
        for code in accepted:
            with self.subTest(accepted=code):
                parse(code)
        for code in rejected:
            with self.subTest(rejected=code):
                with self.assertRaises(Exception):
                    parse(code)

    def test_property_templates_render_expected_formulas(self):
        templates = src_module("property_templates")
        own = {"attackerLocal": "< userC | ('near' : deviceB , ..) >",
               "attackerOwner": "< cloudA | (deviceB : ('owner' : (userC , ..) , ...)) >"}
        self.assertEqual(templates.safetyFormula("OWN-remote", own),
                         "<> (~ attackerLocal /\\ ~ attackerOwner /\\ O (~ attackerLocal /\\ attackerOwner))")
        victim = {**own, "victimOwner": "< cloudA | (deviceB : ('owner' : userA , ...)) >"}
        self.assertIn("~ attackerLocal /\\ victimOwner /\\ ~ attackerOwner", templates.safetyFormula("OWN-remote", victim))
        checker = templates.renderChecker("CTRL-direct", {"deviceOn": "< deviceB | ('on' : true , ..) >",
                                                          "attackerAuthorized": "< deviceB | ('trusted' : (userC , ..) , ...) >"},
                                          forbidSystemEvents=True)
        self.assertIn("ceq E @ S |= attackerActs = true if subject(E) == userC .", checker)
        self.assertIn("eq basic = [] (~ boundReached /\\ ~ sp) .", checker)
        self.assertIn("eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .", checker)
        with self.assertRaises(ValueError):
            templates.renderChecker("OWN-stealth", {"deviceTrustsAttacker": "< deviceB | ... >"})

    def test_slot_checker_accepts_model_states_only(self):
        model = "< deviceB | ('on' : [Bool]) > < cloudA | ([Principal] : ('device' : [Device])) > userC"
        check = interface.checkers.slots(["deviceOn", "attackerAuthorized"], model)
        auth = "attackerAuthorized =| < cloudA | userC : ('device' : deviceB , ...) , ... > ."
        self.assertIsNone(check("deviceOn =| < deviceB | 'on' : true , ... > .\n" + auth))
        self.assertIn("'power'", check("deviceOn =| < deviceB | 'power' : true , ... > .\n" + auth))
        self.assertIn("exactly one proposition", check("deviceOn =| < deviceB | 'on' : true , ... > ."))
        self.assertIn("not events", check("deviceOn =| $ userC 'turnOn' deviceB .\n" + auth))

    @unittest.skipUnless((ROOT / "Maude-3.5.1-macos-arm64" / "maude").exists(), "bundled Maude not available")
    def test_property_templates_reproduce_golden_counterexamples(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            validation = importlib.import_module("validate_property_templates")
        finally:
            sys.path.remove(str(ROOT / "scripts"))
        binary, lib = validation.maudeBinary()
        with tempfile.TemporaryDirectory() as work:
            (Path(work) / "lib").symlink_to(validation.GOLD / "lib")
            for protocol in sorted(validation.MAPPING):
                with self.subTest(protocol=protocol):
                    *_, gold, template, status = validation.validate(protocol, binary, lib, Path(work))
                    self.assertEqual(gold[0], "counterexample")
                    self.assertTrue(status.startswith("same"), status)

    def test_diagram_fewshots_pass_guardrails_and_build_valid_models(self):
        prompts, synthesis, diagram = src_module("prompts_text"), src_module("synthesize"), src_module("diagram")
        checkers = interface.checkers
        body = lambda answer: answer.strip().removeprefix("```").removesuffix("```").strip()
        cases = (
            (prompts.fewshot_diagram1, prompts.policy_shot_a1, prompts.rrls_shot_a1, prompts.init_shot_a1,
             json.loads(body(prompts.policy_vars_shot_a1)), json.loads(body(prompts.filter_shot_a1)), prompts._template1),
            (prompts.fewshot_diagram2, prompts.policy_shot_a2, prompts.rrls_shot_a2, prompts.init_shot_a2,
             {"Job": "Qid", "UserX": "User"}, [1, 2, 3], prompts._template2),
        )
        validate = src_module("model_validation").validate_model
        for d, policy, rrls, init, vtypes, eids, template in cases:
            with self.subTest(diagram=d[:60]):
                ids = [b.id for b in diagram.splitDiagram(d)]
                self.assertIsNone(checkers.labeled(checkers.checkPolicy, ids)(body(policy)))
                self.assertIsNone(checkers.labeled(checkers.checkTransitions, ids)(body(rrls)))
                self.assertIsNone(checkers.checkINIT(body(init)))
                llm = Mock()
                llm.genPolicy.return_value, llm.genRRLs.return_value = body(policy), body(rrls)
                llm.genPolicyVars.return_value, llm.filterEvents.return_value = vtypes, eids
                llm.genInit.return_value = body(init)
                rules, state_template, _, trace = synthesis.synthesizeRules(llm, d)
                # Attribute order inside a template varies between processes (string hashing), so compare contents.
                choices = lambda m: re.sub(r"\{([^}]*)\}", lambda c: "{" + " , ".join(sorted(c.group(1).split(" , "))) + "}", m)
                parts = lambda s: sorted(choices(m) for m in re.findall(r"< \w+|'\w+' : \(?(?:\{[^}]*\}|\[\w+\])|\[\w+\] :", s))
                self.assertEqual(parts(state_template), parts(template))
                self.assertEqual(trace["coverage_issues"], [])
                self.assertIn(llm.genPolicy.call_args.args[0], (prompts.policy_shot_q1, prompts.policy_shot_q2))
                if not (ROOT / "Maude-3.5.1-macos-arm64" / "maude").exists():
                    continue
                with tempfile.TemporaryDirectory() as directory:
                    (Path(directory) / "lib").symlink_to(ROOT / "lib")
                    (Path(directory) / "run").mkdir()
                    model = Path(directory) / "run" / "rules.maude"
                    model.write_text(rules)
                    self.assertEqual(validate(model)["status"], "valid")
        self.assertIn("ev3(UserX, Token)", prompts.rrls_shot_q1)
        self.assertIn("[B3] < UserX | 'token' : Token , ... > => ev3(UserX, Token) .", prompts.rrls_shot_a1)


if __name__ == "__main__":
    unittest.main()


class ThreatModelTests(unittest.TestCase):
    def test_subtype_adds_stage_to_domain_base(self):
        from threat_models import threatModel, SUBTYPE_SCENARIO, THREAT_MODELS
        from property_templates import SUBTYPES
        self.assertEqual(set(SUBTYPE_SCENARIO), set(SUBTYPES))
        base = THREAT_MODELS['iot']['base']
        self.assertEqual(threatModel(), base)
        self.assertTrue(threatModel('CTRL-direct').startswith(base))
        self.assertIn("authorized", threatModel('CTRL-revoked'))
        self.assertIn("no owner", threatModel('OWN-remote'))

    def test_init_checker_rejects_principal_without_attributes(self):
        import checkers
        self.assertIn("< deviceSwitch | nils >", checkers.checkINIT("< userA | ('key' : nils) > < deviceSwitch | >"))
        self.assertIsNone(checkers.checkINIT("< userA | ('key' : nils) > < deviceSwitch | nils >"))
