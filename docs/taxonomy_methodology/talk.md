| Task                               | 模型及trial                        | 原标签／核查项              | Coder A           | Coder B            | Coder C       | result        |
| ---------------------------------- | ---------------------------------- | --------------------------- | ----------------- | ------------------ | ------------- | ------------- |
| `astropy__astropy-8872`            | 三个模型各1、2、3                  | V3                          | 问号              | UNSURE             | OTHER-V5      | V5            |
| `django__django-12125`             | Gemini 3                           | S2                          | CHANGE，候选L1/P1 | S2                 | S2            | S2            |
| `django__django-13343`             | Claude 2                           | V4                          | ACCEPT?，候选P1   | V4                 | V4            | V4            |
| `django__django-15103`             | Claude 1、2                        | L1                          | L1                | S1                 | L1            | L1            |
| `django__django-15741`             | GPT 1                              | S1                          | ACCEPT?           | S1                 | S1            | S1            |
|                                    | GPT 2                              | S1                          | P1                | S1                 | S1            | S1            |
|                                    | GPT 3                              | S1                          | P1                | UNSURE，候选S2/P2  | S1            | S1            |
| `django__django-13023`             | Claude 2                           | V1                          | P1                | CHANGE，候选L1/P1  | P1            | P1            |
|                                    | Gemini 1、3；GPT 2、3              | V1                          | V1                | V1                 | S1            | V1            |
| `django__django-11532`             | Claude 1、3；GPT 3                 | V3                          | UNSURE            | V3                 | V3            | V3            |
|                                    | GPT 1                              | **earliest_link**，分类均V3 | INDETERMINATE     | SUPPORTED          | SUPPORTED     | SUPPORTED     |
| `django__django-13344`             | GPT 1、3                           | L1                          | P1                | L1                 | L1            | L1            |
| `django__django-16560`             | Claude 1                           | L1                          | L1                | S2，也接受S1       | S1            | S1            |
|                                    | Gemini 1                           | L1                          | I1                | S2，也接受S1       | V3            | I1            |
|                                    | Gemini 2、3                        | L1                          | V1                | S2，也接受S1       | V3            | V1            |
|                                    | GPT 1                              | L1                          | L1                | UNSURE             | OTHER         | V5            |
|                                    | GPT 2                              | S1                          | I1                | S1                 | I1            | I1            |
| `django__django-10554`             | Claude 1                           | I1                          | V1                | UNSURE，倾向P1     | P1            | P1            |
| `django__django-15629`             | Claude 2；GPT 1                    | S1                          | S1                | I1                 | S1            | S1            |
| `django__django-15732`             | Claude 1、2；Gemini 3              | S1                          | P1                | S1                 | S1            | S1            |
| `django__django-16502`             | Claude 1、3；GPT 2                 | **earliest_link**，分类均P1 | INDETERMINATE     | SUPPORTED          | SUPPORTED     | SUPPORTED     |
|                                    | Claude 2；Gemini 1、2              | P1                          | P1                | P1                 | V1            | P1            |
|                                    | Gemini 3                           | P1                          | P1                | CHANGE?，候选I1    | P1            | P1            |
| `matplotlib__matplotlib-21568`     | Claude 1；Gemini 1、2              | P1                          | P1                | S1                 | P1            | P1            |
|                                    | GPT 1、2、3                        | P1                          | P1                | P1                 | S2            | P1            |
| `matplotlib__matplotlib-26208`     | Claude 1；GPT 1、2、3              | P2                          | V1                | P2                 | P2            | P2            |
|                                    | Claude 2                           | P2                          | V1                | P2                 | S1            | S1            |
| `psf__requests-2931`               | Gemini 1、3；GPT 2、3              | S1                          | V3                | S1                 | S1            | S1            |
| `pylint-dev__pylint-8898`          | Claude 1；Gemini 1、3；GPT 1、3    | P1                          | V1                | P1                 | P1            | P1            |
|                                    | GPT 2                              | P1                          | I1                | UNSURE             | P1            | I1            |
| `pylint-dev__pylint-4661`          | Claude 1                           | S3                          | V1                | UNSURE             | OTHER-V5      | V5            |
|                                    | Claude 2；Gemini 2、3；GPT 1、2、3 | S3                          | S3                | 空白               | OTHER-V5      | V5            |
|                                    | Claude 3                           | S3                          | V1                | 空白               | OTHER-V5      | V5            |
|                                    | Gemini 1                           | S3                          | CHANGE，候选空白  | 空白               | OTHER-V5      | V5            |
| `scikit-learn__scikit-learn-13135` | GPT 2                              | I1                          | I1                | CHANGE?，候选P1/S2 | I1            | I1            |
| `sphinx-doc__sphinx-9591`          | GPT 3                              | S2                          | S2                | L1                 | S2            | S2            |
| `sphinx-doc__sphinx-11510`         | Claude 2                           | S2                          | V2                | S2                 | V2            | V2            |
| `sympy__sympy-18211`               | Gemini 1、2；GPT 1                 | S1                          | S1                | S1                 | S2            | S1            |
|                                    | Gemini 3                           | **earliest_link**，分类均V3 | 空白              | SUPPORTED          | NOT_SUPPORTED | NOT_SUPPORTED |
| `sympy__sympy-17630`               | GPT 1                              | S1                          | V3                | S1                 | S1            | S1            |
| `sympy__sympy-12489`               | Claude 1                           | P1                          | P1                | S1                 | S1            | P1            |
|                                    | Claude 2、3；Gemini 3              | P1                          | P1                | CHANGE，候选空白   | S1            | P1            |
|                                    | Gemini 1、2                        | P1                          | P1                | CHANGE，候选空白   | P1            | P1            |
|                                    | GPT 3                              | P1                          | P1                | P1                 | S1            | P1            |



**`django__django-16560`／GPT第3次**三人一致建议由 **L1改为I1**，最终标为I1