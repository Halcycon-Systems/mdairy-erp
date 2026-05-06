# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class MdairyFarmer(models.Model):
    _name = 'mdairy.farmer'
    _description = 'Dairy Farmer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'farmer_code'

    # ── Identity ────────────────────────────────────────────────────────────────
    farmer_code = fields.Char(
        string='Farmer Code',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
    )
    name = fields.Char(string='Full Name', required=True, tracking=True)
    id_number = fields.Char(string='National ID / Passport', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender',
    )

    # ── Contact ─────────────────────────────────────────────────────────────────
    phone = fields.Char(string='Primary Phone', tracking=True)
    phone2 = fields.Char(string='Alternate Phone')
    email = fields.Char(string='Email')

    # ── Location ────────────────────────────────────────────────────────────────
    county = fields.Char(string='County')
    sub_county = fields.Char(string='Sub-County')
    ward = fields.Char(string='Ward')
    village = fields.Char(string='Village')
    gps_latitude = fields.Float(string='GPS Latitude', digits=(10, 7))
    gps_longitude = fields.Float(string='GPS Longitude', digits=(10, 7))

    # ── Cooperative / Collection Centre ─────────────────────────────────────────
    cooperative_id = fields.Many2one(
        'mdairy.cooperative',
        string='Cooperative',
        tracking=True,
    )
    collection_centre_id = fields.Many2one(
        'mdairy.collection.centre',
        string='Collection Centre',
        tracking=True,
    )

    # ── Farm Details ────────────────────────────────────────────────────────────
    farm_size_acres = fields.Float(string='Farm Size (Acres)')
    number_of_cows = fields.Integer(string='Number of Dairy Cows')
    animal_breed = fields.Char(string='Predominant Breed')

    # ── Banking / Payout ────────────────────────────────────────────────────────
    bank_name = fields.Char(string='Bank Name')
    bank_account_number = fields.Char(string='Bank Account Number')
    bank_branch = fields.Char(string='Bank Branch')
    mpesa_number = fields.Char(string='MPESA Number', tracking=True)
    payout_method = fields.Selection(
        [
            ('bank', 'Bank Transfer'),
            ('mpesa', 'MPESA'),
            ('cash', 'Cash'),
        ],
        string='Preferred Payout Method',
        default='mpesa',
    )

    # ── Status ──────────────────────────────────────────────────────────────────
    state = fields.Selection(
        [
            ('draft', 'Pending Approval'),
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('inactive', 'Inactive'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    registration_date = fields.Date(
        string='Registration Date',
        default=fields.Date.today,
    )
    notes = fields.Text(string='Notes')

    # ── Computed / Related ──────────────────────────────────────────────────────
    total_collections = fields.Float(
        string='Total Milk Collected (Ltrs)',
        compute='_compute_totals',
        store=True,
    )
    total_payouts = fields.Float(
        string='Total Payouts (KES)',
        compute='_compute_totals',
        store=True,
    )
    collection_ids = fields.One2many(
        'mdairy.collection',
        'farmer_id',
        string='Collection Records',
    )
    payout_ids = fields.One2many(
        'mdairy.payout',
        'farmer_id',
        string='Payout Records',
    )

    # ── Sequence ────────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('farmer_code', _('New')) == _('New'):
                vals['farmer_code'] = self.env['ir.sequence'].next_by_code(
                    'mdairy.farmer'
                ) or _('New')
        return super().create(vals_list)

    # ── Validation ──────────────────────────────────────────────────────────────
    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and not re.match(r'^\+?[\d\s\-]{7,15}$', rec.phone):
                raise ValidationError(_('Phone number "%s" is not valid.') % rec.phone)

    @api.constrains('mpesa_number')
    def _check_mpesa(self):
        for rec in self:
            if rec.mpesa_number and not re.match(r'^(07|01|\+2547|\+2541)\d{8}$', rec.mpesa_number):
                raise ValidationError(
                    _('MPESA number "%s" must be a valid Kenyan mobile number.') % rec.mpesa_number
                )

    # ── Computed ────────────────────────────────────────────────────────────────
    @api.depends('collection_ids.quantity_litres', 'payout_ids.amount', 'payout_ids.state')
    def _compute_totals(self):
        for farmer in self:
            farmer.total_collections = sum(farmer.collection_ids.mapped('quantity_litres'))
            farmer.total_payouts = sum(
                farmer.payout_ids.filtered(lambda p: p.state == 'paid').mapped('amount')
            )

    # ── Actions ─────────────────────────────────────────────────────────────────
    def action_activate(self):
        self.write({'state': 'active'})

    def action_suspend(self):
        self.write({'state': 'suspended'})

    def action_deactivate(self):
        self.write({'state': 'inactive'})
