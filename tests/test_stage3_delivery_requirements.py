"""Requirements-level regressions, including an infeasible perfect-monitor case."""
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from stage3_delivery_requirements import (observed_map, command_envelope,
                                         largest_uncertainty_for_full_direction)


class DeliveryRequirementTests(unittest.TestCase):
    def setUp(self):
        self.mean = 1.012
        self.gain = np.array([[.060, .010], [.010, .060]])
        self.routes = np.array([self.gain[:, 0], -self.gain[:, 0],
                                self.gain[:, 1], -self.gain[:, 1]])*self.mean

    def test_observed_route_reconstruction(self):
        gain, uncertainty, margin = observed_map(self.routes, self.mean, 0.)
        np.testing.assert_allclose(gain, self.gain, rtol=0, atol=1e-15)
        np.testing.assert_allclose(uncertainty, np.full((2, 2), .0095/self.mean))
        self.assertGreater(margin, 0)

    def test_perfect_monitor_does_not_cure_two_route_floor(self):
        result = command_envelope(self.routes, self.mean, 0., .008, (1, -1))
        np.testing.assert_allclose(result['full_direction_correction_allowance_m'], (.027, .027))
        self.assertFalse(result['full_direction_budget_pass'])
        threshold = largest_uncertainty_for_full_direction(self.routes, self.mean, .008, (1, -1))
        self.assertFalse(threshold['feasible_even_with_zero_charge_uncertainty'])
        self.assertIsNone(threshold['maximum_uncertainty_fraction_of_nominal'])

    def test_four_percent_single_route_and_actual_large_bound(self):
        self.assertTrue(command_envelope(self.routes, self.mean, .04, .008, (1, 0))['full_direction_budget_pass'])
        actual = command_envelope(self.routes, self.mean, .4411206, .008, (1, 0))
        self.assertLess(actual['authority_margin_m'], 0)
        self.assertEqual(actual['maximum_common_command_scale'], 0)

    def test_full_precision_threshold_brackets_gate(self):
        threshold = largest_uncertainty_for_full_direction(self.routes, self.mean, .008, (1, 0))
        value = threshold['maximum_uncertainty_fraction_of_nominal']
        self.assertGreater(value, .04)
        self.assertTrue(command_envelope(self.routes, self.mean, value-1e-8, .008, (1, 0))['full_direction_budget_pass'])
        self.assertFalse(command_envelope(self.routes, self.mean, value+1e-8, .008, (1, 0))['full_direction_budget_pass'])

    def test_command_scale_is_inside_budget_and_monotone(self):
        allowances = [command_envelope(self.routes, self.mean, u, .008, (1, -1))
                      for u in (0., .02, .04, .074)]
        scales = [a['maximum_common_command_scale'] for a in allowances]
        self.assertTrue(all(left >= right for left, right in zip(scales, scales[1:])))
        for allowance in allowances:
            self.assertLessEqual(max(allowance['maximum_scale_allowance_m']), .025+1e-14)

    def test_gain_dose_cross_term_cannot_be_discarded(self):
        _, gain_u, _ = observed_map(self.routes, self.mean, .04)
        result = command_envelope(self.routes, self.mean, .04, .008, (1, 0))
        first_order = gain_u[:, 0]*self.mean+abs(self.gain[:, 0])*.04+.008
        np.testing.assert_allclose(np.asarray(result['full_direction_correction_allowance_m'])-first_order,
                                   gain_u[:, 0]*.04, rtol=1e-12, atol=1e-15)

    def test_invalid_dose_and_command_contracts(self):
        for uncertainty in (-.1, self.mean, float('nan')):
            with self.assertRaises(ValueError): observed_map(self.routes, self.mean, uncertainty)
        for direction in ((0, 0), (1.01, 0), (float('nan'), 0), (1,)):
            with self.assertRaises(ValueError): command_envelope(self.routes, self.mean, .04, .008, direction)


if __name__ == '__main__': unittest.main()
