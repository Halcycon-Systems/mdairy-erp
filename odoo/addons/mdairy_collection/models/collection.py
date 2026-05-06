# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MdairyCollection(models.Model):
    _name = 'mdairy.collection'
    _description = 'Milk Collection Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'collection_date desc, session'

    # ── Identity ────────────────────────────────────────────────────────────────
    name = fields.Char(
        string='Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    collection_date = fields.Date(
        string='Collection Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    session = fields.Selection(
        [('morning', 'Morning'), ('evening', 'Evening')],
        string='Session',
        required=True,
        default='morning',
        tracking=True,
    )

    # ── Farmer / Centre ──────────────────────────────────────────────────────────
    farmer_id = fields.Many2one(
        'mdairy.farmer',
        string='Farmer',
        required=True,
        tracking=True,
        domain=[('state', '=', 'active')],
    )
    cooperative_id = fields.Many2one(
        'mdairy.cooperative',
        string='Cooperative',
        related='farmer_id.cooperative_id',
        store=True,
    )
    collection_centre_id = fields.Many2one(
        'mdairy.collection.centre',
        string='Collection Centre',
        related='farmer_id.collection_centre_id',
        store=True,
    )
    collected_by = fields.Many2one('res.users', string='Collected By', default=lambda self: self.env.user)

    # ── Quantity ────────────────────────────────────────────────────────────────
    quantity_litres = fields.Float(
        string='Quantity (Litres)',
        required=True,
        tracking=True,
        digits=(10, 2),
    )
    can_number = fields.Char(string='Can Number(s)')
    temperature_celsius = fields.Float(string='Temperature (°C)', digits=(5, 1))

    # ── Quality ─────────────────────────────────────────────────────────────────
    quality_test_id = fields.Many2one('mdairy.quality.test', string='Quality Test')
    quality_grade = fields.Selection(
        [
            ('A', 'Grade A – Premium'),
            ('B', 'Grade B – Standard'),
            ('C', 'Grade C – Below Standard'),
            ('rejected', 'Rejected'),
        ],
        string='Quality Grade',
        default='A',
        tracking=True,
    )
    rejection_reason = fields.Text(string='Rejection Reason')

    # ── Pricing ─────────────────────────────────────────────────────────────────
    unit_price = fields.Float(
        string='Unit Price (KES/Ltr)',
        digits=(10, 2),
        tracking=True,
    )
    amount_due = fields.Float(
        string='Amount Due (KES)',
        compute='_compute_amount_due',
        store=True,
        digits=(10, 2),
    )

    # ── State ───────────────────────────────────────────────────────────────────
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('invoiced', 'Invoiced'),
            ('paid', 'Paid'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(string='Notes')

    # ── Computed ────────────────────────────────────────────────────────────────
    @api.depends('quantity_litres', 'unit_price', 'quality_grade')
    def _compute_amount_due(self):
        for rec in self:
            if rec.quality_grade == 'rejected':
                rec.amount_due = 0.0
            else:
                rec.amount_due = rec.quantity_litres * rec.unit_price

    @api.onchange('farmer_id', 'collection_date', 'session')
    def _onchange_set_price(self):
        """Auto-populate unit price from the active price configuration."""
        if self.farmer_id:
            price_config = self.env['mdairy.collection.price'].search(
                [
                    ('cooperative_id', 'in', [self.farmer_id.cooperative_id.id, False]),
                    ('date_from', '<=', self.collection_date or fields.Date.today()),
                    '|',
                    ('date_to', '=', False),
                    ('date_to', '>=', self.collection_date or fields.Date.today()),
                ],
                order='cooperative_id desc, date_from desc',
                limit=1,
            )
            if price_config:
                grade = self.quality_grade or 'A'
                if grade == 'A':
                    self.unit_price = price_config.price_grade_a
                elif grade == 'B':
                    self.unit_price = price_config.price_grade_b
                else:
                    self.unit_price = price_config.price_grade_c

    # ── Sequence ────────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('mdairy.collection') or _('New')
        return super().create(vals_list)

    # ── Constraints ─────────────────────────────────────────────────────────────
    @api.constrains('quantity_litres')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity_litres < 0:
                raise ValidationError(_('Quantity cannot be negative.'))

    # ── Actions ─────────────────────────────────────────────────────────────────
    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = 'confirmed'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'
            rec.quality_grade = 'rejected'

    def action_reset_draft(self):
        for rec in self:
            if rec.state not in ('confirmed', 'rejected'):
                raise UserError(_('Only confirmed or rejected records can be reset to draft.'))
            rec.state = 'draft'


class MdairyCollectionPrice(models.Model):
    _name = 'mdairy.collection.price'
    _description = 'Milk Price Configuration'
    _order = 'date_from desc'

    name = fields.Char(string='Description', required=True)
    cooperative_id = fields.Many2one('mdairy.cooperative', string='Cooperative (leave blank for default)')
    date_from = fields.Date(string='Valid From', required=True, default=fields.Date.today)
    date_to = fields.Date(string='Valid To')
    price_grade_a = fields.Float(string='Grade A Price (KES/Ltr)', required=True, digits=(10, 2))
    price_grade_b = fields.Float(string='Grade B Price (KES/Ltr)', required=True, digits=(10, 2))
    price_grade_c = fields.Float(string='Grade C Price (KES/Ltr)', required=True, digits=(10, 2))
    notes = fields.Text(string='Notes')

    @api.constrains('price_grade_a', 'price_grade_b', 'price_grade_c')
    def _check_prices(self):
        for rec in self:
            if rec.price_grade_a <= 0 or rec.price_grade_b <= 0 or rec.price_grade_c <= 0:
                raise ValidationError(_('All prices must be greater than zero.'))
            if not (rec.price_grade_a >= rec.price_grade_b >= rec.price_grade_c):
                raise ValidationError(_('Grade A price must be ≥ Grade B ≥ Grade C.'))
