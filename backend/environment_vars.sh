# Development server
FLASK_APP=backend/app.py
FLASK_ENV=development
FLASK_DEBUG=1

# AUTH0 Setup
AUTH0_DOMAIN="thedevscott.auth0.com"
ALGORITHMS="RS256"
API_AUDIENCE="rentPlants"

# Database setup
DATABASE_NAME="plant_catalog"
DATABASE_HOST="localhost:5432"
DATABASE_PATH="postgres://localhost:5432/plant_catalog"

# For test_app.py
RENTER_TOKEN="<VALID_JWT>"
OWNER_TOKEN="<VALID_JWT>"
DATABASE_TEST_NAME="plant_catalog_test"
DATABASE_TEST_PATH="postgresql://localhost:5432/plant_catalog_test"
