# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMdairyDeduction(TransactionCase):
    """Unit tests for the deduction computation logic."""

    def setUp(self):
        super().setUp()
        self.farmer = self.env['mdairy.farmer'].create({
            'name': 'Deduction Farmer',
        })

    def test_fixed_deduction(self):
        ded = self.env['mdairy.deduction'].create({
            'name': 'SACCO Levy',
            'farmer_id': self.farmer.id,
            'deduction_type': 'fixed',
            'fixed_amount': 500.0,
        })
        self.assertAlmostEqual(ded._compute_period_deduction(gross_amount=10000.0), 500.0)

    def test_percentage_deduction(self):
        ded = self.env['mdairy.deduction'].create({
            'name': 'Insurance 2%',
            'farmer_id': self.farmer.id,
            'deduction_type': 'percentage',
            'percentage': 2.0,
        })
        self.assertAlmostEqual(ded._compute_period_deduction(gross_amount=5000.0), 100.0)

    def test_loan_repayment_limited_to_balance(self):
        ded = self.env['mdairy.deduction'].create({
            'name': 'Loan',
            'farmer_id': self.farmer.id,
            'deduction_type': 'loan_repayment',
            'monthly_repayment': 1000.0,
            'loan_balance': 300.0,   # Balance < repayment
        })
        # Should only deduct the remaining balance
        self.assertAlmostEqual(ded._compute_period_deduction(gross_amount=10000.0), 300.0)

    def test_loan_repayment_full_when_balance_sufficient(self):
        ded = self.env['mdairy.deduction'].create({
            'name': 'Loan 2',
            'farmer_id': self.farmer.id,
            'deduction_type': 'loan_repayment',
            'monthly_repayment': 1000.0,
            'loan_balance': 5000.0,
        })
        self.assertAlmostEqual(ded._compute_period_deduction(gross_amount=10000.0), 1000.0)

    def test_invalid_percentage_raises_validation(self):
        with self.assertRaises(ValidationError):
            self.env['mdairy.deduction'].create({
                'name': 'Bad Percentage',
                'farmer_id': self.farmer.id,
                'deduction_type': 'percentage',
                'percentage': 150.0,  # Over 100%
            })
