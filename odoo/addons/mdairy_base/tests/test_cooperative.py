# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestMdairyCooperative(TransactionCase):
    """Unit tests for the mdairy.cooperative model."""

    def test_cooperative_sequence_assigned(self):
        coop = self.env['mdairy.cooperative'].create({'name': 'Kijani Cooperative'})
        self.assertTrue(coop.code)
        self.assertTrue(coop.code.startswith('COOP/'))

    def test_cooperative_farmer_count(self):
        coop = self.env['mdairy.cooperative'].create({'name': 'Count Test Coop'})
        for i in range(3):
            self.env['mdairy.farmer'].create({
                'name': f'Farmer {i}',
                'cooperative_id': coop.id,
            })
        self.assertEqual(coop.farmer_count, 3)

    def test_collection_centre_created_under_cooperative(self):
        coop = self.env['mdairy.cooperative'].create({'name': 'Centre Coop'})
        centre = self.env['mdairy.collection.centre'].create({
            'name': 'Main Centre',
            'cooperative_id': coop.id,
        })
        self.assertEqual(coop.centre_count, 1)
        self.assertEqual(centre.cooperative_id, coop)
