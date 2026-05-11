import math
import unittest

from xrastlinx import (
    ALPHA,
    ALPHA_INV,
    MARK1_H,
    OMEGA_C,
    PROVEN_PHYSICS,
    REFUSED_NUMERIC_MISMATCH,
    Mark1Attractor,
    evaluate_mark1_relations,
)


class Mark1AttractorTests(unittest.TestCase):
    def setUp(self):
        self.model = Mark1Attractor()

    def test_default_h_is_pi_over_nine(self):
        self.assertAlmostEqual(MARK1_H, math.pi / 9)
        self.assertAlmostEqual(self.model.h, 0.3490658503988659)

    def test_omega_c_is_review_comparison_constant(self):
        self.assertEqual(OMEGA_C, 47 / 125)
        self.assertAlmostEqual(self.model.omega_c, 0.376)

    def test_fraction_split_complements_to_one(self):
        self.assertAlmostEqual(
            self.model.actualized_fraction + self.model.potential_fraction,
            1.0,
        )

    def test_fine_structure_relationships_are_refused_numeric_mismatches(self):
        results = {result.expression: result for result in self.model.fine_structure_relationships()}

        self.assertAlmostEqual(results["4*pi^2*H + pi"].value, 4 * math.pi**3 / 9 + math.pi)
        self.assertAlmostEqual(results["4*pi^2*H + pi"].target, ALPHA_INV)
        self.assertFalse(results["4*pi^2*H + pi"].matches_target)

        self.assertAlmostEqual(results["H / (8*pi)"].value, 1 / 72)
        self.assertAlmostEqual(results["H / (8*pi)"].target, ALPHA)
        self.assertFalse(results["H / (8*pi)"].matches_target)

        self.assertAlmostEqual(results["210*H"].value, 210 * math.pi / 9)
        self.assertAlmostEqual(results["210*H"].target, ALPHA_INV)
        self.assertFalse(results["210*H"].matches_target)

        for result in results.values():
            self.assertEqual(result.status, REFUSED_NUMERIC_MISMATCH)
            self.assertEqual(result.authority, "none")

    def test_no_relationship_claims_proven_physics(self):
        review = evaluate_mark1_relations()

        self.assertEqual(review["H"], MARK1_H)
        self.assertEqual(review["omega_c"], OMEGA_C)
        for relation in review["relations"]:
            self.assertNotEqual(relation["status"], PROVEN_PHYSICS)
            self.assertEqual(relation["authority"], "none")

    def test_shell_closures_center_on_twin_prime_pairs_without_empirical_authority(self):
        results = {result.element: result for result in self.model.shell_closure_offsets()}

        self.assertEqual(results["Magnesium"].nearest_twin_prime_pair, (11, 13))
        self.assertTrue(results["Magnesium"].is_centered)

        self.assertEqual(results["Argon"].nearest_twin_prime_pair, (17, 19))
        self.assertTrue(results["Argon"].is_centered)

        self.assertEqual(results["Zinc"].nearest_twin_prime_pair, (29, 31))
        self.assertTrue(results["Zinc"].is_centered)

        for result in results.values():
            self.assertEqual(result.authority, "none")
            self.assertNotEqual(result.status, PROVEN_PHYSICS)

    def test_helix_turn_estimate_uses_reciprocal_h_and_refuses_mismatch(self):
        result = self.model.helix_turn_estimate()

        self.assertAlmostEqual(result.value, 9 / math.pi)
        self.assertAlmostEqual(result.target, 3.6)
        self.assertGreater(result.relative_error, 0.1)
        self.assertEqual(result.status, REFUSED_NUMERIC_MISMATCH)


if __name__ == "__main__":
    unittest.main()
