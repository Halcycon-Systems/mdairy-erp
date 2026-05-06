# -*- coding: utf-8 -*-
import base64
import json
import logging
import requests
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MdairyMpesaConfig(models.Model):
    """Daraja API configuration for the MPESA B2C integration."""
    _name = 'mdairy.mpesa.config'
    _description = 'MPESA Daraja API Configuration'
    _rec_name = 'name'

    name = fields.Char(string='Configuration Name', required=True, default='Default MPESA Config')
    environment = fields.Selection(
        [('sandbox', 'Sandbox (Testing)'), ('production', 'Production')],
        string='Environment',
        required=True,
        default='sandbox',
    )

    # ── Daraja Credentials ───────────────────────────────────────────────────────
    consumer_key = fields.Char(string='Consumer Key', required=True)
    consumer_secret = fields.Char(string='Consumer Secret', required=True, password=True)
    shortcode = fields.Char(string='Business Shortcode', required=True,
                            help='Paybill or Till number for B2C payouts')
    initiator_name = fields.Char(string='Initiator Name', required=True,
                                  help='API user initiating the transaction')
    security_credential = fields.Text(
        string='Security Credential',
        required=True,
        help='Encrypted initiator password (base64). Use the Safaricom portal to generate.',
    )
    queue_timeout_url = fields.Char(
        string='Queue Timeout URL',
        help='Callback URL when request times out in the queue',
    )
    result_url = fields.Char(
        string='Result URL',
        help='Callback URL for transaction results',
    )
    remarks = fields.Char(string='Default Remarks', default='mDairy Farmer Payout')

    active = fields.Boolean(string='Active', default=True)

    def _get_access_token(self):
        """Obtain a Daraja OAuth access token."""
        self.ensure_one()
        if self.environment == 'sandbox':
            base_url = 'https://sandbox.safaricom.co.ke'
        else:
            base_url = 'https://api.safaricom.co.ke'

        credentials = base64.b64encode(
            f'{self.consumer_key}:{self.consumer_secret}'.encode()
        ).decode()
        try:
            response = requests.get(
                f'{base_url}/oauth/v1/generate?grant_type=client_credentials',
                headers={'Authorization': f'Basic {credentials}'},
                timeout=15,
            )
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException as exc:
            raise UserError(_('Failed to obtain MPESA access token: %s') % exc) from exc

    def send_b2c_payment(self, phone_number, amount, occasion='', remarks=''):
        """Initiate a B2C payment to a farmer's MPESA number."""
        self.ensure_one()
        if self.environment == 'sandbox':
            base_url = 'https://sandbox.safaricom.co.ke'
        else:
            base_url = 'https://api.safaricom.co.ke'

        token = self._get_access_token()
        payload = {
            'InitiatorName': self.initiator_name,
            'SecurityCredential': self.security_credential,
            'CommandID': 'BusinessPayment',
            'Amount': int(amount),
            'PartyA': self.shortcode,
            'PartyB': phone_number,
            'Remarks': remarks or self.remarks,
            'QueueTimeOutURL': self.queue_timeout_url,
            'ResultURL': self.result_url,
            'Occasion': occasion,
        }
        try:
            response = requests.post(
                f'{base_url}/mpesa/b2c/v3/paymentrequest',
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                },
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise UserError(_('MPESA B2C request failed: %s') % exc) from exc

    def action_test_connection(self):
        """Test that we can obtain an access token (sandbox only)."""
        token = self._get_access_token()
        if token:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Successful'),
                    'message': _('Successfully obtained MPESA access token.'),
                    'type': 'success',
                },
            }
