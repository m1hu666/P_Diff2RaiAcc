"""Extract portable agent/runtime source references for the experiment.

Usage:
    python3 scripts/inspect_runtime_source.py --agent-root PATH
    python3 scripts/inspect_runtime_source.py --agent-root PATH --adapter-root PATH

The adapter root is the litellm package directory. If omitted, discovery checks
the supplied checkout's virtual environments and installed distribution metadata.
The resulting portable JSON/CSV evidence is written under
``result/Statistics results`` by default. No provider clients are imported and
no environment configuration is loaded.
"""

import argparse
import ast
import csv
import hashlib
import importlib.metadata
import json
import re
import subprocess
from email.parser import Parser
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = ROOT / 'result' / 'Statistics results'


def git_commit(root):
    """Read an explicitly supplied repository identity without modifying it."""
    if not (root/'.git').exists():
        return None
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, check=False)
    except OSError:
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and re.fullmatch(r'[0-9a-f]{40,64}', value) else None


def source_version(package):
    for name in ('__init__.py', '_version.py', 'version.py'):
        path = package/name
        if path.is_file():
            match = re.search(r'(?m)^__version__\s*=\s*[\'"]([^\'"]+)[\'"]', path.read_text())
            if match:
                return match.group(1)
    for path in sorted(package.parent.glob('litellm-*.dist-info/METADATA')):
        metadata = Parser().parsestr(path.read_text())
        if metadata.get('Name', '').lower() == 'litellm':
            return metadata.get('Version')
    return None


def discover_adapter(agent_root):
    patterns = (
        '.venv/Lib/site-packages/litellm',
        '.venv/lib/python*/site-packages/litellm',
        '.venv/lib64/python*/site-packages/litellm',
        'venv/Lib/site-packages/litellm',
        'venv/lib/python*/site-packages/litellm',
        'venv/lib64/python*/site-packages/litellm',
    )
    candidates = sorted({p.resolve() for pattern in patterns for p in agent_root.glob(pattern)
                         if (p/'main.py').is_file()})
    if len(candidates) == 1:
        return candidates[0], 'checkout environment'
    if len(candidates) > 1:
        raise ValueError('Multiple adapter installations found; specify --adapter-root.')
    try:
        distribution = importlib.metadata.distribution('litellm')
    except importlib.metadata.PackageNotFoundError:
        return None, 'not available'
    package = Path(distribution.locate_file('litellm')).resolve()
    return (package, 'installed distribution') if (package/'main.py').is_file() else (None, 'not available')


def function_index(tree):
    found = {}

    def visit(nodes, prefix=''):
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, prefix+node.name+'.')
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found[prefix+node.name] = node
    visit(tree.body)
    return found


def source_reference(path, logical_path, names):
    content = path.read_text()
    index = function_index(ast.parse(content))
    functions = [{'name': name, 'line': index[name].lineno, 'end_line': index[name].end_lineno}
                 for name in names if name in index]
    return {'path': logical_path, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'functions': functions}


def experiment_yaml(path):
    """Read only relevant scalar settings; do not parse prompt block contents."""
    wanted = {
        'agent.step_limit', 'agent.cost_limit',
        'environment.timeout', 'environment.container_timeout',
        'model.model_name', 'model.set_cache_control',
        'model.model_kwargs.temperature', 'model.model_kwargs.top_p',
        'model.model_kwargs.top_k', 'model.model_kwargs.max_tokens',
        'model.model_kwargs.max_completion_tokens', 'model.model_kwargs.reasoning',
        'model.model_kwargs.reasoning_effort', 'model.model_kwargs.drop_params',
    }
    stack, rows, block_indent = [], [], None
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        indent = len(line)-len(line.lstrip())
        if block_indent is not None:
            if indent > block_indent:
                continue
            block_indent = None
        match = re.match(r'^\s*([A-Za-z_]\w*):(?:\s*(.*))?$', line)
        if not match:
            continue
        key, value = match.groups()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        name = '.'.join([item[1] for item in stack]+[key])
        value = (value or '').strip()
        if value.startswith(('|', '>')):
            block_indent = indent
            continue
        if not value:
            stack.append((indent, key))
            continue
        if name in wanted:
            value = value.split(' #', 1)[0].strip()
            if value[:1] in ('"', "'"):
                try:
                    value = str(ast.literal_eval(value))
                except (ValueError, SyntaxError):
                    pass
            rows.append({'scope': 'SWE-bench configuration', 'setting': name,
                         'value_or_behavior': value,
                         'file': 'mini-swe-agent/src/minisweagent/config/extra/swebench.yaml',
                         'line': line_number})
    return rows


def collect(agent_root, adapter_root, discovery):
    src = agent_root/'src/minisweagent'
    specifications = [
        (src/'models/litellm_model.py', 'mini-swe-agent/src/minisweagent/models/litellm_model.py',
         [('LitellmModel._query', 'request parameters', 'Pass model_kwargs to litellm.completion.'),
          ('LitellmModel.query', 'saved token reports', 'Save the returned normalized response and accumulate the framework cost estimate.')]),
        (src/'agents/default.py', 'mini-swe-agent/src/minisweagent/agents/default.py',
         [('DefaultAgent.query', 'history and limits', 'Send accumulated messages; enforce configured model-call and cost limits.'),
          ('DefaultAgent.parse_action', 'tool protocol', 'Require exactly one bash code block per response.'),
          ('DefaultAgent.has_finished', 'submission', 'Recognize the final-submission marker in shell output.')]),
        (src/'models/utils/cache_control.py', 'mini-swe-agent/src/minisweagent/models/utils/cache_control.py',
         [('set_cache_control', 'cache markers', 'Place an ephemeral cache-control marker on the last message.')]),
        (src/'environments/docker.py', 'mini-swe-agent/src/minisweagent/environments/docker.py',
         [('DockerEnvironment.execute', 'shell execution', 'Execute bash serially in Docker with the configured command timeout.')]),
        (src/'run/utils/save.py', 'mini-swe-agent/src/minisweagent/run/utils/save.py',
         [('save_traj', 'archived configuration', 'Save model, agent and environment configurations with the messages.')]),
    ]
    if adapter_root:
        specifications += [
            (adapter_root/'llms/openai/chat/gpt_5_transformation.py', 'litellm/llms/openai/chat/gpt_5_transformation.py',
             [('OpenAIGPT5Config.map_openai_params', 'GPT sampling and output limit', 'Drop unsupported sampling values when requested; map max_tokens to max_completion_tokens.')]),
            (adapter_root/'llms/anthropic/chat/transformation.py', 'litellm/llms/anthropic/chat/transformation.py',
             [('AnthropicConfig.get_config', 'Anthropic output limit', 'Supply max_tokens from adapter configuration when the client omits it.'),
              ('AnthropicConfig.get_max_tokens_for_model', 'Anthropic limit selection', 'Obtain the model output limit or use the adapter fallback.'),
              ('AnthropicConfig.calculate_usage', 'Anthropic input accounting', 'Include cache writes and cache reads in normalized prompt_tokens.')]),
            (adapter_root/'llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py',
             'litellm/llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py',
             [('VertexGeminiConfig._calculate_usage', 'Gemini output accounting', 'Include reported thinking in completion_tokens unless already included in the candidate count.')]),
        ]
    references, settings = [], []
    for path, logical_path, items in specifications:
        if not path.is_file():
            continue
        reference = source_reference(path, logical_path, [item[0] for item in items])
        references.append(reference)
        locations = {fn['name']: fn['line'] for fn in reference['functions']}
        for function, setting, behavior in items:
            if function in locations:
                settings.append({'scope': 'implementation', 'setting': setting,
                                 'value_or_behavior': behavior, 'file': logical_path,
                                 'line': locations[function]})
    yaml_path = src/'config/extra/swebench.yaml'
    if yaml_path.is_file():
        settings = experiment_yaml(yaml_path)+settings
        references.append({'path': 'mini-swe-agent/src/minisweagent/config/extra/swebench.yaml',
                           'sha256': hashlib.sha256(yaml_path.read_bytes()).hexdigest(), 'functions': []})
        lines = yaml_path.read_text().splitlines()
        for index, line in enumerate(lines, 1):
            if 'output.output | length < 10000' in line:
                settings.append({'scope': 'SWE-bench configuration', 'setting': 'observation truncation',
                                 'value_or_behavior': 'For long output, keep the first and last 5,000 characters.',
                                 'file': 'mini-swe-agent/src/minisweagent/config/extra/swebench.yaml', 'line': index})
                break
    signature = None
    if adapter_root and (adapter_root/'main.py').is_file():
        path = adapter_root/'main.py'
        index = function_index(ast.parse(path.read_text()))
        node = index.get('completion')
        if node:
            names = [arg.arg for arg in node.args.args]
            selected = ('temperature', 'top_p', 'max_tokens', 'max_completion_tokens',
                        'reasoning_effort', 'reasoning', 'thinking', 'seed', 'tools', 'tool_choice')
            signature = {'path': 'litellm/main.py', 'line': node.lineno,
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'named_parameters': [name for name in selected if name in names],
                         'accepts_arbitrary_kwargs': node.args.kwarg is not None}
    adapter_version = source_version(adapter_root) if adapter_root else None
    adapter_repository = adapter_root.parent if adapter_root else None
    return {'schema_version': 2,
            'scope': 'Supplied source evidence; archived run configurations define experimental settings.',
            'agent_source_version': source_version(src), 'agent_git_commit': git_commit(agent_root),
            'adapter': {'available': adapter_root is not None, 'discovery': discovery,
                        'version': adapter_version,
                        'git_commit': git_commit(adapter_repository) if adapter_repository else None},
            'current_completion_signature': signature, 'source_evidence': references, 'settings': settings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent-root', type=Path, required=True, help='mini-SWE-agent repository root')
    parser.add_argument('--adapter-root', type=Path, help='Optional litellm package directory')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    agent_root = args.agent_root.resolve()
    if not (agent_root/'src/minisweagent').is_dir():
        parser.error('The agent root must contain src/minisweagent.')
    if args.adapter_root:
        adapter_root, discovery = args.adapter_root.resolve(), 'explicit adapter root'
        if not (adapter_root/'main.py').is_file():
            parser.error('The adapter root must be a litellm package directory containing main.py.')
    else:
        try:
            adapter_root, discovery = discover_adapter(agent_root)
        except ValueError as exc:
            parser.error(str(exc))
    result = collect(agent_root, adapter_root, discovery)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'runtime_source_evidence.json').write_text(json.dumps(result, indent=2)+'\n')
    with (args.output/'source_settings.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['scope', 'setting', 'value_or_behavior', 'file', 'line'])
        writer.writeheader()
        writer.writerows(result['settings'])
    print(f"Extracted {len(result['settings'])} settings with portable source references.")


if __name__ == '__main__':
    main()
