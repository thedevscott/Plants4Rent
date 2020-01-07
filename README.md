Plants4Rent API (Udacity Capstone)
------------------

## Introduction
Plants4Rent is growing and needs and API to support its digital business needs.
This API has 8 endpoints explained in the "API Docs" section and is
accompanied by a postman_collection for convenience. Note that the
appropriate [auth0](https://auth0.com/) application and api needs to be setup 
with the permission mentioned in the "API Docs-Permissions" section.

[Auth0Login](https://thedevscott.auth0.com/authorize?audience=rentPlants&response_type=token&client_id=wZdUp09vKapcFGclks5MXlbuU0L81F20&redirect_uri=http://localhost:5000) for this project

## Installing Dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform 
in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for 
projects. This keeps your dependencies for each project separate and organaized.
Instructions for setting up a virual enviornment for your platform can be found 
in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r backend/requirements.txt
```

OR

```bash
pipenv install
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices 
framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [psycopg2](https://pypi.org/project/psycopg2/) is used for connecting to
 the POSTGRES database

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object 
Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Local Development

#### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:invoice`	
    - `get:rented`
    - `get:renters`	
    - `post:plants`
    - `patch:plants`
    - `delete:plants`

6. Create new roles for:
    - Renter
        - can `get:invoice`
        - can `get:renter`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Renter role to one and Manager role to the
     other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `plant-rental.postman_collection.json` 
    - Right-clicking the collection folder for renter and manager, navigate to
     the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.

#### Database setup
- Install ['psql'](https://www.postgresql.org/docs/current/tutorial-install.html)
- Create the databases using the 'createdb' command
```bash
createdb plant_catalog
createdb plant_catalog_test
```
- Populate the database by calling the 'populate' function in 'backend/load_db.py' 


#### Environment Variables
[The ENV file](./backend/environment_vars.sh) contains all the environment
 variables used by this project. They can be set by copying, updating and
  pasting the following into your terminal to match your setup:

```bash
# Development server
export FLASK_APP=backend/app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# AUTH0 Setup. Replace these with your own values
export AUTH0_DOMAIN="thedevscott.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="rentPlants"

# Database setup. Update these according to your setup
export DATABASE_NAME="plant_catalog"
export DATABASE_HOST="localhost:5432"
export DATABASE_PATH="postgres://localhost:5432/plant_catalog"

# For test_app.py. Get the JWTs from the URL when logging
export RENTER_TOKEN="<VALID_JWT>"
export OWNER_TOKEN="<VALID_JWT>"
export DATABASE_TEST_NAME="plant_catalog_test"
export DATABASE_TEST_PATH="postgresql://localhost:5432/plant_catalog_test"
```
 
## Running the server

From within the `./backend` directory first ensure you are working using your
 created virtual environment.

Each time you open a new terminal session, run:

NOTE: Only do this if you skipped it above
```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Using Pycharm
- Install the Community version of [PyCharm](https://www.jetbrains.com/pycharm/download)
- Download and Unzip this project
- Open the unzipped project in Pycharm
- Select and interpreter
    - Preferences -> Project:plants4rent -> Project Interpreter
    - Click the gear icon next to the drop down
    - Click add, a window will open
    - Click "Pipenv Environment"
    - Next to 'Base interpreter' select python3.7
    - Ensure 'Install packages from Pipfile' is checked
    - Click Ok
    - Wait for packages to install
    - Click apply & Click Ok
 - Edit and Copy the following:
 ```bash
FLASK_APP=backend/app.py
FLASK_ENV=development
FLASK_DEBUG=1
AUTH0_DOMAIN=thedevscott.auth0.com
ALGORITHMS=RS256
API_AUDIENCE=rentPlants
DATABASE_NAME=plant_catalog
DATABASE_HOST=localhost:5432
DATABASE_PATH=postgres://localhost:5432/plant_catalog
RENTER_TOKEN=VALID_JWT
OWNER_TOKEN=VALID_JWT
DATABASE_TEST_NAME=plant_catalog_test
DATABASE_TEST_PATH=postgresql://localhost:5432/plant_catalog_test
```

 - Open app.py
    - From the menu, click Run and click 'Run app'
    - Stop the app by clicking the red square
    - From the menu, click Run -> Edit Configurations
        - Add the Environment variables by
            - Clicking the Browse icon next to 'Environment variables' field
            - Click the Paste icon to paste the environment variables
            - Click Apply, Click Ok
 - Run the app again
 - Open localhost:5000 in the browser and you should see the plant list
    - This depends on the database setup step above

## Deploying

### Live App Access
This app is deployed on Heroku at [this](https://scott-plants4rent.herokuapp.com/)
address. Click [here](https://thedevscott.auth0.com/authorize?audience=rentPlants&response_type=token&client_id=wZdUp09vKapcFGclks5MXlbuU0L81F20&redirect_uri=https://scott-plants4rent.herokuapp.com/)
 to login/SingUp

### Deploying to Heroku
- Download and unzip the app
- Open a terminal and cd to the app's directory
- Create an account on [Heroku](https://signup.heroku.com/)
- Install Heroku via [command line](https://devcenter.heroku.com/categories/command-line)
    ```bash
    # Mac
    brew tap heroku/brew && brew install heroku
    ```
- Verify install
    ```bash
    which heroku
    ```
- Login via command line
    ```bash
    heroku login
    ```
- Create the Heroku app
    ```bash
     heroku create <name_of_your_app>
    ```
    The output will include a git url for your Heroku application. Copy this as, 
    we'll use it in a moment.

    Now if you check your Heroku Dashboard in the browser, you'll see an 
    application by that name. But it doesn't have our code or anything yet - 
    it's completely empty. Let's get our code up there.
- Add git remote for Heroku to local repository
    ```bash
    remote add heroku <heroku_git_url>
    ```
- Create the DB for your app, note the <HEROKU_DB_PATH> for later steps
    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --app <your_app_name>
    ```
    The app name is the name you used when creating the heroku app.
    
    Run 
    ```bash 
    heroku config --app <your_app_name>
    ``` in order to check your configuration variables in Heroku. You will
   see DATABASE_URL and the URL of the database you just created.
- Populate the database via [load_db](backend/load_db.py)
    - Update your DATABASE_PATH to <HEROKU_DB_PATH>, DATABASE_URL from the
     config
    - From the Heroku app Setting tab, change DATABASE_URL to DATABASE_PATH
     as the app is looking for DATABASE_PATH
    - Run load_db.py go() function to populate the DB

- Setup environment variables
    * From the Heroku dashboard: 
        - click your apps name 
        - click Settings
        - click Reveal Config Vars
        
    * Fill in the following key value pairs with your Auth0 data:
        ```bash
        # Example
        AUTH0_DOMAIN=thedevscott.auth0.com
        ALGORITHMS=RS256
        API_AUDIENCE=rentPlants
        
        DATABASE_PATH=<HEROKU_DB_PATH>
        ```
- Push the app to Heroku
  ```bash
    git push heroku master
    ```
- Open you app's URL in a browser and you should see the plant list
  

## API Docs
### Permissions
    - `get:invoice`	
    - `get:rented`
    - `get:renters`	
    - `post:plants`
    - `patch:plants`
    - `delete:plants`
### Endpoints
* GET /
* GET /plants
    - Description A list of all available plants
    - Permission: None
    - Request Arguments: None
    - Error Codes: 404
    - Return: Status code 200 and JSON with keys: 'success', 'message
    ' & 'plants'
    
* GET /plants/<int:id>
    - Description: View selected plant by given id
    - Permission: None
    - Request Arguments: integer id value as part of URL
    - Error Codes: 404
    - Return: Status code 200 and JSON with keys: 'success', 'message' & 'plants'

* GET /invoice/<int:renter_id>
    - Description: View current invoice for the specified renter by id
    - Permission: 'get:invoice'
    - Request Arguments: renter_id integer value in URL
    - Error Codes: 404, 400, 401, 403
    - Return: Status code 200 and JSON with keys 'success', 'invoice' & 'total'
    
* GET /rented
    - Description: A list of all rented plants and who rented them
    - Permission: 'get:rented'
    - Request Arguments: None
    - Error Codes: 404, 400, 401, 403
    - Return: Status code 200 and JSON with keys 'success', 'message' & 'data'

* GET /renters
    - Description: View a list of all plant renters
    - Permission: 'get:renters'
    - Request Arguments: None
    - Error Codes: 404, 400, 401, 403
    - Return: Status code 200 and JSON with keys 'success' & 'data' (id, name, address, city, state)

* POST /add
    - Description: Adds a new plant entry to the catalog
    - Permission: 'post:plants'
    - Request Arguments: JSON of plant to add with keys 'name', 'description',
     'quantity' and 'price'
    - Error Codes: 422, 400, 401, 403
    - Return: Status code 200 and JSON of plant added to DB
    
* PATCH /plants/<int:plant_id>
    - Description: Upadte the plant entry by a given ID value
    - Permission: 'patch:plants'
    - Request Arguments: JSON of plant to add with keys 'name', 'description',
     'quantity' and 'price'
    - Error Codes: 422, 400, 401, 403
    - Return: Status code 200 and JSON of updated plant
    
* DELETE /plants/<int:plant_id>
    - Description: Deletes the plant with the give ID value
    - Permission: 'delete:plants'
    - Request Arguments: plant_id via URL
    - Error Codes: 422, 400, 401, 403
    - Return: Status code 200 and JSON with keys 'success' & 'id' of deleted plant
