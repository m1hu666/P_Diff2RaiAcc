# Why optional usage details are unavailable

Every saved response has numeric prompt and completion totals. Optional subdivisions have a different reporting contract. This audit re-reads the saved response objects and verifies their numeric/null/missing counts against the extracted coverage table.

The archive shows three distinct situations: a detail object is null (so its nested field is unavailable), a detail object exists but its field is null, or a key is absent. A reported numeric zero is retained as zero and is distinct from all three cases.

These patterns already occur in `messages[*].extra.response.usage`; they are not caused by the statistics extractor dropping numeric values. The normalized state `missing` can include a null parent object; the shape table distinguishes these cases.

The archive does not identify where upstream information was lost or not generated. Provider non-reporting, gateway/adapter conversion, and SDK serialization are possible explanations, not established causes. Native upstream payloads and the exact historical conversion implementation are unavailable. Different saved object shapes do not by themselves prove a version change or a particular backend.

Do not impute optional values as zero, infer thinking off from an absent field, or subtract a partial reasoning sum to obtain complete visible-output usage. Cache/reasoning subdivisions are not added to their corresponding totals again.

| Model | Reasoning numeric | Reasoning leaf null | Reasoning unavailable | Total responses |
| --- | ---: | ---: | ---: | ---: |
| claude-sonnet-4-5-20250929 | 24 | 0 | 12848 | 12872 |
| gemini-3-pro-preview | 452 | 5141 | 6090 | 11683 |
| gpt-5-2025-08-07-medium-reasoning | 3661 | 0 | 263 | 3924 |

See [source shapes](missing_usage_shapes.csv), [examples with exact saved usage objects](missing_usage_examples.json), and [field coverage](usage_field_coverage.csv). Examples contain usage objects and source locations only, not message text.
