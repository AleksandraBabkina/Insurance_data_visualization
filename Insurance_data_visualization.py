from sqlalchemy import create_engine, Column, String, Float, select, or_, and_, Table, MetaData, inspect, text, types
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects import oracle
import oracledb
import pandas as pd
from dash import Dash, html, dcc, Output, Input, dash_table
from dash.dash_table.Format import Group
import dash 
import plotly.express as px
import webbrowser
import sys
import os
import datetime

pd.set_option('display.max_rows', None)

oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

# Header with connection, DO NOT TOUCH
username = 'username'
password = 'password'
dsn = 'dsn'

conection_string = f'oracle+cx_oracle://{username}:{password}@{dsn}' # Opening SQL
engine = create_engine(conection_string) # Engine

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Queries
query1 = """
select * from al_babkina_dashbord_top10prol
"""
query2 = """
select * from al_babkina_dashbord_top10prol_2
"""
query3 = """
select * from al_babkina_dashbord_top10регион
"""
query4 = """
select * from al_babkina_dashbord_дата_расчета
"""

# Load data into DataFrame
df1 = pd.read_sql_query(query1, engine)
df2 = pd.read_sql_query(query2, engine)
df3 = pd.read_sql_query(query3, engine)
df4 = pd.read_sql_query(query4, engine)

# Remove zero values
df1 = df1[(df1['bt'] != 0) & (df1['bt'] != 1)]
df2 = df2[(df2['bt'] != 0) & (df2['bt'] != 1)]
df3 = df3[(df3['bt'] != 0) & (df3['bt'] != 1)]
df4 = df4[(df4['bt'] != 0) & (df4['bt'] != 1)]
df4 = df4[(df4['РЕГИОН_СОБСТВЕННИКА'] != 'None')]

# Convert to percentage format
df1['pross'] = (df1['pross'] * 100).round(2)
df2['pross'] = (df2['pross'] * 100).round(2)
df3['pross'] = (df3['pross'] * 100).round(2)

# Define minimum and maximum values for Y-axis
min_y_df1 = df1['bt'].min() - 100
max_y_df1 = df1['bt'].max() + 100
min_y_df2 = df2['bt'].min() - 100
max_y_df2 = df2['bt'].max() + 100
min_y_df3 = df3['bt'].min() - 100
max_y_df3 = df3['bt'].max() + 100
min_y_df4 = df4['ДАТА_РАСЧЕТА'].min() - datetime.timedelta(days=100)
min_y_df4 = df4['ДАТА_РАСЧЕТА'].max() + datetime.timedelta(days=100)

# Data transformation
df4['РЕГИОН_СОБСТВЕННИКА'] = df4['РЕГИОН_СОБСТВЕННИКА'].astype(str)
df4['РЕГИОН_СОБСТВЕННИКА'] = df4['РЕГИОН_СОБСТВЕННИКА'].fillna('Unknown')
regions = df4['РЕГИОН_СОБСТВЕННИКА'].unique().tolist()

# Calculate the average bt for each unique combination of sk, ДАТА_РАСЧЕТА, and РЕГИОН_СОБСТВЕННИКА
df4_mean = df4.groupby(['sk', 'ДАТА_РАСЧЕТА', 'РЕГИОН_СОБСТВЕННИКА']).agg({'bt': 'mean'}).reset_index()
df4_mean['bt'] = df4_mean['bt'].round().astype(int)
# Calculate the average bt for each unique combination of sk, МЕСЯЦ, and РЕГИОН_СОБСТВЕННИКА
df4_month = df4.groupby(['sk', 'МЕСЯЦ', 'РЕГИОН_СОБСТВЕННИКА']).agg({'bt': 'mean'}).reset_index()
df4_month['bt'] = df4_month['bt'].round().astype(int)
# Calculate the average bt for each unique combination of sk, НЕДЕЛЯ, and РЕГИОН_СОБСТВЕННИКА
df4_week = df4.groupby(['sk', 'НЕДЕЛЯ', 'РЕГИОН_СОБСТВЕННИКА']).agg({'bt': 'mean'}).reset_index()
df4_week['bt'] = df4_week['bt'].round().astype(int)

# Custom color palette
custom_colors1 = ['#C71585', '#FFA07A', '#B22222', '#FF4500', '#BDB76B', '#9932CC', '#6A5ACD', '#4B0082', '#2F4F4F', '#40E0D0', '#00008B', '#006400', '#3CB371', '#696969', '#800000']

# Start of the dashboard
app = Dash(__name__, suppress_callback_exceptions=True)

# Create chart 1
fig1 = px.scatter(df1, 
              x='bt', 
              y='pross', 
              color='sk', 
              title="New Business Transition",
              labels={'sk': 'Insurance', 'bt': 'Tariff', 'pross': 'Repeat Rate (%)', 'num': 'Repeat Count'},
              category_orders={"sk": df1['sk'].unique()},
              color_discrete_sequence=custom_colors1, # Use custom color palette
              hover_data=['bt', 'pross', 'num'])
fig1.update_traces(marker=dict(size=8))  # Increase point size
fig1.update_xaxes(range=[min_y_df1, max_y_df1])
fig1.update_yaxes(tickformat='.2f%')  # Format Y-axis to display percentages
fig1.update_layout(legend_title_text='', title_x=0.4, margin=dict(t=30)) 

# Create chart 2
fig2 = px.scatter(df2, 
              x='bt', 
              y='pross', 
              color='sk', 
              title="Transition Failed",
              labels={'sk': 'Insurance', 'bt': 'Tariff', 'pross': 'Repeat Rate (%)', 'num': 'Repeat Count'},
              category_orders={"sk": df2['sk'].unique()},
              color_discrete_sequence=custom_colors1, # Use custom color palette
              hover_data=['bt', 'pross', 'num'])
fig2.update_traces(marker=dict(size=8))  # Increase point size
fig2.update_xaxes(range=[min_y_df2, max_y_df2])
fig2.update_yaxes(tickformat='.2f%')  # Format Y-axis to display percentages
fig2.update_layout(legend_title_text='', title_x=0.4, margin=dict(t=30))  

# Update chart and table based on selected region
@app.callback(Output('graph-3', 'figure'), [Input('region-dropdown', 'value')])
# Create chart 3
def update_graph(region):
    filtered_df = df3[df3['РЕГИОН_СОБСТВЕННИКА'] == region]
    fig3 = px.scatter(filtered_df,
                      x='bt',
                      y='num',
                      color='sk',
                      title=f"BT by Insurance in {region} Region",
                      labels={'sk': 'Insurance', 'bt': 'Tariff', 'pross': 'Repeat Rate (%)', 'num': 'Repeat Count'},
                      category_orders={"sk": df3['sk'].unique()},
                      color_discrete_sequence=custom_colors1,
                      hover_data=['bt', 'pross', 'num'])
    fig3.update_traces(marker=dict(size=8))
    fig3.update_xaxes(range=[min_y_df3, max_y_df3])
    fig3.update_yaxes(tickformat='.2f%')
    fig3.update_layout(legend_title_text='', title_x=0.4, margin=dict(t=30))
    return fig3

# Update chart and table based on selected region and interval
@app.callback(Output('scatter-plot', 'figure'), [Input('region-dropdown-4', 'value'), Input('interval-radio', 'value')])
def update_graph(region, interval):
    if interval == 'ДАТА_РАСЧЕТА':
        filtered_df4 = df4_mean[df4_mean['РЕГИОН_СОБСТВЕННИКА'] == region]
        x_data = filtered_df4['ДАТА_РАСЧЕТА']
        # Calculate average bt for each date with one sk value
        avg_bt_by_date_sk = filtered_df4.groupby(['ДАТА_РАСЧЕТА', 'sk'])['bt'].mean().reset_index()
        x='ДАТА_РАСЧЕТА'
    elif interval == 'НЕДЕЛЯ':
        filtered_df4 = df4_week[df4_week['РЕГИОН_СОБСТВЕННИКА'] == region]
        x_data = filtered_df4['НЕДЕЛЯ']
        # Calculate average bt for each week with one sk value
        avg_bt_by_date_sk = filtered_df4.groupby(['НЕДЕЛЯ', 'sk'])['bt'].mean().reset_index()
        x='НЕДЕЛЯ'
    elif interval == 'МЕСЯЦ':
        filtered_df4 = df4_month[df4_month['РЕГИОН_СОБСТВЕННИКА'] == region]
        x_data = filtered_df4['МЕСЯЦ']
        # Calculate average bt for each month with one sk value
        avg_bt_by_date_sk = filtered_df4.groupby(['МЕСЯЦ', 'sk'])['bt'].mean().reset_index()
        x='МЕСЯЦ'
    fig4 = px.scatter(
        avg_bt_by_date_sk, 
        x=x, 
        y='bt', 
        color='sk', 
        title=f"Tariff Change by Dates in {region} Region",
        labels={'sk': 'Insurance', 'bt': 'Tariff'},
        category_orders={"sk": df4['sk'].unique()},
        color_discrete_sequence=custom_colors1,
        hover_data=['bt', x]
    )
    fig4.update_traces(marker=dict(size=8))
    fig4.update_layout(legend_title_text='', title_x=0.4, margin=dict(t=30))
    return fig4

# Define page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Top 10 Tariffs by prol Field', href='/'),
        html.Span(' | '),
        dcc.Link('Top 10 Tariffs by Regions', href='/page-2'),
        html.Span(' | '),
        dcc.Link('Skip by Regions/prol/KBM', href='/page-3'),
        html.Span(' | '),
        dcc.Link('Tariff Changes by Dates and Regions', href='/page-4'),
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),
    html.Div(id='page-content')
])

# Page 1 content
page_1_layout = html.Div([
    html.H1("Top 10 Tariffs by prol Field", style={'font-weight': 'bold', 'text-align': 'center'}),
    html.Div([
        dcc.Graph(figure=fig1, style={'display': 'inline-block', 'width': '50%', 'height': '500px'}),
        dcc.Graph(figure=fig2, style={'display': 'inline-block', 'width': '50%', 'height': '500px'})
    ], style={'width': '100%'})
])

# Page 2 content
page_2_layout = html.Div([
    html.H1("Top 10 Tariffs by Regions", style={'font-weight': 'bold', 'text-align': 'center'}),
    html.Br(), 
    html.Br(),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df3['РЕГИОН_СОБСТВЕННИКА'].unique()],
        value=df3['РЕГИОН_СОБСТВЕННИКА'].unique()[0],  # Use the first region by default
        multi=False,
        placeholder='Select Region'
    ),
    html.Br(), 
    html.Br(),
    dcc.Graph(id='graph-3')
])

# Page 3 content
page_3_layout = html.Div([
    html.H1("Skip by Regions/prol/KBM", style={'font-weight': 'bold', 'text-align': 'center'}),
    # You can add graphs for the third page here
])

# Page 4 content
page_4_layout = html.Div([
    html.H1("Tariff Changes by Dates and Regions", style={'font-weight': 'bold', 'text-align': 'center'}),
    html.Br(), 
    html.Br(),
    dcc.Dropdown(
        id='region-dropdown-4',
        options=[{'label': region, 'value': region} for region in df4['РЕГИОН_СОБСТВЕННИКА'].unique()],
        value=regions[0],  # Use the first region by default
        multi=False,
        placeholder='Select Region'
    ),
    html.Br(), 
    html.Br(),
    # Radio buttons for interval selection
    dcc.RadioItems(
        id='interval-radio',
        options=[
            {'label': 'By Date', 'value': 'ДАТА_РАСЧЕТА'},
            {'label': 'By Week', 'value': 'НЕДЕЛЯ'},
            {'label': 'By Month', 'value': 'МЕСЯЦ'}
        ],
        value='ДАТА_РАСЧЕТА',  # Default value
        labelStyle={'display': 'inline-block', 'margin-right': '30px'}
    ),
    html.Br(), 
    html.Br(),
    dcc.Graph(id='scatter-plot')
])

# Update page content based on URL
@app.callback(dash.dependencies.Output('page-content', 'children'), [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return page_1_layout

# Run the application
if __name__ == '__main__':
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True, suppress_callback_exceptions=False)