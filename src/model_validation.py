"""Standalone Maude smoke validation; no configuration or LLM dependencies.

``validate_model(path, maude_binary=None, timeout=30)`` returns a JSON-safe
dictionary. ``valid`` means loading, reducing init to a ground Vertex, and a
one-step search completed. It does not prove protocol correctness or liveness.
An exhausted search is valid, with ``has_successor=False``.
"""

import math
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


_ROOT = Path(__file__).resolve().parents[1]
_COMMANDS = (
    "show module SYSTEM .\n"
    "set print with aliases off .\n"
    "set print mixfix off .\n"
    "red in TRANSITION : init .\n"
    "search [1] in TRANSITION : init =>1 V:Vertex .\n"
    "quit\n"
)
_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_DIAGNOSTIC = re.compile(
    r"(?im)^\s*(?:Warning|Error|Fatal(?: error)?|Advisory):.*"
    r"(?:\n[ \t]+[^\n]*)*"
)


def _text(value):
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""


def _diagnostics(result):
    for stream in (result["stdout"], result["stderr"]):
        for match in _DIAGNOSTIC.finditer(_ANSI.sub("", stream)):
            message = match.group().strip()
            # Only these exact, observed prelude failures are nonfatal. In
            # particular, a dependent SYSTEM/TRANSITION failure is still fatal.
            known = re.fullmatch(
                r'Warning: "(?:[^"\n]*/)?prelude\.maude", line \d+ '
                r'\(fmod META-LEVEL\):\s*('
                r'failed to attach id-hook MetaLevelOpSymbol to metaPrettyPrint\.|'
                r'bad special for operator metaPrettyPrint\.|'
                r'this module contains one or more errors that could not be '
                r'patched up and thus it cannot be used or imported\.)',
                " ".join(message.split()),
            )
            if message.startswith(("Warning:", "Advisory:")):
                result["warnings"].append(message)
            if not known and not message.startswith("Advisory:"):
                result["errors"].append(message)


def _ground(term):
    # Alias printing is disabled, so Maude prints every variable as Name:Sort.
    # Strip strings and quoted identifiers before checking tokens (a Qid such
    # as 'init or a string containing X:Vertex is ordinary ground data).
    tokens = re.sub(r'"(?:\\.|[^"\\])*"|\x27[^\s(),]+', "", term)
    return bool(term.strip()) and not re.search(
        r"(?<![\w'])init(?![\w'])|(?:[\w?]+|\.{2,})\s*:\s*\[?[A-Za-z][\w{},-]*", tokens
    )


def _maude(maude_binary, temporary):
    """Resolve the Maude executable; returns (executable, reported binary, environment)."""
    env = os.environ.copy()
    if maude_binary is not None:
        supplied = os.fspath(maude_binary)
        binary = Path(shutil.which(supplied) or supplied).expanduser().resolve()
    else:
        architecture = {"aarch64": "arm64", "amd64": "x86_64"}.get(
            platform.machine().lower(), platform.machine().lower())
        binary = _ROOT / f"Maude-3.5.1-macos-{architecture}" / "maude"
        if platform.system() != "Darwin" or not binary.is_file():
            found = shutil.which("maude")
            if not found:
                raise FileNotFoundError("No native bundled Maude or maude on PATH; specify maude_binary")
            binary = Path(found).resolve()
    executable = binary
    if maude_binary is None and binary.parent.parent == _ROOT:
        env["MAUDE_LIB"] = str(binary.parent)
        if not os.access(binary, os.X_OK):
            executable = Path(temporary) / "maude"
            shutil.copyfile(binary, executable)
            executable.chmod(0o700)
    return executable, binary, env


_EVENT = re.compile(r"^\$ \w+ '[^']*' \w+(?: \| .*)?$")


def run_checker(path, props=(), maude_binary=None, timeout=600):
    """Model-check a checker.maude (its postProcess load runs modelCheck(init, spec)).

    Returns verdict ``counterexample`` with the attack's event sequence, ``holds``
    when the property holds, or ``error``/``timeout``. ``at_init`` reports the
    truth of each named proposition in the initial state, as a sanity check.
    """
    result = dict(verdict="error", events=[], at_init={}, stdout="", stderr="", warnings=[], errors=[])
    commands = "".join(f"red in CHECK : init |= {p} .\n" for p in props) + "quit\n"
    with tempfile.TemporaryDirectory(prefix="maude-check-") as temporary:
        try:
            checker = Path(path).expanduser().resolve(strict=True)
            executable, _, env = _maude(maude_binary, temporary)
            completed = subprocess.run(
                [str(executable), "-no-banner", "-no-advise", "-no-wrap", "-no-ansi-color", str(checker)],
                input=commands, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=timeout, cwd=str(checker.parent), env=env, shell=False)
            result.update(stdout=completed.stdout, stderr=completed.stderr)
        except subprocess.TimeoutExpired:
            result.update(verdict="timeout", errors=["Maude exceeded the model-checking timeout"])
            return result
        except (OSError, ValueError) as exc:
            result["errors"].append(str(exc))
            return result
    _diagnostics(result)
    out = _ANSI.sub("", result["stdout"])
    check = out.split("reduce in PostProcess", 1)
    if len(check) == 2:
        body = check[1].split("reduce in CHECK", 1)[0]
        result["events"] = [line.strip() for line in body.splitlines() if _EVENT.match(line.strip())]
        if re.search(r"^result Bool: true", body, re.M):
            result["verdict"] = "holds"
        elif result["events"]:
            result["verdict"] = "counterexample"
    for p, value in re.findall(r"^reduce in CHECK : init \|= (\w+) \.\s*\nrewrites:[^\n]*\nresult Bool: (true|false)", out, re.M):
        result["at_init"][p] = value == "true"
    return result


def validate_model(path, maude_binary=None, timeout=30):
    """Validate a model using an explicit executable or the native bundled one.

    Relative imports resolve from the model's directory. The timeout covers
    the entire Maude process, including loading, reduction and search. Unknown
    warnings fail closed because Maude can discard bad equations and exit 0.
    Raw streams, return code, diagnostics, reduced term and search outcome are
    retained. Launch/input failures return ``error`` rather than raising.

    A bundled native binary missing its execute bit is run from an executable
    temporary copy, with its original library directory; no bundle is changed.
    Explicit binaries are used as supplied (or resolved through PATH).
    """
    result = dict(status="error", path=None, maude_binary=None, returncode=None,
                  stdout="", stderr="", warnings=[], errors=[],
                  initial_term=None, has_successor=None)
    with tempfile.TemporaryDirectory(prefix="maude-validation-") as temporary:
        try:
            model = Path(path).expanduser().resolve(strict=True)
            result["path"] = str(model)
            if not model.is_file():
                raise ValueError("Model path must be a file")
            if isinstance(timeout, bool) or not math.isfinite(timeout) or timeout <= 0:
                raise ValueError("timeout must be a positive finite number")
            executable, binary, env = _maude(maude_binary, temporary)
            result["maude_binary"] = str(binary)
            completed = subprocess.run(
                [str(executable), "-no-banner", "-no-advise", "-no-wrap",
                 "-no-ansi-color", str(model)],
                input=_COMMANDS, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=timeout,
                cwd=str(model.parent), env=env, shell=False,
            )
            result.update(stdout=completed.stdout, stderr=completed.stderr,
                          returncode=completed.returncode)
        except subprocess.TimeoutExpired as exc:
            result.update(status="timeout", stdout=_text(exc.stdout), stderr=_text(exc.stderr))
            _diagnostics(result)
            result["errors"].append("Maude exceeded the validation timeout")
            return result
        except (OSError, ValueError, TypeError) as exc:
            result["errors"].append(str(exc))
            return result

    _diagnostics(result)
    if result["returncode"] != 0:
        result["errors"].append(f"Maude exited with code {result['returncode']}")
    output = _ANSI.sub("", result["stdout"])
    # Anchor to the requested command, not an arbitrary result printed by the
    # loaded file. Require exactly one probe to avoid ambiguous transcripts.
    reductions = list(re.finditer(r"(?m)^reduce in TRANSITION : init \.\s*$", output))
    searches = list(re.finditer(
        r"(?m)^search \[1\] in TRANSITION : init =>1 V:Vertex \.\s*$", output))
    if len(reductions) != 1 or len(searches) != 1 or reductions[0].end() >= searches[0].start():
        result["errors"].append("Missing or ambiguous reduction/search transcript")
    else:
        reduction = output[reductions[0].end():searches[0].start()]
        term = re.search(r"(?ms)^result Vertex:\s*(.+?)(?=\n={3,}|\Z)", reduction)
        if term:
            result["initial_term"] = term.group(1).strip()
        if not term or not _ground(result["initial_term"]):
            result["errors"].append("init did not reduce to a ground Vertex without unresolved init/variables")
        search = output[searches[0].end():]
        successor = re.search(r"(?ms)^V:Vertex -->\s*(.+?)(?=\n(?:Bye\.|No more solutions\.|={3,})|\Z)", search)
        if re.search(r"(?m)^Solution 1 \(state \d+\)", search) and successor:
            result["has_successor"] = True
            if not _ground(successor.group(1)):
                result["errors"].append("Search produced an unresolved successor")
        elif re.search(r"(?m)^No (?:more )?solutions?\.", search):
            result["has_successor"] = False
        else:
            result["errors"].append("One-step search did not complete")
    if not result["errors"]:
        result["status"] = "valid"
    return result
