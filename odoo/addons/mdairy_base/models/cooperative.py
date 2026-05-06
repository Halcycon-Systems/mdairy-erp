# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MdairyCooperative(models.Model):
    _name = 'mdairy.cooperative'
    _description = 'Dairy Cooperative'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Cooperative Name', required=True, tracking=True)
    code = fields.Char(string='Code', copy=False, readonly=True, default=lambda self: _('New'))
    registration_number = fields.Char(string='Registration Number')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    county = fields.Char(string='County')

    chairman_name = fields.Char(string='Chairman Name')
    secretary_name = fields.Char(string='Secretary Name')
    treasurer_name = fields.Char(string='Treasurer Name')

    state = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        string='Status',
        default='active',
        tracking=True,
    )

    collection_centre_ids = fields.One2many(
        'mdairy.collection.centre',
        'cooperative_id',
        string='Collection Centres',
    )
    farmer_ids = fields.One2many(
        'mdairy.farmer',
        'cooperative_id',
        string='Farmers',
    )

    farmer_count = fields.Integer(
        string='Farmer Count',
        compute='_compute_farmer_count',
    )
    centre_count = fields.Integer(
        string='Centre Count',
        compute='_compute_centre_count',
    )

    @api.depends('farmer_ids')
    def _compute_farmer_count(self):
        for rec in self:
            rec.farmer_count = len(rec.farmer_ids)

    @api.depends('collection_centre_ids')
    def _compute_centre_count(self):
        for rec in self:
            rec.centre_count = len(rec.collection_centre_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('mdairy.cooperative') or _('New')
        return super().create(vals_list)

    def action_view_farmers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Farmers'),
            'res_model': 'mdairy.farmer',
            'view_mode': 'list,form',
            'domain': [('cooperative_id', '=', self.id)],
            'context': {'default_cooperative_id': self.id},
        }


class MdairyCollectionCentre(models.Model):
    _name = 'mdairy.collection.centre'
    _description = 'Milk Collection Centre'
    _order = 'name'

    name = fields.Char(string='Centre Name', required=True)
    code = fields.Char(string='Code')
    cooperative_id = fields.Many2one('mdairy.cooperative', string='Cooperative', required=True)
    location = fields.Char(string='Location')
    manager_name = fields.Char(string='Manager Name')
    phone = fields.Char(string='Phone')
    capacity_litres = fields.Float(string='Daily Capacity (Litres)')
    state = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        string='Status',
        default='active',
    )
    farmer_ids = fields.One2many(
        'mdairy.farmer',
        'collection_centre_id',
        string='Assigned Farmers',
    )
    farmer_count = fields.Integer(compute='_compute_farmer_count', string='Farmers')

    @api.depends('farmer_ids')
    def _compute_farmer_count(self):
        for rec in self:
            rec.farmer_count = len(rec.farmer_ids)
