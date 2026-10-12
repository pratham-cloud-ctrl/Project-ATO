"""Preserve meaningful source checks while tolerating a near-zero argmax tie."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from stage3_source_sensitivity import compare, reproduction_reference


def refinement(block=1, difference=1e-15):
    return {
        "actual_contact_aperture_count": 192000,
        "maximum_position_difference_m": difference,
        "position_budget_pass": True,
        "largest_position_witness": {
            "block": block, "sample": 2, "contact": 3, "component": 0,
            "time_s": block/200 + 2/4000 + 3*3e-6,
            "coarse_position_m": .01, "fine_position_m": .01+difference,
        },
    }


def physical_study(block=1, *, summary=False):
    """Use actual independent ODE solutions at two different contact apertures."""
    row = refinement(block)
    witness = row["largest_position_witness"]
    for grid, step in (("coarse", .0025), ("fine", .000625)):
        row[f"{grid}_internal_step_s"] = step
        witness[f"{grid}_position_m"] = float(reproduction_reference(
            0, "moving_clean", step).evaluate(witness["time_s"])[0][witness["component"]])
    row["maximum_position_difference_m"] = abs(witness["coarse_position_m"]-witness["fine_position_m"])
    return {"subject_seed": 0, **(
        {"reference_refinements": {"moving_clean": row}} if summary else
        {"references": {"moving_clean": {"refinement": row}}})}


class SourceReproductionTests(unittest.TestCase):
    def test_roundoff_maximum_can_move_to_a_different_valid_aperture(self):
        compare(refinement(1), refinement(599, 2e-15))

    def test_meaningful_maximum_keeps_its_witness_location_comparison(self):
        with self.assertRaises(AssertionError):
            compare(refinement(1, 1e-5), refinement(2, 1e-5))

    def test_roundoff_exception_does_not_accept_wrong_aperture_or_error(self):
        expected = refinement()
        for field, value in (("time_s", .7), ("fine_position_m", .1), ("contact", 16)):
            changed = deepcopy(expected)
            changed["largest_position_witness"][field] = value
            with self.subTest(field=field), self.assertRaises(AssertionError):
                compare(changed, expected)

    def test_roundoff_exception_preserves_qualification_and_numeric_errors(self):
        expected = refinement()
        for field, value in (("position_budget_pass", False),
                             ("maximum_position_difference_m", 1e-5)):
            changed = deepcopy(expected); changed[field] = value
            with self.subTest(field=field), self.assertRaises(AssertionError):
                compare(changed, expected)

    def test_raw_and_summary_allow_different_physically_bound_roundoff_apertures(self):
        for summary in (False, True):
            with self.subTest(summary=summary):
                compare(physical_study(1, summary=summary), physical_study(599, summary=summary))

    def test_roundoff_pair_cannot_be_self_consistent_but_physically_unrelated(self):
        for summary in (False, True):
            expected = physical_study(summary=summary)
            changed = deepcopy(expected)
            row = (changed["reference_refinements"]["moving_clean"] if summary else
                   changed["references"]["moving_clean"]["refinement"])
            # Equal 50 m positions still attain a negligible maximum. Their
            # aperture binding must reject them in either receipt, independently.
            row["largest_position_witness"]["coarse_position_m"] = 50.
            row["largest_position_witness"]["fine_position_m"] = 50.
            row["maximum_position_difference_m"] = 0.
            for actual, saved in ((changed, expected), (expected, changed)):
                with self.subTest(summary=summary), self.assertRaises(AssertionError):
                    compare(actual, saved)

    def test_physically_bound_witness_cannot_be_relabelled_to_another_component(self):
        expected = physical_study()
        changed = deepcopy(expected)
        changed["references"]["moving_clean"]["refinement"]["largest_position_witness"]["component"] = 1
        with self.assertRaises(AssertionError):
            compare(changed, expected)


if __name__ == "__main__":
    unittest.main()
