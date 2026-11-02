"""Check isolated behavior used to distinguish repair errors from regressions.

The checks extract small functions from archived patches and trajectory source
listings. They compare regex parsing, hostname caches, and Sphinx include
behavior, and exercise the SymPy printer's recursive state with lightweight
stubs. An optional historical SymPy checkout enables two equality assertions.
Only the Python standard library is required. These are isolated checks, not
historical repository test runs, SWE-bench evaluations, or automatic labels.
The archive is read-only; --output optionally saves the portable JSON result.
"""

import argparse
import collections
import collections.abc
import csv
import hashlib
import inspect
import json
import re
import sys
import textwrap
import types
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
GPT = "gpt-5-2025-08-07-medium-reasoning"
CLAUDE = "claude-sonnet-4-5-20250929"
GEMINI = "gemini-3-pro-preview"


def load_messages(root, model, task, trial):
    path = root / "data/traj" / model / f"round{trial}" / task / f"{task}.traj.json"
    return json.loads(path.read_text(encoding="utf-8"))["messages"]


def load_patch(root, model, task, trial):
    path = root / "analyse" / model / task / f"{trial}{task}_model.patch"
    return path.read_text(encoding="utf-8")


def numbered_sources(messages):
    """Yield contiguous source listings beginning with archived line one."""
    for message in messages:
        if message.get("role") != "user":
            continue
        current = []
        previous = 0
        for line in message.get("content", "").splitlines():
            match = re.match(r"\s*(\d+)\t(.*)", line)
            if not match:
                if current:
                    yield "\n".join(current) + "\n"
                current, previous = [], 0
                continue
            number = int(match[1])
            if number == 1:
                if current:
                    yield "\n".join(current) + "\n"
                current = [match[2]]
            elif current and number == previous + 1:
                current.append(match[2])
            else:
                if current:
                    yield "\n".join(current) + "\n"
                current = []
            previous = number
        if current:
            yield "\n".join(current) + "\n"


def find_source(messages, marker):
    return next(source for source in numbered_sources(messages) if marker in source)


def apply_file_hunks(source, patch_text, target):
    """Apply matching unified hunks in memory, checking every old/context line."""
    lines = source.splitlines(keepends=True)
    result, position = [], 0
    active = in_hunk = False
    for line in patch_text.splitlines(keepends=True):
        if line.startswith("diff --git "):
            active = line.rstrip().endswith(" b/" + target)
            in_hunk = False
        elif active and line.startswith("@@"):
            start = int(re.match(r"@@ -(\d+)", line)[1]) - 1
            result.extend(lines[position:start])
            position, in_hunk = start, True
        elif active and in_hunk and line[:1] in {" ", "-", "+"}:
            if line[0] in " -":
                if lines[position].rstrip("\n") != line[1:].rstrip("\n"):
                    raise ValueError("Archived patch does not match the source listing")
                if line[0] == " ":
                    result.append(lines[position])
                position += 1
            else:
                result.append(line[1:])
    result.extend(lines[position:])
    return "".join(result)


def splitstrip_functions(patch_text):
    signature = re.search(r"@@.*@@ (def _splitstrip[^\n]+)", patch_text)[1]
    hunk = patch_text[patch_text.index("@@ -229,"):]
    versions = []
    for prefixes in (" -", " +"):
        lines = [line[1:] for line in hunk.splitlines() if line[:1] in prefixes]
        closing = lines.index('    """')
        body = []
        for line in lines[closing + 1:]:
            if line.startswith("def "):
                break
            body.append(line)
        namespace = {"csv": csv}
        exec(compile(signature + "\n" + "\n".join(body), "<archived _splitstrip>", "exec"), namespace)
        versions.append(namespace["_splitstrip"])
    return versions


def check_regex(root):
    baseline, candidate = splitstrip_functions(load_patch(root, GEMINI, "pylint-dev__pylint-8898", 2))
    results = []
    for function in (baseline, candidate):
        pattern = function(r"\d+")[0]
        workaround = function(r"(foo{1\,3})")
        results.append({"parsed_digit_pattern": pattern,
                        "matches_123": bool(re.fullmatch(pattern, "123")),
                        "escaped_quantifier_parts": workaround})
    assert results[0]["matches_123"] and not results[1]["matches_123"]
    assert results[1]["escaped_quantifier_parts"] == ["(foo{1,3})"]
    return {"case": "pylint-dev__pylint-8898/Gemini/2",
            "check": "regex backslash preservation and comma workaround",
            "baseline": results[0], "candidate": results[1], "passed": True}


def check_cache(root):
    messages = load_messages(root, GPT, "django__django-11532", 3)
    source = find_source(messages, "class CachedDnsName:")
    results = []
    for model, name in ((CLAUDE, "Claude"), (GPT, "GPT")):
        candidate_source = apply_file_hunks(source, load_patch(root, model, "django__django-11532", 2),
                                            "django/core/mail/utils.py")
        observations = []
        for version in (source, candidate_source):
            namespace = {}
            exec(compile(version, "<archived CachedDnsName>", "exec"), namespace)
            obj = namespace["CachedDnsName"]()
            with patch("socket.getfqdn", return_value="first.example"):
                first = str(obj)
                try:
                    second = str(obj)
                except UnboundLocalError:
                    second = "UnboundLocalError"
            del obj._fqdn
            with patch("socket.getfqdn", return_value="second.example"):
                after_reset = str(obj)
            observations.append({"first_call": first, "second_call": second,
                                 "after_existing_cache_reset": after_reset})
        assert observations[0]["second_call"] == "first.example"
        assert observations[0]["after_existing_cache_reset"] == "second.example"
        if name == "Claude":
            assert observations[1]["after_existing_cache_reset"] == "first.example"
        else:
            assert observations[1]["second_call"] == "UnboundLocalError"
        results.append({"case": f"django__django-11532/{name}/2",
                        "check": "existing hostname-cache lifecycle",
                        "baseline": observations[0], "candidate": observations[1], "passed": True})
    return results


def patch_function_versions(patch_text, name):
    """Extract a complete function whose definition is in unified-hunk context."""
    versions = []
    for prefixes in (" -", " +"):
        lines = [line[1:] for line in patch_text.splitlines() if line[:1] in prefixes
                 and not line.startswith(("---", "+++"))]
        start = next(i for i, line in enumerate(lines) if line.startswith(f"    def {name}("))
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("    def ")),
                   len(lines))
        namespace = {"List": list, "Tuple": tuple}
        exec(compile(textwrap.dedent("\n".join(lines[start:end])), "<archived option filter>", "exec"),
             namespace)
        versions.append(namespace[name])
    return versions


def check_include_options(root):
    patch_text = load_patch(root, GPT, "sphinx-doc__sphinx-10323", 2)
    prepend = patch_function_versions(patch_text, "prepend_filter")
    append = patch_function_versions(patch_text, "append_filter")
    results = []
    for before, after in zip(prepend, append):
        instance = SimpleNamespace(options={"prepend": "HEAD", "append": "TAIL"})
        lines = before(instance, ["    body\n"])
        results.append(after(instance, lines))
    assert results[0] == ["HEAD\n", "    body\n", "TAIL\n"]
    assert results[1] == ["    HEAD\n", "    body\n", "    TAIL\n"]
    return {"case": "sphinx-doc__sphinx-10323/GPT/2",
            "check": "prepend and append preserve supplied indentation without dedent",
            "baseline": results[0], "candidate": results[1], "passed": True}


def check_literal_events(root):
    messages = load_messages(root, GPT, "sphinx-doc__sphinx-11510", 3)
    numbered = {}
    for marker in ("class Include(BaseInclude, SphinxDirective):", "Include as BaseInclude"):
        message = next(item for item in messages if item.get("role") == "user"
                       and marker in item.get("content", "") and re.search(r"\d+\t", item["content"]))
        for line in message["content"].splitlines():
            match = re.match(r"\s*(\d+)\t(.*)", line)
            if match:
                numbered[int(match[1])] = match[2]
    source = "\n".join(numbered.get(i, "") for i in range(1, max(numbered) + 1)) + "\n"

    class LiteralNode:
        def __init__(self, *args, **kwargs):
            self.text = args[-1] if args else ""
            self.attributes = kwargs

        def astext(self):
            return self.text

        def __iadd__(self, value):
            self.text += str(value)
            return self

    class FileInput:
        def __init__(self, *args, **kwargs):
            self.source_path = kwargs.get("source_path")

        def read(self):
            return "RAW\n"

        def readlines(self):
            return ["RAW\n"]

    class BaseInclude:
        option_spec = {"literal": None}

        def run(self):
            return [LiteralNode("RAW\n")]

    class SphinxDirective:
        pass

    class EventObserved(Exception):
        pass

    def observe_event(*args):
        raise EventObserved

    io_module = types.ModuleType("docutils.io")
    io_module.FileInput = FileInput
    directives = types.ModuleType("docutils.parsers.rst.directives")
    directives.path = lambda value: value
    utils = types.ModuleType("docutils.utils")
    utils.relative_path = lambda base, value: str(value)
    statemachine = types.ModuleType("docutils.statemachine")
    statemachine.string2lines = lambda text, *args, **kwargs: text.splitlines()
    docutils = types.ModuleType("docutils")
    docutils.io, docutils.utils, docutils.statemachine = io_module, utils, statemachine
    parsers, rst = types.ModuleType("docutils.parsers"), types.ModuleType("docutils.parsers.rst")
    rst.directives, parsers.rst, docutils.parsers = directives, rst, parsers
    modules = {module.__name__: module for module in
               (docutils, io_module, utils, statemachine, directives, parsers, rst)}
    results = []
    for model, name in ((CLAUDE, "Claude"), (GEMINI, "Gemini"), (GPT, "GPT")):
        for trial in range(1, 4):
            if model == CLAUDE and trial == 2:
                continue
            candidate_source = apply_file_hunks(source, load_patch(root, model, "sphinx-doc__sphinx-11510", trial),
                                                "sphinx/directives/other.py")
            observations = []
            for version in (source, candidate_source):
                class_source = version[version.index("class Include(BaseInclude"):version.index("def setup(")]
                namespace = {"BaseInclude": BaseInclude, "SphinxDirective": SphinxDirective,
                             "Node": object, "nodes": SimpleNamespace(literal_block=LiteralNode),
                             "io": io_module, "SphinxFileInput": FileInput, "docutils_io": io_module,
                             "docutils_utils": utils, "docutils_statemachine": statemachine,
                             "statemachine": statemachine, "directives": directives,
                             "utils": utils, "Path": Path}
                exec(compile("from __future__ import annotations\n" + class_source,
                             "<archived Include>", "exec"), namespace)
                instance = namespace["Include"]()
                instance.arguments, instance.options = ["included.rst"], {"literal": None}
                events = SimpleNamespace(emit=observe_event)
                instance.env = SimpleNamespace(relfn2path=lambda value: ("included.rst", "included.rst"),
                                               note_included=lambda value: None, events=events, app=events,
                                               docname="index", path2doc=lambda value: "included")
                settings = SimpleNamespace(file_insertion_enabled=True, input_encoding="utf-8",
                                           input_encoding_error_handler="strict", tab_width=8,
                                           record_dependencies=set(), line_length_limit=1000)
                instance.state = SimpleNamespace(document=SimpleNamespace(settings=settings,
                                                                          current_source="index.rst"))
                instance.config = SimpleNamespace(source_encoding="utf-8")
                instance.state_machine = SimpleNamespace(insert_input=lambda *args: None)
                with patch.dict(sys.modules, modules):
                    try:
                        instance.run()
                        observations.append(False)
                    except EventObserved:
                        observations.append(True)
            assert observations == [False, True]
            results.append({"case": f"sphinx-doc__sphinx-11510/{name}/{trial}",
                            "check": "literal include emits source-read with dependency stubs",
                            "baseline": observations[0], "candidate": observations[1], "passed": True})
    return results


def extract_method(source, method):
    lines = source.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(f"    def {method}("))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("    def ")), len(lines))
    return textwrap.dedent("\n".join(lines[start:end]))


def check_printer_state(root):
    messages = load_messages(root, GPT, "sympy__sympy-15345", 2)
    code_source = find_source(messages, "class CodePrinter(StrPrinter):")
    original_source = find_source(messages, "doprint = StrPrinter.doprint")
    doprint_source = extract_method(code_source, "doprint")
    list_source = extract_method(original_source, "_print_list")
    # The symbolic dispatcher is deliberately replaced by a two-case harness.
    # The archived entry-point and recursive list formatter remain unchanged.
    namespace = {"string_types": (str,), "Basic": object, "sympify": lambda value: value}
    exec(compile(doprint_source + "\n" + list_source, "<archived printer methods>", "exec"), namespace)

    class DispatchHarness:
        _not_supported = set()
        _number_symbols = set()
        _settings = {"human": True}
        _print_list = namespace["_print_list"]

        def _print(self, value):
            return self._print_list(value) if isinstance(value, list) else str(value)

        def doprint(self, value):
            return self._print(value)

        def _format_code(self, lines):
            return [line for line in lines if line != ""]

    class CandidateHarness(DispatchHarness):
        doprint = namespace["doprint"]

    modules = {name: types.ModuleType(name) for name in (
        "sympy", "sympy.matrices", "sympy.matrices.expressions",
        "sympy.matrices.expressions.matexpr")}
    modules["sympy.matrices.expressions.matexpr"].MatrixSymbol = object
    with patch.dict(sys.modules, modules):
        baseline = DispatchHarness().doprint([2])
        try:
            candidate = CandidateHarness().doprint([2])
        except AttributeError as error:
            missing = error.name or re.search(r"attribute '([^']+)'", str(error))[1]
            candidate = {"exception": "AttributeError", "missing_attribute": missing}
    assert baseline == "{2}"
    assert candidate == {"exception": "AttributeError", "missing_attribute": "_not_supported"}
    return {"case": "sympy__sympy-15345/GPT/2",
            "check": "recursive printer state with archived methods and dispatch stubs",
            "baseline": baseline, "candidate": candidate, "passed": True}


def added_file_lines(patch_text, target):
    active = False
    result = []
    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            active = line.endswith(" b/" + target)
        elif active and line.startswith("+") and not line.startswith("+++"):
            result.append(line[1:])
    return "\n".join(result) + "\n"


def check_historical_equality(root, sympy_root):
    """Optionally exercise the added method in a supplied historical checkout."""
    source_hashes = {
        "sympy/core/relational.py": "c017d0e64eaa8918a0be8499030342bc1d8e8cf60f6efb91a99a790a94151ecf",
        "sympy/solvers/solveset.py": "186ba1f9b7fa08c11faff83766e19fc2143222578f1459e6f1ffd171bb43d6f6",
    }
    for filename, expected_hash in source_hashes.items():
        if hashlib.sha256((sympy_root / filename).read_bytes()).hexdigest() != expected_hash:
            raise ValueError(f"Historical source differs from the task base commit: {filename}")
    # Compatibility aliases only support importing the old source on Python 3.12.
    for name in ("Mapping", "MutableMapping", "Sequence", "MutableSequence", "Iterable", "Callable"):
        if not hasattr(collections, name):
            setattr(collections, name, getattr(collections.abc, name))
    if not hasattr(inspect, "getargspec"):
        inspect.getargspec = inspect.getfullargspec
    sys.path.insert(0, str(sympy_root.resolve()))
    import sympy
    import mpmath
    from sympy.core.relational import Equality, Relational

    expected_module = (sympy_root / "sympy/__init__.py").resolve()
    if Path(sympy.__file__).resolve() != expected_module:
        raise ValueError("The supplied historical SymPy source was not imported")
    added = added_file_lines(load_patch(root, CLAUDE, "sympy__sympy-18211", 3),
                             "sympy/core/relational.py")
    namespace = {"S": sympy.S}
    exec(compile(textwrap.dedent(added), "<archived Equality._eval_as_set>", "exec"), namespace)
    candidate_method = namespace["_eval_as_set"]
    x = sympy.Symbol("x")
    equations = [sympy.Eq(x * sympy.cos(x) - 3 * sympy.sin(x), 0),
                 sympy.Eq(x**2 + sympy.sqrt(2 * x) + sympy.sin(x), 0)]
    expected = [sympy.ConditionSet(x, equation, sympy.S.Reals) for equation in equations]
    results, candidate_set = [], None
    for method in (Relational._eval_as_set, candidate_method):
        with patch.object(Equality, "_eval_as_set", method):
            observations = []
            for equation, target in zip(equations, expected):
                try:
                    actual = equation.as_set()
                    if method is candidate_method and equation == equations[1]:
                        candidate_set = actual
                    observations.append({"matches_official_assertion": actual == target,
                                         "result": str(actual)})
                except NotImplementedError:
                    observations.append({"matches_official_assertion": False,
                                         "exception": "NotImplementedError"})
            results.append(observations)
    assert not results[0][0]["matches_official_assertion"]
    assert results[1][0]["matches_official_assertion"]
    assert not results[1][1]["matches_official_assertion"]
    transformed = candidate_set.condition.lhs - candidate_set.condition.rhs
    original = equations[1].lhs - equations[1].rhs
    extra_solution = sympy.nsolve(transformed, x, 0.7)
    transformed_residual = float(transformed.subs(x, extra_solution).evalf())
    original_residual = float(original.subs(x, extra_solution).evalf())
    assert extra_solution > 0 and abs(transformed_residual) < 1e-8
    assert abs(original_residual) > 1
    return {"case": "sympy__sympy-18211/Claude/3",
            "check": "two official equality assertions using supplied historical SymPy source",
            "source": {"base_commit": "b4f1aa3540fe68d078d76e78ba59d022dd6df39f",
                       "checked_files_sha256": source_hashes, "mpmath_version": mpmath.__version__},
            "baseline": results[0], "candidate": results[1],
            "counterexample": {"x": float(extra_solution),
                               "candidate_condition_residual": transformed_residual,
                               "original_condition_residual": original_residual},
            "passed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT)
    parser.add_argument("--sympy-root", type=Path,
                        help="Optional SymPy b4f1aa3540fe68d078d76e78ba59d022dd6df39f source checkout")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    checks = [check_regex(arguments.data_root), *check_cache(arguments.data_root),
              check_include_options(arguments.data_root), *check_literal_events(arguments.data_root),
              check_printer_state(arguments.data_root)]
    if arguments.sympy_root:
        checks.append(check_historical_equality(arguments.data_root, arguments.sympy_root))
    result = {"scope": "Isolated archived-function checks; Sphinx and printer checks use dependency/dispatch stubs. "
                       "These checks do not rerun historical repository tests or SWE-bench evaluation.",
              "passed": all(check["passed"] for check in checks), "checks": checks}
    serialized = json.dumps(result, indent=2) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
