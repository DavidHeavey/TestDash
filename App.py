import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# read data
headers = ['Date', 'Count']

df_20 = pd.read_csv('Data/2020.csv', names=headers, header=None, nrows=366, parse_dates=[0])
df_19 = pd.read_csv('Data/2019.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_18 = pd.read_csv('Data/2018.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_17 = pd.read_csv('Data/2017.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_16 = pd.read_csv('Data/2016.csv', names=headers, header=None, nrows=366, parse_dates=[0])
df_r = pd.read_csv('Data/Restrictions_2020.csv', sep=',', names=['Date', 'Restriction'], header=None, nrows=365, parse_dates=[0])
df_all = pd.concat([df_19, df_18, df_17, df_16], axis=0)

print(df_19.head())
print(df_20.Date.dtype)
print(df_20)

# styling
SIDEBAR_STYLE_DICT = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    #'background-color': '#f8f9fa',
}

CONTENT_STYLE_DICT = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

fig1 = px.line(df_all, x='Date', y='Count', title='Traffic Counts')
fig1.update_xaxes(rangeslider_visible=True)
#fig1.update_xaxes(dtick='M1', tickformat='%b', ticklabelmode='period')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(data=df_19, x='Date', y='Count'))
#fig2.update_xaxes(dtick='M1', tickformat='%b', ticklabelmode='period')


sidebar = dbc.Card([
    # dbc.CardBody([
    #     html.H5('Athlone Traffic', className='display-6'),
    #     html.Hr(),
    # ]),
    dbc.CardImg(src='static/AIT_logo.png', top=True),
    dbc.CardBody([
        html.P('Select a page:'),
        html.Hr(),
        dbc.Nav(
        [
            dbc.NavLink("Home", active='exact', href="/", className='my-2'),
            dbc.NavLink("Compare Years", active='exact', href="/compare", className='my-2'),
            dbc.NavLink("Select Dates", active='exact', href="/select"),
        ],
        pills=True, card=True, vertical=True, className='mx-1'
        ),
    ]),
    dbc.CardBody([
        html.Hr(),
        html.H6('Applied Scripting Languages', className='font-weight-bold'),
        html.Hr(),
        html.P('Student ID: A00279257'),
    ]),
], color='light', style={'height':'100vh',
                         'width':'16rem', 'position':'fixed'})

content = html.Div(id='page-content', children=[], style=CONTENT_STYLE_DICT)
# App Layout
# =========================

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    content
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def render_page(pathname):
    if pathname == '/':
        return [
            html.H1('Athlone Traffic Counts'),
            dcc.Graph(id='plot', figure=fig1)
        ]
    elif pathname == '/compare':
        return [
            html.H1('Yearly Traffic Comparison'),
            dcc.Graph(id='plot', figure=fig2)
        ]
    elif pathname == '/select':
        return [
            html.H1('Select Count Date range'),
            dcc.Graph(id='plot', figure=px.line(df_19, x='Date', y='Count', title='Traffic Counts'))
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
