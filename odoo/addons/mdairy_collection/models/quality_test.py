# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MdairyQualityTest(models.Model):
    _name = 'mdairy.quality.test'
    _description = 'Milk Quality Test'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'test_date desc'

    name = fields.Char(
        string='Test Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    test_date = fields.Date(string='Test Date', required=True, default=fields.Date.today)
    session = fields.Selection(
        [('morning', 'Morning'), ('evening', 'Evening')],
        string='Session',
        required=True,
        default='morning',
    )

    # ── Sample Source ────────────────────────────────────────────────────────────
    farmer_id = fields.Many2one('mdairy.farmer', string='Farmer')
    collection_centre_id = fields.Many2one('mdairy.collection.centre', string='Collection Centre')
    sample_source = fields.Selection(
        [('farmer', 'Individual Farmer'), ('bulk_tank', 'Bulk Tank'), ('batch', 'Batch')],
        string='Sample Source',
        default='farmer',
    )

    # ── Physical Parameters ──────────────────────────────────────────────────────
    temperature_celsius = fields.Float(string='Temperature (°C)', digits=(5, 1))
    colour = fields.Selection(
        [('normal', 'Normal'), ('abnormal', 'Abnormal')],
        string='Colour',
        default='normal',
    )
    odour = fields.Selection(
        [('normal', 'Normal'), ('sour', 'Sour'), ('off', 'Off-odour')],
        string='Odour',
        default='normal',
    )

    # ── Chemical Parameters ──────────────────────────────────────────────────────
    fat_percentage = fields.Float(string='Fat (%)', digits=(5, 2))
    protein_percentage = fields.Float(string='Protein (%)', digits=(5, 2))
    lactose_percentage = fields.Float(string='Lactose (%)', digits=(5, 2))
    snf_percentage = fields.Float(string='SNF (%)', digits=(5, 2),
                                  help='Solids Not Fat')
    density = fields.Float(string='Density (g/ml)', digits=(6, 4))
    acidity_ph = fields.Float(string='Acidity (pH)', digits=(5, 2))
    freezing_point = fields.Float(string='Freezing Point (°C)', digits=(5, 3))

    # ── Adulteration Tests ───────────────────────────────────────────────────────
    antibiotics_present = fields.Boolean(string='Antibiotics Detected', default=False)
    water_added = fields.Boolean(string='Water Added', default=False)
    starch_present = fields.Boolean(string='Starch Detected', default=False)
    detergent_present = fields.Boolean(string='Detergent Detected', default=False)
    aflatoxin_ppb = fields.Float(string='Aflatoxin (ppb)', digits=(10, 3))

    # ── Microbiology ─────────────────────────────────────────────────────────────
    total_plate_count = fields.Integer(string='Total Plate Count (cfu/ml)')
    somatic_cell_count = fields.Integer(string='Somatic Cell Count (cells/ml)')

    # ── Result ───────────────────────────────────────────────────────────────────
    grade = fields.Selection(
        [
            ('A', 'Grade A – Premium'),
            ('B', 'Grade B – Standard'),
            ('C', 'Grade C – Below Standard'),
            ('rejected', 'Rejected'),
        ],
        string='Overall Grade',
        compute='_compute_grade',
        store=True,
        tracking=True,
    )
    rejection_reasons = fields.Text(string='Rejection / Downgrade Reasons', readonly=True, compute='_compute_grade', store=True)
    tester_id = fields.Many2one('res.users', string='Tested By', default=lambda self: self.env.user)
    notes = fields.Text(string='Notes')

    # ── Collections that used this test ─────────────────────────────────────────
    collection_ids = fields.One2many('mdairy.collection', 'quality_test_id', string='Collections')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('mdairy.quality.test') or _('New')
        return super().create(vals_list)

    @api.depends(
        'antibiotics_present', 'water_added', 'starch_present', 'detergent_present',
        'acidity_ph', 'fat_percentage', 'snf_percentage', 'temperature_celsius',
        'total_plate_count', 'aflatoxin_ppb',
    )
    def _compute_grade(self):
        for rec in self:
            reasons = []

            # Immediate rejection triggers
            if rec.antibiotics_present:
                reasons.append(_('Antibiotics detected'))
            if rec.detergent_present:
                reasons.append(_('Detergent detected'))
            if rec.aflatoxin_ppb and rec.aflatoxin_ppb > 0.5:
                reasons.append(_('Aflatoxin exceeds 0.5 ppb'))
            if rec.starch_present:
                reasons.append(_('Starch (adulteration) detected'))
            if rec.water_added:
                reasons.append(_('Water addition detected'))
            if rec.acidity_ph and not (6.6 <= rec.acidity_ph <= 6.8):
                reasons.append(_('pH out of range (6.6–6.8)'))

            if reasons:
                rec.grade = 'rejected'
                rec.rejection_reasons = '\n'.join(reasons)
                continue

            # Grade determination
            fat = rec.fat_percentage or 0
            snf = rec.snf_percentage or 0
            tpc = rec.total_plate_count or 0

            if fat >= 3.5 and snf >= 8.5 and tpc <= 200000:
                rec.grade = 'A'
            elif fat >= 3.2 and snf >= 8.0 and tpc <= 500000:
                rec.grade = 'B'
            else:
                rec.grade = 'C'
            rec.rejection_reasons = False

    @api.constrains('acidity_ph')
    def _check_ph(self):
        for rec in self:
            if rec.acidity_ph and not (4.0 <= rec.acidity_ph <= 9.0):
                raise ValidationError(_('pH value "%s" seems unrealistic.') % rec.acidity_ph)
