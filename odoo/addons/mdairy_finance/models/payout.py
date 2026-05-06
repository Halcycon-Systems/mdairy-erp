# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class MdairyPayoutBatch(models.Model):
    """Represents a periodic (e.g. monthly) payout run for all farmers."""
    _name = 'mdairy.payout.batch'
    _description = 'Farmer Payout Batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'period_start desc'

    name = fields.Char(
        string='Batch Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    period_start = fields.Date(string='Period Start', required=True, tracking=True)
    period_end = fields.Date(string='Period End', required=True, tracking=True)
    cooperative_id = fields.Many2one('mdairy.cooperative', string='Cooperative')
    notes = fields.Text(string='Notes')

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('computed', 'Computed'),
            ('approved', 'Approved'),
            ('disbursed', 'Disbursed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    payout_ids = fields.One2many('mdairy.payout', 'batch_id', string='Payouts')
    payout_count = fields.Integer(compute='_compute_payout_count', string='# Payouts')
    total_gross = fields.Float(compute='_compute_totals', string='Total Gross (KES)', store=True, digits=(14, 2))
    total_deductions = fields.Float(compute='_compute_totals', string='Total Deductions (KES)', store=True, digits=(14, 2))
    total_net = fields.Float(compute='_compute_totals', string='Total Net (KES)', store=True, digits=(14, 2))

    @api.depends('payout_ids')
    def _compute_payout_count(self):
        for rec in self:
            rec.payout_count = len(rec.payout_ids)

    @api.depends('payout_ids.gross_amount', 'payout_ids.total_deductions', 'payout_ids.amount')
    def _compute_totals(self):
        for rec in self:
            rec.total_gross = sum(rec.payout_ids.mapped('gross_amount'))
            rec.total_deductions = sum(rec.payout_ids.mapped('total_deductions'))
            rec.total_net = sum(rec.payout_ids.mapped('amount'))

    def action_compute_payouts(self):
        """Compute individual farmer payouts from confirmed collections in the period."""
        for batch in self:
            if batch.state != 'draft':
                raise UserError(_('Batch must be in Draft to compute payouts.'))

            domain = [
                ('state', '=', 'confirmed'),
                ('collection_date', '>=', batch.period_start),
                ('collection_date', '<=', batch.period_end),
            ]
            if batch.cooperative_id:
                domain.append(('cooperative_id', '=', batch.cooperative_id.id))

            collections = self.env['mdairy.collection'].search(domain)
            farmer_collections = {}
            for col in collections:
                farmer_collections.setdefault(col.farmer_id.id, []).append(col)

            # Remove existing draft payouts for this batch
            batch.payout_ids.filtered(lambda p: p.state == 'draft').unlink()

            payout_vals = []
            for farmer_id, cols in farmer_collections.items():
                farmer = self.env['mdairy.farmer'].browse(farmer_id)
                gross = sum(c.amount_due for c in cols)
                total_litres = sum(c.quantity_litres for c in cols)

                # Compute deductions
                deductions = self.env['mdairy.deduction'].search([
                    ('farmer_id', '=', farmer_id),
                    ('state', '=', 'active'),
                ])
                deduction_lines = []
                total_deduction = 0.0
                for ded in deductions:
                    amount = ded._compute_period_deduction(gross)
                    total_deduction += amount
                    deduction_lines.append((0, 0, {
                        'deduction_id': ded.id,
                        'name': ded.name,
                        'amount': amount,
                    }))

                net = max(0.0, gross - total_deduction)
                payout_vals.append({
                    'batch_id': batch.id,
                    'farmer_id': farmer_id,
                    'period_start': batch.period_start,
                    'period_end': batch.period_end,
                    'total_litres': total_litres,
                    'gross_amount': gross,
                    'total_deductions': total_deduction,
                    'amount': net,
                    'payout_method': farmer.payout_method,
                    'mpesa_number': farmer.mpesa_number,
                    'bank_name': farmer.bank_name,
                    'bank_account_number': farmer.bank_account_number,
                    'deduction_line_ids': deduction_lines,
                    'collection_ids': [(6, 0, [c.id for c in cols])],
                })

            self.env['mdairy.payout'].create(payout_vals)
            batch.state = 'computed'

    def action_approve(self):
        for batch in self:
            if batch.state != 'computed':
                raise UserError(_('Batch must be Computed before approval.'))
            batch.payout_ids.filtered(lambda p: p.state == 'draft').write({'state': 'approved'})
            batch.state = 'approved'

    def action_disburse(self):
        for batch in self:
            if batch.state != 'approved':
                raise UserError(_('Batch must be Approved before disbursement.'))
            batch.payout_ids.filtered(lambda p: p.state == 'approved').write({
                'state': 'paid',
                'payment_date': fields.Date.today(),
            })
            # Mark collections as paid
            batch.payout_ids.mapped('collection_ids').write({'state': 'paid'})
            batch.state = 'disbursed'

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class MdairyPayout(models.Model):
    """Individual farmer payout within a batch."""
    _name = 'mdairy.payout'
    _description = 'Farmer Payout'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'period_start desc, farmer_id'

    name = fields.Char(
        string='Payout Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    batch_id = fields.Many2one('mdairy.payout.batch', string='Payout Batch', ondelete='cascade')
    farmer_id = fields.Many2one('mdairy.farmer', string='Farmer', required=True, tracking=True)
    period_start = fields.Date(string='Period Start', required=True)
    period_end = fields.Date(string='Period End', required=True)

    total_litres = fields.Float(string='Total Litres', digits=(10, 2))
    gross_amount = fields.Float(string='Gross Amount (KES)', digits=(14, 2))
    total_deductions = fields.Float(string='Total Deductions (KES)', digits=(14, 2))
    amount = fields.Float(string='Net Payout (KES)', digits=(14, 2), tracking=True)

    payout_method = fields.Selection(
        [('bank', 'Bank Transfer'), ('mpesa', 'MPESA'), ('cash', 'Cash')],
        string='Payout Method',
    )
    mpesa_number = fields.Char(string='MPESA Number')
    bank_name = fields.Char(string='Bank')
    bank_account_number = fields.Char(string='Account Number')
    payment_date = fields.Date(string='Payment Date')
    transaction_reference = fields.Char(string='Transaction Reference', tracking=True)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    deduction_line_ids = fields.One2many('mdairy.payout.deduction.line', 'payout_id', string='Deduction Lines')
    collection_ids = fields.Many2many('mdairy.collection', string='Collections')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('mdairy.payout') or _('New')
        return super().create(vals_list)

    def action_mark_paid(self):
        for rec in self:
            if rec.state != 'approved':
                raise UserError(_('Only approved payouts can be marked as paid.'))
            rec.write({'state': 'paid', 'payment_date': fields.Date.today()})

    def action_mark_failed(self):
        self.write({'state': 'failed'})


class MdairyPayoutDeductionLine(models.Model):
    _name = 'mdairy.payout.deduction.line'
    _description = 'Payout Deduction Line'

    payout_id = fields.Many2one('mdairy.payout', string='Payout', ondelete='cascade')
    deduction_id = fields.Many2one('mdairy.deduction', string='Deduction Rule')
    name = fields.Char(string='Description', required=True)
    amount = fields.Float(string='Amount (KES)', digits=(14, 2))
