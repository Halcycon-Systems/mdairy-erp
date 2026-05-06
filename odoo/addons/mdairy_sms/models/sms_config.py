# -*- coding: utf-8 -*-
import json
import logging
import requests

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MdairySmsConfig(models.Model):
    """SMS Gateway configuration supporting Africa's Talking and Twilio."""
    _name = 'mdairy.sms.config'
    _description = 'SMS Gateway Configuration'
    _rec_name = 'name'

    name = fields.Char(string='Configuration Name', required=True, default='Default SMS Gateway')
    provider = fields.Selection(
        [
            ('africastalking', "Africa's Talking"),
            ('twilio', 'Twilio'),
            ('custom', 'Custom HTTP API'),
        ],
        string='SMS Provider',
        required=True,
        default='africastalking',
    )

    # ── Africa's Talking ─────────────────────────────────────────────────────────
    at_username = fields.Char(string="Africa's Talking Username")
    at_api_key = fields.Char(string="Africa's Talking API Key", password=True)
    at_sender_id = fields.Char(string="Sender ID (shortcode)")
    at_environment = fields.Selection(
        [('sandbox', 'Sandbox'), ('production', 'Production')],
        string="AT Environment",
        default='sandbox',
    )

    # ── Twilio ───────────────────────────────────────────────────────────────────
    twilio_account_sid = fields.Char(string='Twilio Account SID')
    twilio_auth_token = fields.Char(string='Twilio Auth Token', password=True)
    twilio_from_number = fields.Char(string='From Number')

    # ── Custom HTTP ──────────────────────────────────────────────────────────────
    custom_api_url = fields.Char(string='API URL')
    custom_api_key = fields.Char(string='API Key', password=True)
    custom_payload_template = fields.Text(
        string='Payload Template (JSON)',
        help='Use {to}, {message}, {api_key} placeholders',
    )

    active = fields.Boolean(string='Active', default=True)

    def send_sms(self, to: str, message: str) -> dict:
        """Dispatch a single SMS. Returns provider response dict."""
        self.ensure_one()
        if self.provider == 'africastalking':
            return self._send_via_africastalking(to, message)
        elif self.provider == 'twilio':
            return self._send_via_twilio(to, message)
        elif self.provider == 'custom':
            return self._send_via_custom(to, message)
        raise UserError(_('Unknown SMS provider: %s') % self.provider)

    def _send_via_africastalking(self, to: str, message: str) -> dict:
        if self.at_environment == 'sandbox':
            base_url = 'https://api.sandbox.africastalking.com/version1/messaging'
        else:
            base_url = 'https://api.africastalking.com/version1/messaging'

        payload = {
            'username': self.at_username,
            'to': to,
            'message': message,
        }
        if self.at_sender_id:
            payload['from'] = self.at_sender_id

        try:
            response = requests.post(
                base_url,
                data=payload,
                headers={
                    'apiKey': self.at_api_key,
                    'Accept': 'application/json',
                },
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise UserError(_("Africa's Talking SMS failed: %s") % exc) from exc

    def _send_via_twilio(self, to: str, message: str) -> dict:
        url = f'https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json'
        try:
            response = requests.post(
                url,
                data={'To': to, 'From': self.twilio_from_number, 'Body': message},
                auth=(self.twilio_account_sid, self.twilio_auth_token),
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise UserError(_('Twilio SMS failed: %s') % exc) from exc

    def _send_via_custom(self, to: str, message: str) -> dict:
        try:
            payload_str = self.custom_payload_template.format(
                to=to, message=message, api_key=self.custom_api_key
            )
            payload = json.loads(payload_str)
            response = requests.post(
                self.custom_api_url,
                json=payload,
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, json.JSONDecodeError, KeyError) as exc:
            raise UserError(_('Custom SMS API failed: %s') % exc) from exc

    def action_test_sms(self):
        """Wizard to send a test SMS."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Send Test SMS'),
            'res_model': 'mdairy.sms.test.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_config_id': self.id},
        }
