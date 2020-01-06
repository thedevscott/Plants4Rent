from flask import Flask, request, abort, jsonify

from flask_cors import CORS
from backend.database.models import Catalog, Renter, Rented, setup_db, \
    db_drop_and_create_all
from backend.auth.auth import AuthError, requires_auth
from backend.database.models import database_path

app = Flask(__name__)
setup_db(app, database_path)
CORS(app)


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------

@app.route('/')
@app.route('/plants')
def get_plants():
    """A list of all available plants
    :return: JSON with keys: 'success', 'message' & 'plants'
    """
    try:
        results = Catalog.query.all()

        if results:
            plants = [plant.short() for plant in results]

            return jsonify({
                'success': True,
                'plants': plants,
                'message': 'Enjoy our wonderful selection'
            })

        return jsonify({
            'success': True,
            'message': 'The catalog is empty',
            'plants': None
        })
    except Exception as e:
        print(str(e))
        abort(404)


@app.route('/plants/<int:plant_id>')
def get_plants_by_id(plant_id):
    """View selected plant by given id
    :return: JSON with keys: 'success', 'message' & 'plants'
    """
    try:
        results = Catalog.query.get_or_404(plant_id)

        return jsonify({
            'success': True,
            'plants': results.long(),
            'message': 'Enjoy this wonderful plant'
        })
    except Exception as e:
        abort(404)


@app.route('/invoice/<int:renter_id>')
@requires_auth('get:invoice')
def get_renter_invoice(jwt, renter_id):
    """View current invoice for the specified renter
    :return: JSON with keys 'success', 'invoice' & 'total'
    """
    try:
        results = Rented.query.filter_by(renter_id=renter_id).all()

        if not results:
            return jsonify({
                'success': True,
                'invoice': None,
                'total': 0.0
            })

        # Build the invoice
        invoice = {}
        total = 0.0

        for rental in results:
            plant_name = rental.Catalog.long()['name']
            plant_price = rental.Catalog.long()['price']

            total += plant_price

            if plant_name not in invoice:
                entry = {
                    'count': 1,
                    'price': plant_price
                }
                invoice[plant_name] = entry
            else:
                invoice[plant_name]['count'] += 1
                invoice[plant_name]['price'] += plant_price

        return jsonify({
            'success': True,
            'invoice': invoice,
            'total': total
        })
    except Exception as e:
        abort(404)


@app.route('/rented')
@requires_auth('get:rented')
def get_rented_plants(jwt):
    """A list of all rented plants and who rented them
    :return: JSON with keys 'success', 'message' & 'data'
    """
    try:
        results = Rented.query.all()
        data = {}

        if not results:
            return jsonify({
                'success': True,
                'message': 'Get some clients',
                'data': None
            })

        for entry in results:
            client_name = entry.Renter.name
            plant_name = entry.Catalog.name
            plant_price = entry.Catalog.price

            # New client entry
            if client_name not in data:
                # Make dict for this clients plants
                data[client_name] = {}
                data[client_name]['total'] = plant_price
            else:
                data[client_name]['total'] += plant_price

            # Update existing plant
            if plant_name in data[client_name]:
                data[client_name][plant_name]['count'] += 1
                data[client_name][plant_name]['price'] += plant_price
            else:
                # Add new plant
                data_entry = {
                    'name': plant_name,
                    'count': 1,
                    'price': plant_price
                }
                data[client_name][plant_name] = data_entry

        return jsonify({
            'success': True,
            'message': 'Follow up & keep the plants alive',
            'data': data
        })
    except Exception as e:
        abort(404)


@app.route('/renters')
@requires_auth('get:renters')
def get_renters(jwt):
    """View a list of all plant renters
    :return: JSON with keys 'success' & 'data' (id, name, address, city, state)
    """
    try:
        results = Renter.query.all()
        data = []
        if not results:
            return jsonify({
                'success': True,
                'data': None
            })

        data = [renter.long() for renter in results]

        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        abort(404)


@app.route('/add', methods=['POST'])
@requires_auth('post:plants')
def add_plant(jwt):
    """Adds a new plant entry to the catalog
    :return: JSON of plant added to DB
    """
    try:
        plant = Catalog(name=request.json.get('name'),
                        description=request.json.get('description'),
                        quantity=request.json.get('quantity'),
                        price=request.json.get('price'))

        plant.insert()

        return jsonify({
            'success': True,
            'plant': plant.long()
        })
    except Exception as e:
        abort(422)


@app.route('/plants/<int:plant_id>', methods=['PATCH'])
@requires_auth('patch:plants')
def update_plant_entry(jwt, plant_id):
    """Update the plant entry by a given ID value
    :param plant_id: integer id of the plant to update
    :return: JSON of updated plant
    """
    try:
        plant = Catalog.query.get_or_404(plant_id)
        plant.name = request.json.get('name')
        plant.description = request.json.get('description')
        plant.quantity = request.json.get('quantity')
        plant.price = request.json.get('price')

        plant.update()

        return jsonify({
            'success': True,
            'plant': plant.long()
        })
    except Exception as e:
        abort(422)


@app.route('/plants/<int:plant_id>', methods=['DELETE'])
@requires_auth('delete:plants')
def delete_plant(jwt, plant_id):
    """Deletes the plant with the give ID value
    :param plant_id: integer id for a given plant to be deleted
    :return: JSON with keys 'success' & 'id' of deleted plant
    """
    try:
        plant = Catalog.query.get_or_404(plant_id)

        plant.delete()

        return jsonify({
            'success': True,
            'id': plant_id
        })
    except Exception as e:
        abort(422)


# ----------------------------------------------------------------------------
# Error Handlers
# ----------------------------------------------------------------------------
@app.errorhandler(422)
def unprocessable(error):
    """Error handling for unprocessable entity
    :param error: The error object
    :return JSON indication failure with keys 'success', 'error' & 'message'
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404 HTTP status code
    :param error: The error object
    :return: JSON indicating failure 'success' bool, 'error' code & 'message'
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    """Authorization error handler. Takes AuthErrors and puts them in JSON
    format
    :param error: The error object
    :return JSON with 'code' and 'description' of the authorization error
    """

    return jsonify(error.error), error.status_code


if __name__ == '__main__':
    app.run(debug=True)
