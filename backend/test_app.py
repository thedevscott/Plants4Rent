import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from backend.app import app
from backend.load_db import go
from backend.database.models import setup_db, db_drop_and_create_all


class PlantRentalTestCase(unittest.TestCase):
    """This class represents the plants4sale test case"""

    def setUp(self):
        """Define variables for test and initialize app"""
        self.renter_token = os.environ.get('RENTER_TOKEN')
        self.owner_token = os.environ.get('OWNER_TOKEN')
        self.database_name = os.environ.get('DATABASE_TEST_NAME')
        self.database_path = os.environ.get('DATABASE_TEST_PATH')

        self.owner_headers = {'Authorization': 'Bearer ' + self.owner_token}
        self.renter_headers = {'Authorization': 'Bearer ' + self.renter_token}
        self.json_headers = {'Content-Type': 'application/json',
                             'Authorization': 'Bearer ' + self.owner_token}

        self.app = app
        self.client = self.app.test_client()

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
            # Recreate tables and reload them for each test
            db_drop_and_create_all()
            go()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_plants(self):
        response = self.client.get('/plants')

        self.assertEqual(response.status_code, 200)
        self.assertIn('plants', json.loads(response.data))

    def test_get_plants_by_id(self):
        response = self.client.get('/plants/1')
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('success', reply)
        self.assertIn('plants', reply)
        self.assertIn('message', reply)
        self.assertEqual(len(reply['plants']), 5)

    def test_get_renter_invoice(self):
        response = self.client.get('/invoice/1', headers=self.renter_headers)
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('invoice', reply)
        self.assertIn('success', reply)
        self.assertIn('total', reply)

    def test_get_rented_plants(self):
        response = self.client.get('/rented', headers=self.renter_headers)
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('message', reply)
        self.assertIn('success', reply)
        self.assertIn('data', reply)

    def test_get_renters(self):
        response = self.client.get('/renters', headers=self.owner_headers)
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('success', reply)
        self.assertIn('data', reply)

    def test_add_plant(self):
        plant = {
            "name": "Thyme",
            "description": "Makes a lovely tea for studying",
            "quantity": 40,
            "price": 4.97
        }
        response = self.client.post('/add', headers=self.json_headers,
                                    json=plant, )
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('plant', reply)
        self.assertIn('success', reply)

    def test_update_plant_entry(self):
        plant = {
            "name": "Rosemary",
            "description": "Makes a lovely tea for studying",
            "quantity": 40,
            "price": 4.97
        }
        response = self.client.patch('/plants/2', headers=self.json_headers,
                                     json=plant)
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('success', reply)
        self.assertIn('plant', reply)

    def test_delete_plant(self):
        response = self.client.delete('/plants/4', headers=self.owner_headers)
        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        self.assertIn('success', reply)
        self.assertIn('id', reply)

    # ----------------------------------------------------------------------
    #  Error Checks
    # ----------------------------------------------------------------------

    def test_404_get_plants_by_id(self):
        response = self.client.get('/plants/100000000000000000')
        self.assertEqual(response.status_code, 404)

        reply = json.loads(response.data)
        self.assertIn('error', reply)
        self.assertIn('success', reply)
        self.assertIn('message', reply)

    def test_401_get_renter_invoice(self):
        response = self.client.get('/invoice/1')
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)

    def test_401_get_rented_plants(self):
        response = self.client.get('/rented', )
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)

    def test_401_get_renters(self):
        response = self.client.get('/renters')
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)

    def test_401_add_plant(self):
        plant = {
            "name": "Thyme",
            "description": "Makes a lovely tea for studying",
            "quantity": 40,
            "price": 4.97
        }
        response = self.client.post('/add', json=plant)
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)

    def test_401_update_plant_entry(self):
        plant = {
            "name": "Rosemary",
            "description": "Makes a lovely tea for studying",
            "quantity": 40,
            "price": 4.97
        }
        response = self.client.patch('/plants/2', json=plant)
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)

    def test_401_delete_plant(self):
        response = self.client.delete('/plants/4')
        self.assertEqual(response.status_code, 401)

        reply = json.loads(response.data)
        self.assertIn('code', reply)
        self.assertIn('description', reply)
