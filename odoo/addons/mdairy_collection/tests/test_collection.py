# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMdairyCollection(TransactionCase):
    """Unit tests for milk collection records."""

    def setUp(self):
        super().setUp()
        self.cooperative = self.env['mdairy.cooperative'].create({'name': 'Test Coop'})
        self.farmer = self.env['mdairy.farmer'].create({
            'name': 'Test Farmer',
            'cooperative_id': self.cooperative.id,
        })
        self.farmer.action_activate()

    def _create_collection(self, litres=10.0, grade='A', price=45.0):
        return self.env['mdairy.collection'].create({
            'farmer_id': self.farmer.id,
            'quantity_litres': litres,
            'quality_grade': grade,
            'unit_price': price,
        })

    def test_collection_sequence_assigned(self):
        col = self._create_collection()
        self.assertTrue(col.name)
        self.assertNotEqual(col.name, 'New')
        self.assertTrue(col.name.startswith('COL/'))

    def test_collection_amount_computed(self):
        col = self._create_collection(litres=20.0, price=45.0)
        self.assertAlmostEqual(col.amount_due, 900.0)

    def test_rejected_collection_amount_is_zero(self):
        col = self._create_collection(grade='rejected', price=45.0)
        self.assertAlmostEqual(col.amount_due, 0.0)

    def test_negative_quantity_raises_validation(self):
        with self.assertRaises(ValidationError):
            self._create_collection(litres=-1.0)

    def test_confirm_collection(self):
        col = self._create_collection()
        self.assertEqual(col.state, 'draft')
        col.action_confirm()
        self.assertEqual(col.state, 'confirmed')

    def test_reject_collection(self):
        col = self._create_collection()
        col.action_reject()
        self.assertEqual(col.state, 'rejected')
        self.assertEqual(col.quality_grade, 'rejected')

    def test_reset_to_draft_from_confirmed(self):
        col = self._create_collection()
        col.action_confirm()
        col.action_reset_draft()
        self.assertEqual(col.state, 'draft')

    def test_collection_cooperative_related(self):
        col = self._create_collection()
        self.assertEqual(col.cooperative_id, self.cooperative)
