---
layout: default
---

# **Artifact_2.py** #

```python
# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: Artifact_2.py
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
import re  # needed for the regex pattern matching

from dash import dcc
from dash import html
import dash_leaflet as dl
from dash import dash_table as dt
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
import base64

from AnimalShelter_CRUD import AnimalShelter


# Function to create regex pattern
def create_regex_pattern(keywords):
    return re.compile(".*" + ".*|.*".join(keywords) + ".*", re.IGNORECASE)


# Function to retrieve data based on filter criteria
def get_filtered_data(shelter, breed_keywords, sex, min_age, max_age):
    query = {"$or": [{"breed": {"$regex": create_regex_pattern(breed_keywords)}}]}
    if sex is not None:
        query["sex_upon_outcome"] = sex
    query["age_upon_outcome_in_weeks"] = {"$gte": min_age, "$lte": max_age}
    return pd.DataFrame.from_records(shelter.getRecordCriteria(query))


# Filter criteria dictionary
filter_criteria = {
    'All': {
    'breed_keywords': [],
    'sex': None,  # Set it to None, so it won't filter by sex
    'min_age': 0.0,
    'max_age': 999.0
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

# Initialize app and shelter
app = JupyterDash('SimpleExample')
username = "myUserAdmins2"
password = "123456"
shelter = AnimalShelter(password, username)
df = pd.DataFrame.from_records(shelter.getRecordCriteria({}))

image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# App layout
app.layout = html.Div([
    # create an anchor for the image/logo
    # make the image a href to the website, www.snhu.edu
    # open the link in a new tab by setting a blank target
    html.A([
        html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                             height=250, width=251))], href='https://www.snhu.edu', target="_blank"),
    html.Center(html.B(html.H1('CS499 Artifact Two Enhancement'))),
    html.Hr(),
    # create the radio buttons to act as a filter
    # set the default on initial load to 'All'
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
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        row_selectable="single",  # allow a row to be selected
        selected_rows=[],
        filter_action="native",  # allow a filter
        sort_action="native",  # allow sorting
        page_action="native",  # enable pagination
        page_current=0,  # set start page
        page_size=10,  # set rows per page

    ),
    html.Br(),
    html.Hr(),
    # This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
             style={'display': 'flex', 'justify-content': 'center'},
             children=[
                 html.Div(
                     id='graph-id',
                     className='col s12 m6',
                 ),
                 html.Div(
                     id='map-id',
                     className='col s12 m6',
                 )
             ])
])


# Callbacks
@app.callback([Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    criteria = filter_criteria.get(filter_type, filter_criteria['All'])
    df = get_filtered_data(shelter, **criteria)
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data = df.to_dict('records')
    return data, columns


@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    dffPie = pd.DataFrame.from_dict(viewData)

    # Check if 'age_upon_outcome_in_weeks' exists in the DataFrame
    if 'age_upon_outcome_in_weeks' in dffPie.columns:
        # Convert 'age_upon_outcome_in_weeks' to numeric (if it's not already)
        dffPie['age_upon_outcome_in_weeks'] = pd.to_numeric(dffPie['age_upon_outcome_in_weeks'], errors='coerce')

        # Filter the data based on your criteria
        # For example, you might want to filter by age, breed, or any other column
        filtered_data = dffPie[dffPie['age_upon_outcome_in_weeks'] > 20]

        # Check if the DataFrame is empty
        if filtered_data.empty:
            return []

        return [
            dcc.Graph(
                figure=px.pie(filtered_data, names='breed')
            )
        ]
    else:
        # Return an empty list if the column doesn't exist
        return []


# call back for selecting a row and then plotting the geo-marker
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(virtualRows):
    # austin Texas is [30.75, -97.48]

    # create the views
    if not virtualRows:  # build a default view if there are no selected lines
        markerArray = (30.75, -97.48)  # default marker at Austin Animal Shelter
        toolTip = "Austin Animal Center"
        popUpHeading = "Austin Animal Center"
        popUpParagraph = "Shelter Home Location"

    else:  # build the contextual views based on the selection
        dff = pd.DataFrame(df.iloc[virtualRows])  # convert the datatable to a dataframe
        coordLat = float(dff['location_lat'].to_string().split()[1])  # strip out the lat
        coordLong = float(dff['location_long'].to_string().split()[1])  # strip out the long
        markerArray = (coordLat, coordLong)  # build the array based on selection

        toolTip = dff['breed']
        popUpHeading = "Animal Name"
        popUpParagraph = dff['name']

    # return the map with a child marker
    #  is set to the values found in markerArray
    # map centers/moves to view the new marker instead of holding a fixed center
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


# Run the app
if __name__ == '__main__':
    app.run_server(mode='jupyterlab', port=8090, dev_tools_ui=True, dev_tools_hot_reload=True, threaded=True)
```

# **AnimalShelter_CRUD.py** #

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse


class AnimalShelter(object):
    _instance = None  # Class variable to store the instance

    def __new__(cls, _password, _username='aacUser'):
        if cls._instance is None:
            cls._instance = super(AnimalShelter, cls).__new__(cls)
            username = urllib.parse.quote_plus(_username)
            password = urllib.parse.quote_plus(_password)
            cls._instance.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/?authSource=AAC')
            cls._instance.dataBase = cls._instance.client['AAC']
        return cls._instance

    def __init__(self, _password, _username='aacUser'):
        # Property variables
        self.records_updated = 0
        self.records_matched = 0
        self.records_deleted = 0

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
```

[back](./)
