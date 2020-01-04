from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

from backend.database.models import Catalog, Renter, Rented, setup_db, \
    db_drop_and_create_all

app = Flask(__name__)
setup_db(app)


# db_drop_and_create_all()


@app.route('/')
@app.route('/plants')
def get_plants():
    """A list of all available plants
    :return:
    """

    results = Catalog.query.all()

    if results:
        plants = [plant.short() for plant in results]

        return jsonify({
            'success': True,
            'plants': plants
        })

    return jsonify({
        'success': True,
        'message': 'The catalog is empty'
    })


@app.route('/invoice')
def get_renter_invoice():
    """View current invoice for the logged in renter
    :return:
    """
    pass


@app.route('/rented')
def get_rented_plants():
    """A list of all rented plants and who rented them
    :return:
    """
    pass


@app.route('/renters')
def get_renters():
    """View a list of all plant renters
    :return:
    """
    pass


@app.route('/add', methods=['POST'])
def add_plant():
    """Adds a new plant entry to the catalog
    :return:
    """
    pass


@app.route('/plant/<int:id>', methods=['PATCH'])
def update_plant_entry(id):
    """Upadte the plant entry by a given ID value
    :param id: integer id of the plant to update
    :return:
    """
    pass


@app.route('/plant/<int:id>', methods=['DELETE'])
def delete_plant(id):
    """Deletes the plant with the give ID value
    :param id: integer id for a given plant to be deleted
    :return:
    """
    pass


if __name__ == '__main__':
    app.run(debug=True)
