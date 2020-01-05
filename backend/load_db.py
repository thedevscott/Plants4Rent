"""Simple helper script for loading DB elements"""

import random

from backend.app import app
from backend.database.models import Catalog, Rented, Renter, setup_db

setup_db(app)

# List of plants
plants = [
    {
        'name': "Rose",
        'description': 'Beautiful Crimson Rose suitable for the most'
                       'alluring of spaces',
        'quantity': 30,
        'price': 25.97
    },

    {
        'name': "Golden Pathos",
        'description': 'The easiest of all houseplants to grow, even if you '
                       'are a person who forgets to water your plants',
        'quantity': 30,
        'price': 5.97
    },

    {
        'name': "Peace Lily",
        'description': 'Peace lily fits in well in just about every style of '
                       'interior design, particular country and causal looks.',
        'quantity': 20,
        'price': 15.97
    },

    {
        'name': "Weigela",
        'description': 'This old-fashioned deciduous shrub, which bears '
                       'profuse clusters of flowers in spring, is virtually '
                       'carefree, save for a bit of pruning and watering.',
        'quantity': 50,
        'price': 10.97
    }
]

# List of customers
renters = [
    {
        'name': 'Julie Ray',
        'address': '1234 Ray Port Ln',
        'city': 'Los Angeles',
        'state': 'CA'
    },

    {
        'name': 'Will Constant',
        'address': '45 Constant View Rd',
        'city': 'Springfield',
        'state': 'VA'
    },

    {
        'name': 'Essence Allure',
        'address': '90 Scent Ln',
        'city': 'New York',
        'state': 'NY'
    },

    {
        'name': 'Hero Anga',
        'address': '77 Angalitic Rd',
        'city': 'Maui',
        'state': 'HI'
    },
]
# ---------------------------------------------------------------------------
# Add each plant to the database
# ---------------------------------------------------------------------------
for plant in plants:
    sell_plant = Catalog(name=plant['name'],
                         description=plant['description'],
                         quantity=plant['quantity'],
                         price=plant['price'])

    sell_plant.insert()

# ---------------------------------------------------------------------------
# Add Renters to the database
# ---------------------------------------------------------------------------
for renter in renters:
    client = Renter(name=renter['name'],
                    address=renter['address'],
                    city=renter['city'],
                    state=renter['state'])

    client.insert()

# ---------------------------------------------------------------------------
# Rent out some plants
# ---------------------------------------------------------------------------
for i in range(1, len(renters)):
    plant = Rented(plant_id=random.choice(range(1, len(plants) + 1)),
                   renter_id=random.choice(range(1, len(renters) + 1))
                   )
    plant.insert()
