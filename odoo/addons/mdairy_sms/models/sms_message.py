# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MdairySmsMessage(models.Model):
    """Log of all SMS messages dispatched by mDairy."""
    _name = 'mdairy.sms.message'
    _description = 'SMS Message Log'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(
        string='Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    farmer_id = fields.Many2one('mdairy.farmer', string='Farmer')
    to_number = fields.Char(string='Recipient Number', required=True)
    message_body = fields.Text(string='Message', required=True)
    template_id = fields.Many2one('mdairy.sms.template', string='Template Used')
    config_id = fields.Many2one('mdairy.sms.config', string='SMS Gateway')

    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
        ],
        string='Status',
        default='pending',
        tracking=True,
    )
    provider_response = fields.Text(string='Provider Response')
    error_message = fields.Text(string='Error Message')
    sent_at = fields.Datetime(string='Sent At')

    # ── Related record ───────────────────────────────────────────────────────────
    res_model = fields.Char(string='Related Document Model')
    res_id = fields.Integer(string='Related Document ID')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('mdairy.sms.message') or _('New')
        return super().create(vals_list)

    def action_send(self):
        """Send the SMS via the configured gateway."""
        for rec in self:
            if rec.state == 'sent':
                continue
            config = rec.config_id or self.env['mdairy.sms.config'].search(
                [('active', '=', True)], limit=1
            )
            if not config:
                raise UserError(_('No active SMS gateway configuration found.'))
            try:
                result = config.send_sms(to=rec.to_number, message=rec.message_body)
                rec.write({
                    'state': 'sent',
                    'provider_response': str(result),
                    'sent_at': fields.Datetime.now(),
                    'config_id': config.id,
                })
            except UserError as exc:
                rec.write({'state': 'failed', 'error_message': str(exc)})
                _logger.error('SMS send failed for %s: %s', rec.name, exc)
                raise

    @api.model
    def send_to_farmer(self, farmer, message_body: str, template=None, res_model=None, res_id=None):
        """Convenience method: create and immediately send an SMS to a farmer."""
        phone = farmer.mpesa_number or farmer.phone
        if not phone:
            _logger.warning('Farmer %s has no phone number; SMS not sent.', farmer.name)
            return False
        msg = self.create({
            'farmer_id': farmer.id,
            'to_number': phone,
            'message_body': message_body,
            'template_id': template.id if template else False,
            'res_model': res_model,
            'res_id': res_id,
        })
        msg.action_send()
        return msg
