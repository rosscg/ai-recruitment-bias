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

# Test Data
df = pd.read_csv(
    'data/hiring-patterns.csv')


#Params not represented:
#Skill Requirements met,
#Top 3 soft skills candidate selected from fixed list,


gender_interviewd_df = df.groupby('Gender')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
gender_hired_df = df.groupby('Gender')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
gender_df = df.groupby('Gender').count()["Internships"].reset_index().join(gender_interviewd_df['interviewed']).join(gender_hired_df['hired'])
gender_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
gender_df['ratio-interviewed'] = gender_df['interviewed']/gender_df['total']
gender_df['ratio-hired'] = gender_df['hired']/gender_df['interviewed']

disabled_interviewd_df = df.groupby('Disabled')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
disabled_hired_df = df.groupby('Disabled')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
disabled_df = df.groupby('Disabled').count()["Internships"].reset_index().join(disabled_interviewd_df['interviewed']).join(disabled_hired_df['hired'])
disabled_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
disabled_df['ratio-interviewed'] = disabled_df['interviewed']/disabled_df['total']
disabled_df['ratio-hired'] = disabled_df['hired']/disabled_df['interviewed']

ethnicity_interviewd_df = df.groupby('Ethnicity')['Interviewed'].apply(lambda x: (x=='Yes').sum()).reset_index(name='interviewed')
ethnicity_hired_df = df.groupby('Ethnicity')['Hired'].apply(lambda x: (x=='Yes').sum()).reset_index(name='hired')
ethnicity_df = df.groupby('Ethnicity').count()["Internships"].reset_index().join(ethnicity_interviewd_df['interviewed']).join(ethnicity_hired_df['hired'])
ethnicity_df.rename(index=str, columns={"Internships": "total"}, inplace=True)
ethnicity_df['ratio-interviewed'] = ethnicity_df['interviewed']/ethnicity_df['total']
ethnicity_df['ratio-hired'] = ethnicity_df['hired']/ethnicity_df['interviewed']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(className="container", children=[

    html.Div(className="row", children=[
        html.Div(className="three columns", children=[
            html.H2('Bias Portfolio', style={'color': 'gray'})
        ]),
    ]),

    html.Div([
        html.Div([
            html.H5("Categorical Class Comparisons:"),
            html.P("These graphs represent acceptance rates per class. Clear trends in line graphs, or large differences in the bar chart could signify a bias. Take note of sample size per class before making judgements of bias.", style={'color': 'gray', 'fontSize': 14})
        ], className="twelve columns"),
    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Scatter(
                        #x = [random_x],
                        y=df.groupby('Internships')['Hired'].apply(lambda x: (x=='Yes').sum())/df.groupby('Internships').count()['Applicant ID'],
                        mode = 'lines',
                        name = 'lines'
                        )
                    ],
                    layout=go.Layout(
                        title='Number of Internships',
                        showlegend=False,
                        margin=go.layout.Margin(l=20, r=20, t=50, b=50)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='internships2'
            ),
        ], className="four columns"),

        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Scatter(
                        #x = [random_x],
                        y=df.groupby('Uni Ranking')['Hired'].apply(lambda x: (x=='Yes').sum())/df.groupby('Uni Ranking').count()['Applicant ID'],
                        mode = 'lines',
                        name = 'lines'
                        )
                    ],
                    layout=go.Layout(
                        title='Uni Ranking',
                        showlegend=False,
                        margin=go.layout.Margin(l=20, r=20, t=50, b=50)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='uniranking'
            ),
        ], className="four columns"),

        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df['Department of study'],
                            y=df.groupby('Department of study')['Hired'].apply(lambda x: (x=='Yes').sum())/df.groupby('Department of study').count()['Applicant ID'],
                            name='Hired',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                    ],
                    layout=go.Layout(
                        title='Department of Study',
                        showlegend=False,
                        margin=go.layout.Margin(l=20, r=20, t=50, b=50)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='deptartment'
            ),
        ], className="four columns")

    ], className="row"),


    html.Div([
        html.Div([
            html.H5("Binary Class Comparisons:"),
            html.P("The following values represent the parity between classes for chances of interview and chances of being hired. A value of 100% signifies perfect parity.", style={'color': 'gray', 'fontSize': 14})
        ], className="twelve columns"),
    ], className="row"),


    html.Div([
        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=gender_df['Gender'],
                            y=gender_df['total'],
                            name='Total',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x=gender_df['Gender'],
                            y=gender_df['interviewed'],
                            name='Interviewed',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x=gender_df['Gender'],
                            y=gender_df['hired'],
                            name='Admissions',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Gender',
                        showlegend=False,
                        #legend=go.layout.Legend(
                        #    x=0,
                        #    y=-1.0
                        #),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='interview-gender'
            ),
            html.P("Interview Comparison: {:.0f}%".format(100*gender_df.loc[gender_df['Gender'] == 'Female']['ratio-interviewed'].values[0] / gender_df.loc[gender_df['Gender'] == 'Male']['ratio-interviewed'].values[0])),
            html.P("Hiring Comparison: {:.0f}%".format(100*gender_df.loc[gender_df['Gender'] == 'Female']['ratio-hired'].values[0] / gender_df.loc[gender_df['Gender'] == 'Male']['ratio-hired'].values[0])),
        ], className="four columns"),


        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=disabled_df['Disabled'],
                            y=disabled_df['total'],
                            name='Total',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x=disabled_df['Disabled'],
                            y=disabled_df['interviewed'],
                            name='Interviewed',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x=disabled_df['Disabled'],
                            y=disabled_df['hired'],
                            name='Admissions',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Disability',
                        showlegend=False,
                        legend=go.layout.Legend(
                            x=0,
                            y=-1.0
                        ),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='interview-disabled'
            ),
            html.P("Interview Comparison: {:.0f}%".format(100*disabled_df.loc[disabled_df['Disabled'] == 'Yes']['ratio-interviewed'].values[0] / disabled_df.loc[disabled_df['Disabled'] == 'No']['ratio-interviewed'].values[0])),
            html.P("Hiring Comparison: {:.0f}%".format(100*disabled_df.loc[disabled_df['Disabled'] == 'Yes']['ratio-hired'].values[0] / disabled_df.loc[disabled_df['Disabled'] == 'No']['ratio-hired'].values[0])),
        ], className="four columns"),


        html.Div([
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=ethnicity_df['Ethnicity'],
                            y=ethnicity_df['total'],
                            name='Total',
                            marker=go.bar.Marker(
                                color='rgb(225, 128, 0)'
                            )
                        ),
                        go.Bar(
                            x=ethnicity_df['Ethnicity'],
                            y=ethnicity_df['interviewed'],
                            name='Interviewed',
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x=ethnicity_df['Ethnicity'],
                            y=ethnicity_df['hired'],
                            name='Admissions',
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Ethnicity',
                        showlegend=False,
                        legend=go.layout.Legend(
                            x=0,
                            y=-1.0
                        ),
                        margin=go.layout.Margin(l=20, r=20, t=50, b=20)
                    )
                ),
                style={'height': 200,'width': '100%'},
                id='ethnicity-disabled'
            ),
            html.P("Interview Comparison: {:.0f}%".format(100*ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'BME']['ratio-interviewed'].values[0] / ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'White']['ratio-interviewed'].values[0])),
            html.P("Hiring Comparison: {:.0f}%".format(100*ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'BME']['ratio-hired'].values[0] / ethnicity_df.loc[ethnicity_df['Ethnicity'] == 'White']['ratio-hired'].values[0])),
        ], className="four columns"),

    ], className="row"),

])



if __name__ == '__main__':
    app.run_server(debug=True)
