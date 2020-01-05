import os
from sqlalchemy import Column, String, Integer, Float
from flask_sqlalchemy import SQLAlchemy
import json

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(
#     os.path.join(project_dir, database_filename))

database_name = 'plant_catalog'
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app):
    """Binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """Drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple
    verisons of a database
    """
    db.drop_all()
    db.create_all()


class Catalog(db.Model):
    """A persistent plant 'catalog' entity.
    Extends the base SQLAlchemy Model
    """
    __tablename__ = 'Catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    description = Column(String(), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    renters = db.relationship('Rented', backref='Catalog', lazy=True)

    def short(self):
        """Short form representation of the Catalog model"""

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def long(self):
        """Long form representation of the Catalog model"""

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
        }

    def insert(self):
        """Inserts a new model into a database
        the model must have a unique name
        the model must have a description
        the model must have a quantity
        the model must have a price
        EXAMPLE
            plant = Catalog(name=req_name, description=req_desc,
                quantity=req_count, price=req_price)
            plant.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a new model from a database
        the model must exist in the database
        EXAMPLE
            plant = Catalog(name=req_name, description=req_desc,
                quantity=req_count, price=req_price)
            plant.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a new model into a database
        the model must exist in the database
        EXAMPLE
            plant = Catalog.query.filter(plant.id == id).one_or_none()
            plant.title = 'Coffee'
            plant.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Renter(db.Model):
    """A persistent plant 'Renter' entity.
    Extends the base SQLAlchemy Model
    """
    __tablename__ = 'Renter'

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    address = Column(String(), nullable=False)
    city = Column(String(), nullable=False)
    state = Column(String(), nullable=False)

    plants = db.relationship('Rented', backref='Renter', lazy=True)

    def short(self):
        """Short form representation of the Renter model"""

        return {
            'id': self.id,
            'name': self.name,
        }

    def long(self):
        """Long form representation of the Renter model"""

        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state
        }

    def insert(self):
        """Inserts a new model into a database
        the model must have a unique name
        the model must have a address
        the model must have a city
        the model must have a state
        EXAMPLE
            renter = Renter(name=req_name, address=req_addr,
                city=req_city, state=req_state)
            renter.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a new model from a database
        the model must exist in the database
        EXAMPLE
            renter = Renter(name=req_name, address=req_addr,
                city=req_city, state=req_state)
            renter.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a new model into a database
        the model must exist in the database
        EXAMPLE
            renter = Renter(name=req_name, address=req_addr,
                city=req_city, state=req_state)
            renter.address = '1234 ABC Lane'
            renter.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Rented(db.Model):
    """A persistent plant 'Rented' entity.
    Extends the base SQLAlchemy Model
    """
    __tablename__ = 'Rented'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, db.ForeignKey('Catalog.id'), nullable=False)
    renter_id = Column(Integer, db.ForeignKey('Renter.id'), nullable=False)

    def values(self):
        """Representation of the Rented model"""

        return {
            'id': self.id,
            'plant_id': self.plant_id,
            'renter_id': self.renter_id,
        }

    def insert(self):
        """Inserts a new model into a database
        the model must have a plant id
        the model must have a renter id
        EXAMPLE
            rented = Rented(plant_id=req_plant_id, renter_id=req_renter_id)
            rented.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a new model from a database
        the model must exist in the database
        EXAMPLE
            rented = Rented(plant_id=req_plant_id, renter_id=req_renter_id)
            rented.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """Updates a new model into a database
        the model must exist in the database
        EXAMPLE
            rented = Rented.query.filter(plant.id == id).one_or_none()
            renter.renter_id = 6
            renter.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
