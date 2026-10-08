"""Independent corner cases for Stage2 timing and resource admission."""
import importlib.util
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ato_budgets',ROOT/'scripts/run_architecture_budgets.py')
budgets=importlib.util.module_from_spec(spec)
spec.loader.exec_module(budgets)


class ArchitectureBudgets(unittest.TestCase):
    def test_periodic_mask_wrap_and_overlap(self):
        # On a10ms circle [-1,2] and [1,4] cover5ms, not6ms.
        intervals,fraction=budgets.periodic_union(.010,[0,.002],.002,.001)
        self.assertAlmostEqual(fraction,.5)
        self.assertAlmostEqual(budgets.minimum_window_usable(intervals,.010,.005),0)

    def test_full_recovery_masks_every_sample(self):
        _,fraction=budgets.periodic_union(.008,[0,.002,.004],.009)
        self.assertEqual(fraction,1)

    def test_two_sources_aligned_do_not_double_global_blanking(self):
        _,single=budgets.periodic_union(.025,[0],.0015,.0001)
        _,double=budgets.periodic_union(.025,[0,0],.0015,.0001)
        self.assertAlmostEqual(single,.064)
        self.assertEqual(single,double)

    def test_reference_and_failed_architectures(self):
        result=budgets.calculate()
        c=result['compute_and_transport']
        self.assertAlmostEqual(c['analytical_cycles_per_s'],43198600)
        self.assertTrue(c['128MHz_60pct_budget_pass'])
        self.assertFalse(c['64MHz_60pct_budget_pass'])
        self.assertFalse(c['two_second_raw4k_fits_physical_ram'])
        self.assertFalse(result['telemetry']['raw4k_1M_target_pass'])

    def test_energy_balance_and_all_max_rejection(self):
        result=budgets.calculate()
        by_id={p['id']:p for p in result['profiles']}
        motor=by_id['motor_reference']
        # Hand-computed rail=24V*3mA*400us*40Hz*2 sources=2.304mW.
        self.assertAlmostEqual(motor['rail_power_mW'],2.304)
        for p in result['profiles']:
            self.assertAlmostEqual(p['total_battery_power_mW'],
                p['conservative_case_heat_mW']+p['bulk_load_power_mW'])
        self.assertFalse(by_id['cartesian_max_rejected']['all_selected_continuous_gates_pass'])
        self.assertFalse(by_id['pressure_high_current_stress']['selected_continuous_gates']['steady_selected_package_rise'])
        self.assertFalse(by_id['pressure_reference']['motor_observation_gates']['global_coverage'])

    def test_voltage_demand_does_not_disappear(self):
        #20mA*2kohm+4V exceeds40V: raw-current knob cannot override load.
        self.assertGreater(.020*2000+4,40)
        result=budgets.calculate()
        cases=[r for r in result['compliance_sweep'] if r['bulk_load_ohm']==2000]
        self.assertTrue(all(r['max_current_at500us_mA']<=18 for r in cases))
        self.assertTrue(all(math.isfinite(r['max_current_at500us_mA']) for r in cases))

    def test_filtering_propagates_dense_invalidity(self):
        #FIR support7.5ms is longer than any gap in the120Hz staggered train.
        _,fraction=budgets.periodic_union(1/120,[0,.002,.004],.0017+.0075,.0001)
        self.assertEqual(fraction,1)
        #The40Hz archive mask expands to1.5ms+7.5ms+0.1ms=9.1ms/25ms.
        _,fraction=budgets.periodic_union(.025,[0],.0015+.0075,.0001)
        self.assertAlmostEqual(fraction,.364)


if __name__=='__main__': unittest.main()
