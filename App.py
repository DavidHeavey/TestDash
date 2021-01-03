import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
import datetime as dt


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
# =====================================================================================================================
# Read Data
# =====================================================================================================================
headers = ['Date', '2020', '2019', '2018', '2017', '2016', 'Restrictions']
df = pd.read_csv('https://raw.githubusercontent.com/DavidHeavey/TestDash/master/Data/Counts.csv', names=headers, header=0, sep=',')
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
# create Baseline based on mean 2016 to 2019
df['Baseline'] = df.iloc[:, 2:5].mean(axis=1)
df['Baseline'] = df['Baseline'].astype(int)

# dates restrictions change
rest_cat_list = df['Restrictions'].unique()
dates_list = df['Date'].tolist()
rest_list = df['Restrictions'].tolist()
rest_dates = []

for item in rest_cat_list:
    rest_dates.append(dates_list[rest_list.index(item)])

# print(rest_dates)
# print(f'length of rest dates is {len(rest_dates)}')
# print(rest_cat_list)
# print(f'length of rest cats is {len(rest_cat_list)}')
rest_dict = dict(zip(rest_dates, rest_cat_list))
# print('rest dict:' , rest_dict)
# =====================================================================================================================
# Styling
# =====================================================================================================================
SIDEBAR_STYLE_DICT = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
}

CONTENT_STYLE_DICT = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'margin-bottom': 0,
}

# =====================================================================================================================
# Define Fig 1
# =====================================================================================================================
fig1 = px.line(df, x='Date', y='2020', title='Traffic Counts 2020 and Baseline :', height=800, labels={'2020': 'Vehicle Count'})
fig1.update_xaxes(dtick='M1', tickformat='%b', ticklabelmode='period', rangeslider_visible=True)
fig1.add_scatter(x=df['Date'], y=df['Baseline'], mode='lines', name='Baseline')
fig1.update_traces(hovertemplate='%{x|%d-%B}<br>%{y}')
fig1.update_layout(hovermode="x")
fig1.data[0].name = '2020'
fig1.data[0].showlegend = True
colors = ['snow', 'dimgrey','darkgrey', 'silver','lightgrey', 'peru', 'indianred']
for i in range(6):
    fig1.add_vrect(x0=rest_dates[i], x1=rest_dates[i+1], line_width=0, fillcolor=colors[i], opacity=0.2, annotation_text=rest_cat_list[i])
end = dt.date(2020, 12, 31)
fig1.add_vrect(x0=rest_dates[6], x1=end, line_width=0, fillcolor=colors[6], opacity=0.4, annotation_text=rest_cat_list[6])

# =====================================================================================================================
# Define Fig 2
# =====================================================================================================================
col = df['2020']
col1 = df['Baseline']
stats_list = ['MAX', 'MIN', 'MEAN', 'MEDIAN', 'STD DEV']
stats_values = [col.max(), col.min(), col.mean(), col.median(), col.std()]
stats_r = [round(i) for i in stats_values]
stats_values_1 = [col1.max(), col1.min(), col1.mean(), col1.median(), col1.std()]
stats_r_1 = [round(i) for i in stats_values_1]
stats_20 = {'stat_names': stats_list, 'y-values': stats_r}
stats_B = {'stat_names': stats_list, 'y-values': stats_r_1}

# create fig 2
fig2 = px.bar(stats_20, x=stats_list, y=stats_r, height=700, barmode='group', title='Statistics Comparison :',
              text=stats_r, labels={'x': 'Statistics', 'y': 'Vehicle Counts'})
# add second trace for Baseline
fig2.add_bar(x=stats_list, y=stats_r_1, name='Baseline', text=stats_r_1, textposition='auto')
fig2.data[0].name = '2020'
fig2.data[0].showlegend = True

# =====================================================================================================================
# Define Fig 3
# =====================================================================================================================
# remove Baseline and Restrictions
df_counts_only = df.drop(['Restrictions', 'Baseline'], axis=1)
df_counts_only = df_counts_only.set_index('Date')

# get monthly totals
df_monthly = df_counts_only.resample('M').sum()
df_monthly['Month'] = pd.DatetimeIndex(df_monthly.index).to_period('M')
df_monthly['Month'] = df_monthly['Month'].dt.strftime('%b')
# reverse order
df_monthly = df_monthly.iloc[:, ::-1]
df_monthly_tot = df_monthly.append(df_monthly.sum(numeric_only=True), ignore_index=True)
df_monthly_tot['Month'][12] = 'Total'

# create table
fig3 = ff.create_table(df_monthly_tot, height_constant=40)

# =====================================================================================================================
# Define Fig 4
# =====================================================================================================================
# Use dict of lists for Barchart
year_list = df_monthly_tot.columns.tolist()
year_list.remove('Month')
# print('Years:', year_list)
year_totals_list = df_monthly_tot.iloc[12, :].tolist()
year_totals_list.remove('Total')
year_totals_list_int = [int(i) for i in year_totals_list]
# print('Totals:', year_totals_list_int)
years_dict = {'Years': year_list, 'Totals': year_totals_list_int}

# create fig 4
fig4 = px.bar(years_dict, x=year_list, y=year_totals_list_int, height=700,
              text=year_totals_list_int, labels={'x': 'Year', 'y': 'Total Vehicle Counts'})

# =====================================================================================================================
# Define SideBar + Main Window
# =====================================================================================================================
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
            dbc.NavLink('Daily Counts', active='exact', href="/", className='my-2'),
            dbc.NavLink('Compare Statistics', active='exact', href="/compare", className='my-2'),
            dbc.NavLink('Monthly Table', active='exact', href="/table", className='my-2'),
            dbc.NavLink('Yearly Totals', active='exact', href="/totals", className='my-2'),
        ],
            pills=True, card=True, vertical=True, className='mx-1'
        ),
        # dcc.Dropdown(
        #     id='year_selected',
        #     options=[
        #         {'label':'2020', 'value':'2020'},
        #         {'label':'2019', 'value':'2019'}
        #     ],
        #     value=['2020','2019'],
        #     multi=True
        # ),
    ]),

    dbc.CardBody([
        html.Hr(),
        html.H6('Applied Scripting Languages', className='font-weight-bold'),
        html.Hr(),
        html.P('Student ID: A00279257'),
        html.Hr(),
        dcc.Link('Traffic Count Data Source here...', href='https://www.nratrafficdata.ie')
    ]),
], color='light', style={'height':'100vh',
                         'width':'16rem', 'position':'fixed'})

# Define MainWindow

content = html.Div(id='page-content', children=[], style=CONTENT_STYLE_DICT)

# =====================================================================================================================
# App Layout
# =====================================================================================================================

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    content,
])
# =====================================================================================================================
# Callback Def
# =====================================================================================================================
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def render_page(pathname):
    if pathname == '/':
        return [
            html.H1('Athlone Traffic Counts'),
            dcc.Graph(id='plot', figure=fig1,)
        ]
    elif pathname == '/compare':
        return [
            html.H1('Yearly Traffic Comparison'),
            dcc.Graph(id='plot2', figure=fig2,)
        ]
    elif pathname == '/table':
        return [
            html.H1('Monthly Totals for recent years :'),
            dcc.Graph(id='plot3', figure=fig3),
        ]
    elif pathname == '/totals':
        return [
            html.H1('Yearly Totals'),
            dcc.Graph(id='plot4', figure=fig4),
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
