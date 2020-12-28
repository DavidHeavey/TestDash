import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime

# external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/lux/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

headers = ['Date', 'Count']

df_20 = pd.read_csv('Data/2020.csv', names=headers, header=None, nrows=366, parse_dates=[0])
df_19 = pd.read_csv('Data/2019.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_18 = pd.read_csv('Data/2018.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_17 = pd.read_csv('Data/2017.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_16 = pd.read_csv('Data/2016.csv', names=headers, header=None, nrows=365, parse_dates=[0])
df_r = pd.read_csv('Data/Restrictions_2020.csv',sep=',', names=['Date', 'Restriction'], header=None, nrows=365, parse_dates=[0])

print(df_19.head())
# print(df_20.Date.dtype)
# print(df_20)

# fig = px.line(df_19, x='Date', y='Count', title='Traffic Counts')
# fig.update_xaxes(dtick='M1', tickformat='%b', ticklabelmode='period')
# fig.show()

# App Layout
# =========================

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div('Traffic Dashboard', className='text-left text-primary bg-dark'),
                width=1)
        ,
        dbc.Col(html.H1('The chart goes here')),
        ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
