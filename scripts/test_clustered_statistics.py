"""Small deterministic checks of dependence preservation and denominator logic."""

import unittest

from audit_usage_missingness import source_shape
from clustered_sensitivity import bootstrap, value, total


class ClusteredStatisticsTests(unittest.TestCase):
    def test_paired_resampling_preserves_identical_model_differences(self):
        specs = [dict(model=model, kind='resource', metric='steps', measure='mean',
                      numerator=i, denominator=0, scale=1) for model, i in [('A', 1), ('B', 2)]]
        summary, pairs = bootstrap([[1, 2, 2], [1, 20, 20], [1, 5, 5]], specs, ['A', 'B'], 199, 42)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]['difference_ci95_lower'], 0)
        self.assertEqual(pairs[0]['difference_ci95_upper'], 0)
        self.assertGreater(summary[0]['ci95_upper'], summary[0]['ci95_lower'])

    def test_repository_sums_preserve_task_weighting(self):
        spec = dict(model='A', kind='resource', metric='steps', measure='mean', numerator=1, denominator=0, scale=1)
        vectors = [[1, 10], [1, 10], [1, 100]]
        blocks = [total(vectors[:2]), vectors[2]]
        summary, _ = bootstrap(vectors, [spec], ['A'], 199, 42, blocks)
        self.assertEqual(summary[0]['estimate'], 40)
        self.assertEqual(value(total(blocks), spec), 40)
        self.assertNotEqual(summary[0]['estimate'], (10+100)/2)

    def test_composition_recomputes_denominator(self):
        spec = dict(numerator=1, denominator=2, scale=100)
        self.assertEqual(value(total([[1, 1, 1], [1, 0, 3]]), spec), 25)
        self.assertIsNone(value([1, 0, 0], spec))

    def test_singleton_has_no_estimation_interval(self):
        spec = dict(model='A', kind='resource', metric='steps', measure='mean', numerator=1, denominator=0, scale=1)
        summary, _ = bootstrap([[1, 10]], [spec], ['A'], 199, 42)
        self.assertIsNone(summary[0]['ci95_lower'])
        self.assertEqual(summary[0]['interval_status'], 'insufficient_clusters')

    def test_usage_shape_distinguishes_zero_and_unavailability(self):
        field = 'completion_tokens_details.reasoning_tokens'
        self.assertEqual(source_shape({'completion_tokens_details': None}, field), 'parent_null:completion_tokens_details')
        self.assertEqual(source_shape({'completion_tokens_details': {'reasoning_tokens': None}}, field), 'leaf_null')
        self.assertEqual(source_shape({'completion_tokens_details': {}}, field), 'key_absent:'+field)
        self.assertEqual(source_shape({'completion_tokens_details': {'reasoning_tokens': 0}}, field), 'numeric')


if __name__ == '__main__':
    unittest.main()
