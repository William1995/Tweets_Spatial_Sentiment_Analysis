# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import time
import plotly.graph_objects as go
import dash_table
import pandas as pd
from lib import*

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('2020 US President Candidate Election Visualization'),
    html.H2('CS-226 Group5 Final Project'),
    html.H4('Support Modes:'),
    dcc.Link('Candidate Twitter Popularity in Each State', href='/page-1'),
    html.Br(),
    dcc.Link('Candidate Twitter Sentiment Analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Candidate Twitter Comparison in Each State', href='/page-3'),
    html.Br(),
])

##################Page-1#######################
page_1_layout = html.Div([
    html.H1('Candidate Twitter Popularity in Each State'),
    html.H2('Candidate'),
    dcc.Dropdown(
        id = 'Candidate_dropdown',
        options = [
            {'label': 'Biden', 'value': 'biden'},
            {'label': 'Trump', 'value': 'trump'},
        ],
        value = 'biden'
    ),
    html.H2('Time Period'),
    dcc.RadioItems(
        id = 'Time_period_RadioItems',
        options = [
            {'label': '10/28-11/02 (Before Election)', 'value': 'before'},
            {'label': '11/02-11/10 (During Election)', 'value': 'during'},
        ],
        value = 'before',
        labelStyle = {'display': 'block'}
    ),

    dcc.Graph(id='hotmap', style={"height": "600px", "width":"1000px"}),

    html.Br(),
    dcc.Link('Candidate Twitter Sentiment Analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Candidate Twitter Comparison in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('Homepage', href='/'),
])

@app.callback(dash.dependencies.Output('hotmap', 'figure'),
              [dash.dependencies.Input('Candidate_dropdown', 'value'), dash.dependencies.Input('Time_period_RadioItems', 'value')])

def draw_map(candidate,time_period):

    code = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY'
            ,'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ'
            ,'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA'
            ,'VT','WA','WI','WV','WY']

    if candidate == 'biden':
        candidate_mode = time_period + '_' + candidate
        color = 'Blues'
        value = generate_hotmap_data(candidate_mode)

    elif candidate == 'trump':
        candidate_mode = time_period + '_' + candidate
        color = 'Reds'
        value = generate_hotmap_data(candidate_mode)

    fig = go.Figure(data = go.Choropleth(
        locations = code,
        z = value,
        locationmode = 'USA-states',
        colorscale = color,
        autocolorscale = False,
        marker_line_color = 'White', # line markers between states
        marker_line_width = 1,
        colorbar = go.choropleth.ColorBar(
        title = str(candidate)),
        geo = 'geo2'
        ), 

        layout = go.Layout(
        geo2 = dict(
        scope = 'usa',
        showframe = False,
        showland = True,
        showcountries = False,       
        bgcolor = 'rgba(235, 50, 255, 0.0)',),
        showlegend = True,
        font = dict(
        size = 20
        )
        )
    )

    return fig

##################Page-1#######################

##################Page-2#######################
page_2_layout = html.Div([
    html.H1('Candidate Twitter Sentiment Analysis'),
    html.H2('Candidate'),
    dcc.Dropdown(
        id = 'Candidate_dropdown',
        options = [
            {'label': 'Biden', 'value': 'biden'},
            {'label': 'Trump', 'value': 'trump'},
        ],
        value = 'biden'
    ),
    html.H2('Sentiment mode'),
    dcc.RadioItems(
        id = 'Sentiment_mode_RadioItems',
        options = [
            {'label': 'Positive count', 'value': 'positive'},
            {'label': 'Negative count', 'value': 'negative'},
            {'label': 'State tendency', 'value': 'tendency'},
        ],
        value = 'positive',
        labelStyle = {'display': 'inline-block'}
    ),
    html.H2('Time Period'),
    dcc.RadioItems(
        id = 'Time_period_RadioItems',
        options = [
            {'label': '10/28-11/02 (Before Election)', 'value': 'before'},
            {'label': '11/02-11/10 (During Election)', 'value': 'during'},
        ],
        value = 'before',
        labelStyle = {'display': 'block'}
    ),

    dcc.Graph(id='hotmap2', style={"height": "600px", "width":"1000px"}),

    html.Br(),
    dcc.Link('Candidate Twitter Popularity in Each State', href='/page-1'),
    html.Br(),
    dcc.Link('Candidate Twitter Comparison in Each State', href='/page-3'),
    html.Br(),
    dcc.Link('Homepage', href='/'),
])

@app.callback(dash.dependencies.Output('hotmap2', 'figure'),
              [dash.dependencies.Input('Candidate_dropdown', 'value'), dash.dependencies.Input('Sentiment_mode_RadioItems', 'value'), dash.dependencies.Input('Time_period_RadioItems', 'value')])

def draw_map(candidate,sentiment_mode,time_period):

    code = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY'
            ,'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ'
            ,'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA'
            ,'VT','WA','WI','WV','WY']

    if sentiment_mode == 'tendency':
        color = 'Agsunset'
        candidate_mode = time_period + '_' + candidate
        value = sentiment_compare_mode(candidate_mode)

    else:
        if sentiment_mode == 'positive':
            color = 'Peach'
        elif sentiment_mode == 'negative':
            color = 'Purples'

        if candidate == 'biden':
            candidate_mode = time_period + '_' + candidate + '_' + sentiment_mode
            value = generate_hotmap_data(candidate_mode)

        elif candidate == 'trump':
            candidate_mode = time_period + '_' + candidate + '_' + sentiment_mode
            value = generate_hotmap_data(candidate_mode)


    fig = go.Figure( data = go.Choropleth(
        locations = code,
        z = value,
        locationmode = 'USA-states',
        colorscale = color,
        autocolorscale = False,
        marker_line_color = 'White', # line markers between states
        marker_line_width = 1,
        colorbar = go.choropleth.ColorBar(
        title = str(candidate)),
        geo = 'geo2'
        ), 

        layout = go.Layout(
        geo2 = dict(
        scope = 'usa',
        showframe = False,
        showland = True,
        showcountries = False,       
        bgcolor = 'rgba(235, 50, 255, 0.0)',),
        showlegend = True,
        font = dict(
        size = 20
        )
        )
    )

    return fig
##################Page-2#######################

##################Page-3#######################
page_3_layout = html.Div([
    html.H1('Candidate Twitter Prediciton in Each State'),
    html.H2('Biden (Blue) v.s. Trump (Red)'),
    html.H3('Comparison mode'),
    dcc.RadioItems(
        id = 'Comparison_mode_RadioItems',
        options = [
            {'label': 'Prediciton: Popularity', 'value': 'popularity'},
            {'label': 'Positive count', 'value': 'positive'},
            {'label': 'Negative count', 'value': 'negative'},
            {'label': 'State tendency', 'value': 'tendency'},
            {'label': 'Prediciton: State tendency', 'value': 'prediciton'},
        ],
        value = 'popularity',
        labelStyle = {'display': 'block'}
    ),
    html.H3('Time Period'),
    dcc.RadioItems(
        id = 'Time_period_RadioItems',
        options = [
            {'label': '10/28-11/02 (Before Election)', 'value': 'before'},
            {'label': '11/02-11/10 (During Election)', 'value': 'during'},
        ],
        value = 'before',
        labelStyle = {'display': 'block'}
    ),

    html.Div('For the time period(11/02-11/10), the tendency in each state is inclined to Biden. Therefore, the color is all blue!', style={'margin-top': 20, 'fontSize': 16, 'color':'Red'}),

    html.Div(id='output-text', style={'margin-top': 20, 'fontSize': 40}),

    dcc.Graph(id='hotmap3', style={"height": "600px", "width":"1000px"}),

    html.Br(),
    dcc.Link('Candidate Twitter Popularity in Each State', href='/page-1'),
    html.Br(),
    dcc.Link('Candidate Twitter Sentiment Analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Homepage', href='/'),
])

@app.callback(dash.dependencies.Output('hotmap3', 'figure'),
              [dash.dependencies.Input('Comparison_mode_RadioItems', 'value'), dash.dependencies.Input('Time_period_RadioItems', 'value')])

def draw_map(comparison_mode,time_period):

    code = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY'
            ,'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ'
            ,'NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA'
            ,'VT','WA','WI','WV','WY']

    value = candidate_comparison(comparison_mode,time_period)

    if time_period == 'during' and (comparison_mode == 'tendency' or comparison_mode == 'prediciton'):
        color = 'Blues'
    else:
        color = 'RdBu'

    fig = go.Figure( data = go.Choropleth(
        locations = code,
        z = value,
        locationmode = 'USA-states',
        colorscale = color,
        autocolorscale = False,
        marker_line_color = 'White', # line markers between states
        marker_line_width = 1,
        colorbar = go.choropleth.ColorBar(
        title = comparison_mode),
        geo = 'geo2'
        ), 

        layout = go.Layout(
        geo2 = dict(
        scope = 'usa',
        showframe = False,
        showland = True,
        showcountries = False,       
        bgcolor = 'rgba(235, 50, 255, 0.0)',),
        showlegend = True,
        font = dict(
        size = 20
        )
        )
    )

    return fig

@app.callback(
    dash.dependencies.Output('output-text', 'children'),
    [dash.dependencies.Input('Comparison_mode_RadioItems', 'value'), dash.dependencies.Input('Time_period_RadioItems', 'value')])
def update_output(comparison_mode,time_period):
    if comparison_mode == 'popularity' or comparison_mode == 'prediciton':
        biden,trump = compute_voter(comparison_mode,time_period)
        return '=== Biden: {} || Trump: {} ==='.format(biden,trump)

    else:
        return '==='

##################Page-3#######################

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)