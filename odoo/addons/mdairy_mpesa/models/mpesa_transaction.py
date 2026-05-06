# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MdairyMpesaTransaction(models.Model):
    """Tracks every MPESA B2C payment attempt linked to a farmer payout."""
    _name = 'mdairy.mpesa.transaction'
    _description = 'MPESA B2C Transaction'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(
        string='Transaction Reference',
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    payout_id = fields.Many2one('mdairy.payout', string='Payout', ondelete='cascade')
    farmer_id = fields.Many2one('mdairy.farmer', string='Farmer', related='payout_id.farmer_id', store=True)
    phone_number = fields.Char(string='Phone Number', required=True)
    amount = fields.Float(string='Amount (KES)', required=True, digits=(14, 2))
    remarks = fields.Char(string='Remarks')

    # ── Request ─────────────────────────────────────────────────────────────────
    conversation_id = fields.Char(string='ConversationID (Safaricom)')
    originator_conversation_id = fields.Char(string='OriginatorConversationID')
    request_payload = fields.Text(string='Request Payload (JSON)')
    request_timestamp = fields.Datetime(string='Request Time', default=fields.Datetime.now)

    # ── Result ──────────────────────────────────────────────────────────────────
    result_code = fields.Char(string='Result Code')
    result_description = fields.Char(string='Result Description')
    mpesa_receipt_number = fields.Char(string='MPESA Receipt Number')
    receiver_public_name = fields.Char(string='Receiver Name')
    transaction_amount = fields.Float(string='Transaction Amount', digits=(14, 2))
    b2c_utility_account_balance = fields.Float(string='Utility Account Balance', digits=(14, 2))
    transaction_completed_date = fields.Datetime(string='Completion Time')
    result_payload = fields.Text(string='Result Payload (JSON)')

    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('queued', 'Queued'),
            ('success', 'Successful'),
            ('failed', 'Failed'),
            ('timeout', 'Timeout'),
        ],
        string='Status',
        default='pending',
        tracking=True,
    )
    config_id = fields.Many2one('mdairy.mpesa.config', string='MPESA Configuration')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('mdairy.mpesa.transaction') or _('New')
        return super().create(vals_list)

    def action_send(self):
        """Send the B2C payment request to Safaricom Daraja."""
        for rec in self:
            if rec.state not in ('pending', 'failed', 'timeout'):
                raise UserError(_('Transaction is already processed.'))
            config = rec.config_id or self.env['mdairy.mpesa.config'].search(
                [('active', '=', True)], limit=1
            )
            if not config:
                raise UserError(_('No active MPESA configuration found. Please configure MPESA settings.'))
            try:
                result = config.send_b2c_payment(
                    phone_number=rec.phone_number,
                    amount=rec.amount,
                    remarks=rec.remarks or _('Farmer Payout'),
                )
                rec.write({
                    'conversation_id': result.get('ConversationID'),
                    'originator_conversation_id': result.get('OriginatorConversationID'),
                    'request_payload': str(result),
                    'state': 'queued',
                })
            except UserError as exc:
                rec.write({'state': 'failed', 'result_description': str(exc)})
                raise

    def process_callback(self, payload: dict):
        """Handle the Daraja B2C result callback."""
        self.ensure_one()
        result = payload.get('Result', {})
        code = str(result.get('ResultCode', '-1'))
        description = result.get('ResultDesc', '')

        params = {item['Key']: item['Value']
                  for item in result.get('ResultParameters', {}).get('ResultParameter', [])}

        self.write({
            'result_code': code,
            'result_description': description,
            'mpesa_receipt_number': params.get('TransactionID'),
            'receiver_public_name': params.get('ReceiverPartyPublicName'),
            'transaction_amount': params.get('TransactionAmount', 0),
            'b2c_utility_account_balance': params.get('B2CUtilityAccountAvailableFunds', 0),
            'result_payload': str(payload),
            'state': 'success' if code == '0' else 'failed',
        })

        if code == '0' and self.payout_id:
            self.payout_id.write({
                'state': 'paid',
                'transaction_reference': params.get('TransactionID'),
                'payment_date': fields.Date.today(),
            })
