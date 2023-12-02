---
layout: default
---

# **Application.py** #

```python
# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: Application.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'Uses а Dаsh аррliсаtion to mаnаge user рet ԁаtа from аnimаl shelters.'
# =============================================================================
print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Course: ' + __course__)
print('Username: ' + __username__)
print('Password: ' + __password__)
print('Description: ' + __description__)
print('# ' + '=' * 78)


#Imports for libraries
from Authentication import authenticate_user, logout_user, get_current_user
import base64
import re
import dash_bootstrap_components as dbc
from bson import ObjectId
import dash
from passlib.hash import pbkdf2_sha256
from waitress import serve
from dash import Dash, dcc, html, Input, Output, State, callback, MATCH, no_update, ALL, dash_table as dt
from dash.exceptions import PreventUpdate
import dash_leaflet as dl
import pandas as pd
from pymongo import MongoClient
from AnimalClass import AnimalShelter

# Loads data from file
try:
    # Reading a CSV file has a time complexity of O(N), where N is the number of rows in the file.
    df = pd.read_csv('animal_data.csv', index_col=0)
    animal_id_index = df.columns.get_loc('animal_id')
    df = df.astype(str)
    df.insert(animal_id_index, 'count_down_column', df.index.astype(str))
    unnamed_column = df.pop(df.columns[0])
    df.insert(0, 'Unnamed_Column', unnamed_column)
except FileNotFoundError:
    df = pd.DataFrame()

# Defines the login modal layout and location with chosen customizations
login_modal = dbc.Modal(
    [
        dbc.ModalHeader("Login"),
        dbc.ModalBody(
            [
                dcc.Input(id='username-input-modal', type='text', placeholder='Enter your username'),
                dcc.Input(id='password-input-modal', type='password', placeholder='Enter your password'),
                html.Div(id='login-message-modal', style={'color': 'red'})
            ]
        ),
        dbc.ModalFooter(
            dbc.Button('Login', id='login-button-modal', n_clicks=0, color='primary'),
        ),
    ],
    id='login-modal',
    is_open=False,
)

# Initialize the Dash app with Bootstrap components CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Print DataFrame columns and first few rows for inspection
print(df.columns)
print(df.head())

# Connections to MongoDB
client = MongoClient('mongodb://myUserAdmins2:123456@localhost:27017/AAC?authSource=AAC')
db = client['AAC']
collection = db['animals']
collection_users = db['users']

# Initialize the DataFrame with records from MongoDB
# Fetching records from MongoDB has a time complexity of O(N), where N is the number of records.
df = pd.DataFrame(list(collection.find({}, projection={'_id': 0})))

# Ensure 'Chip_ID' column is added only once and exclude '_id' field
if 'Chip_ID' not in df.columns:
    df['Chip_ID'] = ''

# Ensure 'animal_id' column is added if it can't be found
# Adding a column to a DataFrame has a time complexity of O(N), where N is the number of rows in the DataFrame.
if 'animal_id' not in df.columns:
    df['animal_id'] = range(1, len(df) + 1)

# Define order of columns for DataTable
columns_order = [
    {"name": "animal_id", "id": "animal_id", "deletable": False, "selectable": True},
    {"name": "Chip_ID", "id": "Chip_ID", "deletable": False, "selectable": True, "presentation": "dropdown"},
] + [
    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
    if i not in ["animal_id", "Chip_ID"] and i != "1"  # Exclude unexpected '1' column
]

# Function to create regex pattern
def create_regex_pattern(keywords):
    return re.compile(".*" + ".*|.*".join(keywords) + ".*", re.IGNORECASE)

# Retrieves data based on filter criteria
def get_filtered_data(shelter, breed_keywords, sex, min_age, max_age, location_lat=None, location_long=None):
    query = {"$or": [{"breed": {"$regex": create_regex_pattern(breed_keywords)}}]}
    if sex is not None:
        query["sex_upon_outcome"] = sex
    query["age_upon_outcome_in_weeks"] = {"$gte": min_age, "$lte": max_age}

    # Add latitude and longitude filtering if provided
    if location_lat is not None and location_long is not None:
        query["location_lat"] = location_lat
        query["location_long"] = location_long

    return pd.DataFrame.from_records(shelter.getRecordCriteria(query))

# Dictionary Criteria
filter_criteria = {
    'All': {
        'breed_keywords': [],
        'sex': "Intact Male",
        'min_age': 1,
        'max_age': 2
    },
    'Water': {
        'breed_keywords': ['newf', 'chesa', 'lab'],
        'sex': "Intact Female",
        'min_age': 26.0,
        'max_age': 156.0
    },
    'Mountain': {
        'breed_keywords': ['german', 'mala', 'old english', 'husk', 'rott'],
        'sex': "Intact Male",
        'min_age': 26.0,
        'max_age': 156.0
    },
    'Disaster': {
        'breed_keywords': ['german', 'golden', 'blood', 'dober', 'rott'],
        'sex': "Intact Male",
        'min_age': 20.0,
        'max_age': 300.0
    }
}

# Credentials to connect to MongoDB
app.config.suppress_callback_exceptions = True
username = "myUserAdmins2"
password = "123456"
shelter = AnimalShelter(password, username)
df = pd.DataFrame.from_records(collection.find({}, projection={'_id': 0}))

# Adding image for logo on Dashboard
with open('Grazioso_Salvare_Logo.png', 'rb') as f:
    encoded_image = base64.b64encode(f.read())

# Global variable for filter type
current_filter_type = 'All'

# Layout of the app criteria
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.A([
        html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                             height=250, width=251))], href='https://www.snhu.edu', target="_blank"),
    html.Center(html.B(html.H1('CS499 Artifact Two Enhancement'))),
    html.Hr(),
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Water Rescue', 'value': 'Water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label': 'Disaster Rescue or Individual Tracking', 'value': 'Disaster'},
        ],
        value='All'
    ),
    html.Hr(),

    # Adds the button to show register page
    html.Button('Open Register', id='open-register-button-modal', n_clicks=0),
    dbc.Modal(
        [
            dbc.ModalHeader("Register"),
            dbc.ModalBody(
                [
                    dcc.Input(id='register-username-input-modal', type='text', placeholder='Enter your username'),
                    dcc.Input(id='register-password-input-modal', type='password', placeholder='Enter your password'),
                    html.Div(id='register-message-modal', style={'color': 'red'})
                ]
            ),
            dbc.ModalFooter(
                dbc.Button('Register', id='register-button-modal', n_clicks=0, color='primary'),
            ),
        ],
        id='register-modal',
        is_open=False,
    ),

    # Adds the button component for add animal
    html.Div([
        html.H3('Add New Animal Data', style={'textAlign': 'center'}),
        dcc.Input(id='new-animal-name', type='text', placeholder='Animal Name'),
        dcc.Input(id='new-animal-breed', type='text', placeholder='Breed'),
        dcc.Input(id='new-animal-age', type='number', placeholder='Age in Weeks'),
        dcc.Input(id='new-animal-sex', type='text', placeholder='Sex'),
        dcc.Input(id='new-animal-chip-id', type='text', placeholder='Chip ID'),
        html.Div(id='debug-output'),
        html.Button('Add Animal', id='add-animal-button', n_clicks=0, disabled=True),
    ], style={'width': '100%', 'margin': 'auto', 'text-align': 'center'}),
    html.Hr(),

    # Parameters for the DataTable
    dt.DataTable(
        id='datatable-id',
        columns=columns_order,
        data=df.to_dict('records'),
        editable=True,
        row_selectable="single",
        selected_rows=[],
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Button('Open Login', id='open-login-button', style={'display': 'block'}),
    login_modal,
    html.Div(id='auth-status'),
    html.Br(),
    html.Hr(),

    # Map that uses the library leaflet to show where the animal is located, if data contains it
    html.Div(
        id='map-id',
        style={'width': '700px', 'height': '450px', 'margin': 'auto'},
    ),
])

# Callback for Add Animal button component with authentication
@app.callback(
    [
        Output('new-animal-name', 'value'),
        Output('new-animal-breed', 'value'),
        Output('new-animal-age', 'value'),
        Output('new-animal-sex', 'value'),
        Output('new-animal-chip-id', 'value'),
        Output('add-animal-button', 'disabled'),
    ],
    [
        Input('add-animal-button', 'n_clicks'),
        Input('auth-status', 'children'),
    ],
    [
        State('new-animal-name', 'value'),
        State('new-animal-breed', 'value'),
        State('new-animal-age', 'value'),
        State('new-animal-sex', 'value'),
        State('new-animal-chip-id', 'value'),
    ],
    prevent_initial_call=True
)
def handle_add_animal_button(n_clicks, auth_status, name, breed, age, sex, chip_id):
    # Checks the status of authorization
    if auth_status is not None:
        return '', '', '', '', '', False
    else:
        return '', '', '', '', '', True


# Callback for the login button component
@app.callback(
    [
        Output('auth-status', 'children'),
        Output('login-modal', 'is_open'),
        Output('login-message-modal', 'children'),
        Output('url', 'pathname'),
    ],
    [
        Input('login-button-modal', 'n_clicks'),
        Input('open-login-button', 'n_clicks'),
    ],
    [
        State('username-input-modal', 'value'),
        State('password-input-modal', 'value'),
        State('url', 'pathname'),
        State('login-modal', 'is_open'),
    ],
    prevent_initial_call=True
)
def login_user(login_button_clicks, open_login_clicks, username, password, url_pathname, is_login_modal_open):
    try:
        # Checking if the login button is clicked on
        if login_button_clicks:
            # Authenticate the user
            authenticated = authenticate_user(username, password)

            if authenticated:
                # If authenticated the window will close and display a welcome message with the users name
                return (
                    f"Authentication Status: Welcome, {username}!",
                    False,
                    None,
                    url_pathname,
                )
            else:
                # What shows if the wrong credentials are entered.
                return (
                    "Authentication Status: Invalid username or password.",
                    True,
                    "Invalid username or password.",
                    url_pathname,
                )

        # Checking if the button is clicked
        elif open_login_clicks:
            # Open the login modal
            return no_update, True, no_update, no_update

        # Keeps you in the same state until action is used
        else:
            return no_update, no_update, no_update, no_update

    except Exception as e:
        print(f"Error in login callback: {str(e)}")
        return (
            f"Authentication Status: Error - {str(e)}",
            False,
            None,
            url_pathname,
        )

# Callback to switch the map marker depending on selected rows in the data
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "selected_rows")]
)
def update_map(selected_rows):
    global df
    toolTip = "Austin Animal Center"
    if not selected_rows:
        # Removes the map marker until a row is selected
        return [dl.Map(style={'width': '700px', 'height': '450px'}, center=(30.75, -97.48), zoom=10,
                       children=[dl.TileLayer(id="base-layer-id")])]

    try:
        dff = pd.DataFrame(df.iloc[selected_rows])
        if 'location_lat' in dff.columns and 'location_long' in dff.columns:
            coordLat = float(dff['location_lat'].to_string().split()[1])
            coordLong = float(dff['location_long'].to_string().split()[1])
            markerArray = (coordLat, coordLong)
        else:
            markerArray = (30.75, -97.48)

        popUpHeading = "Animal Name"
        popUpParagraph = dff['name'].iloc[0] if 'name' in dff.columns else "Unknown"

    except Exception as e:
        print(f"Error in update_map callback: {str(e)}")
        return dash.no_update

    print(f"Update Map callback - Marker Array: {markerArray}")
    print(f"Update Map callback - Data: {df.head()}")
    return [dl.Map(style={'width': '700px', 'height': '450px'}, center=markerArray,
                   zoom=10, children=[dl.TileLayer(id="base-layer-id"),
                                      dl.Marker(position=markerArray, children=[
                                          dl.Tooltip(toolTip),
                                          dl.Popup([
                                              html.H1(popUpHeading),
                                              html.P(popUpParagraph)
                                          ])
                                      ])
                                      ])
            ]

# Callback that updates the animal data with the filtering, combined it with the "Add Animal" button click.
@app.callback(
    Output('datatable-id', 'data'),
    [
        Input('filter-type', 'value'),
        Input('add-animal-button', 'n_clicks')
    ],
    [
        State('new-animal-name', 'value'),
        State('new-animal-breed', 'value'),
        State('new-animal-age', 'value'),
        State('new-animal-sex', 'value'),
        State('new-animal-chip-id', 'value'),  # Added Chip ID state
        State('datatable-id', 'data')
    ],
    prevent_initial_call=True
)
def update_data(selected_filter_type, n_clicks, name, breed, age, sex, chip_id, existing_data):
    global df, current_filter_type

    try:
        print("Triggered by:", dash.callback_context.triggered_id)

        if 'filter-type' in dash.callback_context.triggered_id:
            print("Filter type change")
            current_filter_type = selected_filter_type
            criteria = filter_criteria.get(current_filter_type, filter_criteria['All'])
            df_filtered = get_filtered_data(shelter, **criteria)

            # Controls NaN values
            df_filtered = df_filtered.fillna('')  # Values that don't exist is inputs a empty string to prevent errors.

            df = df_filtered.copy()

            # Makes ObjectId a string
            for record in df.to_dict('records'):
                if '_id' in record:
                    record['_id'] = str(record['_id'])

            print("Updated data:", df.to_dict('records'))
            return df.to_dict('records')

        elif 'add-animal-button' in dash.callback_context.triggered_id:
            print("Add animal button clicked")

            if n_clicks > 0:
                new_animal = {
                    'name': name,
                    'breed': breed,
                    'age_upon_outcome_in_weeks': age,
                    'sex_upon_outcome': sex,
                    'Chip_ID': chip_id  # The additiona Chip_ID column I added for new pet data
                }

                # Adds new animal data used to the MongoDB collection
                collection.insert_one(new_animal)

                # Allows new animal data to be show after adding
                df = pd.DataFrame(list(collection.find({}, projection={'_id': 0})))

                # Saves data without index column
                df.to_csv('animal_data.csv', index=False)

            for record in df.to_dict('records'):
                if '_id' in record:
                    record['_id'] = str(record['_id'])

            print("Updated data:", df.to_dict('records'))
            return df.to_dict('records')

    except Exception as e:
        print(f"Error: {str(e)}")
        return dash.no_update


@app.callback(
    [
        Output('register-modal', 'is_open'),
        Output('register-message-modal', 'children'),
        Output('debug-output', 'children'),
    ],
    [
        Input('open-register-button-modal', 'n_clicks'),
        Input('register-button-modal', 'n_clicks'),
    ],
    [
        State('register-username-input-modal', 'value'),
        State('register-password-input-modal', 'value'),
        State('register-modal', 'is_open'),
    ],
    prevent_initial_call=True
)
def manage_register_modal(open_clicks, register_button_clicks, register_username, register_password, is_register_modal_open):
    try:
        print("Callback triggered.")
        print(f"open_clicks: {open_clicks}, register_button_clicks: {register_button_clicks}")
        print(f"register_username: {register_username}, register_password: {register_password}, is_register_modal_open: {is_register_modal_open}")

        # Checks if you try to open register window
        if open_clicks and not register_button_clicks:
            print("Open Register button clicked.")
            return not is_register_modal_open, None, None

        # Checks if you click the register button inside open register window
        elif register_button_clicks:
            print("Register button clicked.")
            # How I check if the username entered is already taken
            existing_user = collection_users.find_one({'username': register_username})
            if existing_user:
                print("Username already exists.")
                return is_register_modal_open, "Username already exists. Choose a different one.", None

            # Hashes the password for security
            hashed_password = pbkdf2_sha256.hash(register_password)

            # adds the new user to the users collection in the database
            result = collection_users.insert_one({'username': register_username, 'password': hashed_password})

            # Verify user was added
            if result.inserted_id:
                print("Registration successful. You can now log in.")
                return False, "Registration successful. You can now log in.", None
            else:
                print("Error during user registration.")
                return is_register_modal_open, "Error during user registration.", None

        # Keeps window open until action
        else:
            print("No button clicked.")
            return is_register_modal_open, None, None

    except Exception as e:
        print(f"Error in registration callback: {str(e)}")
        return is_register_modal_open, f"Error during registration: {str(e)}", None


if __name__ == '__main__':
    serve(app.server, host='0.0.0.0', port=8050)
```

# **AnimalClass.py** #

```python
# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: AnimalClass.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'Manages the class used in the Application.py which is "AnimalShelter".'
# =============================================================================
print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Course: ' + __course__)
print('Username: ' + __username__)
print('Password: ' + __password__)
print('Description: ' + __description__)
print('# ' + '=' * 78)




from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

class AnimalShelter(object):
    _instance = None  # Class variable to store the instance

    def __new__(cls, _password, _username='aacUser'):
        if cls._instance is None:
            # Creating a new instance involves setting up a MongoDB client connection,
            # assuming MongoClient connection setup has a constant time complexity.
            cls._instance = super(AnimalShelter, cls).__new__(cls)
            username = urllib.parse.quote_plus(_username)
            password = urllib.parse.quote_plus(_password)
            # Overall time complexity of creating a new instance is O(1).
            cls._instance.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/?authSource=AAC')
            cls._instance.dataBase = cls._instance.client['AAC']
        return cls._instance

    def __init__(self, _password, _username='myUserAdmins2'):
        # Property variables
        self.records_updated = 0  # Variable to store the number of records updated
        self.records_matched = 0  # Variable to store the number of records matched
        self.records_deleted = 0  # Variable to store the number of records deleted

    def createRecord(self, data):
        if data:
            _insert_valid = self.dataBase.animals.insert_one(data)
            return _insert_valid.acknowledged
        else:
            return False  # or raise an exception if needed

    def getRecordId(self, post_id):
        _data = self.dataBase.animals.find_one({'_id': ObjectId(post_id)})
        return _data

    def getRecordCriteria(self, criteria):
        if criteria:
            _data = list(self.dataBase.animals.find(criteria, {'_id': 0}))
        else:
            _data = list(self.dataBase.animals.find({}, {'_id': 0}))
        return _data

    def updateRecord(self, query, new_value):
        if not query:
            raise Exception("No search criteria is present.")
        elif not new_value:
            raise Exception("No update value is present.")
        else:
            _update_valid = self.dataBase.animals.update_many(query, {"$set": new_value})
            self.records_updated = _update_valid.modified_count
            self.records_matched = _update_valid.matched_count
            return _update_valid.modified_count > 0

    def deleteRecord(self, query):
        if not query:
            raise Exception("No search criteria is present.")
        else:
            _delete_valid = self.dataBase.animals.delete_many(query)
            self.records_deleted = _delete_valid.deleted_count
            return _delete_valid.deleted_count > 0

    def addAnimal(self, name, breed, age, sex):
        new_animal = {'name': name, 'breed': breed, 'age_upon_outcome_in_weeks': age, 'sex_upon_outcome': sex}
        return self.createRecord(new_animal)
```

# **Authentication.py** #

```python
# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: Authentication.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'Authentication control for user login and logout'
# =============================================================================
print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Course: ' + __course__)
print('Username: ' + __username__)
print('Password: ' + __password__)
print('Description: ' + __description__)
print('# ' + '=' * 78)


from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://myUserAdmins2:123456@localhost:27017/AAC?authSource=AAC')
db = client['AAC']  # Name of the database
collection_users = db['users']  # Collection registered users are stored in.

def authenticate_user(username, password):
    # Find the user in the 'users' collection by username
    user = collection_users.find_one({'username': username})

    if user and pbkdf2_sha256.verify(password, user['password']):
        return True
    else:
        return False

def logout_user():
    global current_user
    current_user = None

current_user = None  # Global variable to store the current user

def authenticate_user(username, password):
    global current_user
    # Searches 'users' collection for username
    user = collection_users.find_one({'username': username})

    if user and pbkdf2_sha256.verify(password, user['password']):
        current_user = username  # Sets the current user
        return True
    else:
        current_user = None  # Resets the current user on failed authentication
        return False

def get_current_user():
    return current_user
```

# **WSGI_Server.py** #

```python
# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: WSGI_Server.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'File used to start wsgi server'
# =============================================================================
print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Course: ' + __course__)
print('Username: ' + __username__)
print('Password: ' + __password__)
print('Description: ' + __description__)
print('# ' + '=' * 78)

from Application import app
from Authentication import authenticate_user, logout_user, get_current_user

if __name__ == "__main__":
    app.run_server()
```

[back](./)
