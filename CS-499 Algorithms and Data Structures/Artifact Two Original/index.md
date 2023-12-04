---
layout: default
---

# **

```python
# =============================================================================
# Created By  : Dustin Morris
# =============================================================================
# Interpreter: Python 3.12
# File Name: AnimalShelter.py
# =============================================================================


from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from animal_shelter import AnimalShelter





###########################
# Data Manipulation / Model
###########################
# FIX ME change for your username and password and CRUD Python module name
#username = "accuser"
#password = "changeme"
shelter = AnimalShelter(username, password)


# class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.read({})



#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_salvare_Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('CS-340 Dustin Morris'))),
    html.Hr(),
    html.Img(id='customer-image',src='data:image/jpeg;base64,{}'.format(encoded_image.decode()),alt='customer image'),
    html.Div(
        
#FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.


    ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
        page_size=10,
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'text-transform': 'capitalize'
        },
        filter_action="native",
        sort_mode="multi",
        sort_action="native"
        
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ]),
    
    html.H1('Cameron Carr The Greatest to Ever do IT!!')
])

#############################################
# Interaction Between Components / Controller
#############################################



    
@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
### FIX ME Add code to filter interactive data table with MongoDB queries
        
        
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
        data=df.to_dict('records')
        
        
        return (data,columns)




@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_graphs(viewData):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["breed"],
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            for column in ["breed", "animal_type", "date_of_birth"]
        ]
    )

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_map(viewData):
#FIXME: Add in the code for your geolocation chart
#If you completed the Module Six Assignment, you can copy in the code you created here.
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
                        html.P(dff.iloc[1,9])
                    ])
                ])
            ])
    ]


app
```

[back](./)
