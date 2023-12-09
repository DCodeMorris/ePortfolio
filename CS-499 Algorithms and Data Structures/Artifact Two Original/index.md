---
layout: default
---

# **app.ipynb** #

```python
# =============================================================================
# Created By  : Dustin Morris
# =============================================================================
# Interpreter: Python 3.12
# File Name: app.ipynb
# =============================================================================


from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output
from bson.json_util import dumps

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from shelter import AnimalShelter



###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "myUserAdmins2"
password = "password"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read({}))


#########################
# Dashboard Layout / View
#########################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']                            
app = JupyterDash('SimpleExample')

app.layout = html.Div([
    dcc.RadioItems(
        id='rd',
        options=[
            {'label': 'Water Rescue', 'value': 'Water Rescue'},
            {'label': 'Mountain', 'value': 'Mountain or Wilderness Rescue'},
            {'label': 'Disaster Rescue ', 'value': 'Disaster Rescue or Individual Tracking'},
            {'label': 'Reset', 'value': 'Reset'}
        ],
        value='Water Rescue',
        labelStyle={'display': 'inline-block'}
    ),
    html.Hr(),
    html.Div(id='dd-output-container', children = [
            dash_table.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ])]),
    html.Hr(),
    html.Div(id='map-id'),
    html.Hr(),
    html.Div(id='graph-id')
    ])



   
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('rd', 'value')]
    )
def update_output(value):
    df = pd.DataFrame.from_records(shelter.read({}))
    
    if value == 'Water Rescue':
        df = pd.DataFrame.from_records(shelter.read({'$or':[{"breed":"Labrador Retriever Mix"},
                                                        {"breed":"Chesapeake Bay Retriever"},
                                                        {"breed":"Newfoundland"}
                                                       ],"age_upon_outcome_in_weeks":{'$gt':26,'$lt':156},
                                                    "sex_upon_outcome":"Intact Female"}))
    if value == 'Mountain or Wilderness Rescue':
    
        df = pd.DataFrame.from_records(shelter.read({'$or':[{"breed":"German Shepherd"},
                                                        {"breed":"Alaskan Malamute"},
                                                        {"breed":"Old English Sheepdog"},
                                                        {"breed":"Siberian Husky"} ,
                                                        {"breed":"Rottweiler"}  
                                                       ],"age_upon_outcome_in_weeks":{'$gt':26,'$lt':156},
                                                    "sex_upon_outcome":"Intact Male"}))
    if value == 'Disaster Rescue or Individual Tracking':
        df = pd.DataFrame.from_records(shelter.read({'$or':[{"breed":"German Shepherd"},
                                                        {"breed":"Doberman Pinscher"},
                                                        {"breed":"Golden Retriever"},
                                                        {"breed":"Bloodhound"} ,
                                                        {"breed":"Rottweiler"}  
                                                       ],"age_upon_outcome_in_weeks":{'$gt':20,'$lt':300},
                                                    "sex_upon_outcome":"Intact Male"}))
        
    return [
            dash_table.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ],
                data=df.to_dict('records'),
                editable=True,
                style_cell={'textAlign': 'left'},
                 style_cell_conditional=[
                {
                    'if': {'column_id': s},
                    'textAlign': 'left'
                } for s in ['animal_type','color','breed','animal_id']
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(0, 128, 0)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(0, 238, 0)',
                'fontWeight': 'bold'
            },
            
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,

            )
        
       ]



@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_map(viewData):
#FIXME Add in the code for your geolocation chart
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[30.75,-97.48], children=[
                dl.Tooltip(dff.iloc[0,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[0,10]),
                    html.H3("Animal Color"),
                    html.P(dff.iloc[0,5]),
                    html.H3("Animal ID"),
                    html.P(dff.iloc[0,2]),
                    
                ])
            ])
        ])
    ]


#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
app

```

[back](./)
