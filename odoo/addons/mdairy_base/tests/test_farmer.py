# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMdairyFarmer(TransactionCase):
    """Unit tests for the mdairy.farmer model."""

    def setUp(self):
        super().setUp()
        self.cooperative = self.env['mdairy.cooperative'].create({
            'name': 'Test Cooperative',
        })

    def test_farmer_sequence_assigned_on_create(self):
        """Farmer code should be set automatically by the sequence."""
        farmer = self.env['mdairy.farmer'].create({
            'name': 'Jane Wanjiru',
            'cooperative_id': self.cooperative.id,
        })
        self.assertTrue(farmer.farmer_code)
        self.assertNotEqual(farmer.farmer_code, 'New')
        self.assertTrue(farmer.farmer_code.startswith('FMR/'))

    def test_farmer_default_state_is_draft(self):
        farmer = self.env['mdairy.farmer'].create({'name': 'John Kamau'})
        self.assertEqual(farmer.state, 'draft')

    def test_farmer_activate(self):
        farmer = self.env['mdairy.farmer'].create({'name': 'Mary Njeri'})
        farmer.action_activate()
        self.assertEqual(farmer.state, 'active')

    def test_farmer_suspend(self):
        farmer = self.env['mdairy.farmer'].create({'name': 'Peter Mwangi'})
        farmer.action_activate()
        farmer.action_suspend()
        self.assertEqual(farmer.state, 'suspended')

    def test_invalid_phone_raises_validation(self):
        with self.assertRaises(ValidationError):
            self.env['mdairy.farmer'].create({
                'name': 'Bad Phone',
                'phone': 'not-a-phone',
            })

    def test_invalid_mpesa_number_raises_validation(self):
        with self.assertRaises(ValidationError):
            self.env['mdairy.farmer'].create({
                'name': 'Bad MPESA',
                'mpesa_number': '12345',
            })

    def test_valid_mpesa_number(self):
        farmer = self.env['mdairy.farmer'].create({
            'name': 'Good MPESA',
            'mpesa_number': '0712345678',
        })
        self.assertEqual(farmer.mpesa_number, '0712345678')

    def test_farmer_payout_method_default_mpesa(self):
        farmer = self.env['mdairy.farmer'].create({'name': 'Default Method'})
        self.assertEqual(farmer.payout_method, 'mpesa')

    def test_farmer_deactivate(self):
        farmer = self.env['mdairy.farmer'].create({'name': 'To Deactivate'})
        farmer.action_activate()
        farmer.action_deactivate()
        self.assertEqual(farmer.state, 'inactive')
