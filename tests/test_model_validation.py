"""Run with python3 -m unittest discover -s tests -p test_model_validation.py."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from src.model_validation import validate_model


VALID = """==========================================
reduce in TRANSITION : init .
rewrites: 1 in 0ms cpu (0ms real)
result Vertex: idle @ < system | nils >
==========================================
search [1] in TRANSITION : init =>1 V:Vertex .

Solution 1 (state 1)
states: 2 rewrites: 2 in 0ms cpu (0ms real)
V:Vertex --> idle @ < userA | nils >
Bye.
"""
PRELUDE = '''Warning: "prelude.maude", line 2860 (fmod META-LEVEL): failed to attach id-hook MetaLevelOpSymbol to metaPrettyPrint.
Warning: "prelude.maude", line 2860 (fmod META-LEVEL): bad special for operator metaPrettyPrint.
Warning: "prelude.maude", line 2130 (fmod META-LEVEL): this module contains one or more errors that could not be patched up and thus it cannot be used or imported.
'''


class ModelValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.model = Path(self.directory.name) / 'model with spaces;$(false).maude'
        self.model.write_text('mod SYSTEM is endm\nmod TRANSITION is endm\n')

    def run_output(self, stdout=VALID, stderr='', code=0):
        with patch('src.model_validation.subprocess.run', return_value=
                   subprocess.CompletedProcess([], code, stdout, stderr)) as run:
            result = validate_model(self.model, '/fake/maude')
        json.dumps(result)
        return result, run

    def test_valid_and_safe_invocation(self):
        result, run = self.run_output()
        self.assertEqual(result['status'], 'valid')
        self.assertTrue(result['has_successor'])
        args, kwargs = run.call_args
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0][-1], str(self.model.resolve()))
        self.assertFalse(kwargs['shell'])
        self.assertEqual(kwargs['cwd'], str(self.model.parent.resolve()))
        self.assertEqual(kwargs['timeout'], 30)
        self.assertTrue(kwargs['input'].endswith('quit\n'))
        self.assertIn('set print with aliases off .', kwargs['input'])

    def test_zero_exit_is_not_success(self):
        for output in ('', 'Bye.\n', 'result Vertex: validLooking\n'):
            with self.subTest(output=output):
                self.assertEqual(self.run_output(output)[0]['status'], 'error')

    def test_generated_errors_even_with_valid_probe_and_exit_zero(self):
        for diagnostic in (
            'Warning: "rules.maude", line 5: syntax error',
            'Warning: "rules.maude", line 5: bad token X.',
            'Warning: "rules.maude", line 5 (mod SYSTEM):\n    this module is unusable.',
            'Warning: "rules.maude", line 5 (fmod META-LEVEL): bad special for operator metaPrettyPrint.',
            'Error: module TRANSITION does not exist.',
            'Warning: "prelude.maude", line 1 (fmod META-LEVEL): unexpected failure.',
        ):
            for stream in ('stdout', 'stderr'):
                with self.subTest(diagnostic=diagnostic, stream=stream):
                    result, _ = self.run_output(
                        VALID + (diagnostic if stream == 'stdout' else ''),
                        PRELUDE + (diagnostic if stream == 'stderr' else ''))
                    self.assertEqual(result['status'], 'error')
                    self.assertIn(diagnostic, result['errors'])

    def test_known_prelude_warning_is_reported(self):
        result, _ = self.run_output(stderr=PRELUDE)
        self.assertEqual(result['status'], 'valid')
        self.assertEqual(len(result['warnings']), 3)
        self.assertEqual(result['stderr'], PRELUDE)

    def test_bad_reductions(self):
        for replacement in ('result Vertex: init', 'result [Vertex]: broken',
                            'result Vertex: idle @ S:Soup',
                            'result Vertex: idle @ ..:Set',
                            'result Vertex: wrapper(init)', 'result Bool: true'):
            with self.subTest(replacement=replacement):
                result, _ = self.run_output(VALID.replace(
                    'result Vertex: idle @ < system | nils >', replacement))
                self.assertEqual(result['status'], 'error')

    def test_quoted_data_is_ground(self):
        result, _ = self.run_output(VALID.replace('idle @ < system | nils >',
                                                  '''idle @ < system | ('init, "X:Vertex") >'''))
        self.assertEqual(result['status'], 'valid')

    def test_no_successors_is_valid(self):
        for message in ('No solution.', 'No solutions.', 'No more solutions.'):
            output = VALID[:VALID.index('Solution 1')] + message + '\nBye.\n'
            result, _ = self.run_output(output)
            self.assertEqual(result['status'], 'valid')
            self.assertFalse(result['has_successor'])

    def test_missing_search_and_unresolved_successor(self):
        for output in (VALID[:VALID.index('Solution 1')],
                       VALID.replace('V:Vertex --> idle @ < userA | nils >',
                                     'V:Vertex --> E:Event @ null')):
            self.assertEqual(self.run_output(output)[0]['status'], 'error')

    def test_nonzero_exit(self):
        self.assertEqual(self.run_output(code=1)[0]['status'], 'error')

    def test_timeout_preserves_partial_bytes(self):
        with patch('src.model_validation.subprocess.run', side_effect=
                   subprocess.TimeoutExpired('maude', 0.1, b'partial', PRELUDE.encode())):
            result = validate_model(self.model, '/fake/maude', timeout=0.1)
        self.assertEqual(result['status'], 'timeout')
        self.assertEqual(result['stdout'], 'partial')
        self.assertEqual(len(result['warnings']), 3)
        json.dumps(result)

    def test_invalid_inputs_and_launch_failure(self):
        for timeout in (0, -1, float('nan'), float('inf'), None):
            self.assertEqual(validate_model(self.model, '/fake/maude', timeout)['status'], 'error')
        self.assertEqual(validate_model(self.model.parent / 'missing')['status'], 'error')
        self.assertEqual(validate_model(self.model, '/nonexistent/maude')['status'], 'error')

    def test_real_fake_executable_and_timeout(self):
        executable = self.model.parent / 'fake maude'
        executable.write_text(f'#!{sys.executable}\nimport sys\n'
                              'assert sys.stdin.read().endswith("quit\\n")\n'
                              f'print({VALID!r})\n')
        executable.chmod(0o700)
        self.assertEqual(validate_model(self.model, executable)['status'], 'valid')
        executable.write_text(f'#!{sys.executable}\nimport time\n'
                              'print("partial", flush=True)\ntime.sleep(10)\n')
        result = validate_model(self.model, executable, timeout=0.2)
        self.assertEqual(result['status'], 'timeout')
        self.assertIn('partial', result['stdout'])


if __name__ == '__main__':
    unittest.main()
