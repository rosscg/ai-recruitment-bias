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
print(df.Gender.unique())


# Counting values per gender
gender_not_interviewd_df = df.groupby('Gender')['Interviewed'].apply(lambda x: (x=='No').sum()).reset_index(name='count')
gender_interviewd_df = df.groupby('Gender')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='count')
gender_hired_df = df.groupby('Gender')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='count')


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
    ),


    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=gender_not_interviewd_df['Gender'],
                    y=gender_not_interviewd_df['count'],
                    name='Not Interviewed by Gender',
                    marker=go.bar.Marker(
                        color='rgb(225, 128, 0)'
                    )
                ),
                go.Bar(
                    x=gender_interviewd_df['Gender'],
                    y=gender_interviewd_df['count'],
                    name='Interviewed by Gender',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
                go.Bar(
                    x=gender_hired_df['Gender'],
                    y=gender_hired_df['count'],
                    name='Admissions by Gender',
                    marker=go.bar.Marker(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=go.Layout(
                title='Admissions by Gender',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='interview-gender'
    )

])



if __name__ == '__main__':
    app.run_server(debug=True)
