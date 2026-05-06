# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MdairyDeduction(models.Model):
    _name = 'mdairy.deduction'
    _description = 'Farmer Deduction Rule'
    _inherit = ['mail.thread']
    _order = 'farmer_id, name'

    name = fields.Char(string='Deduction Name', required=True)
    farmer_id = fields.Many2one('mdairy.farmer', string='Farmer', required=True, tracking=True)
    deduction_type = fields.Selection(
        [
            ('fixed', 'Fixed Amount (KES)'),
            ('percentage', 'Percentage of Gross'),
            ('loan_repayment', 'Loan Repayment'),
        ],
        string='Type',
        required=True,
        default='fixed',
    )
    fixed_amount = fields.Float(string='Fixed Amount (KES)', digits=(14, 2))
    percentage = fields.Float(string='Percentage (%)', digits=(5, 2))
    loan_balance = fields.Float(string='Loan Balance (KES)', digits=(14, 2))
    monthly_repayment = fields.Float(string='Monthly Repayment (KES)', digits=(14, 2))

    state = fields.Selection(
        [('active', 'Active'), ('completed', 'Completed'), ('suspended', 'Suspended')],
        string='Status',
        default='active',
        tracking=True,
    )
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    notes = fields.Text(string='Notes')

    @api.constrains('percentage')
    def _check_percentage(self):
        for rec in self:
            if rec.deduction_type == 'percentage' and not (0 < rec.percentage <= 100):
                raise ValidationError(_('Percentage must be between 0 and 100.'))

    def _compute_period_deduction(self, gross_amount):
        """Return the deduction amount for this period given the gross."""
        self.ensure_one()
        if self.deduction_type == 'fixed':
            return self.fixed_amount
        elif self.deduction_type == 'percentage':
            return gross_amount * (self.percentage / 100)
        elif self.deduction_type == 'loan_repayment':
            return min(self.monthly_repayment, self.loan_balance)
        return 0.0
