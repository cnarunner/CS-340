# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configure CRUD class and database.
from CRUD import CRUD

###########################
# Data Manipulation / Model
###########################
# username and password and CRUD Python module name

username = "aacuser"
password = "simplepass"

# Connect to database via CRUD Module
crud = CRUD(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(crud.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
# df.drop(columns=['_id'],inplace=True)
df_good_col = df[["age_upon_outcome", "animal_id", "animal_type", "breed", "color", "date_of_birth", "name", "outcome_type",
          "sex_upon_outcome"]]

## Debug
print(len(df.to_dict(orient='records')))
print(df.columns)
print(df_good_col.columns)

#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

# Add in Grazioso Salvare’s logo
image_filename = 'GraziosoSalvareLogo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Place the HTML image tag in the line below into the app.layout code according to your design
# html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))


app.layout = html.Div([
    html.Div(className='row',
             style={'display': 'flex'},
             children=[
                 html.Div(id='hidden-div', style={'display': 'none'}),
                 html.A([
                     html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                              height=100, width=100
                              )
                 ],
                     href='https://www.snhu.edu', target='_blank'),
                 # Also remember to include a unique identifier such as your name or date
                 html.Center(html.B(html.H1(children=[
                     'Bryce Jensen',
                     html.Br(),
                     'SNHU - CS-340',
                     html.Br(),
                     'Grazioso Salvare Dashboard'
                 ])))
             ]
             ),

    html.Hr(),
    html.Div(
        # Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.

        dcc.RadioItems(
            id='filter_type',
            options=[
                {'label': "All (Reset)", 'value': "All"},
                {'label': "Water Rescue", 'value': "WaterR"},
                {'label': "Mountain or Wilderness Rescue", 'value': "MountainR"},
                {'label': "Disaster or Individual Tracking Rescue", 'value': "DisasterR"},
            ],
            value="All"
        )
    ),

    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df_good_col.columns
        ],
        data=df.to_dict('records'),
        # Set up the features for your interactive data table to make it user-friendly for your client
        editable=False,             # disable editing of data
        filter_action="native",     # Enable filtering
        sort_action="native",       # Enable sorting
        column_selectable=False,    # Disable column selecting
        row_selectable="single",    # Allow one row to be selected at a time
        row_deletable=False,        # Disable deletions
        selected_columns=[],        # No default column selected
        selected_rows=[0],          # The first row is selected by default
        page_action="native",       # Enable pages for table
        page_current=0,             # Sets current page to the first one
        page_size=10                # Only 10 table rows per page
    ),

    html.Br(),
    html.Hr(),

    # Dropdown for selecting what type of chart is shown.
    html.Div(
        dcc.Dropdown(
            id='graph_type',
            style=dict(
                width='40%',
                verticalAlign="middle"
            ),
            options=[
                {'label': "Bar Graph", 'value': 0},
                {'label': "Pie Chart", 'value': 1}
            ],
            value=0
        )
    ),
    # This sets up the dashboard so that the chart and geolocation chart are side-by-side
    html.Div(className='row',
             style={'display': 'flex'},
             children=[
                 html.Div(
                     id='graph-id',
                     className='col s12 m6',
                 ),
                 html.Div(
                     id='map-id',
                     className='col s12 m6',
                 )
             ]
             )
])


#############################################
# Interaction Between Components / Controller
#############################################
@app.callback([
    Output('datatable-id', 'data'),
    Output('datatable-id', 'columns')],
    [Input('filter_type', 'value')]
)
# code to filter interactive data table with MongoDB queries
def update_dashboard(filter_type):
    global df_new
    if filter_type == 'WaterR':
        df_new = pd.DataFrame.from_records(crud.read({
            "animal_type": 'Dog',
            'breed': {"$in": ["Labrador Retriever Mix",
                              "Chesapeake Bay Retriever",
                              "Newfoundland"
                              ]
                      },
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26.0,
                                          "$lte": 156.0
                                          }
        }))

    if filter_type == 'MountainR':
        df_new = pd.DataFrame.from_records(crud.read({
            "animal_type": 'Dog',
            'breed': {"$in": ["German Shepherd",
                              "Alaskan Malamute",
                              "Old English Sheepdog",
                              "Siberian Husky",
                              "Rottweiler"
                              ]
                      },
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26.0,
                                          "$lte": 156.0
                                          }
        }))

    elif filter_type == "DisasterR":
        df_new = pd.DataFrame.from_records(crud.read({
            "animal_type": 'Dog',
            'breed': {"$in": ["Doberman Pinscher",
                              "German Shepard",
                              "Golden Retriever",
                              "Bloodhound",
                              "Rottweiler"
                              ]
                      },
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20.0,
                                          "$lte": 300.0
                                          }
        }))

    elif filter_type == "All":
        df_new = df

    columns=[
            {"name": i,
             "id": i,
             "deletable": False,
             "selectable": True} for i in df_good_col.columns
        ]
    data = df_new.to_dict('records')

    return (data, columns)


# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('graph_type', 'value')])
def update_graphs(viewData, graph_type):
    # add code for chart of your choice (e.g. pie chart) #
    # graph_type = 1
    if graph_type == 0:
        graph_data = pd.DataFrame.from_dict(viewData)
        graph = px.histogram(
            graph_data,
            x='breed',
            height=750,
            width=1000,
            color='breed',
            title='Breed distribution',
            text_auto=True,
        ).update_xaxes(categoryorder='total descending')  # Sorts from most to least. (Looks nicer.)

        return [
            html.Div(children=[
                dcc.Graph(figure=graph)
            ])
        ]

    elif graph_type == 1:
        df = pd.DataFrame.from_dict(viewData)
        graph = px.pie(
            df,
            names='breed',
            title='Preferred Animals',
            height=500,
            width=1000
        )
        graph.update_traces(textposition='inside')
        graph.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return [
            html.Div(children=[
                dcc.Graph(figure=graph)
            ])
        ]


# This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
    if viewData is None:
        return
    elif index is None:
        return

    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else:
        row = index[0]

    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '750px', 'height': '500px'}, center=[30.75, -97.48], zoom=8, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], children=[
                dl.Tooltip(dff.iloc[row, 4]),
                dl.Popup([
                    html.H3(children=["Animal Name: ",
                                      dff.iloc[row, 9]
                                      ]
                            ),
                    html.P(children=["Latitude: ",
                                     dff.iloc[row, 13],
                                     html.Br(),
                                     "Longitude: ",
                                     dff.iloc[row, 14]
                                     ]
                           )
                ])
            ])
        ])
    ]


app.run_server(debug=True)
