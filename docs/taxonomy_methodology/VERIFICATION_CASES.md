# Existing failure assignments: coder review packet

This page presents the authors' current labels and analyses for independent verification by Coders A, B, and C. It is generated from the canonical annotations and task notes; the descriptions are existing interpretations, not additional evidence. Check each trial against the [failure codebook](../failure_analysis/FAILURE_CODEBOOK.md) and the linked materials, then record both the category decision and chronological-link judgment in the assigned coder sheet using the [coder instructions](CODING_GUIDE.md).

Each task lists shared source materials once and provides a candidate patch and trajectory for each failed trial. The linked benchmark test-ID file lists expected tests from the dataset, not this trial's execution outcome. Some retained assignments explicitly note that further verification is needed.

## Task index

- [astropy__astropy-14182](#task-astropy__astropy-14182) (7 trials)
- [astropy__astropy-13398](#task-astropy__astropy-13398) (9 trials)
- [astropy__astropy-8872](#task-astropy__astropy-8872) (9 trials)
- [django__django-12125](#task-django__django-12125) (1 trial)
- [django__django-13343](#task-django__django-13343) (1 trial)
- [django__django-13401](#task-django__django-13401) (1 trial)
- [django__django-15103](#task-django__django-15103) (2 trials)
- [django__django-11276](#task-django__django-11276) (3 trials)
- [django__django-15741](#task-django__django-15741) (3 trials)
- [django__django-14771](#task-django__django-14771) (4 trials)
- [django__django-15022](#task-django__django-15022) (4 trials)
- [django__django-13023](#task-django__django-13023) (5 trials)
- [django__django-13406](#task-django__django-13406) (5 trials)
- [django__django-11532](#task-django__django-11532) (6 trials)
- [django__django-13344](#task-django__django-13344) (6 trials)
- [django__django-14140](#task-django__django-14140) (6 trials)
- [django__django-11790](#task-django__django-11790) (7 trials)
- [django__django-16560](#task-django__django-16560) (7 trials)
- [django__django-10554](#task-django__django-10554) (9 trials)
- [django__django-14155](#task-django__django-14155) (9 trials)
- [django__django-15629](#task-django__django-15629) (9 trials)
- [django__django-15732](#task-django__django-15732) (9 trials)
- [django__django-16502](#task-django__django-16502) (9 trials)
- [matplotlib__matplotlib-20859](#task-matplotlib__matplotlib-20859) (1 trial)
- [matplotlib__matplotlib-24570](#task-matplotlib__matplotlib-24570) (1 trial)
- [matplotlib__matplotlib-26291](#task-matplotlib__matplotlib-26291) (1 trial)
- [matplotlib__matplotlib-25311](#task-matplotlib__matplotlib-25311) (3 trials)
- [matplotlib__matplotlib-21568](#task-matplotlib__matplotlib-21568) (9 trials)
- [matplotlib__matplotlib-26208](#task-matplotlib__matplotlib-26208) (9 trials)
- [psf__requests-2931](#task-psf__requests-2931) (4 trials)
- [pylint-dev__pylint-8898](#task-pylint-dev__pylint-8898) (8 trials)
- [pylint-dev__pylint-4661](#task-pylint-dev__pylint-4661) (9 trials)
- [scikit-learn__scikit-learn-13135](#task-scikit-learn__scikit-learn-13135) (1 trial)
- [scikit-learn__scikit-learn-15100](#task-scikit-learn__scikit-learn-15100) (1 trial)
- [scikit-learn__scikit-learn-26194](#task-scikit-learn__scikit-learn-26194) (9 trials)
- [sphinx-doc__sphinx-10323](#task-sphinx-doc__sphinx-10323) (1 trial)
- [sphinx-doc__sphinx-9591](#task-sphinx-doc__sphinx-9591) (1 trial)
- [sphinx-doc__sphinx-8056](#task-sphinx-doc__sphinx-8056) (5 trials)
- [sphinx-doc__sphinx-8548](#task-sphinx-doc__sphinx-8548) (7 trials)
- [sphinx-doc__sphinx-11510](#task-sphinx-doc__sphinx-11510) (9 trials)
- [sphinx-doc__sphinx-7748](#task-sphinx-doc__sphinx-7748) (9 trials)
- [sympy__sympy-15345](#task-sympy__sympy-15345) (1 trial)
- [sympy__sympy-18211](#task-sympy__sympy-18211) (5 trials)
- [sympy__sympy-17630](#task-sympy__sympy-17630) (8 trials)
- [sympy__sympy-12489](#task-sympy__sympy-12489) (9 trials)

<a id="task-astropy__astropy-14182"></a>

### astropy__astropy-14182 (7 failed trials)

**Task summary:** The reStructuredText table writer does not accept additional header_rows such as units.

**Current task analysis:** The seven failed trials implement header writing without adjusting where the reader starts table data. The two passing trials account for the number of header rows when setting the data start line, supporting the tested write/read behavior.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/astropy__astropy-14182_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/astropy__astropy-14182_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/astropy__astropy-14182_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/astropy__astropy-14182_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/astropy__astropy-14182_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/1astropy__astropy-14182_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| Claude-2 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-14182/2astropy__astropy-14182_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-14182/1astropy__astropy-14182_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-14182/2astropy__astropy-14182_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-14182/3astropy__astropy-14182_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-14182/1astropy__astropy-14182_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Adds configurable header rows to RST writing but does not update the reader offset, leaving round-trip table reading inconsistent with the written layout. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-14182/3astropy__astropy-14182_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-14182/astropy__astropy-14182.traj.json) |

<a id="task-astropy__astropy-13398"></a>

### astropy__astropy-13398 (9 failed trials)

**Task summary:** Transforming nearby terrestrial objects from ITRS to observed coordinates through an inertial frame introduces inappropriate aberration effects.

**Current task analysis:** All nine failed trials introduce a direct transformation path but omit atmospheric refraction handling. The geometric near-Earth case can improve while the refraction-dependent cases required by the tests remain unsupported.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/astropy__astropy-13398_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/astropy__astropy-13398_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/astropy__astropy-13398_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/astropy__astropy-13398_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/astropy__astropy-13398_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/1astropy__astropy-13398_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| Claude-2 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/2astropy__astropy-13398_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| Claude-3 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-13398/3astropy__astropy-13398_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| Gemini-1 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-13398/1astropy__astropy-13398_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| Gemini-2 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-13398/2astropy__astropy-13398_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| Gemini-3 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-13398/3astropy__astropy-13398_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| GPT-1 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-13398/1astropy__astropy-13398_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| GPT-2 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-13398/2astropy__astropy-13398_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) |
| GPT-3 | P1 Misinterpretation / Domain Knowledge Lack | Adds a direct terrestrial-to-observed coordinate transform but omits atmospheric refraction handling required for existing observed-frame behavior. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-13398/3astropy__astropy-13398_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) |

<a id="task-astropy__astropy-8872"></a>

### astropy__astropy-8872 (9 failed trials)

**Task summary:** Quantity construction promotes a float16 input to float64 instead of preserving the floating-point dtype.

**Current task analysis:** The nine candidate patches use different dtype predicates and preserve the reported float16 input. They retain boolean-to-float behavior already present in the baseline, whereas the reference patch also changes that policy. Their original V3 assignments are retained pending further verification; the retained artifacts do not identify the official failing assertion for these nine outcomes.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/astropy__astropy-8872_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/astropy__astropy-8872_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/astropy__astropy-8872_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/astropy__astropy-8872_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/astropy__astropy-8872_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/1astropy__astropy-8872_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| Claude-2 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/2astropy__astropy-8872_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| Claude-3 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/claude-sonnet-4-5-20250929/astropy__astropy-8872/3astropy__astropy-8872_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| Gemini-1 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-8872/1astropy__astropy-8872_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| Gemini-2 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-8872/2astropy__astropy-8872_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| Gemini-3 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gemini-3-pro-preview/astropy__astropy-8872/3astropy__astropy-8872_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| GPT-1 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-8872/1astropy__astropy-8872_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| GPT-2 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-8872/2astropy__astropy-8872_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) |
| GPT-3 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch preserves the reported float16 input, and boolean-to-float conversion is also present in the baseline. This does not establish a new regression; the retained artifacts do not identify the official failing assertion. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/astropy__astropy-8872/3astropy__astropy-8872_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) |

**Interpretation note:** The original documentation and deleted code in the reference patch explicitly show boolean conversion before the repair. A difference from the reference implementation does not establish either a new regression or the reason for a failed evaluation. Retention of the V3 labels does not mean that the recheck confirmed those attributions.

<a id="task-django__django-12125"></a>

### django__django-12125 (1 failed trials)

**Task summary:** Migration serialization uses an unqualified class name for nested classes, generating an invalid import path.

**Current task analysis:** Gemini trial 3 adds module-search logic around the existing path instead of using the nested class qualified name at serialization. The other eight trials use the relevant qualified-name information and pass.

**Shared materials:** [Issue](../../analyse/gemini-3-pro-preview/django__django-12125/django__django-12125_problem_statement.txt) · [Hints](../../analyse/gemini-3-pro-preview/django__django-12125/django__django-12125_hints.txt) · [Reference patch](../../analyse/gemini-3-pro-preview/django__django-12125/django__django-12125_gold.patch) · [Evaluation tests](../../analyse/gemini-3-pro-preview/django__django-12125/django__django-12125_test.patch) · [Benchmark test IDs](../../analyse/gemini-3-pro-preview/django__django-12125/django__django-12125_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Gemini-3 | S2 Incorrect Repair Strategy | Attempts to reconstruct nested class paths by searching modules instead of serializing the qualified class name, leaving nested-class import paths incorrect. | [Patch](../../analyse/gemini-3-pro-preview/django__django-12125/3django__django-12125_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-12125/django__django-12125.traj.json) |

<a id="task-django__django-13343"></a>

### django__django-13343 (1 failed trials)

**Task summary:** FileField deconstruction serializes an evaluated storage instance instead of retaining the supplied storage callable.

**Current task analysis:** Claude trial 2 changes storage into a property and fails the evaluated initialization and deconstruction behavior. The passing trials retain access to the original callable while preserving the expected storage interface.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/django__django-13343_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/django__django-13343_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/django__django-13343_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/django__django-13343_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/django__django-13343_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-2 | V4 Execution Timing Mismatch | Defers storage evaluation through a property instead of retaining the original callable alongside an eagerly evaluated storage instance, conflicting with field initialization and deconstruction expectations. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13343/2django__django-13343_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13343/django__django-13343.traj.json) |

<a id="task-django__django-13401"></a>

### django__django-13401 (1 failed trials)

**Task summary:** Field copies inherited from abstract models share a creation counter and can be incorrectly treated as equal across models.

**Current task analysis:** GPT trial 2 uses object identity as an ordering tie-breaker. That ordering differs from the deterministic model-based ordering expected by the tests. The other eight trials preserve the required equality and ordering behavior.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/django__django-13401_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/django__django-13401_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/django__django-13401_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/django__django-13401_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/django__django-13401_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-2 | S2 Incorrect Repair Strategy | Uses object identity as a tie-breaker in field ordering rather than stable model metadata, so the order does not follow the tested model-name ordering contract. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13401/2django__django-13401_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13401/django__django-13401.traj.json) |

**Interpretation note:** Object identity distinguishes objects but does not implement a stable model-name ordering.

<a id="task-django__django-15103"></a>

### django__django-15103 (2 failed trials)

**Task summary:** json_script requires an element identifier even when the caller does not need one.

**Current task analysis:** Claude trials 1 and 2 make the low-level utility argument optional but omit the corresponding template-filter entry point. Their reproduction focuses on direct Python calls. The remaining trials cover the relevant interface change and pass.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/django__django-15103_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/django__django-15103_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/django__django-15103_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/django__django-15103_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/django__django-15103_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | L1 Incomplete Scope / Wrong Layer | Makes the low-level json_script helper accept an omitted element ID but leaves the template-filter entry point requiring that argument. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/1django__django-15103_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15103/django__django-15103.traj.json) |
| Claude-2 | L1 Incomplete Scope / Wrong Layer | Makes the low-level json_script helper accept an omitted element ID but leaves the template-filter entry point requiring that argument. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15103/2django__django-15103_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15103/django__django-15103.traj.json) |

<a id="task-django__django-11276"></a>

### django__django-11276 (3 failed trials)

**Task summary:** Django intends to replace its custom HTML escaping implementation with the standard-library implementation.

**Current task analysis:** All three Gemini trials call html.escape but then convert the apostrophe entity back from &#x27; to &#39;. This preserves the former output spelling and fails the exact output expected after the accepted refactoring. Claude and GPT pass.

**Shared materials:** [Issue](../../analyse/gemini-3-pro-preview/django__django-11276/django__django-11276_problem_statement.txt) · [Hints](../../analyse/gemini-3-pro-preview/django__django-11276/django__django-11276_hints.txt) · [Reference patch](../../analyse/gemini-3-pro-preview/django__django-11276/django__django-11276_gold.patch) · [Evaluation tests](../../analyse/gemini-3-pro-preview/django__django-11276/django__django-11276_test.patch) · [Benchmark test IDs](../../analyse/gemini-3-pro-preview/django__django-11276/django__django-11276_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Gemini-1 | S2 Incorrect Repair Strategy | Uses html.escape but replaces its apostrophe entity with the previous representation, conflicting with the exact output expected for the standard-library refactoring. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11276/1django__django-11276_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-11276/django__django-11276.traj.json) |
| Gemini-2 | S2 Incorrect Repair Strategy | Uses html.escape but replaces its apostrophe entity with the previous representation, conflicting with the exact output expected for the standard-library refactoring. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11276/2django__django-11276_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-11276/django__django-11276.traj.json) |
| Gemini-3 | S2 Incorrect Repair Strategy | Uses html.escape but replaces its apostrophe entity with the previous representation, conflicting with the exact output expected for the standard-library refactoring. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11276/3django__django-11276_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-11276/django__django-11276.traj.json) |

**Interpretation note:** Both apostrophe entities denote the same HTML character. The recorded mismatch concerns the exact output contract; its performance effect was not measured.

<a id="task-django__django-15741"></a>

### django__django-15741 (3 failed trials)

**Task summary:** get_format does not accept a lazy string argument, affecting consumers such as the date template filter.

**Current task analysis:** Claude and Gemini convert the argument to a string and pass, using force_str and str respectively. All three GPT trials return without performing the required conversion, leaving downstream consumers with the unsupported lazy argument.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/django__django-15741_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/django__django-15741_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/django__django-15741_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/django__django-15741_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/django__django-15741_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Returns a lazy format argument without normalizing it before subsequent format lookup, leaving lazy-string support incomplete. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/1django__django-15741_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15741/django__django-15741.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Returns a lazy format argument without normalizing it before subsequent format lookup, leaving lazy-string support incomplete. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/2django__django-15741_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15741/django__django-15741.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Returns a lazy format argument without normalizing it before subsequent format lookup, leaving lazy-string support incomplete. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15741/3django__django-15741_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15741/django__django-15741.traj.json) |

<a id="task-django__django-14771"></a>

### django__django-14771 (4 failed trials)

**Task summary:** The development-server autoreloader does not propagate interpreter -X options to the child process.

**Current task analysis:** Gemini trial 2 and the three GPT trials emit separate argument tokens such as ["-X", "utf8"], while the tests expect the combined form ["-Xutf8"]. The remaining trials match the tested subprocess argument structure.

**Shared materials:** [Issue](../../analyse/gemini-3-pro-preview/django__django-14771/django__django-14771_problem_statement.txt) · [Hints](../../analyse/gemini-3-pro-preview/django__django-14771/django__django-14771_hints.txt) · [Reference patch](../../analyse/gemini-3-pro-preview/django__django-14771/django__django-14771_gold.patch) · [Evaluation tests](../../analyse/gemini-3-pro-preview/django__django-14771/django__django-14771_test.patch) · [Benchmark test IDs](../../analyse/gemini-3-pro-preview/django__django-14771/django__django-14771_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Gemini-2 | V2 Strict Output Format Mismatch | Passes interpreter -X options as separate flag/value arguments, while the tests compare against combined argument strings such as -Xutf8. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14771/2django__django-14771_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-14771/django__django-14771.traj.json) |
| GPT-1 | V2 Strict Output Format Mismatch | Passes interpreter -X options as separate flag/value arguments, while the tests compare against combined argument strings such as -Xutf8. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14771/1django__django-14771_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-14771/django__django-14771.traj.json) |
| GPT-2 | V2 Strict Output Format Mismatch | Passes interpreter -X options as separate flag/value arguments, while the tests compare against combined argument strings such as -Xutf8. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14771/2django__django-14771_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-14771/django__django-14771.traj.json) |
| GPT-3 | V2 Strict Output Format Mismatch | Passes interpreter -X options as separate flag/value arguments, while the tests compare against combined argument strings such as -Xutf8. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14771/3django__django-14771_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14771/django__django-14771.traj.json) |

**Interpretation note:** Alternative command-line spellings can be accepted by the interpreter. The failure here is the exact argument-vector contract checked by the benchmark, rather than proof that the alternative never works.

<a id="task-django__django-15022"></a>

### django__django-15022 (4 failed trials)

**Task summary:** Admin searches containing several terms can create unnecessary joins over related fields.

**Current task analysis:** Claude trial 1 and Gemini trial 2 retain sequential filters precisely when joins are possible, leaving the expensive case unchanged. Gemini trial 1 uses subqueries without eliminating the repeated joins; Gemini trial 3 uses an existence-based strategy that does not satisfy the tested behavior. The notes also describe a candidate combined-filter strategy being reconsidered after a repository test whose expected result is updated by the benchmark test patch.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/django__django-15022_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/django__django-15022_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/django__django-15022_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/django__django-15022_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/django__django-15022_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S2 Incorrect Repair Strategy | Keeps the repeated filter loop precisely when related-field joins are present, so the branch requiring join consolidation remains unchanged. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15022/1django__django-15022_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15022/django__django-15022.traj.json) |
| Gemini-1 | S2 Incorrect Repair Strategy | Introduces a subquery but retains repeated joins across search terms instead of consolidating the related-field conditions. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15022/1django__django-15022_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-15022/django__django-15022.traj.json) |
| Gemini-2 | S2 Incorrect Repair Strategy | Keeps the repeated filter loop precisely when related-field joins are present, so the branch requiring join consolidation remains unchanged. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15022/2django__django-15022_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-15022/django__django-15022.traj.json) |
| Gemini-3 | S2 Incorrect Repair Strategy | Uses Exists-based filtering without resolving the repeated related-field join pattern identified by the issue. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15022/3django__django-15022_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-15022/django__django-15022.traj.json) |

**Interpretation note:** A repository test whose expected result changes with the accepted fix can influence the repair direction when the agent runs the original test unchanged.

<a id="task-django__django-13023"></a>

### django__django-13023 (5 failed trials)

**Task summary:** DecimalField lets exceptions from invalid nonnumeric inputs escape instead of converting them consistently to ValidationError.

**Current task analysis:** Gemini trials 1 and 3 and GPT trials 2 and 3 modify the model DecimalField but omit ValueError from its exception handling. Claude trial 2 instead modifies the form-field DecimalField, leaving the model-field conversion path targeted by the issue and tests unchanged. Passing trials handle the required exception types in the target module.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/django__django-13023_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/django__django-13023_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/django__django-13023_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/django__django-13023_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/django__django-13023_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-2 | V1 Specification-Oracle Gap | Changes DecimalField.to_python in django/forms/fields.py rather than the model DecimalField in django/db/models/fields/__init__.py, leaving the target conversion path unchanged. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13023/2django__django-13023_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13023/django__django-13023.traj.json) |
| Gemini-1 | V1 Specification-Oracle Gap | Handles the reported TypeError but omits ValueError, which the added validation tests also require DecimalField.to_python to translate into ValidationError. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13023/1django__django-13023_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-13023/django__django-13023.traj.json) |
| Gemini-3 | V1 Specification-Oracle Gap | Handles the reported TypeError but omits ValueError, which the added validation tests also require DecimalField.to_python to translate into ValidationError. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13023/3django__django-13023_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-13023/django__django-13023.traj.json) |
| GPT-2 | V1 Specification-Oracle Gap | Handles the reported TypeError but omits ValueError, which the added validation tests also require DecimalField.to_python to translate into ValidationError. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13023/2django__django-13023_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13023/django__django-13023.traj.json) |
| GPT-3 | V1 Specification-Oracle Gap | Handles the reported TypeError but omits ValueError, which the added validation tests also require DecimalField.to_python to translate into ValidationError. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13023/3django__django-13023_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-13023/django__django-13023.traj.json) |

**Interpretation note:** The additional ValueError case distinguishes four incomplete exception-handling repairs from Claude trial 2, which instead changes the wrong module and leaves the target conversion path untouched.

<a id="task-django__django-13406"></a>

### django__django-13406 (5 failed trials)

**Task summary:** Reassigning a pickled query to a queryset does not restore the iterable behavior needed for values-based query results.

**Current task analysis:** Claude trial 2 and all three Gemini trials preserve the original values_list result structure, while the benchmark expects dictionary-like values results when only the query is restored. GPT trial 1 has a separate implementation-state failure: a compound edit partially applies before its final awk stage fails, and an uninspected residual assignment inside QuerySet.values_list makes query.py syntactically invalid.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/django__django-13406_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/django__django-13406_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/django__django-13406_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/django__django-13406_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/django__django-13406_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-2 | V1 Specification-Oracle Gap | Preserves values_list iterable types across query serialization, while the benchmark expects a dictionary iterable when a deserialized query has selected values; this differs from the tested compatibility contract. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13406/2django__django-13406_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13406/django__django-13406.traj.json) |
| Gemini-1 | V1 Specification-Oracle Gap | Preserves values_list iterable types across query serialization, while the benchmark expects a dictionary iterable when a deserialized query has selected values; this differs from the tested compatibility contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13406/1django__django-13406_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-13406/django__django-13406.traj.json) |
| Gemini-2 | V1 Specification-Oracle Gap | Preserves values_list iterable types across query serialization, while the benchmark expects a dictionary iterable when a deserialized query has selected values; this differs from the tested compatibility contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13406/2django__django-13406_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-13406/django__django-13406.traj.json) |
| Gemini-3 | V1 Specification-Oracle Gap | Preserves values_list iterable types across query serialization, while the benchmark expects a dictionary iterable when a deserialized query has selected values; this differs from the tested compatibility contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13406/3django__django-13406_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-13406/django__django-13406.traj.json) |
| GPT-1 | I1 Tool Failure / Silent State Hallucination | A compound edit partially applies earlier sed changes before its final awk stage fails; the agent then inspects only the query setter and submits with an assignment inside the open clone._iterable_class expression, leaving query.py syntactically invalid. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13406/1django__django-13406_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-13406/django__django-13406.traj.json) |

**Interpretation note:** The four result-contract failures are V1 cases. GPT trial 1 is an I1 case because the failed compound edit leaves an unrecovered syntax error before the query-restoration behavior can be exercised.

<a id="task-django__django-11532"></a>

### django__django-11532 (6 failed trials)

**Task summary:** A non-ASCII hostname can cause email Message-ID generation to fail under a legacy email encoding.

**Current task analysis:** Claude trial 2 supports the local IDNA fix but adds a second cache that survives the established _fqdn reset, leaving a stale hostname. GPT trial 2 supports the first lookup but reads an unassigned local fqdn on a later cache hit. Both independently reproducible cache-lifecycle regressions are V3. Claude trials 1 and 3 and GPT trials 1 and 3 repair Message-ID locally while preserving the baseline Unicode cache behavior; their original V3 assignments are retained pending further verification.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/django__django-11532_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/django__django-11532_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/django__django-11532_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/django__django-11532_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/django__django-11532_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch converts the Message-ID hostname to IDNA while retaining the baseline Unicode DNS cache. An unchanged cache does not establish a new regression; the retained per-test evaluation evidence does not identify another primary failure for this attempt. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/1django__django-11532_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-11532/django__django-11532.traj.json) |
| Claude-2 | V3 Regression of Existing Behavior | Supports IDNA Message-ID generation but adds a second hostname cache that survives the existing _fqdn invalidation operation. After a hostname change and the established cache reset, it returns the stale hostname instead of refreshing it, a confirmed cache-lifecycle regression. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/2django__django-11532_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-11532/django__django-11532.traj.json) |
| Claude-3 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch converts the Message-ID hostname to IDNA while retaining the baseline Unicode DNS cache. An unchanged cache does not establish a new regression; the retained per-test evaluation evidence does not identify another primary failure for this attempt. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11532/3django__django-11532_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-11532/django__django-11532.traj.json) |
| GPT-1 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch converts the Message-ID hostname to IDNA while retaining the baseline Unicode DNS cache. An unchanged cache does not establish a new regression; the retained per-test evaluation evidence does not identify another primary failure for this attempt. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11532/1django__django-11532_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-11532/django__django-11532.traj.json) |
| GPT-2 | V3 Regression of Existing Behavior | Supports the first IDNA hostname lookup but assigns local fqdn only on a cache miss and reads it outside that branch. A second lookup raises UnboundLocalError, whereas the baseline returns its cached hostname, a confirmed repeated-call regression. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11532/2django__django-11532_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-11532/django__django-11532.traj.json) |
| GPT-3 | V3 Regression of Existing Behavior | Original V3 assignment retained pending further verification. The patch converts the Message-ID hostname to IDNA while retaining the baseline Unicode DNS cache. An unchanged cache does not establish a new regression; the retained per-test evaluation evidence does not identify another primary failure for this attempt. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11532/3django__django-11532_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-11532/django__django-11532.traj.json) |

**Interpretation note:** An unchanged baseline cache value is not evidence of a newly introduced regression. The retained V3 labels for Claude/GPT trials 1 and 3 do not mean that the recheck confirmed their primary failure. A complete per-test evaluation trace is needed.

<a id="task-django__django-13344"></a>

### django__django-13344 (6 failed trials)

**Task summary:** An asynchronous middleware chain can return an unawaited coroutine where an HTTP response is expected.

**Current task analysis:** The failed trials attempt to infer asynchronous behavior in the lower-level exception handler from wrapped callbacks. This treats downstream symptoms without correcting the middleware initialization or capability information at the appropriate layer. Claude trial 2 and Gemini trials 1 and 2 pass.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/django__django-13344_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/django__django-13344_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/django__django-13344_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/django__django-13344_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/django__django-13344_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/1django__django-13344_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-13344/django__django-13344.traj.json) |
| Claude-3 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-13344/3django__django-13344_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-13344/django__django-13344.traj.json) |
| Gemini-3 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/gemini-3-pro-preview/django__django-13344/3django__django-13344_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-13344/django__django-13344.traj.json) |
| GPT-1 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13344/1django__django-13344_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-13344/django__django-13344.traj.json) |
| GPT-2 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13344/2django__django-13344_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13344/django__django-13344.traj.json) |
| GPT-3 | L1 Incomplete Scope / Wrong Layer | Changes downstream exception handling instead of initializing the middleware asynchronous mode at its construction boundary, leaving the middleware capability information inconsistent. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-13344/3django__django-13344_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-13344/django__django-13344.traj.json) |

<a id="task-django__django-14140"></a>

### django__django-14140 (6 failed trials)

**Task summary:** Q.deconstruct assumes a single child is a key/value tuple and fails for expression children such as Exists.

**Current task analysis:** Claude trials 1 and 3, all Gemini trials, and GPT trial 3 guard the tuple-specific branch while preserving the older keyword-argument representation. These patches avoid the reported indexing error but do not produce the positional-argument deconstruction format checked by the benchmark tests.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/django__django-14140_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/django__django-14140_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/django__django-14140_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/django__django-14140_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/django__django-14140_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/1django__django-14140_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-14140/django__django-14140.traj.json) |
| Claude-3 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14140/3django__django-14140_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-14140/django__django-14140.traj.json) |
| Gemini-1 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14140/1django__django-14140_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-14140/django__django-14140.traj.json) |
| Gemini-2 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14140/2django__django-14140_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-14140/django__django-14140.traj.json) |
| Gemini-3 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14140/3django__django-14140_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-14140/django__django-14140.traj.json) |
| GPT-3 | V2 Strict Output Format Mismatch | Preserves the special keyword-argument form for a single tuple child, whereas the added tests require the unified positional deconstruction format. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14140/3django__django-14140_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14140/django__django-14140.traj.json) |

**Interpretation note:** Avoiding the indexing crash does not by itself satisfy the required serialization contract.

<a id="task-django__django-11790"></a>

### django__django-11790 (7 failed trials)

**Task summary:** AuthenticationForm no longer sets the username widget maxlength as expected.

**Current task analysis:** Claude trial 1, all Gemini trials, and GPT trial 2 store a string-valued maxlength where the tests expect an integer. GPT trials 1 and 3 defer the adjustment until rendering, whereas the tests inspect the earlier form state. The remaining Claude trials pass.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/django__django-11790_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/django__django-11790_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/django__django-11790_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/django__django-11790_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/django__django-11790_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V2 Strict Output Format Mismatch | Restores the widget maxlength as a string rather than the integer asserted in widget.attrs; matching rendered HTML alone does not meet this internal representation contract. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-11790/1django__django-11790_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-11790/django__django-11790.traj.json) |
| Gemini-1 | V2 Strict Output Format Mismatch | Restores the widget maxlength as a string rather than the integer asserted in widget.attrs; matching rendered HTML alone does not meet this internal representation contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11790/1django__django-11790_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-11790/django__django-11790.traj.json) |
| Gemini-2 | V2 Strict Output Format Mismatch | Restores the widget maxlength as a string rather than the integer asserted in widget.attrs; matching rendered HTML alone does not meet this internal representation contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11790/2django__django-11790_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-11790/django__django-11790.traj.json) |
| Gemini-3 | V2 Strict Output Format Mismatch | Restores the widget maxlength as a string rather than the integer asserted in widget.attrs; matching rendered HTML alone does not meet this internal representation contract. | [Patch](../../analyse/gemini-3-pro-preview/django__django-11790/3django__django-11790_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-11790/django__django-11790.traj.json) |
| GPT-1 | V4 Execution Timing Mismatch | Updates maxlength during later widget rendering rather than form initialization, leaving widget.attrs without the value when the tests inspect it. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11790/1django__django-11790_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-11790/django__django-11790.traj.json) |
| GPT-2 | V2 Strict Output Format Mismatch | Restores the widget maxlength as a string rather than the integer asserted in widget.attrs; matching rendered HTML alone does not meet this internal representation contract. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11790/2django__django-11790_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-11790/django__django-11790.traj.json) |
| GPT-3 | V4 Execution Timing Mismatch | Updates maxlength during later widget rendering rather than form initialization, leaving widget.attrs without the value when the tests inspect it. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-11790/3django__django-11790_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-11790/django__django-11790.traj.json) |

**Interpretation note:** A matching HTML rendering can coexist with a different internal attribute type or initialization time. These are separate contracts.

<a id="task-django__django-16560"></a>

### django__django-16560 (7 failed trials)

**Task summary:** Model constraints cannot consistently expose a configurable validation error code.

**Current task analysis:** Claude trial 1, all Gemini trials, and GPT trials 1 and 3 omit the PostgreSQL ExclusionConstraint subclass while updating more central constraint classes. GPT trial 2 is assigned to incomplete compatibility handling. Gemini trials 2 and 3 and GPT trial 3 additionally replace the legacy unique_together code for field-based uniqueness, violating the compatibility expectation in the tests.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/django__django-16560_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/django__django-16560_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/django__django-16560_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/django__django-16560_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/django__django-16560_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16560/1django__django-16560_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-16560/django__django-16560.traj.json) |
| Gemini-1 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16560/1django__django-16560_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-16560/django__django-16560.traj.json) |
| Gemini-2 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16560/2django__django-16560_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-16560/django__django-16560.traj.json) |
| Gemini-3 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16560/3django__django-16560_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-16560/django__django-16560.traj.json) |
| GPT-1 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16560/1django__django-16560_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-16560/django__django-16560.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Adds configurable constraint error codes but does not preserve the legacy unique_together code for the field-based uniqueness case. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16560/2django__django-16560_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-16560/django__django-16560.traj.json) |
| GPT-3 | L1 Incomplete Scope / Wrong Layer | Adds violation_error_code to core model constraints but omits the PostgreSQL ExclusionConstraint subclass, leaving the requested interface incomplete across constraint implementations. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16560/3django__django-16560_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-16560/django__django-16560.traj.json) |

**Interpretation note:** Some trials exhibit more than one defect. A single primary category is an annotation convention and should not imply that other observed defects are absent.

<a id="task-django__django-10554"></a>

### django__django-10554 (9 failed trials)

**Task summary:** Evaluating a derived union queryset can affect its source queryset and leave required ordering columns absent from generated SQL.

**Current task analysis:** Claude trial 1 submits reproduction or test code without a production fix. Claude trials 2 and 3, Gemini trials 2 and 3, and GPT trials 1 and 3 clone shared subqueries but do not repair SQL projection for ordering. Gemini trial 1 and GPT trial 2 remove ordering rather than preserve the required query behavior.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/django__django-10554_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/django__django-10554_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/django__django-10554_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/django__django-10554_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/django__django-10554_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | I1 Tool Failure / Silent State Hallucination | Submits reproduction and test additions without a production-code repair for the combined-query ordering defect. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/1django__django-10554_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-10554/django__django-10554.traj.json) |
| Claude-2 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/2django__django-10554_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-10554/django__django-10554.traj.json) |
| Claude-3 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-10554/3django__django-10554_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-10554/django__django-10554.traj.json) |
| Gemini-1 | S2 Incorrect Repair Strategy | Removes ordering from combined subqueries to avoid the immediate error, changing query ordering rather than satisfying the ORDER BY projection requirement. | [Patch](../../analyse/gemini-3-pro-preview/django__django-10554/1django__django-10554_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-10554/django__django-10554.traj.json) |
| Gemini-2 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/gemini-3-pro-preview/django__django-10554/2django__django-10554_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-10554/django__django-10554.traj.json) |
| Gemini-3 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/gemini-3-pro-preview/django__django-10554/3django__django-10554_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-10554/django__django-10554.traj.json) |
| GPT-1 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-10554/1django__django-10554_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-10554/django__django-10554.traj.json) |
| GPT-2 | S2 Incorrect Repair Strategy | Removes ordering from combined subqueries to avoid the immediate error, changing query ordering rather than satisfying the ORDER BY projection requirement. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-10554/2django__django-10554_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-10554/django__django-10554.traj.json) |
| GPT-3 | S2 Incorrect Repair Strategy | Clones combined subqueries to avoid shared-state mutation but leaves SQL ORDER BY expressions unsupported when their columns are absent from the SELECT list. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-10554/3django__django-10554_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-10554/django__django-10554.traj.json) |

**Interpretation note:** The failure analysis distinguishes shared-state mutation from the SQL projection requirement for ordering combined queries.

<a id="task-django__django-14155"></a>

### django__django-14155 (9 failed trials)

**Task summary:** A resolver representation does not display useful details when its view is a functools.partial object.

**Current task analysis:** All nine failed trials unwrap partial objects and lose information about their bound arguments. The reference implementation instead uses the partial object representation for this case, preserving the underlying callable and supplied arguments.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/django__django-14155_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/django__django-14155_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/django__django-14155_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/django__django-14155_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/django__django-14155_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/1django__django-14155_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-14155/django__django-14155.traj.json) |
| Claude-2 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/2django__django-14155_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-14155/django__django-14155.traj.json) |
| Claude-3 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-14155/3django__django-14155_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-14155/django__django-14155.traj.json) |
| Gemini-1 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14155/1django__django-14155_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-14155/django__django-14155.traj.json) |
| Gemini-2 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14155/2django__django-14155_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-14155/django__django-14155.traj.json) |
| Gemini-3 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gemini-3-pro-preview/django__django-14155/3django__django-14155_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-14155/django__django-14155.traj.json) |
| GPT-1 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14155/1django__django-14155_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-14155/django__django-14155.traj.json) |
| GPT-2 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14155/2django__django-14155_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-14155/django__django-14155.traj.json) |
| GPT-3 | P2 Distracted by Hints / TODOs | Unwraps functools.partial for display following a suggested direction, losing the bound argument information that a useful representation must retain. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-14155/3django__django-14155_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14155/django__django-14155.traj.json) |

<a id="task-django__django-15629"></a>

### django__django-15629 (9 failed trials)

**Task summary:** Foreign keys do not consistently inherit the collation of their referenced primary-key field.

**Current task analysis:** All nine failed trials update the foreign-key definition used during table creation but omit schema alteration logic that must synchronize existing foreign keys when the primary-key collation changes. Creation tests can pass while alteration tests fail.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/django__django-15629_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/django__django-15629_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/django__django-15629_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/django__django-15629_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/django__django-15629_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/1django__django-15629_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15629/django__django-15629.traj.json) |
| Claude-2 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/2django__django-15629_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15629/django__django-15629.traj.json) |
| Claude-3 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15629/3django__django-15629_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-15629/django__django-15629.traj.json) |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15629/1django__django-15629_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-15629/django__django-15629.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15629/2django__django-15629_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-15629/django__django-15629.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15629/3django__django-15629_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-15629/django__django-15629.traj.json) |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15629/1django__django-15629_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15629/django__django-15629.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15629/2django__django-15629_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15629/django__django-15629.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Propagates a referenced primary-key collation during foreign-key creation but omits synchronizing existing foreign keys when the primary-key collation is altered. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15629/3django__django-15629_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15629/django__django-15629.traj.json) |

<a id="task-django__django-15732"></a>

### django__django-15732 (9 failed trials)

**Task summary:** Dropping a single-field unique_together constraint is ambiguous when another uniqueness constraint exists on that field.

**Current task analysis:** All nine failed trials exclude a primary-key constraint but do not handle the distinct unique=True constraint case. Multiple non-primary unique constraints remain candidates, so the operation still fails the second evaluated scenario.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/django__django-15732_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/django__django-15732_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/django__django-15732_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/django__django-15732_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/django__django-15732_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/1django__django-15732_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15732/django__django-15732.traj.json) |
| Claude-2 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/2django__django-15732_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15732/django__django-15732.traj.json) |
| Claude-3 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-15732/3django__django-15732_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-15732/django__django-15732.traj.json) |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15732/1django__django-15732_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-15732/django__django-15732.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15732/2django__django-15732_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-15732/django__django-15732.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gemini-3-pro-preview/django__django-15732/3django__django-15732_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-15732/django__django-15732.traj.json) |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15732/1django__django-15732_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15732/django__django-15732.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15732/2django__django-15732_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15732/django__django-15732.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Handles a unique_together conflict with a primary key but leaves the corresponding unique=True conflict ambiguous when identifying which database constraint to remove. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-15732/3django__django-15732_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15732/django__django-15732.traj.json) |

<a id="task-django__django-16502"></a>

### django__django-16502 (9 failed trials)

**Task summary:** The development server does not consistently suppress a response body for HEAD requests.

**Current task analysis:** All nine failed trials remove the body but fail the benchmark checks on response-header handling, including the expected absence of Content-Length in the tested case.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/django__django-16502_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/django__django-16502_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/django__django-16502_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/django__django-16502_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/django__django-16502_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/1django__django-16502_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/django__django-16502/django__django-16502.traj.json) |
| Claude-2 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/2django__django-16502_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/django__django-16502/django__django-16502.traj.json) |
| Claude-3 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/claude-sonnet-4-5-20250929/django__django-16502/3django__django-16502_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/django__django-16502/django__django-16502.traj.json) |
| Gemini-1 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16502/1django__django-16502_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/django__django-16502/django__django-16502.traj.json) |
| Gemini-2 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16502/2django__django-16502_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/django__django-16502/django__django-16502.traj.json) |
| Gemini-3 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gemini-3-pro-preview/django__django-16502/3django__django-16502_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/django__django-16502/django__django-16502.traj.json) |
| GPT-1 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16502/1django__django-16502_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-16502/django__django-16502.traj.json) |
| GPT-2 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16502/2django__django-16502_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-16502/django__django-16502.traj.json) |
| GPT-3 | P1 Misinterpretation / Domain Knowledge Lack | Suppresses the HEAD response body but does not satisfy the tested response-header handling, including the required treatment of Content-Length. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/django__django-16502/3django__django-16502_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-16502/django__django-16502.traj.json) |

**Interpretation note:** The absence of Content-Length is a case-specific benchmark expectation and does not imply that HTTP forbids a Content-Length header in every HEAD response.

<a id="task-matplotlib__matplotlib-20859"></a>

### matplotlib__matplotlib-20859 (1 failed trials)

**Task summary:** Legend rejects SubFigure as a valid parent even though a SubFigure can host its own legend.

**Current task analysis:** Gemini trial 2 treats SubFigure like an Axes-style container and redirects ownership to the outer figure. This fails to preserve the SubFigure as the legend host. The other eight trials pass.

**Shared materials:** [Issue](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859_problem_statement.txt) · [Hints](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859_hints.txt) · [Reference patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859_gold.patch) · [Evaluation tests](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859_test.patch) · [Benchmark test IDs](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Gemini-2 | P1 Misinterpretation / Domain Knowledge Lack | Treats SubFigure as an Axes-like container and assigns its parent figure rather than preserving SubFigure as the legend host. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-20859/2matplotlib__matplotlib-20859_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859.traj.json) |

<a id="task-matplotlib__matplotlib-24570"></a>

### matplotlib__matplotlib-24570 (1 failed trials)

**Task summary:** HPacker reverses top and bottom alignment.

**Current task analysis:** GPT trial 1 inspects the shared alignment helper and both packers, then deliberately remaps top/bottom only in HPacker. This leaves VPacker top/bottom behavior unfixed and is the earliest unrecovered logical omission (S1). A later extension of the remapping to left/right also reverses HPacker placement, a secondary strategy defect.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-1 | S1 Partial Fix / Incomplete Logic | After reading the shared alignment helper and both packers, the agent deliberately remaps top and bottom only for HPacker. The corrected syntax still leaves VPacker top/bottom inconsistent with the tested alignment contract. This incomplete strategy is the earliest unrecovered breakdown. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-24570/1matplotlib__matplotlib-24570_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570.traj.json) |

**Interpretation note:** The observed differences are numeric layout behavior, not merely output formatting. Under the manuscript single-primary rule, the earlier incomplete fix is counted once as S1; the later S2 manifestation is not counted again.

<a id="task-matplotlib__matplotlib-26291"></a>

### matplotlib__matplotlib-26291 (1 failed trials)

**Task summary:** An inset axes operation fails during tight-bounding-box computation when the renderer is not available through the expected path.

**Current task analysis:** GPT trial 1 changes the figure state but does not supply the required renderer to the downstream operation. The other eight trials complete the renderer-handling repair and pass.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Updates the inset artist figure state without fixing the renderer supplied to the subsequent bounding-box calculation. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26291/1matplotlib__matplotlib-26291_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291.traj.json) |

<a id="task-matplotlib__matplotlib-25311"></a>

### matplotlib__matplotlib-25311 (3 failed trials)

**Task summary:** A figure containing a draggable legend cannot be pickled because the stored canvas includes objects that cannot be serialized.

**Current task analysis:** Claude and Gemini trace the inheritance hierarchy to the shared draggable implementation and add serialization handling. The three GPT trials avoid the immediate serialization error but do not preserve draggable behavior after loading and cover only selected subclasses.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-1 | L1 Incomplete Scope / Wrong Layer | Removes or bypasses non-pickleable canvas state at upper draggable classes without preserving the complete inherited draggable behavior after unpickling. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/1matplotlib__matplotlib-25311_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) |
| GPT-2 | L1 Incomplete Scope / Wrong Layer | Removes or bypasses non-pickleable canvas state at upper draggable classes without preserving the complete inherited draggable behavior after unpickling. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/2matplotlib__matplotlib-25311_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) |
| GPT-3 | L1 Incomplete Scope / Wrong Layer | Removes or bypasses non-pickleable canvas state at upper draggable classes without preserving the complete inherited draggable behavior after unpickling. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-25311/3matplotlib__matplotlib-25311_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) |

**Interpretation note:** The assessed requirement includes behavior after deserialization, rather than merely successful pickle creation.

<a id="task-matplotlib__matplotlib-21568"></a>

### matplotlib__matplotlib-21568 (9 failed trials)

**Task summary:** Date-axis labels have unclear spacing when usetex is enabled.

**Current task analysis:** Claude and Gemini focus on spacing around colons, while GPT makes broader rendering changes. The resulting strings do not provide the explicit TeX spacing required by the tests, leaving ordinary spaces where TeX math mode does not preserve the intended spacing. All nine trials fail.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/1matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| Claude-2 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/2matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| Claude-3 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-21568/3matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| Gemini-1 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-21568/1matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| Gemini-2 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-21568/2matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| Gemini-3 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-21568/3matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| GPT-1 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-21568/1matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| GPT-2 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-21568/2matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |
| GPT-3 | P1 Misinterpretation / Domain Knowledge Lack | Changes colon spacing or replaces date rendering without preserving the explicit LaTeX space separators required by the tested date-label output. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-21568/3matplotlib__matplotlib-21568_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) |

<a id="task-matplotlib__matplotlib-26208"></a>

### matplotlib__matplotlib-26208 (9 failed trials)

**Task summary:** Creating a twinned axis can corrupt the data limits of an existing plot with categorical units.

**Current task analysis:** All nine failed trials concentrate on limit-management code and nearby TODO comments. They do not propagate the original axis unit information to the twin, leaving the underlying categorical-unit mismatch unresolved.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/1matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| Claude-2 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/2matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| Claude-3 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/claude-sonnet-4-5-20250929/matplotlib__matplotlib-26208/3matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| Gemini-1 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-26208/1matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| Gemini-2 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-26208/2matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| Gemini-3 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gemini-3-pro-preview/matplotlib__matplotlib-26208/3matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| GPT-1 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26208/1matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| GPT-2 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26208/2matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |
| GPT-3 | P2 Distracted by Hints / TODOs | Changes data-limit handling around a TODO but leaves shared-axis unit propagation unresolved, so the twin axis still interprets categorical coordinates incorrectly. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/matplotlib__matplotlib-26208/3matplotlib__matplotlib-26208_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) |

<a id="task-psf__requests-2931"></a>

### psf__requests-2931 (4 failed trials)

**Task summary:** Requests coerces byte request bodies to strings instead of sending the original bytes.

**Current task analysis:** The repair must preserve body bytes while retaining the conversion needed for byte-valued URL parameters. Gemini trials 1 and 3 and GPT trials 2 and 3 return bytes early from _encode_params without handling the URL case. GPT trial 1 passes with a decode-or-return fallback that separates the evaluated body and URL inputs.

**Shared materials:** [Issue](../../analyse/gemini-3-pro-preview/psf__requests-2931/psf__requests-2931_problem_statement.txt) · [Hints](../../analyse/gemini-3-pro-preview/psf__requests-2931/psf__requests-2931_hints.txt) · [Reference patch](../../analyse/gemini-3-pro-preview/psf__requests-2931/psf__requests-2931_gold.patch) · [Evaluation tests](../../analyse/gemini-3-pro-preview/psf__requests-2931/psf__requests-2931_test.patch) · [Benchmark test IDs](../../analyse/gemini-3-pro-preview/psf__requests-2931/psf__requests-2931_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Preserves bytes in request bodies by changing the shared parameter encoder but omits the decoding still required for bytes used in URL parameters. | [Patch](../../analyse/gemini-3-pro-preview/psf__requests-2931/1psf__requests-2931_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/psf__requests-2931/psf__requests-2931.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Preserves bytes in request bodies by changing the shared parameter encoder but omits the decoding still required for bytes used in URL parameters. | [Patch](../../analyse/gemini-3-pro-preview/psf__requests-2931/3psf__requests-2931_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/psf__requests-2931/psf__requests-2931.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Preserves bytes in request bodies by changing the shared parameter encoder but omits the decoding still required for bytes used in URL parameters. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/psf__requests-2931/2psf__requests-2931_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/psf__requests-2931/psf__requests-2931.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Preserves bytes in request bodies by changing the shared parameter encoder but omits the decoding still required for bytes used in URL parameters. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/psf__requests-2931/3psf__requests-2931_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/psf__requests-2931/psf__requests-2931.traj.json) |

<a id="task-pylint-dev__pylint-8898"></a>

### pylint-dev__pylint-8898 (8 failed trials)

**Task summary:** Comma-separated regular-expression options are split inside repetition quantifiers such as {1,3}.

**Current task analysis:** Claude trial 2 handles quantifier commas while preserving the existing configuration parser conventions and passes. Claude trials 1 and 3 and GPT trials 2 and 3 change grouping-sensitive splitting; Gemini trials 1 and 3 and GPT trial 1 use CSV parsing without resolving the quantifier case. Gemini trial 2 correctly traces the parser and adopts a quoting/escaping workaround, but its generic CSV escape rule consumes existing regex backslashes and changes matching semantics. Configuration deletion is a secondary execution defect.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/pylint-dev__pylint-8898_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/pylint-dev__pylint-8898_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/pylint-dev__pylint-8898_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/pylint-dev__pylint-8898_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/pylint-dev__pylint-8898_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P1 Misinterpretation / Domain Knowledge Lack | Treats parentheses or square brackets as shielding commas in the configuration list, changing existing list-splitting behavior beyond the intended quantifier-comma handling. | [Patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/1pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| Claude-3 | P1 Misinterpretation / Domain Knowledge Lack | Treats parentheses or square brackets as shielding commas in the configuration list, changing existing list-splitting behavior beyond the intended quantifier-comma handling. | [Patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-8898/3pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| Gemini-1 | P1 Misinterpretation / Domain Knowledge Lack | Uses CSV parsing for regex configuration entries; raw commas in quantifiers are still interpreted as list separators. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-8898/1pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| Gemini-2 | V3 Regression of Existing Behavior | The CSV escaping workaround supports comma-bearing patterns, but replacing shared _splitstrip consumes existing regex backslashes: \d+ becomes d+ and no longer matches digits. This confirmed regression in previously valid patterns takes precedence over co-occurring parser and execution defects. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-8898/2pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| Gemini-3 | P1 Misinterpretation / Domain Knowledge Lack | Uses CSV parsing for regex configuration entries; raw commas in quantifiers are still interpreted as list separators. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-8898/3pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| GPT-1 | P1 Misinterpretation / Domain Knowledge Lack | Uses CSV parsing for regex configuration entries; raw commas in quantifiers are still interpreted as list separators. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-8898/1pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| GPT-2 | P1 Misinterpretation / Domain Knowledge Lack | Treats parentheses or square brackets as shielding commas in the configuration list, changing existing list-splitting behavior beyond the intended quantifier-comma handling. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-8898/2pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |
| GPT-3 | P1 Misinterpretation / Domain Knowledge Lack | Treats parentheses or square brackets as shielding commas in the configuration list, changing existing list-splitting behavior beyond the intended quantifier-comma handling. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-8898/3pylint-dev__pylint-8898_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) |

**Interpretation note:** The issue explicitly permits escaping, so disagreement with the raw-quantifier test alone does not establish P1. Gemini trial 2 is V3 because its supported comma-escaping workaround also changes an existing digit pattern from \d+ to d+, a directly reproducible regression.

<a id="task-pylint-dev__pylint-4661"></a>

### pylint-dev__pylint-4661 (9 failed trials)

**Task summary:** Pylint stores persistent statistics in a legacy home-directory location instead of a platform-appropriate cache directory.

**Current task analysis:** Claude trials 1 and 3, Gemini trials 1 and 3, and all GPT trials select a data-directory location. Claude trial 2 and Gemini trial 2 choose a cache directory but implement a narrower manual path rule. The reference change uses appdirs to obtain the platform cache location, and the benchmark tests compare against appdirs.user_cache_dir.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/pylint-dev__pylint-4661_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/pylint-dev__pylint-4661_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/pylint-dev__pylint-4661_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/pylint-dev__pylint-4661_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/pylint-dev__pylint-4661_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/1pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| Claude-2 | S3 Hardcoding / Bad Practices | Manually chooses an XDG cache path but does not implement the platform-aware cache-directory behavior supplied by appdirs. | [Patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/2pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| Claude-3 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/claude-sonnet-4-5-20250929/pylint-dev__pylint-4661/3pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| Gemini-1 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-4661/1pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| Gemini-2 | S3 Hardcoding / Bad Practices | Manually chooses an XDG cache path but does not implement the platform-aware cache-directory behavior supplied by appdirs. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-4661/2pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| Gemini-3 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/gemini-3-pro-preview/pylint-dev__pylint-4661/3pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| GPT-1 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-4661/1pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| GPT-2 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-4661/2pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |
| GPT-3 | S3 Hardcoding / Bad Practices | Manually selects an XDG data directory, whereas the benchmark requires the platform-specific application cache directory. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/pylint-dev__pylint-4661/3pylint-dev__pylint-4661_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) |

**Interpretation note:** The diagnostic distinction is required path and platform behavior, rather than merely the choice to use a dependency.

<a id="task-scikit-learn__scikit-learn-13135"></a>

### scikit-learn__scikit-learn-13135 (1 failed trials)

**Task summary:** KBinsDiscretizer with the kmeans strategy can construct nonmonotonic bin edges from unsorted cluster centers.

**Current task analysis:** GPT trial 2 sorts the resulting bin edges rather than sorting the centers before calculating boundaries, leaving an incorrect discretization strategy. The notes link this direction to an earlier edit command that did not apply as intended. Passing trials sort the centers; some also retain an unnecessary later edge sort.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-2 | I1 Tool Failure / Silent State Hallucination | The trajectory proposes sorting cluster centers, but the initial edit does not take effect; the final patch sorts bin edges instead and leaves the discretization logic incorrect. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-13135/2scikit-learn__scikit-learn-13135_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135.traj.json) |

**Interpretation note:** The ineffective initial edit and the incorrect final discretization logic are distinct parts of the recorded failure.

<a id="task-scikit-learn__scikit-learn-15100"></a>

### scikit-learn__scikit-learn-15100 (1 failed trials)

**Task summary:** strip_accents_unicode leaves combining accents in strings that are already normalized into decomposed form.

**Current task analysis:** Claude trial 3 has repeated action-format and editing problems. The notes describe an edit-and-cleanup sequence that removes unrelated vectorizer implementation while the agent checks only the intended accent fix. The other eight trials pass with accent removal that also handles already-normalized strings.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-3 | I1 Tool Failure / Silent State Hallucination | Rejected or ineffective editing actions are followed by state confusion and a destructive replacement that removes unrelated VectorizerMixin implementation. | [Patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-15100/3scikit-learn__scikit-learn-15100_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100.traj.json) |

<a id="task-scikit-learn__scikit-learn-26194"></a>

### scikit-learn__scikit-learn-26194 (9 failed trials)

**Task summary:** The first ROC threshold uses a finite sentinel that can be confusing for probability-valued prediction scores.

**Current task analysis:** All nine failed trials calculate or clip to a finite initial threshold. The accepted behavior represents the no-positive-predictions point with positive infinity, and the benchmark tests explicitly require that sentinel. The issue includes a tentative clipping suggestion that differs from the accepted change.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/1scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| Claude-2 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/2scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| Claude-3 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/claude-sonnet-4-5-20250929/scikit-learn__scikit-learn-26194/3scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| Gemini-1 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gemini-3-pro-preview/scikit-learn__scikit-learn-26194/1scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| Gemini-2 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gemini-3-pro-preview/scikit-learn__scikit-learn-26194/2scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| Gemini-3 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gemini-3-pro-preview/scikit-learn__scikit-learn-26194/3scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| GPT-1 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-26194/1scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| GPT-2 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-26194/2scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |
| GPT-3 | P2 Distracted by Hints / TODOs | Follows the suggested finite-threshold workaround rather than using positive infinity for the no-positive-predictions endpoint required by the ROC contract. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/scikit-learn__scikit-learn-26194/3scikit-learn__scikit-learn-26194_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) |

**Interpretation note:** A threshold above the largest score is not intrinsically invalid. The relevant failure is disagreement with the specified infinity-sentinel behavior, not that finite thresholds necessarily produce an incorrect ROC point.

<a id="task-sphinx-doc__sphinx-10323"></a>

### sphinx-doc__sphinx-10323 (1 failed trials)

**Task summary:** literalinclude applies dedentation after prepend and append, removing indentation intentionally supplied by those options.

**Current task analysis:** GPT trial 2 moves dedent before prepend/append but also infers indentation from the included body. Even with no dedent option, a body line starting with four spaces makes the patch add those spaces to previously verbatim prepend/append strings. This confirmed regression is assigned V3 under the preference over a co-occurring strategy error. The other eight trials pass.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-2 | V3 Regression of Existing Behavior | Moves dedent before prepend/append but additionally infers indentation from included lines. Even when dedent is absent, previously verbatim prepend/append strings acquire extra indentation. This separate existing-behavior regression takes precedence over the co-occurring target-combination error. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-10323/2sphinx-doc__sphinx-10323_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323.traj.json) |

**Interpretation note:** The new target-combination test also exposes the extra indentation. Its membership in FAIL_TO_PASS does not erase the independently demonstrated regression in the pre-existing no-dedent scenario.

<a id="task-sphinx-doc__sphinx-9591"></a>

### sphinx-doc__sphinx-9591 (1 failed trials)

**Task summary:** A property return annotation is displayed as plain text instead of being parsed into a reference.

**Current task analysis:** GPT trial 3 reformats the annotation upstream but does not change the downstream branch that emits it as plain text. Without invoking the annotation parser in that branch, the required link is still absent. The other eight trials pass.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-3 | S2 Incorrect Repair Strategy | Formats the property annotation at the data-production layer while the downstream attribute path still emits it as plain text rather than parsing cross-references. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-9591/3sphinx-doc__sphinx-9591_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591.traj.json) |

<a id="task-sphinx-doc__sphinx-8056"></a>

### sphinx-doc__sphinx-8056 (5 failed trials)

**Task summary:** Napoleon does not correctly handle NumPy-style documentation that gives several parameter names on one declaration line.

**Current task analysis:** Claude trial 1 splits names without respecting napoleon_use_param=False; trial 2 splits type fields without the corresponding parameter fields. GPT trial 1 changes the list-style output and removes class markup, trial 2 falls back to list formatting despite napoleon_use_param=True, and trial 3 groups parameter declarations separately from type declarations. The passing Claude and Gemini alternatives split names at an output stage while matching the tested format.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V2 Strict Output Format Mismatch | Splits parameter names during final formatting without restricting the change to napoleon_use_param=True, changing the list-format behavior under the disabled setting. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/1sphinx-doc__sphinx-8056_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) |
| Claude-2 | V2 Strict Output Format Mismatch | Splits type fields but does not split the corresponding parameter fields, leaving the generated field structure inconsistent. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8056/2sphinx-doc__sphinx-8056_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) |
| GPT-1 | V2 Strict Output Format Mismatch | Removes class-role markup from list-format output under napoleon_use_param=False, changing an existing output contract beyond the requested name splitting. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-8056/1sphinx-doc__sphinx-8056_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) |
| GPT-2 | V2 Strict Output Format Mismatch | Falls back to list formatting for multiple names even when napoleon_use_param=True requires parameter fields. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-8056/2sphinx-doc__sphinx-8056_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) |
| GPT-3 | V2 Strict Output Format Mismatch | Emits all parameter descriptions before all type fields rather than interleaving each parameter with its type as expected by the tests. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-8056/3sphinx-doc__sphinx-8056_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) |

**Interpretation note:** The checked field ordering and configuration-dependent output are part of the benchmark contract; similar rendered text alone does not establish equivalence.

<a id="task-sphinx-doc__sphinx-8548"></a>

### sphinx-doc__sphinx-8548 (7 failed trials)

**Task summary:** The inherited-members option omits inherited instance attributes and their documentation.

**Current task analysis:** The failed trials focus on retrieving or rendering documentation without completing member discovery. Gemini does not update importer.py to include the inherited instance attributes, while Claude trials 2 and 3 and GPT trials 2 and 3 likewise omit the discovery prerequisite. An attribute assigned in a base-class initializer cannot be discovered solely through dir() on the derived class.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-2 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/2sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| Claude-3 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-8548/3sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-8548/1sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-8548/2sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-8548/3sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-8548/2sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Changes inherited-member documentation lookup but omits discovering inherited instance attributes before documentation is generated. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-8548/3sphinx-doc__sphinx-8548_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) |

<a id="task-sphinx-doc__sphinx-11510"></a>

### sphinx-doc__sphinx-11510 (9 failed trials)

**Task summary:** Including a reStructuredText file bypasses the source-read event used by extensions to transform source content.

**Current task analysis:** Claude trials 1 and 3 and all Gemini and GPT trials enable source-read processing for parsed includes but also apply the event to literal include content. The baseline includes literal text verbatim, and a transforming handler now changes that existing behavior. These eight trials are V3 under the confirmed-regression preference; event-identity and other integration defects may coexist. Claude trial 2 delegates literal/code modes and passes its archived local and existing tests; its original S2 assignment is retained pending further verification because the retained official evaluation evidence does not identify the primary defect.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/1sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| Claude-2 | S2 Incorrect Repair Strategy | Original S2 assignment retained pending further verification. The patch reimplements parsed includes while delegating literal/code modes and supplying the included document name. Archived local and existing tests pass; the retained official evaluation evidence does not identify the primary defect, and reimplementation breadth alone is insufficient. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/2sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| Claude-3 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-11510/3sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| Gemini-1 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-11510/1sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| Gemini-2 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-11510/2sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| Gemini-3 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-11510/3sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| GPT-1 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-11510/1sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| GPT-2 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-11510/2sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |
| GPT-3 | V3 Regression of Existing Behavior | Enables source-read processing for parsed include content but also applies it to literal includes, whose baseline content bypasses the event and remains verbatim. A transforming handler therefore changes previously valid literal content. This confirmed regression takes precedence over co-occurring strategy or event-identity defects. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-11510/3sphinx-doc__sphinx-11510_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) |

**Interpretation note:** Literal transformations are visible in several saved executions. The diagnostic script additionally reconstructs all eight final Include implementations from archived source and patches and checks literal event reachability using dependency stubs. It does not run the full historical Sphinx suite. A broad rewrite alone does not establish a failure category.

<a id="task-sphinx-doc__sphinx-7748"></a>

### sphinx-doc__sphinx-7748 (9 failed trials)

**Task summary:** Autodoc recognizes only the first of several leading signatures in a function docstring.

**Current task analysis:** The failed patches add support for reading several signatures but leave multiline signature normalization incomplete. Continuation backslashes remain in output checked by the tests, including the return-annotation handling in Gemini trial 1. All nine trials are labeled as failures.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/1sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| Claude-2 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/2sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| Claude-3 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sphinx-doc__sphinx-7748/3sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| Gemini-1 | V2 Strict Output Format Mismatch | Collects consecutive overload signatures but retains the continuation backslash in the first return annotation, conflicting with the clean overload signature expected by the added tests. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-7748/1sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| Gemini-2 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-7748/2sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| Gemini-3 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/gemini-3-pro-preview/sphinx-doc__sphinx-7748/3sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| GPT-1 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-7748/1sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| GPT-2 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-7748/2sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |
| GPT-3 | V2 Strict Output Format Mismatch | Collects multiple signatures but does not fully normalize the continuation syntax expected by the overload-signature tests. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sphinx-doc__sphinx-7748/3sphinx-doc__sphinx-7748_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) |

<a id="task-sympy__sympy-15345"></a>

### sympy__sympy-15345 (1 failed trials)

**Task summary:** The Mathematica printer emits Python-style syntax for Max and Min expressions.

**Current task analysis:** GPT trial 2 produces Max/Min syntax but also replaces the StrPrinter.doprint entry point with the inherited CodePrinter implementation. The archived recursive list formatter calls self.doprint again; the inner call deletes state still owned by the outer call. An isolated execution of those archived methods reproduces AttributeError for a nonempty list. This existing-behavior regression is assigned V3. The other eight trials pass.

**Shared materials:** [Issue](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/sympy__sympy-15345_problem_statement.txt) · [Hints](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/sympy__sympy-15345_hints.txt) · [Reference patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/sympy__sympy-15345_gold.patch) · [Evaluation tests](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/sympy__sympy-15345_test.patch) · [Benchmark test IDs](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/sympy__sympy-15345_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| GPT-2 | V3 Regression of Existing Behavior | Supports Max/Min syntax but removes the StrPrinter.doprint delegation. The inherited CodePrinter entry point owns and deletes state also used by recursive self.doprint calls. An isolated check of the archived methods shows that printing a nonempty list raises AttributeError after the inner call deletes the outer state, a regression beyond the local Max/Min repair. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-15345/2sympy__sympy-15345_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-15345/sympy__sympy-15345.traj.json) |

**Interpretation note:** The printer check uses the archived method bodies with dispatch stubs; it is not a historical full-suite execution. The diagnostic script documents this scope explicitly.

<a id="task-sympy__sympy-18211"></a>

### sympy__sympy-18211 (5 failed trials)

**Task summary:** Converting a relational expression that cannot be solved explicitly into a set raises an error instead of returning a symbolic set.

**Current task analysis:** The failed trials use different symbolic-set fallback strategies. Gemini trials 1 and 2 and GPT trial 1 retain their S1 assignments for limited relational coverage. Claude trial 3 adds an Equality-specific solveset fallback: the first official target assertion passes, but the second returns a ConditionSet over a transformed equation that admits an extraneous positive solution, so this trial is S2. Gemini trial 3 changes the lower-level solver's exception contract; archived original tests report DID NOT RAISE, supporting V3.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/sympy__sympy-18211_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/sympy__sympy-18211_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/sympy__sympy-18211_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/sympy__sympy-18211_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/sympy__sympy-18211_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-3 | S2 Incorrect Repair Strategy | Adds an Equality-specific fallback through solveset. The first benchmark equation returns the expected ConditionSet, but the second returns a ConditionSet over a squared, transformed equation rather than the original condition. The transformed condition admits an extraneous positive solution, leaving the target symbolic-set behavior incorrect. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-18211/3sympy__sympy-18211_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-18211/sympy__sympy-18211.traj.json) |
| Gemini-1 | S1 Partial Fix / Incomplete Logic | Adds a fallback for equalities but leaves unsupported inequalities on the previous exception-raising path, so Relational.as_set support remains incomplete. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-18211/1sympy__sympy-18211_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/sympy__sympy-18211/sympy__sympy-18211.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Adds a fallback for equalities but leaves unsupported inequalities on the previous exception-raising path, so Relational.as_set support remains incomplete. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-18211/2sympy__sympy-18211_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sympy__sympy-18211/sympy__sympy-18211.traj.json) |
| Gemini-3 | V3 Regression of Existing Behavior | Returns ConditionSet from the lower-level inequality solver to support the local as_set case, but changes the exception contract of existing solver callers. Archived original tests report DID NOT RAISE; editing those test expectations does not repair the production-code regression. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-18211/3sympy__sympy-18211_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sympy__sympy-18211/sympy__sympy-18211.traj.json) |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Adds a fallback for equalities but leaves unsupported inequalities on the previous exception-raising path, so Relational.as_set support remains incomplete. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-18211/1sympy__sympy-18211_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-18211/sympy__sympy-18211.traj.json) |

**Interpretation note:** Claude trial 3 does not modify the lower-level inequality solver. The two official equality assertions were checked against its archived method using the exact historical SymPy source. The diagnostic script provides this optional source-dependent check separately from its standard-library-only checks.

<a id="task-sympy__sympy-17630"></a>

### sympy__sympy-17630 (8 failed trials)

**Task summary:** Block-matrix operations reduce a ZeroMatrix to scalar zero, breaking later matrix operations.

**Current task analysis:** The eight failed trials modify block multiplication without correcting the matrix-addition behavior that still produces scalar zero. Gemini trial 1 is the only passing trial.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/sympy__sympy-17630_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/sympy__sympy-17630_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/sympy__sympy-17630_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/sympy__sympy-17630_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/sympy__sympy-17630_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/1sympy__sympy-17630_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| Claude-2 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/2sympy__sympy-17630_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| Claude-3 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-17630/3sympy__sympy-17630_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| Gemini-2 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-17630/2sympy__sympy-17630_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| Gemini-3 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-17630/3sympy__sympy-17630_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| GPT-1 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-17630/1sympy__sympy-17630_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| GPT-2 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-17630/2sympy__sympy-17630_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) |
| GPT-3 | S1 Partial Fix / Incomplete Logic | Patches block-matrix multiplication without handling the related matrix-addition behavior, leaving ZeroMatrix expressions reducible to scalar zero. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-17630/3sympy__sympy-17630_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) |

<a id="task-sympy__sympy-12489"></a>

### sympy__sympy-12489 (9 failed trials)

**Task summary:** Permutation methods construct base-class instances instead of preserving a subclass.

**Current task analysis:** All nine failed trials update selected _af_new paths but leave other constructors or hard-coded base-class references unchanged. The tests substitute a subclass and expose the remaining construction paths that do not preserve it.

**Shared materials:** [Issue](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/sympy__sympy-12489_problem_statement.txt) · [Hints](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/sympy__sympy-12489_hints.txt) · [Reference patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/sympy__sympy-12489_gold.patch) · [Evaluation tests](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/sympy__sympy-12489_test.patch) · [Benchmark test IDs](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/sympy__sympy-12489_test_ids.json)

| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |
| --- | --- | --- | --- | --- |
| Claude-1 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/1sympy__sympy-12489_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| Claude-2 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/2sympy__sympy-12489_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| Claude-3 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/claude-sonnet-4-5-20250929/sympy__sympy-12489/3sympy__sympy-12489_model.patch) | [Log](../../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| Gemini-1 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-12489/1sympy__sympy-12489_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| Gemini-2 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-12489/2sympy__sympy-12489_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| Gemini-3 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gemini-3-pro-preview/sympy__sympy-12489/3sympy__sympy-12489_model.patch) | [Log](../../data/traj/gemini-3-pro-preview/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| GPT-1 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-12489/1sympy__sympy-12489_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| GPT-2 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-12489/2sympy__sympy-12489_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
| GPT-3 | P1 Misinterpretation / Domain Knowledge Lack | Replaces selected _af_new construction paths but leaves other hardcoded Permutation constructors, so operations do not consistently preserve subclass instances. | [Patch](../../analyse/gpt-5-2025-08-07-medium-reasoning/sympy__sympy-12489/3sympy__sympy-12489_model.patch) | [Log](../../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) |
