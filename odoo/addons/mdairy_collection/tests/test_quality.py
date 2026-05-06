# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestMdairyQualityTest(TransactionCase):
    """Unit tests for milk quality grading logic."""

    def _create_test(self, **kwargs):
        defaults = {
            'fat_percentage': 3.5,
            'snf_percentage': 8.5,
            'acidity_ph': 6.7,
            'antibiotics_present': False,
            'water_added': False,
            'starch_present': False,
            'detergent_present': False,
            'total_plate_count': 100000,
        }
        defaults.update(kwargs)
        return self.env['mdairy.quality.test'].create(defaults)

    def test_grade_a_for_premium_parameters(self):
        qt = self._create_test(fat_percentage=3.6, snf_percentage=8.6, total_plate_count=150000)
        self.assertEqual(qt.grade, 'A')

    def test_grade_b_for_standard_parameters(self):
        qt = self._create_test(fat_percentage=3.3, snf_percentage=8.1, total_plate_count=400000)
        self.assertEqual(qt.grade, 'B')

    def test_grade_c_for_low_fat(self):
        qt = self._create_test(fat_percentage=2.8, snf_percentage=7.5, total_plate_count=600000)
        self.assertEqual(qt.grade, 'C')

    def test_rejected_if_antibiotics_detected(self):
        qt = self._create_test(antibiotics_present=True)
        self.assertEqual(qt.grade, 'rejected')
        self.assertIn('Antibiotics', qt.rejection_reasons)

    def test_rejected_if_detergent_detected(self):
        qt = self._create_test(detergent_present=True)
        self.assertEqual(qt.grade, 'rejected')

    def test_rejected_if_ph_out_of_range(self):
        qt = self._create_test(acidity_ph=5.0)
        self.assertEqual(qt.grade, 'rejected')

    def test_rejected_if_aflatoxin_high(self):
        qt = self._create_test(aflatoxin_ppb=0.8)
        self.assertEqual(qt.grade, 'rejected')

    def test_quality_test_sequence_assigned(self):
        qt = self._create_test()
        self.assertTrue(qt.name)
        self.assertTrue(qt.name.startswith('QT/'))
