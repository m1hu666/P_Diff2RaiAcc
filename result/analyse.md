# Failure Analysis and Trial-Level Catalogue

The evaluated dataset contains 900 trials: 100 tasks, three model groups, and three trials per task. The archived labels record 658 resolved trials and 242 unresolved trials (26.9%). The unresolved trials span 45 tasks. Every unresolved trial is listed individually in Appendix A with its model, trial number, and primary category.

The five stages and 11 subcategories follow the reconciled study taxonomy. The accompanying [catalogue CSV](Statistics%20results/full/failures/failure_trial_catalog.csv) includes a trial-specific diagnosis and a repository-relative index of available patches, issue descriptions, hints, trajectories, and verified outcome records. The [codebook](../FINAL-CODEBOOK/FAILURE_CODEBOOK.md) defines the category boundaries.

Artifact paths are provided for navigation and reproducibility. They identify the archived inputs used by the public catalogue without asserting that every linked artifact independently establishes the assigned cause.

## Scope and interpretation

Each unresolved trial retains one primary category. Secondary defects may coexist, but are not counted again. Assignments awaiting further verification remain in their existing categories, with evidence limitations stated in their diagnoses and case notes; retention does not mean that a recheck confirmed the attribution. An evaluation outcome and its qualitative explanation are separate: a failed label does not establish a cause, and a difference from the reference patch does not establish incorrectness. In particular, V1/V2 annotations identify a specification or representation distinction; they do not automatically establish that the patch is semantically correct or that the benchmark is invalid. V5 identifies a reconciled evaluation-infrastructure blocker; it remains a recorded unresolved outcome but does not describe a model repair defect.

The counts below are descriptive. The three trials on one task and the model results for that task are dependent. Category percentages do not constitute model-comparison significance tests, and the unresolved trials are not treated as independent statistical samples. Within-model percentages use that model's number of failures as the denominator. The CSV summaries additionally report category incidence among all evaluated attempts per model and the number of distinct tasks. Task coverage can overlap across categories, so distinct-task counts must not be added across rows. The annotations are study data; they do not constitute a new independent-coder agreement study.

## Recorded outcomes

| Model | Attempts | Unresolved trials | Failure rate | Tasks with a failure |
| --- | --- | --- | --- | --- |
| Claude | 300 | 70 | 23.3% | 31 |
| Gemini | 300 | 82 | 27.3% | 31 |
| GPT | 300 | 90 | 30.0% | 38 |

Model groups are Claude (`claude-sonnet-4-5-20250929`), Gemini (`gemini-3-pro-preview`), and GPT (`gpt-5-2025-08-07-medium-reasoning`). Trial numbers identify the archived rounds and do not imply paired random seeds across model providers.

## Distribution by broader stage

| Stage | Claude, n (%) | Gemini, n (%) | GPT, n (%) | Total, n (%) | Distinct tasks |
| --- | --- | --- | --- | --- | --- |
| Problem Understanding | 24 (34.3%) | 24 (29.3%) | 23 (25.6%) | 71 (29.3%) | 11 |
| Localization | 5 (7.1%) | 1 (1.2%) | 6 (6.7%) | 12 (5.0%) | 4 |
| Strategy & Logic | 18 (25.7%) | 26 (31.7%) | 24 (26.7%) | 68 (28.1%) | 16 |
| Implementation & Execution | 1 (1.4%) | 1 (1.2%) | 6 (6.7%) | 8 (3.3%) | 5 |
| Validation & Harness Constraints | 22 (31.4%) | 30 (36.6%) | 31 (34.4%) | 83 (34.3%) | 18 |

## Distribution by subcategory

| Code | Broader stage | Subcategory | Claude | Gemini | GPT | Total | Share of failures | Distinct tasks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Problem Understanding | Misinterpretation / Domain Knowledge Lack | 16 | 15 | 14 | 45 | 18.6% | 8 |
| P2 | Problem Understanding | Distracted by Hints / TODOs | 8 | 9 | 9 | 26 | 10.7% | 3 |
| L1 | Localization | Incomplete Scope / Wrong Layer | 5 | 1 | 6 | 12 | 5.0% | 4 |
| S1 | Strategy & Logic | Partial Fix / Incomplete Logic | 14 | 16 | 19 | 49 | 20.2% | 10 |
| S2 | Strategy & Logic | Incorrect Strategy | 4 | 10 | 5 | 19 | 7.9% | 7 |
| I1 | Implementation & Execution | Tool Failure / Silent State Hallucination | 1 | 1 | 6 | 8 | 3.3% | 5 |
| V1 | Validation & Harness Constraints | Specification-Oracle Gap | 1 | 7 | 2 | 10 | 4.1% | 3 |
| V2 | Validation & Harness Constraints | Strict Output Format Mismatch | 9 | 10 | 11 | 30 | 12.4% | 6 |
| V3 | Validation & Harness Constraints | Regression of Existing Behavior | 5 | 7 | 10 | 22 | 9.1% | 7 |
| V4 | Validation & Harness Constraints | Execution Timing Mismatch | 1 | 0 | 2 | 3 | 1.2% | 2 |
| V5 | Validation & Harness Constraints | Evaluation Infrastructure Failure | 6 | 6 | 6 | 18 | 7.4% | 2 |

The largest category is S1 (partial or incomplete logic). Its count describes the assigned repair failures in this dataset; it does not demonstrate a general reasoning limit or establish that localization is solved. The I1 category counts primary tool, execution, or saved patch-state failures, so it also does not measure every transient tool error recovered during otherwise successful or differently classified trajectories.

## Task-level outcome index

S denotes a recorded success and F a recorded failure. Within each model cell, the order is trial 1, trial 2, trial 3. A dash in the CSV category columns denotes a successful trial, which receives no failure category.

| Task | Claude | Gemini | GPT | Unresolved / 9 | Primary categories |
| --- | --- | --- | --- | --- | --- |
| [astropy__astropy-13398](#case-astropy__astropy-13398) | F F F | F F F | F F F | 9 | P1 |
| [astropy__astropy-14182](#case-astropy__astropy-14182) | F F S | F F F | F S F | 7 | S1 |
| [astropy__astropy-8872](#case-astropy__astropy-8872) | F F F | F F F | F F F | 9 | V5 |
| [django__django-10554](#case-django__django-10554) | F F F | F F F | F F F | 9 | P1, S2 |
| [django__django-11276](#case-django__django-11276) | S S S | F F F | S S S | 3 | S2 |
| [django__django-11532](#case-django__django-11532) | F F F | S S S | F F F | 6 | V3 |
| [django__django-11790](#case-django__django-11790) | F S S | F F F | F F F | 7 | V2, V4 |
| [django__django-12125](#case-django__django-12125) | S S S | S S F | S S S | 1 | S2 |
| [django__django-13023](#case-django__django-13023) | S F S | F S F | S F F | 5 | P1, V1 |
| [django__django-13343](#case-django__django-13343) | S F S | S S S | S S S | 1 | V4 |
| [django__django-13344](#case-django__django-13344) | F S F | S S F | F F F | 6 | L1 |
| [django__django-13401](#case-django__django-13401) | S S S | S S S | S F S | 1 | S2 |
| [django__django-13406](#case-django__django-13406) | S F S | F F F | F S S | 5 | I1, V1 |
| [django__django-14140](#case-django__django-14140) | F S F | F F F | S S F | 6 | V2 |
| [django__django-14155](#case-django__django-14155) | F F F | F F F | F F F | 9 | P2 |
| [django__django-14771](#case-django__django-14771) | S S S | S F S | F F F | 4 | V2 |
| [django__django-15022](#case-django__django-15022) | F S S | F F F | S S S | 4 | S2 |
| [django__django-15103](#case-django__django-15103) | F F S | S S S | S S S | 2 | L1 |
| [django__django-15629](#case-django__django-15629) | F F F | F F F | F F F | 9 | S1 |
| [django__django-15732](#case-django__django-15732) | F F F | F F F | F F F | 9 | S1 |
| [django__django-15741](#case-django__django-15741) | S S S | S S S | F F F | 3 | S1 |
| [django__django-16502](#case-django__django-16502) | F F F | F F F | F F F | 9 | P1 |
| [django__django-16560](#case-django__django-16560) | F S S | F F F | F F F | 7 | L1, I1, V1 |
| [matplotlib__matplotlib-20859](#case-matplotlib__matplotlib-20859) | S S S | S F S | S S S | 1 | P1 |
| [matplotlib__matplotlib-21568](#case-matplotlib__matplotlib-21568) | F F F | F F F | F F F | 9 | P1 |
| [matplotlib__matplotlib-24570](#case-matplotlib__matplotlib-24570) | S S S | S S S | F S S | 1 | S1 |
| [matplotlib__matplotlib-25311](#case-matplotlib__matplotlib-25311) | S S S | S S S | F F F | 3 | L1 |
| [matplotlib__matplotlib-26208](#case-matplotlib__matplotlib-26208) | F F F | F F F | F F F | 9 | P2, S1 |
| [matplotlib__matplotlib-26291](#case-matplotlib__matplotlib-26291) | S S S | S S S | F S S | 1 | S1 |
| [psf__requests-2931](#case-psf__requests-2931) | S S S | F S F | S F F | 4 | V3 |
| [pylint-dev__pylint-4661](#case-pylint-dev__pylint-4661) | F F F | F F F | F F F | 9 | V5 |
| [pylint-dev__pylint-8898](#case-pylint-dev__pylint-8898) | F S F | F F F | F F F | 8 | P1, I1, V3 |
| [scikit-learn__scikit-learn-13135](#case-scikit-learn__scikit-learn-13135) | S S S | S S S | S F S | 1 | I1 |
| [scikit-learn__scikit-learn-15100](#case-scikit-learn__scikit-learn-15100) | S S F | S S S | S S S | 1 | I1 |
| [scikit-learn__scikit-learn-26194](#case-scikit-learn__scikit-learn-26194) | F F F | F F F | F F F | 9 | P2 |
| [sphinx-doc__sphinx-10323](#case-sphinx-doc__sphinx-10323) | S S S | S S S | S F S | 1 | V3 |
| [sphinx-doc__sphinx-11510](#case-sphinx-doc__sphinx-11510) | F F F | F F F | F F F | 9 | V2, V3 |
| [sphinx-doc__sphinx-7748](#case-sphinx-doc__sphinx-7748) | F F F | F F F | F F F | 9 | V2 |
| [sphinx-doc__sphinx-8056](#case-sphinx-doc__sphinx-8056) | F F S | S S S | F F F | 5 | V2 |
| [sphinx-doc__sphinx-8548](#case-sphinx-doc__sphinx-8548) | S F F | F F F | S F F | 7 | S1 |
| [sphinx-doc__sphinx-9591](#case-sphinx-doc__sphinx-9591) | S S S | S S S | S S F | 1 | S2 |
| [sympy__sympy-12489](#case-sympy__sympy-12489) | F F F | F F F | F F F | 9 | P1 |
| [sympy__sympy-15345](#case-sympy__sympy-15345) | S S S | S S S | S F S | 1 | V3 |
| [sympy__sympy-17630](#case-sympy__sympy-17630) | F F F | S F F | F F F | 8 | S1 |
| [sympy__sympy-18211](#case-sympy__sympy-18211) | S S F | F F F | F S S | 5 | S1, S2, V3 |

## Case analyses

The following cases cover every task with an unresolved trial and summarize the task requirements, recorded outcomes, and assigned failure-mode attributions.

<a id="case-astropy__astropy-13398"></a>

### astropy__astropy-13398

**Issue.** Transforming nearby terrestrial objects from ITRS to observed coordinates through an inertial frame introduces inappropriate aberration effects.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials introduce a direct transformation path but omit atmospheric refraction handling. The geometric near-Earth case can improve while the refraction-dependent cases required by the tests remain unsupported.

**Primary assignments.** P1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-astropy__astropy-14182"></a>

### astropy__astropy-14182

**Issue.** The reStructuredText table writer does not accept additional header_rows such as units.

**Recorded outcomes.** Claude: F F S; Gemini: F F F; GPT: F S F.

**Analysis.** The seven failed trials implement header writing without adjusting where the reader starts table data. The two passing trials account for the number of header rows when setting the data start line, supporting the tested write/read behavior.

**Primary assignments.** S1: Claude-1, Claude-2, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-3.

<a id="case-astropy__astropy-8872"></a>

### astropy__astropy-8872

**Issue.** Quantity construction promotes a float16 input to float64 instead of preserving the floating-point dtype.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** The reconciled review assigns all nine recorded failures to V5. Test collection is blocked by an evaluation-dependency deprecation warning treated as an error, before the candidate float16 behavior can be assessed.

**Primary assignments.** V5: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** The candidate patches preserve the reported float16 input. The archived failed outcomes do not establish a regression in their boolean conversion behavior; the V5 assignment describes the evaluation blocker identified during coder discussion.

<a id="case-django__django-10554"></a>

### django__django-10554

**Issue.** Evaluating a derived union queryset can affect its source queryset and leave required ordering columns absent from generated SQL.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trial 1 mistakes an earlier partial repair for a complete fix and submits reproduction or test changes without a production repair. The other eight failed trials alter combined-query handling but leave the required ordering projection unresolved or remove ordering.

**Primary assignments.** P1: Claude-1; S2: Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** Claude trial 1 is assigned P1 for its mistaken interpretation of the remaining target work. The other failed trials retain S2 for their submitted strategies.

<a id="case-django__django-11276"></a>

### django__django-11276

**Issue.** Django intends to replace its custom HTML escaping implementation with the standard-library implementation.

**Recorded outcomes.** Claude: S S S; Gemini: F F F; GPT: S S S.

**Analysis.** All three Gemini trials call html.escape but then convert the apostrophe entity back from &#x27; to &#39;. This preserves the former output spelling and fails the exact output expected after the accepted refactoring. Claude and GPT pass.

**Primary assignments.** S2: Gemini-1, Gemini-2, Gemini-3.

**Interpretation.** Both apostrophe entities denote the same HTML character. The recorded mismatch concerns the exact output contract; its performance effect was not measured.

<a id="case-django__django-11532"></a>

### django__django-11532

**Issue.** A non-ASCII hostname can cause email Message-ID generation to fail under a legacy email encoding.

**Recorded outcomes.** Claude: F F F; Gemini: S S S; GPT: F F F.

**Analysis.** Claude trial 2 adds a second hostname cache that survives the established _fqdn reset, leaving a stale hostname. GPT trial 2 reads an unassigned local fqdn on a cache hit. These directly reproduced cache-lifecycle regressions are V3. For Claude trials 1 and 3 and GPT trials 1 and 3, the discussion retained V3 following coders B and C: local Message-ID conversion leaves Unicode hostname state in the shared cache, which coder C identified as affecting later sending.

**Primary assignments.** V3: Claude-1, Claude-2, Claude-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** The retained per-test archive does not independently confirm the later-send explanation for Claude/GPT trials 1 and 3. Their V3 labels and the SUPPORTED chronological-link judgment for GPT trial 1 are reconciled reviewer judgments; they do not assert a new independent reproduction of that explanation.

<a id="case-django__django-11790"></a>

### django__django-11790

**Issue.** AuthenticationForm no longer sets the username widget maxlength as expected.

**Recorded outcomes.** Claude: F S S; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trial 1, all Gemini trials, and GPT trial 2 store a string-valued maxlength where the tests expect an integer. GPT trials 1 and 3 defer the adjustment until rendering, whereas the tests inspect the earlier form state. The remaining Claude trials pass.

**Primary assignments.** V2: Claude-1, Gemini-1, Gemini-2, Gemini-3, GPT-2; V4: GPT-1, GPT-3.

**Interpretation.** A matching HTML rendering can coexist with a different internal attribute type or initialization time. These are separate contracts.

<a id="case-django__django-12125"></a>

### django__django-12125

**Issue.** Migration serialization uses an unqualified class name for nested classes, generating an invalid import path.

**Recorded outcomes.** Claude: S S S; Gemini: S S F; GPT: S S S.

**Analysis.** Gemini trial 3 adds module-search logic around the existing path instead of using the nested class qualified name at serialization. The other eight trials use the relevant qualified-name information and pass.

**Primary assignments.** S2: Gemini-3.

<a id="case-django__django-13023"></a>

### django__django-13023

**Issue.** DecimalField lets exceptions from invalid nonnumeric inputs escape instead of converting them consistently to ValidationError.

**Recorded outcomes.** Claude: S F S; Gemini: F S F; GPT: S F F.

**Analysis.** Claude trial 2 interprets the model-save defect as a forms-field problem and changes the wrong DecimalField. Gemini trials 1 and 3 and GPT trials 2 and 3 change the model DecimalField but omit the ValueError case required by the additional tests.

**Primary assignments.** P1: Claude-2; V1: Gemini-1, Gemini-3, GPT-2, GPT-3.

**Interpretation.** Claude trial 2 is P1 because its repair follows an incorrect interpretation of the target component. The other four retain V1 for the additional tested exception case.

<a id="case-django__django-13343"></a>

### django__django-13343

**Issue.** FileField deconstruction serializes an evaluated storage instance instead of retaining the supplied storage callable.

**Recorded outcomes.** Claude: S F S; Gemini: S S S; GPT: S S S.

**Analysis.** Claude trial 2 changes storage into a property and fails the evaluated initialization and deconstruction behavior. The passing trials retain access to the original callable while preserving the expected storage interface.

**Primary assignments.** V4: Claude-2.

<a id="case-django__django-13344"></a>

### django__django-13344

**Issue.** An asynchronous middleware chain can return an unawaited coroutine where an HTTP response is expected.

**Recorded outcomes.** Claude: F S F; Gemini: S S F; GPT: F F F.

**Analysis.** The failed trials attempt to infer asynchronous behavior in the lower-level exception handler from wrapped callbacks. This treats downstream symptoms without correcting the middleware initialization or capability information at the appropriate layer. Claude trial 2 and Gemini trials 1 and 2 pass.

**Primary assignments.** L1: Claude-1, Claude-3, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-django__django-13401"></a>

### django__django-13401

**Issue.** Field copies inherited from abstract models share a creation counter and can be incorrectly treated as equal across models.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: S F S.

**Analysis.** GPT trial 2 uses object identity as an ordering tie-breaker. That ordering differs from the deterministic model-based ordering expected by the tests. The other eight trials preserve the required equality and ordering behavior.

**Primary assignments.** S2: GPT-2.

**Interpretation.** Object identity distinguishes objects but does not implement a stable model-name ordering.

<a id="case-django__django-13406"></a>

### django__django-13406

**Issue.** Reassigning a pickled query to a queryset does not restore the iterable behavior needed for values-based query results.

**Recorded outcomes.** Claude: S F S; Gemini: F F F; GPT: F S S.

**Analysis.** Claude trial 2 and all three Gemini trials preserve the original values_list result structure, while the benchmark expects dictionary-like values results when only the query is restored. GPT trial 1 has a separate implementation-state failure: a compound edit partially applies before its final awk stage fails, and an uninspected residual assignment inside QuerySet.values_list makes query.py syntactically invalid.

**Primary assignments.** I1: GPT-1; V1: Claude-2, Gemini-1, Gemini-2, Gemini-3.

**Interpretation.** The four result-contract failures are V1 cases. GPT trial 1 is an I1 case because the failed compound edit leaves an unrecovered syntax error before the query-restoration behavior can be exercised.

<a id="case-django__django-14140"></a>

### django__django-14140

**Issue.** Q.deconstruct assumes a single child is a key/value tuple and fails for expression children such as Exists.

**Recorded outcomes.** Claude: F S F; Gemini: F F F; GPT: S S F.

**Analysis.** Claude trials 1 and 3, all Gemini trials, and GPT trial 3 guard the tuple-specific branch while preserving the older keyword-argument representation. These patches avoid the reported indexing error but do not produce the positional-argument deconstruction format checked by the benchmark tests.

**Primary assignments.** V2: Claude-1, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-3.

**Interpretation.** Avoiding the indexing crash does not by itself satisfy the required serialization contract.

<a id="case-django__django-14155"></a>

### django__django-14155

**Issue.** A resolver representation does not display useful details when its view is a functools.partial object.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials unwrap partial objects and lose information about their bound arguments. The reference implementation instead uses the partial object representation for this case, preserving the underlying callable and supplied arguments.

**Primary assignments.** P2: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-django__django-14771"></a>

### django__django-14771

**Issue.** The development-server autoreloader does not propagate interpreter -X options to the child process.

**Recorded outcomes.** Claude: S S S; Gemini: S F S; GPT: F F F.

**Analysis.** Gemini trial 2 and the three GPT trials emit separate argument tokens such as ["-X", "utf8"], while the tests expect the combined form ["-Xutf8"]. The remaining trials match the tested subprocess argument structure.

**Primary assignments.** V2: Gemini-2, GPT-1, GPT-2, GPT-3.

**Interpretation.** Alternative command-line spellings can be accepted by the interpreter. The failure here is the exact argument-vector contract checked by the benchmark, rather than proof that the alternative never works.

<a id="case-django__django-15022"></a>

### django__django-15022

**Issue.** Admin searches containing several terms can create unnecessary joins over related fields.

**Recorded outcomes.** Claude: F S S; Gemini: F F F; GPT: S S S.

**Analysis.** Claude trial 1 and Gemini trial 2 retain sequential filters precisely when joins are possible, leaving the expensive case unchanged. Gemini trial 1 uses subqueries without eliminating the repeated joins; Gemini trial 3 uses an existence-based strategy that does not satisfy the tested behavior. The notes also describe a candidate combined-filter strategy being reconsidered after a repository test whose expected result is updated by the benchmark test patch.

**Primary assignments.** S2: Claude-1, Gemini-1, Gemini-2, Gemini-3.

**Interpretation.** A repository test whose expected result changes with the accepted fix can influence the repair direction when the agent runs the original test unchanged.

<a id="case-django__django-15103"></a>

### django__django-15103

**Issue.** json_script requires an element identifier even when the caller does not need one.

**Recorded outcomes.** Claude: F F S; Gemini: S S S; GPT: S S S.

**Analysis.** Claude trials 1 and 2 make the low-level utility argument optional but omit the corresponding template-filter entry point. Their reproduction focuses on direct Python calls. The remaining trials cover the relevant interface change and pass.

**Primary assignments.** L1: Claude-1, Claude-2.

<a id="case-django__django-15629"></a>

### django__django-15629

**Issue.** Foreign keys do not consistently inherit the collation of their referenced primary-key field.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials update the foreign-key definition used during table creation but omit schema alteration logic that must synchronize existing foreign keys when the primary-key collation changes. Creation tests can pass while alteration tests fail.

**Primary assignments.** S1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-django__django-15732"></a>

### django__django-15732

**Issue.** Dropping a single-field unique_together constraint is ambiguous when another uniqueness constraint exists on that field.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials exclude a primary-key constraint but do not handle the distinct unique=True constraint case. Multiple non-primary unique constraints remain candidates, so the operation still fails the second evaluated scenario.

**Primary assignments.** S1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-django__django-15741"></a>

### django__django-15741

**Issue.** get_format does not accept a lazy string argument, affecting consumers such as the date template filter.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: F F F.

**Analysis.** Claude and Gemini convert the argument to a string and pass, using force_str and str respectively. All three GPT trials return without performing the required conversion, leaving downstream consumers with the unsupported lazy argument.

**Primary assignments.** S1: GPT-1, GPT-2, GPT-3.

<a id="case-django__django-16502"></a>

### django__django-16502

**Issue.** The development server does not consistently suppress a response body for HEAD requests.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials remove the body but fail the benchmark checks on response-header handling, including the expected absence of Content-Length in the tested case.

**Primary assignments.** P1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** The absence of Content-Length is a case-specific benchmark expectation and does not imply that HTTP forbids a Content-Length header in every HEAD response.

<a id="case-django__django-16560"></a>

### django__django-16560

**Issue.** Model constraints cannot consistently expose a configurable validation error code.

**Recorded outcomes.** Claude: F S S; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trial 1 updates core constraint classes but omits the PostgreSQL ExclusionConstraint subclass (L1). Gemini trial 1 and GPT trials 2 and 3 retain unintended edits that break representation or construction (I1). Gemini trials 2 and 3 implement the general error-code request but miss an additional legacy unique_together requirement (V1). GPT trial 1 is I1 because its verified patch changes an unchanged source-context line to mojibake, unlike the trajectory's final submission.

**Primary assignments.** L1: Claude-1; I1: Gemini-1, GPT-1, GPT-2, GPT-3; V1: Gemini-2, Gemini-3.

**Interpretation.** The GPT trial 1 I1 attribution concerns a concrete saved patch-state mismatch; it does not show that the model intended the corrupted context line. Other trials distinguish incomplete subclass coverage, retained editing defects, and an additional compatibility assertion.

<a id="case-matplotlib__matplotlib-20859"></a>

### matplotlib__matplotlib-20859

**Issue.** Legend rejects SubFigure as a valid parent even though a SubFigure can host its own legend.

**Recorded outcomes.** Claude: S S S; Gemini: S F S; GPT: S S S.

**Analysis.** Gemini trial 2 treats SubFigure like an Axes-style container and redirects ownership to the outer figure. This fails to preserve the SubFigure as the legend host. The other eight trials pass.

**Primary assignments.** P1: Gemini-2.

<a id="case-matplotlib__matplotlib-21568"></a>

### matplotlib__matplotlib-21568

**Issue.** Date-axis labels have unclear spacing when usetex is enabled.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trials 1, 2, and 3 group colons but omit explicit space handling. Gemini trials 1 and 2 escape spaces but leave colons unchanged; Gemini trial 3 moves spaces outside math spans. GPT trials 1 and 3 return unwrapped text, while GPT trial 2 uses mbox text rendering. These different interpretations do not implement the combined colon-and-separator behavior required by the tested date-label output. All nine P1 assignments are retained.

**Primary assignments.** P1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** The diagnoses distinguish the actual saved edits; they do not describe Gemini space escaping or GPT text rendering as unchanged spaces inside math mode.

<a id="case-matplotlib__matplotlib-24570"></a>

### matplotlib__matplotlib-24570

**Issue.** HPacker reverses top and bottom alignment.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: F S S.

**Analysis.** GPT trial 1 inspects the shared alignment helper and both packers, then deliberately remaps top/bottom only in HPacker. This leaves VPacker top/bottom behavior unfixed and is the earliest unrecovered logical omission (S1). A later extension of the remapping to left/right also reverses HPacker placement, a secondary strategy defect.

**Primary assignments.** S1: GPT-1.

**Interpretation.** The observed differences are numeric layout behavior, not merely output formatting. Under the manuscript single-primary rule, the earlier incomplete fix is counted once as S1; the later S2 manifestation is not counted again.

<a id="case-matplotlib__matplotlib-25311"></a>

### matplotlib__matplotlib-25311

**Issue.** A figure containing a draggable legend cannot be pickled because the stored canvas includes objects that cannot be serialized.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: F F F.

**Analysis.** Claude and Gemini trace the inheritance hierarchy to the shared draggable implementation and add serialization handling. The three GPT trials avoid the immediate serialization error but do not preserve draggable behavior after loading and cover only selected subclasses.

**Primary assignments.** L1: GPT-1, GPT-2, GPT-3.

**Interpretation.** The assessed requirement includes behavior after deserialization, rather than merely successful pickle creation.

<a id="case-matplotlib__matplotlib-26208"></a>

### matplotlib__matplotlib-26208

**Issue.** Creating a twinned axis can corrupt the data limits of an existing plot with categorical units.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** Eight failed trials retain P2 after coder reconciliation. Claude trial 2 instead preserves the reported data limits around relim but does not set the original axis units on the new twin axes, leaving required behavior incomplete (S1).

**Primary assignments.** P2: Claude-1, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3; S1: Claude-2.

**Interpretation.** The task-level assignments reflect the final coder discussion. The saved Claude trial 2 trajectory links its change to the unit-change callback rather than demonstrating that a nearby TODO determined the repair.

<a id="case-matplotlib__matplotlib-26291"></a>

### matplotlib__matplotlib-26291

**Issue.** An inset axes operation fails during tight-bounding-box computation when the renderer is not available through the expected path.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: F S S.

**Analysis.** GPT trial 1 changes the figure state but does not supply the required renderer to the downstream operation. The other eight trials complete the renderer-handling repair and pass.

**Primary assignments.** S1: GPT-1.

<a id="case-psf__requests-2931"></a>

### psf__requests-2931

**Issue.** Requests coerces byte request bodies to strings instead of sending the original bytes.

**Recorded outcomes.** Claude: S S S; Gemini: F S F; GPT: S F F.

**Analysis.** Gemini trials 1 and 3 and GPT trials 2 and 3 establish the requested binary-body behavior but return bytes from the shared encoder on the existing URL-parameter path, breaking previously supported byte-valued URL construction. GPT trial 1 passes with a decode-or-return fallback that separates the evaluated body and URL inputs.

**Primary assignments.** V3: Gemini-1, Gemini-3, GPT-2, GPT-3.

<a id="case-pylint-dev__pylint-4661"></a>

### pylint-dev__pylint-4661

**Issue.** Pylint stores persistent statistics in a legacy home-directory location rather than a location selected under the XDG Base Directory specification.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials are assigned V5. The added evaluation test imports appdirs unconditionally, but appdirs is unavailable in the sb-cli evaluation environment for submissions that resolve the path without that package. Test collection therefore terminates before test_pylint_home can exercise candidate behavior.

**Primary assignments.** V5: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** The reference patch declares appdirs in setup.cfg, whereas the candidate implementations do not require that package. Their data-versus-cache policy and abstraction choices differ from the reference, but the recorded evaluation never reaches those differences; V5 records the collection-stage dependency blocker rather than treating manual XDG path handling as the demonstrated cause of failure.

<a id="case-pylint-dev__pylint-8898"></a>

### pylint-dev__pylint-8898

**Issue.** Comma-separated regular-expression options are split inside repetition quantifiers such as {1,3}.

**Recorded outcomes.** Claude: F S F; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trials 1 and 3, Gemini trials 1 and 3, and GPT trials 1 and 3 retain P1 for their regex-list parsing directions. Gemini trial 2 retains V3 because its shared CSV escape rule consumes backslashes in previously valid patterns. GPT trial 2 is I1: its submitted edit removes the _TYPE_TRANSFORMERS table, preventing normal option parsing before the new splitter runs.

**Primary assignments.** P1: Claude-1, Claude-3, Gemini-1, Gemini-3, GPT-1, GPT-3; I1: GPT-2; V3: Gemini-2.

**Interpretation.** The GPT trial 2 diagnosis follows the retained repository-state defect; its regex-splitting logic may have additional problems but is not the selected primary category.

<a id="case-scikit-learn__scikit-learn-13135"></a>

### scikit-learn__scikit-learn-13135

**Issue.** KBinsDiscretizer with the kmeans strategy can construct nonmonotonic bin edges from unsorted cluster centers.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: S F S.

**Analysis.** GPT trial 2 sorts the resulting bin edges rather than sorting the centers before calculating boundaries, leaving an incorrect discretization strategy. The notes link this direction to an earlier edit command that did not apply as intended. Passing trials sort the centers; some also retain an unnecessary later edge sort.

**Primary assignments.** I1: GPT-2.

**Interpretation.** The ineffective initial edit and the incorrect final discretization logic are distinct parts of the recorded failure.

<a id="case-scikit-learn__scikit-learn-15100"></a>

### scikit-learn__scikit-learn-15100

**Issue.** strip_accents_unicode leaves combining accents in strings that are already normalized into decomposed form.

**Recorded outcomes.** Claude: S S F; Gemini: S S S; GPT: S S S.

**Analysis.** Claude trial 3 has repeated action-format and editing problems. The notes describe an edit-and-cleanup sequence that removes unrelated vectorizer implementation while the agent checks only the intended accent fix. The other eight trials pass with accent removal that also handles already-normalized strings.

**Primary assignments.** I1: Claude-3.

<a id="case-scikit-learn__scikit-learn-26194"></a>

### scikit-learn__scikit-learn-26194

**Issue.** The first ROC threshold uses a finite sentinel that can be confusing for probability-valued prediction scores.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials calculate or clip to a finite initial threshold. The accepted behavior represents the no-positive-predictions point with positive infinity, and the benchmark tests explicitly require that sentinel. The issue includes a tentative clipping suggestion that differs from the accepted change.

**Primary assignments.** P2: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** A threshold above the largest score is not intrinsically invalid. The relevant failure is disagreement with the specified infinity-sentinel behavior, not that finite thresholds necessarily produce an incorrect ROC point.

<a id="case-sphinx-doc__sphinx-10323"></a>

### sphinx-doc__sphinx-10323

**Issue.** literalinclude applies dedentation after prepend and append, removing indentation intentionally supplied by those options.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: S F S.

**Analysis.** GPT trial 2 implements the issue-requested filter ordering by applying dedent before prepend and append, so user-supplied option content is no longer processed by dedentation. It additionally infers indentation from the included body and applies it to those strings. In the pre-existing no-dedent path, previously verbatim prepend and append content therefore gains extra indentation, supporting the retained V3 label. The other eight trials pass.

**Primary assignments.** V3: GPT-2.

**Interpretation.** The V3 attribution rests on separate evidence for both conditions: the reordered filters implement the issue-reported dedent behavior, while the before-and-after no-dedent comparison demonstrates the regression introduced by unconditional indentation inheritance.

<a id="case-sphinx-doc__sphinx-11510"></a>

### sphinx-doc__sphinx-11510

**Issue.** Including a reStructuredText file bypasses the source-read event used by extensions to transform source content.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** Claude trial 2 performs the source-read transformation but passes event text with an extra trailing newline relative to the added exact-string assertion (V2). The other failed trials retain V3 for applying source-read transformations to previously literal include content.

**Primary assignments.** V2: Claude-2; V3: Claude-1, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

**Interpretation.** Claude trial 2 is distinguished by a concrete representation mismatch, while the remaining V3 trials change prior literal-include behavior.

<a id="case-sphinx-doc__sphinx-7748"></a>

### sphinx-doc__sphinx-7748

**Issue.** Autodoc recognizes only the first of several leading signatures in a function docstring.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** The failed patches add support for reading several signatures but leave multiline signature normalization incomplete. Continuation backslashes remain in output checked by the tests, including the return-annotation handling in Gemini trial 1. All nine trials are labeled as failures.

**Primary assignments.** V2: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-sphinx-doc__sphinx-8056"></a>

### sphinx-doc__sphinx-8056

**Issue.** Napoleon does not correctly handle NumPy-style documentation that gives several parameter names on one declaration line.

**Recorded outcomes.** Claude: F F S; Gemini: S S S; GPT: F F F.

**Analysis.** Claude trial 1 splits names without respecting napoleon_use_param=False; trial 2 splits type fields without the corresponding parameter fields. GPT trial 1 changes the list-style output and removes class markup, trial 2 falls back to list formatting despite napoleon_use_param=True, and trial 3 groups parameter declarations separately from type declarations. The passing Claude and Gemini alternatives split names at an output stage while matching the tested format.

**Primary assignments.** V2: Claude-1, Claude-2, GPT-1, GPT-2, GPT-3.

**Interpretation.** The checked field ordering and configuration-dependent output are part of the benchmark contract; similar rendered text alone does not establish equivalence.

<a id="case-sphinx-doc__sphinx-8548"></a>

### sphinx-doc__sphinx-8548

**Issue.** The inherited-members option omits inherited instance attributes and their documentation.

**Recorded outcomes.** Claude: S F F; Gemini: F F F; GPT: S F F.

**Analysis.** The failed trials focus on retrieving or rendering documentation without completing member discovery. Gemini does not update importer.py to include the inherited instance attributes, while Claude trials 2 and 3 and GPT trials 2 and 3 likewise omit the discovery prerequisite. An attribute assigned in a base-class initializer cannot be discovered solely through dir() on the derived class.

**Primary assignments.** S1: Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-2, GPT-3.

<a id="case-sphinx-doc__sphinx-9591"></a>

### sphinx-doc__sphinx-9591

**Issue.** A property return annotation is displayed as plain text instead of being parsed into a reference.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: S S F.

**Analysis.** GPT trial 3 reformats the annotation upstream but does not change the downstream branch that emits it as plain text. Without invoking the annotation parser in that branch, the required link is still absent. The other eight trials pass.

**Primary assignments.** S2: GPT-3.

<a id="case-sympy__sympy-12489"></a>

### sympy__sympy-12489

**Issue.** Permutation methods construct base-class instances instead of preserving a subclass.

**Recorded outcomes.** Claude: F F F; Gemini: F F F; GPT: F F F.

**Analysis.** All nine failed trials update selected _af_new paths but leave other constructors or hard-coded base-class references unchanged. The tests substitute a subclass and expose the remaining construction paths that do not preserve it.

**Primary assignments.** P1: Claude-1, Claude-2, Claude-3, Gemini-1, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-sympy__sympy-15345"></a>

### sympy__sympy-15345

**Issue.** The Mathematica printer emits Python-style syntax for Max and Min expressions.

**Recorded outcomes.** Claude: S S S; Gemini: S S S; GPT: S F S.

**Analysis.** GPT trial 2 produces Max/Min syntax but also replaces the StrPrinter.doprint entry point with the inherited CodePrinter implementation. The archived recursive list formatter calls self.doprint again; the inner call deletes state still owned by the outer call. An isolated execution of those archived methods reproduces AttributeError for a nonempty list. This existing-behavior regression is assigned V3. The other eight trials pass.

**Primary assignments.** V3: GPT-2.

**Interpretation.** The printer check uses the archived method bodies with dispatch stubs; it is not a historical full-suite execution. The diagnostic script documents this scope explicitly.

<a id="case-sympy__sympy-17630"></a>

### sympy__sympy-17630

**Issue.** Block-matrix operations reduce a ZeroMatrix to scalar zero, breaking later matrix operations.

**Recorded outcomes.** Claude: F F F; Gemini: S F F; GPT: F F F.

**Analysis.** The eight failed trials modify block multiplication without correcting the matrix-addition behavior that still produces scalar zero. Gemini trial 1 is the only passing trial.

**Primary assignments.** S1: Claude-1, Claude-2, Claude-3, Gemini-2, Gemini-3, GPT-1, GPT-2, GPT-3.

<a id="case-sympy__sympy-18211"></a>

### sympy__sympy-18211

**Issue.** Converting a relational expression that cannot be solved explicitly into a set raises an error instead of returning a symbolic set.

**Recorded outcomes.** Claude: S S F; Gemini: F F F; GPT: F S S.

**Analysis.** The failed trials use different symbolic-set fallback strategies. Gemini trials 1 and 2 and GPT trial 1 retain their S1 assignments for limited relational coverage. Claude trial 3 adds an Equality-specific solveset fallback: the first official target assertion passes, but the second returns a ConditionSet over a transformed equation that admits an extraneous positive solution, so this trial is S2. Gemini trial 3 changes the lower-level solver's exception contract; archived original tests report DID NOT RAISE, supporting V3.

**Primary assignments.** S1: Gemini-1, Gemini-2, GPT-1; S2: Claude-3; V3: Gemini-3.

**Interpretation.** Claude trial 3 does not modify the lower-level inequality solver. The two official equality assertions were checked against its archived method using the exact historical SymPy source. The diagnostic script provides this optional source-dependent check separately from its standard-library-only checks.

## Appendix A. Complete unresolved-trial catalogue

All 242 rows below correspond one-to-one to the archived `label=false` records. The full stage and subcategory names are repeated to make each assignment self-contained. Trial links open the archived trajectories indexed for each attempt.

| No. | Task | Model | Trial | Subcategory | Broader stage |
| --- | --- | --- | --- | --- | --- |
| 1 | astropy__astropy-13398 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 2 | astropy__astropy-13398 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 3 | astropy__astropy-13398 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 4 | astropy__astropy-13398 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 5 | astropy__astropy-13398 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 6 | astropy__astropy-13398 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 7 | astropy__astropy-13398 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 8 | astropy__astropy-13398 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 9 | astropy__astropy-13398 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-13398/astropy__astropy-13398.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 10 | astropy__astropy-14182 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 11 | astropy__astropy-14182 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 12 | astropy__astropy-14182 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 13 | astropy__astropy-14182 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 14 | astropy__astropy-14182 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 15 | astropy__astropy-14182 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 16 | astropy__astropy-14182 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-14182/astropy__astropy-14182.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 17 | astropy__astropy-8872 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 18 | astropy__astropy-8872 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 19 | astropy__astropy-8872 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 20 | astropy__astropy-8872 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 21 | astropy__astropy-8872 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 22 | astropy__astropy-8872 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 23 | astropy__astropy-8872 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 24 | astropy__astropy-8872 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 25 | astropy__astropy-8872 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/astropy__astropy-8872/astropy__astropy-8872.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 26 | django__django-10554 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-10554/django__django-10554.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 27 | django__django-10554 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 28 | django__django-10554 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 29 | django__django-10554 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 30 | django__django-10554 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 31 | django__django-10554 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 32 | django__django-10554 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 33 | django__django-10554 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 34 | django__django-10554 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-10554/django__django-10554.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 35 | django__django-11276 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-11276/django__django-11276.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 36 | django__django-11276 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-11276/django__django-11276.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 37 | django__django-11276 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-11276/django__django-11276.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 38 | django__django-11532 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 39 | django__django-11532 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 40 | django__django-11532 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 41 | django__django-11532 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 42 | django__django-11532 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 43 | django__django-11532 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-11532/django__django-11532.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 44 | django__django-11790 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-11790/django__django-11790.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 45 | django__django-11790 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-11790/django__django-11790.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 46 | django__django-11790 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-11790/django__django-11790.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 47 | django__django-11790 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-11790/django__django-11790.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 48 | django__django-11790 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-11790/django__django-11790.traj.json) | V4 Execution Timing Mismatch | Validation & Harness Constraints |
| 49 | django__django-11790 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-11790/django__django-11790.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 50 | django__django-11790 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-11790/django__django-11790.traj.json) | V4 Execution Timing Mismatch | Validation & Harness Constraints |
| 51 | django__django-12125 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-12125/django__django-12125.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 52 | django__django-13023 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13023/django__django-13023.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 53 | django__django-13023 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-13023/django__django-13023.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 54 | django__django-13023 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-13023/django__django-13023.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 55 | django__django-13023 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13023/django__django-13023.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 56 | django__django-13023 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-13023/django__django-13023.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 57 | django__django-13343 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13343/django__django-13343.traj.json) | V4 Execution Timing Mismatch | Validation & Harness Constraints |
| 58 | django__django-13344 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 59 | django__django-13344 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 60 | django__django-13344 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 61 | django__django-13344 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 62 | django__django-13344 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 63 | django__django-13344 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-13344/django__django-13344.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 64 | django__django-13401 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-13401/django__django-13401.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 65 | django__django-13406 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-13406/django__django-13406.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 66 | django__django-13406 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-13406/django__django-13406.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 67 | django__django-13406 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-13406/django__django-13406.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 68 | django__django-13406 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-13406/django__django-13406.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 69 | django__django-13406 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-13406/django__django-13406.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 70 | django__django-14140 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 71 | django__django-14140 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 72 | django__django-14140 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 73 | django__django-14140 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 74 | django__django-14140 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 75 | django__django-14140 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14140/django__django-14140.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 76 | django__django-14155 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 77 | django__django-14155 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 78 | django__django-14155 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 79 | django__django-14155 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 80 | django__django-14155 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 81 | django__django-14155 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 82 | django__django-14155 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 83 | django__django-14155 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 84 | django__django-14155 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14155/django__django-14155.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 85 | django__django-14771 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-14771/django__django-14771.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 86 | django__django-14771 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-14771/django__django-14771.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 87 | django__django-14771 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-14771/django__django-14771.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 88 | django__django-14771 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-14771/django__django-14771.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 89 | django__django-15022 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15022/django__django-15022.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 90 | django__django-15022 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-15022/django__django-15022.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 91 | django__django-15022 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-15022/django__django-15022.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 92 | django__django-15022 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-15022/django__django-15022.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 93 | django__django-15103 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15103/django__django-15103.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 94 | django__django-15103 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15103/django__django-15103.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 95 | django__django-15629 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 96 | django__django-15629 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 97 | django__django-15629 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 98 | django__django-15629 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 99 | django__django-15629 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 100 | django__django-15629 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 101 | django__django-15629 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 102 | django__django-15629 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 103 | django__django-15629 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15629/django__django-15629.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 104 | django__django-15732 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 105 | django__django-15732 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 106 | django__django-15732 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 107 | django__django-15732 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 108 | django__django-15732 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 109 | django__django-15732 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 110 | django__django-15732 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 111 | django__django-15732 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 112 | django__django-15732 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15732/django__django-15732.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 113 | django__django-15741 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-15741/django__django-15741.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 114 | django__django-15741 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-15741/django__django-15741.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 115 | django__django-15741 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-15741/django__django-15741.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 116 | django__django-16502 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 117 | django__django-16502 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 118 | django__django-16502 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 119 | django__django-16502 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 120 | django__django-16502 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 121 | django__django-16502 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 122 | django__django-16502 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 123 | django__django-16502 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 124 | django__django-16502 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-16502/django__django-16502.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 125 | django__django-16560 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/django__django-16560/django__django-16560.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 126 | django__django-16560 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/django__django-16560/django__django-16560.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 127 | django__django-16560 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/django__django-16560/django__django-16560.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 128 | django__django-16560 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/django__django-16560/django__django-16560.traj.json) | V1 Specification-Oracle Gap | Validation & Harness Constraints |
| 129 | django__django-16560 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/django__django-16560/django__django-16560.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 130 | django__django-16560 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/django__django-16560/django__django-16560.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 131 | django__django-16560 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/django__django-16560/django__django-16560.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 132 | matplotlib__matplotlib-20859 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-20859/matplotlib__matplotlib-20859.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 133 | matplotlib__matplotlib-21568 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 134 | matplotlib__matplotlib-21568 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 135 | matplotlib__matplotlib-21568 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 136 | matplotlib__matplotlib-21568 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 137 | matplotlib__matplotlib-21568 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 138 | matplotlib__matplotlib-21568 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 139 | matplotlib__matplotlib-21568 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 140 | matplotlib__matplotlib-21568 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 141 | matplotlib__matplotlib-21568 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-21568/matplotlib__matplotlib-21568.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 142 | matplotlib__matplotlib-24570 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-24570/matplotlib__matplotlib-24570.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 143 | matplotlib__matplotlib-25311 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 144 | matplotlib__matplotlib-25311 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 145 | matplotlib__matplotlib-25311 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-25311/matplotlib__matplotlib-25311.traj.json) | L1 Incomplete Scope / Wrong Layer | Localization |
| 146 | matplotlib__matplotlib-26208 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 147 | matplotlib__matplotlib-26208 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 148 | matplotlib__matplotlib-26208 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 149 | matplotlib__matplotlib-26208 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 150 | matplotlib__matplotlib-26208 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 151 | matplotlib__matplotlib-26208 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 152 | matplotlib__matplotlib-26208 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 153 | matplotlib__matplotlib-26208 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 154 | matplotlib__matplotlib-26208 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/matplotlib__matplotlib-26208/matplotlib__matplotlib-26208.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 155 | matplotlib__matplotlib-26291 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/matplotlib__matplotlib-26291/matplotlib__matplotlib-26291.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 156 | psf__requests-2931 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/psf__requests-2931/psf__requests-2931.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 157 | psf__requests-2931 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/psf__requests-2931/psf__requests-2931.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 158 | psf__requests-2931 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/psf__requests-2931/psf__requests-2931.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 159 | psf__requests-2931 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/psf__requests-2931/psf__requests-2931.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 160 | pylint-dev__pylint-4661 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 161 | pylint-dev__pylint-4661 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 162 | pylint-dev__pylint-4661 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 163 | pylint-dev__pylint-4661 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 164 | pylint-dev__pylint-4661 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 165 | pylint-dev__pylint-4661 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 166 | pylint-dev__pylint-4661 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 167 | pylint-dev__pylint-4661 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 168 | pylint-dev__pylint-4661 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/pylint-dev__pylint-4661/pylint-dev__pylint-4661.traj.json) | V5 Evaluation Infrastructure Failure | Validation & Harness Constraints |
| 169 | pylint-dev__pylint-8898 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 170 | pylint-dev__pylint-8898 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 171 | pylint-dev__pylint-8898 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 172 | pylint-dev__pylint-8898 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 173 | pylint-dev__pylint-8898 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 174 | pylint-dev__pylint-8898 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 175 | pylint-dev__pylint-8898 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 176 | pylint-dev__pylint-8898 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/pylint-dev__pylint-8898/pylint-dev__pylint-8898.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 177 | scikit-learn__scikit-learn-13135 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/scikit-learn__scikit-learn-13135/scikit-learn__scikit-learn-13135.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 178 | scikit-learn__scikit-learn-15100 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/scikit-learn__scikit-learn-15100/scikit-learn__scikit-learn-15100.traj.json) | I1 Tool Failure / Silent State Hallucination | Implementation & Execution |
| 179 | scikit-learn__scikit-learn-26194 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 180 | scikit-learn__scikit-learn-26194 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 181 | scikit-learn__scikit-learn-26194 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 182 | scikit-learn__scikit-learn-26194 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 183 | scikit-learn__scikit-learn-26194 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 184 | scikit-learn__scikit-learn-26194 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 185 | scikit-learn__scikit-learn-26194 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 186 | scikit-learn__scikit-learn-26194 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 187 | scikit-learn__scikit-learn-26194 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/scikit-learn__scikit-learn-26194/scikit-learn__scikit-learn-26194.traj.json) | P2 Distracted by Hints / TODOs | Problem Understanding |
| 188 | sphinx-doc__sphinx-10323 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-10323/sphinx-doc__sphinx-10323.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 189 | sphinx-doc__sphinx-11510 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 190 | sphinx-doc__sphinx-11510 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 191 | sphinx-doc__sphinx-11510 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 192 | sphinx-doc__sphinx-11510 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 193 | sphinx-doc__sphinx-11510 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 194 | sphinx-doc__sphinx-11510 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 195 | sphinx-doc__sphinx-11510 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 196 | sphinx-doc__sphinx-11510 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 197 | sphinx-doc__sphinx-11510 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-11510/sphinx-doc__sphinx-11510.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 198 | sphinx-doc__sphinx-7748 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 199 | sphinx-doc__sphinx-7748 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 200 | sphinx-doc__sphinx-7748 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 201 | sphinx-doc__sphinx-7748 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 202 | sphinx-doc__sphinx-7748 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 203 | sphinx-doc__sphinx-7748 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 204 | sphinx-doc__sphinx-7748 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 205 | sphinx-doc__sphinx-7748 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 206 | sphinx-doc__sphinx-7748 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-7748/sphinx-doc__sphinx-7748.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 207 | sphinx-doc__sphinx-8056 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 208 | sphinx-doc__sphinx-8056 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 209 | sphinx-doc__sphinx-8056 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 210 | sphinx-doc__sphinx-8056 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 211 | sphinx-doc__sphinx-8056 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-8056/sphinx-doc__sphinx-8056.traj.json) | V2 Strict Output Format Mismatch | Validation & Harness Constraints |
| 212 | sphinx-doc__sphinx-8548 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 213 | sphinx-doc__sphinx-8548 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 214 | sphinx-doc__sphinx-8548 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 215 | sphinx-doc__sphinx-8548 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 216 | sphinx-doc__sphinx-8548 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 217 | sphinx-doc__sphinx-8548 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 218 | sphinx-doc__sphinx-8548 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-8548/sphinx-doc__sphinx-8548.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 219 | sphinx-doc__sphinx-9591 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sphinx-doc__sphinx-9591/sphinx-doc__sphinx-9591.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 220 | sympy__sympy-12489 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 221 | sympy__sympy-12489 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 222 | sympy__sympy-12489 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 223 | sympy__sympy-12489 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 224 | sympy__sympy-12489 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 225 | sympy__sympy-12489 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 226 | sympy__sympy-12489 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 227 | sympy__sympy-12489 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 228 | sympy__sympy-12489 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sympy__sympy-12489/sympy__sympy-12489.traj.json) | P1 Misinterpretation / Domain Knowledge Lack | Problem Understanding |
| 229 | sympy__sympy-15345 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-15345/sympy__sympy-15345.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 230 | sympy__sympy-17630 | Claude | [1](../data/traj/claude-sonnet-4-5-20250929/round1/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 231 | sympy__sympy-17630 | Claude | [2](../data/traj/claude-sonnet-4-5-20250929/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 232 | sympy__sympy-17630 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 233 | sympy__sympy-17630 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 234 | sympy__sympy-17630 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 235 | sympy__sympy-17630 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 236 | sympy__sympy-17630 | GPT | [2](../data/traj/gpt-5-2025-08-07-medium-reasoning/round2/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 237 | sympy__sympy-17630 | GPT | [3](../data/traj/gpt-5-2025-08-07-medium-reasoning/round3/sympy__sympy-17630/sympy__sympy-17630.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 238 | sympy__sympy-18211 | Claude | [3](../data/traj/claude-sonnet-4-5-20250929/round3/sympy__sympy-18211/sympy__sympy-18211.traj.json) | S2 Incorrect Strategy | Strategy & Logic |
| 239 | sympy__sympy-18211 | Gemini | [1](../data/traj/gemini-3-pro-preview/round1/sympy__sympy-18211/sympy__sympy-18211.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 240 | sympy__sympy-18211 | Gemini | [2](../data/traj/gemini-3-pro-preview/round2/sympy__sympy-18211/sympy__sympy-18211.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |
| 241 | sympy__sympy-18211 | Gemini | [3](../data/traj/gemini-3-pro-preview/round3/sympy__sympy-18211/sympy__sympy-18211.traj.json) | V3 Regression of Existing Behavior | Validation & Harness Constraints |
| 242 | sympy__sympy-18211 | GPT | [1](../data/traj/gpt-5-2025-08-07-medium-reasoning/round1/sympy__sympy-18211/sympy__sympy-18211.traj.json) | S1 Partial Fix / Incomplete Logic | Strategy & Logic |

## Reproduction and data fields

From the repository root, rebuild this document and its tables with:

```bash
python3 scripts/build_failure_analysis.py
```

The editable inputs are [trial annotations](../FINAL-CODEBOOK/failure_annotations.csv), [category definitions](../FINAL-CODEBOOK/failure_codebook.json), and [English case notes](../FINAL-CODEBOOK/failure_case_notes.json). The script checks exact coverage of all recorded failures, uniqueness, outcome consistency, category validity, evidence-file availability, and the patch/trajectory hashes attached to the annotations. Changed evidence requires annotation review rather than automatic reuse of an old explanation.

The [validation result](Statistics%20results/audits/failures/failure_analysis_validation.json) records the coverage checks. [Category](Statistics%20results/full/failures/failure_taxonomy_summary.csv), [stage](Statistics%20results/full/failures/failure_stage_summary.csv), [model](Statistics%20results/full/failures/failure_model_summary.csv), and [task](Statistics%20results/full/failures/failure_task_summary.csv) CSVs reproduce the descriptive counts. Hashes identify the indexed input snapshot. The catalogue builder performs no API calls, benchmark execution, or automatic causal classification.
