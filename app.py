# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


df = pd.read_csv(
    'data/hiring-patterns.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    #generate_table(df),

    dcc.Graph(
        id='ranking-internships',
        figure={
            'data': [
                go.Scatter(
                    x=df['Uni Ranking'],
                    y=df['Internships'],
                    text='TestText',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='First'
                )],
            'layout': go.Layout(
                xaxis={'type': 'linear', 'title': 'Uni Rankings'},
                yaxis={'title': 'Number of Internships'},
                margin={'l': 10, 'b': 10, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )

])




if __name__ == '__main__':
    app.run_server(debug=True)
