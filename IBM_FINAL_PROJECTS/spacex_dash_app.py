# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


launch_sites = spacex_df['Launch Site'].unique()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([
                                    html.Label("Launch Site Drop-down Input:"),
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[{'label': 'All Sites', 'value': 'ALL'},
                                                 *[{'label': site, 'value': site} for site in launch_sites]
                                                 ],
                                        value='ALL Sites',
                                        placeholder="Select a Launch Site",
                                        searchable=True
                                    ),

                                ]),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                html.Div([
                                    html.Label("Range Slider"),
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min = min_payload,
                                        max = max_payload,
                                        step = 1000,
                                        marks={0: '0', 2500:'2500', 5000: '5000', 10000:'10000'},
                                        value=[min_payload, max_payload]
                                    ),
                                ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),


                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
               Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        success_counts = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(success_counts,
                     values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Count success (1) and failure (0) for the selected site
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']

        # Create pie chart for success vs failure
        fig = px.pie(class_counts,
                     values='count',
                     names='class',
                     title=f'Success vs Failure for {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
               Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value"))

def get_scatter_plot(entered_site,pay_load_range):
    if entered_site == 'ALL':
        flitered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= pay_load_range[0])&
            (spacex_df['Payload Mass (kg)'] <= pay_load_range[1])
        ]
        fig = px.scatter(flitered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Payload vs. Success for All Sites',
                         labels={'class': 'Launch Outcome (0=Failure, 1=Success)'}
                         )
        return fig

    else:
        # Create pie chart for success vs failure
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        flitered_df = filtered_df[
            (spacex_df['Payload Mass (kg)'] >= pay_load_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= pay_load_range[1])
            ]
        fig = px.scatter(flitered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Success for {entered_site}',
                         labels={'class': 'Launch Outcome (0=Failure, 1=Success)'}
                         )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
