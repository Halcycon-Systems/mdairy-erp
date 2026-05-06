# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MdairySmsTemplate(models.Model):
    """Reusable SMS message templates with variable substitution."""
    _name = 'mdairy.sms.template'
    _description = 'SMS Template'
    _order = 'name'

    name = fields.Char(string='Template Name', required=True)
    event_type = fields.Selection(
        [
            ('collection_confirmed', 'Milk Collection Confirmed'),
            ('collection_rejected', 'Milk Collection Rejected'),
            ('payout_approved', 'Payout Approved'),
            ('payout_disbursed', 'Payout Disbursed'),
            ('payout_failed', 'Payout Failed'),
            ('registration', 'Farmer Registration'),
            ('custom', 'Custom'),
        ],
        string='Event Type',
        required=True,
    )
    body = fields.Text(
        string='Message Body',
        required=True,
        help=(
            'Available variables: {farmer_name}, {amount}, {litres}, '
            '{date}, {session}, {grade}, {reference}, {phone}'
        ),
    )
    active = fields.Boolean(string='Active', default=True)
    language = fields.Char(string='Language', default='en')

    def render(self, context: dict) -> str:
        """Render the template body with the given context dict."""
        self.ensure_one()
        try:
            return self.body.format(**context)
        except KeyError as exc:
            return self.body  # Return unrendered if variable missing


class MdairySmsTestWizard(models.TransientModel):
    """Wizard to send a test SMS from the configuration form."""
    _name = 'mdairy.sms.test.wizard'
    _description = 'Test SMS Wizard'

    config_id = fields.Many2one('mdairy.sms.config', string='SMS Gateway', required=True)
    to_number = fields.Char(string='To Number', required=True)
    message = fields.Text(string='Message', required=True, default='mDairy ERP: Test message. If you received this, the SMS gateway is working correctly.')

    def action_send_test(self):
        self.ensure_one()
        self.env['mdairy.sms.message'].create({
            'to_number': self.to_number,
            'message_body': self.message,
            'config_id': self.config_id.id,
        }).action_send()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Test SMS Sent'),
                'message': _('Test SMS dispatched to %s.') % self.to_number,
                'type': 'success',
            },
        }
